from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.crops.models import Crop, CropVariety
from apps.markets.models import Mandi, MandiPrice
from apps.farmers.models import FarmerProfile
from apps.buyers.models import BuyerProfile, BuyerRequirement, BuyerEnquiry
from apps.fpos.models import FPO, FPOMembership, FPOCropLot
from apps.schemes.models import Scheme, SchemeBookmark
from apps.crop_wellness.models import DiseaseProfile, CropHealthAnalysis
from apps.transactions.models import Transaction
from apps.logistics.models import StorageFacility, Transporter
from apps.web3_ledger.service import compute_canonical_hash, generate_digital_receipt, verify_receipt_integrity
from apps.assistant.engine import process_krishi_query
import pytest
from datetime import date

User = get_user_model()

@pytest.mark.django_db
class TestAuthenticationAndRoles:
    def test_farmer_registration(self, client):
        resp = client.post(reverse('accounts:register_farmer'), {
            'username': 'test_farmer_99',
            'first_name': 'Suresh',
            'last_name': 'Yadav',
            'phone_number': '9812999000',
            'state': 'Haryana',
            'district': 'Karnal',
            'landholding_acres': 3.0,
            'password': 'password123',
        })
        assert resp.status_code == 302
        user = User.objects.get(username='test_farmer_99')
        assert user.role == User.Role.FARMER
        assert user.farmer_profile.district == 'Karnal'

    def test_user_login_and_logout(self, client):
        user = User.objects.create_user(username='login_test', password='secretpassword', role=User.Role.FARMER)
        login_resp = client.post(reverse('accounts:login'), {
            'username': 'login_test',
            'password': 'secretpassword',
        })
        assert login_resp.status_code == 302
        logout_resp = client.get(reverse('accounts:logout'))
        assert logout_resp.status_code == 302

@pytest.mark.django_db
class TestNetRealisationCalculator:
    def test_calculator_math_and_ranking(self, client):
        crop = Crop.objects.create(name='Test Wheat', standard_msp_quintal=2275.0)
        resp = client.get(reverse('calculator:calculate'), {'crop': crop.id, 'quantity': 50.0})
        assert resp.status_code == 200
        results = resp.context['results']
        assert len(results) == 4
        for res in results:
            expected_net = res['gross_revenue'] - res['total_costs']
            assert abs(res['net_realisation'] - expected_net) < 0.01
            assert res['net_per_qtl'] > 0

    def test_pdf_report_export(self, client):
        resp = client.get(reverse('calculator:export_pdf'))
        assert resp.status_code == 200
        assert resp['Content-Type'] == 'application/pdf'
        assert len(resp.content) > 1000

@pytest.mark.django_db
class TestMarketIntelligence:
    def test_mandi_price_filtering(self, client):
        crop = Crop.objects.create(name='Test Mustard', standard_msp_quintal=5650.0)
        mandi = Mandi.objects.create(name='Karnal Test Mandi', district='Karnal', state='Haryana')
        MandiPrice.objects.create(
            mandi=mandi, crop=crop, min_price=5400, max_price=5800, modal_price=5650,
            arrival_quantity_quintals=250, price_date=date.today(), is_demo_data=False
        )
        resp = client.get(reverse('markets:list'), {'crop': crop.id})
        assert resp.status_code == 200
        assert len(resp.context['prices']) >= 1

@pytest.mark.django_db
class TestCropWellnessAndSafety:
    def test_disease_profile_and_safety_disclaimer(self, client):
        crop = Crop.objects.create(name='Test Rice')
        disease = DiseaseProfile.objects.create(
            crop=crop, name_en='Test Blast', symptoms='Spots', treatment='Fungicide', default_severity='MODERATE'
        )
        analysis = CropHealthAnalysis.objects.create(
            crop=crop, predicted_disease=disease, confidence_score=0.92, severity='MODERATE'
        )
        resp = client.get(reverse('wellness:detail', kwargs={'analysis_id': analysis.id}))
        assert resp.status_code == 200
        assert 'preliminary AI screening' in analysis.disclaimer

@pytest.mark.django_db
class TestGovernmentSchemes:
    def test_scheme_directory_and_eligibility(self, client):
        scheme = Scheme.objects.create(
            name='PM-KISAN Test', level=Scheme.Level.CENTRAL, applicable_state='All India',
            objective='Direct income support', benefits='₹6000/yr', eligibility_criteria='All landholding farmers',
            official_portal_url='https://pmkisan.gov.in', last_verified_date=date.today()
        )
        resp = client.get(reverse('schemes:list'), {'q': 'PM-KISAN'})
        assert resp.status_code == 200
        assert scheme in resp.context['schemes']

        wiz_resp = client.post(reverse('schemes:eligibility'), {
            'land_size': '2.5', 'is_fpo': 'no', 'crop_type': 'Cereal'
        })
        assert wiz_resp.status_code == 200
        assert len(wiz_resp.context['results']) >= 1

@pytest.mark.django_db
class TestAIKrishiAssistantGrounded:
    def test_grounded_price_and_scheme_responses(self):
        crop = Crop.objects.create(name='Wheat', name_hi='गेहूं')
        mandi = Mandi.objects.create(name='Karnal APMC', district='Karnal', state='Haryana')
        MandiPrice.objects.create(
            mandi=mandi, crop=crop, min_price=2240, max_price=2300, modal_price=2275,
            price_date=date.today()
        )
        hi_res = process_krishi_query("गेहूं का भाव क्या है?", lang='hi')
        assert "2275" in hi_res
        assert "Karnal APMC" in hi_res

        scheme_res = process_krishi_query("योजना के बारे में बताओ", lang='hi')
        assert "सरकारी योजनाएं" in scheme_res

@pytest.mark.django_db
class TestBuyerAndFPONetwork:
    def test_buyer_requirement_and_fpo_membership(self, client):
        b_user = User.objects.create_user(username='buyer_test', password='password', role=User.Role.BUYER)
        buyer = BuyerProfile.objects.create(user=b_user, business_name='Agro Mills Ltd', contact_phone='9812000000')
        crop = Crop.objects.create(name='Paddy')
        req = BuyerRequirement.objects.create(
            buyer=buyer, crop=crop, quantity_required_quintals=100.0, offered_price_per_quintal=3500.0,
            valid_until=date.today()
        )
        resp = client.get(reverse('buyers:list'))
        assert resp.status_code == 200
        assert req in resp.context['requirements']

@pytest.mark.django_db
class TestWeb3TrustLedger:
    def test_canonical_hash_and_tamper_detection(self):
        payload = {"receipt_code": "KS-TEST-001", "quantity": 50, "rate": 2275}
        h1, c1 = compute_canonical_hash(payload)
        h2, c2 = compute_canonical_hash(payload)
        assert h1 == h2

        altered_payload = {"receipt_code": "KS-TEST-001", "quantity": 50, "rate": 9999}
        h_alt, _ = compute_canonical_hash(altered_payload)
        assert h1 != h_alt

    def test_receipt_verification_workflow(self, client):
        user = User.objects.create_user(username='farmer_txn', password='pass', role=User.Role.FARMER)
        farmer = FarmerProfile.objects.create(user=user, state='Haryana', district='Karnal')
        crop = Crop.objects.create(name='Wheat Web3')
        txn = Transaction.objects.create(
            farmer=farmer, crop=crop, quantity_quintals=50.0, agreed_rate_per_quintal=2300.0,
            gross_amount=115000.0, net_payable_to_farmer=114000.0, transaction_date=date.today()
        )
        receipt = generate_digital_receipt(txn)
        
        check = verify_receipt_integrity(receipt.receipt_code)
        assert check['verified'] is True
        assert check['status'] == 'VALID_AUTHENTIC'

        resp = client.get(reverse('web3_ledger:verify'), {'code': receipt.receipt_code, 'tamper': '1'})
        assert resp.status_code == 200
        assert resp.context['result']['verified'] is False
        assert resp.context['result']['status'] == 'TAMPERED_WARNING'

@pytest.mark.django_db
class TestMultilingualAndAccessibility:
    def test_language_switch(self, client):
        resp = client.get(reverse('multilingual:switch', kwargs={'lang_code': 'pa'}))
        assert resp.status_code == 302
        assert client.session.get('django_language') == 'pa'

    def test_accessibility_toggle(self, client):
        resp = client.get(reverse('accessibility:toggle') + '?theme=dark&simple_mode=1')
        assert resp.status_code == 302
        assert client.session.get('a11y_theme') == 'dark'
        assert client.session.get('a11y_simple') is True
