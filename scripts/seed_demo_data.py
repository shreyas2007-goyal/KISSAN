"""
Comprehensive database seeder for KisanSAATHI 2.0 demonstration.
Populates realistic agricultural records across all modules:
Users, Crops, Varieties, Mandis, Prices, Schemes, Diseases, Storages, Transporters,
Transactions, Digital Receipts, and Blockchain Anchors.
"""
import os
import sys
from pathlib import Path
from datetime import date, timedelta

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from apps.accounts.models import AuditLog
from apps.farmers.models import FarmerProfile, FarmerCrop
from apps.buyers.models import BuyerProfile, BuyerRequirement, BuyerEnquiry
from apps.fpos.models import FPO, FPOMembership, FPOCropLot, FPOMemberContribution
from apps.crops.models import Crop, CropVariety
from apps.markets.models import Mandi, MandiPrice
from apps.schemes.models import Scheme, SchemeBookmark
from apps.crop_wellness.models import DiseaseProfile
from apps.logistics.models import StorageFacility, Transporter
from apps.transactions.models import Transaction
from apps.web3_ledger.service import generate_digital_receipt
from apps.notifications.models import Notification
from apps.accessibility.models import UserAccessibilityPreference

User = get_user_model()

def seed_all():
    print("Seeding KisanSAATHI 2.0 Core Demonstration Database...")

    # 1. Superuser / Admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'Dr. Satish',
            'last_name': 'Kumar (Krishi Officer)',
            'email': 'admin@kisansaathi.in',
            'role': User.Role.PLATFORM_ADMIN,
            'is_staff': True,
            'is_superuser': True,
            'preferred_language': 'hi',
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Created Admin user (admin / admin123)")

    # 2. Farmer User 1: Ramesh Kumar (Karnal, Haryana)
    farmer1, created = User.objects.get_or_create(
        username='ramesh_karnal',
        defaults={
            'first_name': 'Ramesh',
            'last_name': 'Kumar',
            'phone_number': '9812044001',
            'role': User.Role.FARMER,
            'preferred_language': 'hi',
        }
    )
    if created:
        farmer1.set_password('farmer123')
        farmer1.save()
        UserAccessibilityPreference.objects.create(user=farmer1)
        print("Created Farmer user (ramesh_karnal / farmer123)")

    farmer_prof1, _ = FarmerProfile.objects.get_or_create(
        user=farmer1,
        defaults={
            'state': 'Haryana',
            'district': 'Karnal',
            'village': 'Kachhwa',
            'landholding_acres': 3.5,
            'has_kcc': True,
        }
    )

    # 3. Farmer User 2: Gurpreet Singh (Ludhiana, Punjab)
    farmer2, created = User.objects.get_or_create(
        username='gurpreet_pb',
        defaults={
            'first_name': 'Gurpreet',
            'last_name': 'Singh',
            'phone_number': '9872011002',
            'role': User.Role.FARMER,
            'preferred_language': 'pa',
        }
    )
    if created:
        farmer2.set_password('farmer123')
        farmer2.save()
        UserAccessibilityPreference.objects.create(user=farmer2)
        print("Created Farmer user (gurpreet_pb / farmer123)")

    farmer_prof2, _ = FarmerProfile.objects.get_or_create(
        user=farmer2,
        defaults={
            'state': 'Punjab',
            'district': 'Ludhiana',
            'village': 'Samrala',
            'landholding_acres': 8.0,
            'has_kcc': True,
        }
    )

    # 4. Buyer User: Shiva Agro Traders (Karnal Mandi)
    buyer_user, created = User.objects.get_or_create(
        username='shiva_agro',
        defaults={
            'first_name': 'Shiva',
            'last_name': 'Agrawal',
            'phone_number': '9896011223',
            'role': User.Role.BUYER,
            'preferred_language': 'en',
        }
    )
    if created:
        buyer_user.set_password('buyer123')
        buyer_user.save()
        print("Created Buyer user (shiva_agro / buyer123)")

    buyer_prof, _ = BuyerProfile.objects.get_or_create(
        user=buyer_user,
        defaults={
            'business_name': 'Shiva Agro Mills & Commodity Traders',
            'category': BuyerProfile.Category.FOOD_PROCESSOR,
            'gst_number': '06AABCU9603R1ZM',
            'mandi_license_number': 'HR-KRN-APMC-8841',
            'verification_level': BuyerProfile.VerificationLevel.LEVEL_4,
            'is_verified': True,
            'state': 'Haryana',
            'district': 'Karnal',
            'contact_phone': '+91 98960 11223',
            'description': 'Leading grain processor purchasing high-grade Sharbati wheat, Basmati paddy, and yellow mustard directly from farmers and FPOs.'
        }
    )

    # 5. FPO Admin User: Kisan Samriddhi FPO
    fpo_user, created = User.objects.get_or_create(
        username='fpo_samriddhi',
        defaults={
            'first_name': 'Baldev',
            'last_name': 'Sharma (CEO)',
            'phone_number': '9812555666',
            'role': User.Role.FPO_ADMIN,
            'preferred_language': 'hi',
        }
    )
    if created:
        fpo_user.set_password('fpo123')
        fpo_user.save()
        print("Created FPO Admin user (fpo_samriddhi / fpo123)")

    fpo_obj, _ = FPO.objects.get_or_create(
        admin_user=fpo_user,
        defaults={
            'name': 'Kisan Samriddhi Farmers Producer Company Ltd',
            'registration_number': 'U01100HR2022PTC104521',
            'state': 'Haryana',
            'district': 'Karnal',
            'headquarters': 'Main Road, Taraori, Karnal',
            'contact_phone': '+91 98125 55666',
            'is_verified': True,
        }
    )
    FPOMembership.objects.get_or_create(fpo=fpo_obj, farmer=farmer_prof1, defaults={'share_units': 15})
    FPOMembership.objects.get_or_create(fpo=fpo_obj, farmer=farmer_prof2, defaults={'share_units': 25})

    # 6. Crops & Varieties
    crops_data = [
        ('Wheat', 'गेहूं', 'ਕਣਕ', Crop.Category.CEREAL, 2275.00, 120, 'Major staple rabi cereal with guaranteed MSP procurement.'),
        ('Paddy (Basmati)', 'धान (बासमती)', 'ਝੋਨਾ (ਬਾਸਮਤੀ)', Crop.Category.CEREAL, 2320.00, 140, 'Premium aromatic rice demanded by international exporters.'),
        ('Mustard (Rape & Mustard)', 'सरसों', 'ਸਰ੍ਹੋਂ', Crop.Category.OILSEED, 5650.00, 110, 'High-oil content rabi oilseed crop with robust local crushing demand.'),
        ('Cotton', 'कपास / नरमा', 'ਕਪਾਹ', Crop.Category.CASH_CROP, 7121.00, 160, 'Long staple fiber commercial crop.'),
        ('Potato', 'आलू', 'ਆਲੂ', Crop.Category.VEGETABLE, 1150.00, 90, 'High-volume tuber vegetable crop.'),
        ('Tomato', 'टमाटर', 'ਟਮਾਟਰ', Crop.Category.VEGETABLE, 1400.00, 85, 'Perishable high-value horticultural vegetable.'),
        ('Gram (Chana)', 'चना', 'ਛੋਲੇ', Crop.Category.PULSE, 5440.00, 115, 'Key protein-rich rabi legume with vital soil nitrogen-fixation benefits.'),
    ]
    created_crops = {}
    for name, hi, pa, cat, msp, days, desc in crops_data:
        c, _ = Crop.objects.get_or_create(
            name=name,
            defaults={
                'name_hi': hi,
                'name_pa': pa,
                'category': cat,
                'standard_msp_quintal': msp,
                'typical_growing_days': days,
                'description': desc,
            }
        )
        created_crops[name] = c

    # Varieties
    CropVariety.objects.get_or_create(crop=created_crops['Wheat'], variety_name='HD-2967', defaults={'maturity_days': 125, 'ideal_soil': 'Alluvial Loam'})
    CropVariety.objects.get_or_create(crop=created_crops['Wheat'], variety_name='DBW-187 (Karan Vandana)', defaults={'maturity_days': 120, 'ideal_soil': 'Rich Loam with good drainage'})
    CropVariety.objects.get_or_create(crop=created_crops['Paddy (Basmati)'], variety_name='Pusa Basmati 1121', defaults={'maturity_days': 140, 'ideal_soil': 'Clay Loam'})
    CropVariety.objects.get_or_create(crop=created_crops['Mustard (Rape & Mustard)'], variety_name='Pusa Bold', defaults={'maturity_days': 110, 'ideal_soil': 'Sandy Loam'})

    # 7. Farmer Crops in Ground
    FarmerCrop.objects.get_or_create(
        farmer=farmer_prof1,
        crop=created_crops['Wheat'],
        defaults={
            'acres': 2.5,
            'sowing_date': date(2026, 11, 10),
            'expected_harvest_date': date(2027, 4, 15),
            'estimated_quantity_quintals': 48.0,
            'status': FarmerCrop.Status.VEGETATIVE,
        }
    )
    FarmerCrop.objects.get_or_create(
        farmer=farmer_prof1,
        crop=created_crops['Mustard (Rape & Mustard)'],
        defaults={
            'acres': 1.0,
            'sowing_date': date(2026, 10, 20),
            'expected_harvest_date': date(2027, 3, 10),
            'estimated_quantity_quintals': 18.0,
            'status': FarmerCrop.Status.FLOWERING,
        }
    )

    # 8. Mandis
    mandis_data = [
        ('Karnal Grain Market (APMC)', 'Haryana', 'Karnal', 1.00, 15.00),
        ('Panipat Grain Mandi', 'Haryana', 'Panipat', 1.00, 15.00),
        ('Khanna Grain Market (Asia Max)', 'Punjab', 'Ludhiana', 1.25, 18.00),
        ('Narela Terminal Mandi', 'Delhi', 'North Delhi', 1.50, 20.00),
        ('Ambala City Mandi Yard', 'Haryana', 'Ambala', 1.00, 15.00),
        ('Indore Grain APMC', 'Madhya Pradesh', 'Indore', 1.00, 16.00),
    ]
    created_mandis = {}
    for name, st, dist, fee, unl in mandis_data:
        m, _ = Mandi.objects.get_or_create(
            name=name, district=dist, state=st,
            defaults={'market_fee_percent': fee, 'unloading_charge_per_quintal': unl}
        )
        created_mandis[name] = m

    # 9. Mandi Prices
    today = date.today()
    prices_data = [
        (created_mandis['Karnal Grain Market (APMC)'], created_crops['Wheat'], 2240.0, 2320.0, 2275.0, 1450.0, MandiPrice.Source.AGMARKNET, False),
        (created_mandis['Narela Terminal Mandi'], created_crops['Wheat'], 2350.0, 2480.0, 2450.0, 3200.0, MandiPrice.Source.AGMARKNET, False),
        (created_mandis['Khanna Grain Market (Asia Max)'], created_crops['Wheat'], 2250.0, 2340.0, 2290.0, 2800.0, MandiPrice.Source.AGMARKNET, False),
        (created_mandis['Karnal Grain Market (APMC)'], created_crops['Paddy (Basmati)'], 3400.0, 3950.0, 3750.0, 890.0, MandiPrice.Source.AGMARKNET, False),
        (created_mandis['Panipat Grain Mandi'], created_crops['Paddy (Basmati)'], 3450.0, 4050.0, 3820.0, 750.0, MandiPrice.Source.DATA_GOV_IN, False),
        (created_mandis['Karnal Grain Market (APMC)'], created_crops['Mustard (Rape & Mustard)'], 5400.0, 5820.0, 5650.0, 420.0, MandiPrice.Source.AGMARKNET, False),
        (created_mandis['Indore Grain APMC'], created_crops['Gram (Chana)'], 5300.0, 5680.0, 5520.0, 680.0, MandiPrice.Source.AGMARKNET, False),
        (created_mandis['Narela Terminal Mandi'], created_crops['Tomato'], 1200.0, 1650.0, 1420.0, 1150.0, MandiPrice.Source.APMC_DIRECT, False),
        (created_mandis['Karnal Grain Market (APMC)'], created_crops['Potato'], 950.0, 1250.0, 1120.0, 1540.0, MandiPrice.Source.APMC_DIRECT, False),
        (created_mandis['Khanna Grain Market (Asia Max)'], created_crops['Cotton'], 6800.0, 7350.0, 7150.0, 560.0, MandiPrice.Source.AGMARKNET, False),
    ]
    for m, c, pmin, pmax, pmodal, arr, src, is_demo in prices_data:
        MandiPrice.objects.get_or_create(
            mandi=m, crop=c, price_date=today,
            defaults={
                'min_price': pmin,
                'max_price': pmax,
                'modal_price': pmodal,
                'arrival_quantity_quintals': arr,
                'source': src,
                'is_demo_data': is_demo,
            }
        )

    # 10. Buyer Requirements
    BuyerRequirement.objects.get_or_create(
        buyer=buyer_prof,
        crop=created_crops['Wheat'],
        defaults={
            'quantity_required_quintals': 500.0,
            'minimum_order_quintals': 10.0,
            'offered_price_per_quintal': 2360.0, # Premium over Karnal mandi modal
            'quality_specifications': 'Max moisture 11.5%, Foreign matter < 0.75%, Zero pesticide taint.',
            'delivery_point': 'Shiva Agro Mill Gate, GT Road, Karnal (Free Weighment)',
            'payment_terms': BuyerRequirement.PaymentTerms.IMMEDIATE,
            'valid_until': today + timedelta(days=25),
            'is_active': True,
        }
    )
    BuyerRequirement.objects.get_or_create(
        buyer=buyer_prof,
        crop=created_crops['Mustard (Rape & Mustard)'],
        defaults={
            'quantity_required_quintals': 250.0,
            'minimum_order_quintals': 5.0,
            'offered_price_per_quintal': 5720.0,
            'quality_specifications': 'Oil content minimum 41%, clean grain with moisture < 8%.',
            'delivery_point': 'Karnal Processing Yard',
            'payment_terms': BuyerRequirement.PaymentTerms.SAME_DAY,
            'valid_until': today + timedelta(days=30),
            'is_active': True,
        }
    )

    # 11. FPO Collective Lot
    fpo_lot, _ = FPOCropLot.objects.get_or_create(
        fpo=fpo_obj,
        crop=created_crops['Wheat'],
        lot_code='FPO-KRN-WHT-2026-001',
        defaults={
            'aggregated_quantity_quintals': 85.0,
            'target_price_per_quintal': 2410.0,
            'quality_grade': 'Grade A - FAQ Machine Cleaned',
            'storage_facility': 'FPO Central Warehouse, Taraori',
            'status': FPOCropLot.Status.OFFERED_TO_BUYERS,
        }
    )
    FPOMemberContribution.objects.get_or_create(
        lot=fpo_lot, farmer=farmer_prof1,
        defaults={'contributed_quantity_quintals': 35.0, 'received_payment_amount': 0.0}
    )
    FPOMemberContribution.objects.get_or_create(
        lot=fpo_lot, farmer=farmer_prof2,
        defaults={'contributed_quantity_quintals': 50.0, 'received_payment_amount': 0.0}
    )

    # 12. Disease Profiles
    diseases = [
        ('Wheat', 'Wheat Rust (Yellow & Brown)', 'गेहूं का रतुआ रोग (पीला व भूरा)', 'ਕਣਕ ਦਾ ਕੁੰਗੀ ਰੋਗ', 'Fungal: Puccinia striiformis',
         'Bright yellow pustules forming linear stripes along leaf veins; powder rubs off on fingers.',
         'खेत की निगरानी करें; संक्रमण दिखते ही प्रोपिकोनाजोल या मैंकोजेब का छिड़काव करें।',
         'Spray Propiconazole 25% EC @ 1ml/liter water; avoid excessive nitrogen fertilizer.',
         'Propiconazole 25% EC (Tilt)', 'MODERATE'),
        ('Wheat', 'Karnal Bunt', 'करनाल बंट रोग', 'ਕਰਨਾਲ ਬੰਟ', 'Fungal: Tilletia indica',
         'Partial grain conversion into black foul-smelling powder (trimethylamine fishy odor).',
         'बीज उपचार कार्बेन्डाजिम से करें; बालियां निकलने के समय अनुकूल मौसम में फफूंदनाशक दें।',
         'Use certified disease-free seed; crop rotation with non-cereal crops.',
         'Carbendazim 50% WP seed treatment', 'SEVERE'),
        ('Paddy (Basmati)', 'Rice Blast (Leaf & Neck Blast)', 'धान का झुलसा रोग (ब्लास्ट)', 'ਝੋਨੇ ਦਾ ਬਲਾਸਟ ਰੋਗ', 'Fungal: Magnaporthe oryzae',
         'Spindle-shaped elliptical lesions with gray centers and brown margins on leaves; neck turns black and snaps.',
         'रोग प्रतिरोधक किस्में उगाएं; प्रारंभिक धब्बे दिखते ही ट्राइसाइक्लाजोल का छिड़काव करें।',
         'Avoid excessive urea; spray Tricyclazole 75% WP @ 0.6g/liter water at tillering.',
         'Tricyclazole 75% WP (Baan)', 'SEVERE'),
        ('Mustard (Rape & Mustard)', 'White Rust & Alternaria Blight', 'सरसों का सफेद रतुआ व झुलसा', 'ਸਰ੍ਹੋਂ ਦਾ ਚਿੱਟਾ ਰੋਗ', 'Oomycete: Albugo candida',
         'White creamy pustules on lower leaf surface; stag-head floral malformation; brown concentric rings.',
         'सफेद फफोले दिखते ही मैंकोजेब या रिडोमिल गोल्ड का छिड़काव करें।',
         'Early sowing in October; spray Mancozeb 75% WP @ 2g/liter water.',
         'Metalaxyl 8% + Mancozeb 64% WP', 'MODERATE'),
        ('Potato', 'Late Blight of Potato', 'आलू का पछेती झुलसा रोग', 'ਆਲੂਆਂ ਦਾ ਪਿਛੇਤਾ ਝੁਲਸਾ ਰੋਗ', 'Oomycete: Phytophthora infestans',
         'Water-soaked dark lesions on leaf tips turning purplish-black with white mildew underneath under humid conditions.',
         'नमी और कोहरे के मौसम में सुरक्षात्मक छिड़काव करें; बीमार पौधों को नष्ट करें।',
         'Preventive spray of Mancozeb @ 2.5g/L; curative spray with Cymoxanil + Mancozeb @ 3g/L.',
         'Cymoxanil 8% + Mancozeb 64% WP', 'SEVERE'),
    ]
    for crop_name, en, hi, pa, causal, symp, treat, prev, pest, sev in diseases:
        c_obj = created_crops.get(crop_name)
        if c_obj:
            DiseaseProfile.objects.get_or_create(
                crop=c_obj, name_en=en,
                defaults={
                    'name_hi': hi,
                    'name_pa': pa,
                    'causal_agent': causal,
                    'symptoms': symp,
                    'symptoms_hi': treat,
                    'treatment': prev,
                    'treatment_hi': treat,
                    'preventive_measures': prev,
                    'recommended_pesticide': pest,
                    'default_severity': sev,
                }
            )

    # 13. Government Schemes
    schemes = [
        ('PM-KISAN Samman Nidhi Yojana', 'पीएम-किसान सम्मान निधि योजना', 'Ministry of Agriculture & Farmers Welfare', Scheme.Level.CENTRAL, 'All India',
         'Direct financial income support to all landholding farmer families across the country.',
         'देश के सभी भूमिधारक किसान परिवारों को आय सहायता प्रदान करना।',
         '₹6,000 per year transferred directly into Aadhaar-seeded bank accounts in 3 equal installments of ₹2,000.',
         '₹6,000 प्रति वर्ष (प्रत्येक ₹2,000 की 3 किस्तों में सीधे बैंक खाते में)।',
         'All farmer families holding cultivable agricultural land in their name. Exclusion: Institutional landholders, income tax payers.',
         'https://pmkisan.gov.in', '155261 / 1800-115-526', date(2026, 11, 1)),
        ('Pradhan Mantri Fasal Bima Yojana (PMFBY)', 'प्रधानमंत्री फसल बीमा योजना', 'Ministry of Agriculture & Farmers Welfare', Scheme.Level.CENTRAL, 'All India',
         'Comprehensive insurance cover against crop loss due to non-preventable natural risks from pre-sowing to post-harvest.',
         'प्राकृतिक आपदाओं, कीटों व बीमारियों के कारण फसल नुकसान से वित्तीय सुरक्षा।',
         'Low premium: Max 2% for Kharif, 1.5% for Rabi, and 5% for Annual Commercial/Horticultural crops. Balance subsidized by Govt.',
         'खरीफ के लिए अधिकतम 2%, रबी के लिए 1.5% प्रीमियम; शेष संपूर्ण प्रीमियम सरकार वहन करती है।',
         'All farmers growing notified crops in notified areas including sharecroppers and tenant farmers.',
         'https://pmfby.gov.in', '1800-180-1551', date(2026, 10, 15)),
        ('Soil Health Card Scheme', 'मृदा स्वास्थ्य कार्ड योजना', 'Department of Agriculture & Farmers Welfare', Scheme.Level.CENTRAL, 'All India',
         'Assessment of soil nutrient status and customized fertilizer application recommendations.',
         'खेत की मिट्टी के 12 पोषक तत्वों की जांच और संतुलित उर्वरक उपयोग की सिफारिश।',
         'Free soil testing report covering Macro nutrients (N, P, K), Secondary nutrient (S), and Micronutrients (Zn, Fe, Cu, Mn, Bo).',
         'मुफ्त मृदा परीक्षण रिपोर्ट; अनावश्यक खाद का खर्च बचाकर 10-15% उत्पादन में वृद्धि।',
         'Available to all farmers across India every 3 years for cycle testing.',
         'https://soilhealth.dac.gov.in', '011-23382012', date(2026, 9, 20)),
        ('Pradhan Mantri Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop)', 'पीएम कृषि सिंचाई योजना (पर ड्रॉप मोर क्रॉप)', 'Ministry of Jal Shakti & MoA', Scheme.Level.CENTRAL, 'All India',
         'Promotion of micro-irrigation technologies (drip and sprinkler systems) for precision water use.',
         'ड्रिप और स्प्रिंकलर सिंचाई प्रणालियों की स्थापना पर सब्सिडी।',
         'Up to 55% financial subsidy for Small/Marginal farmers and 45% for other farmers for installing micro-irrigation kits.',
         'लघु व सीमांत किसानों को 55% तथा अन्य किसानों को 45% तक सरकारी अनुदान।',
         'Farmers having cultivable land with assured water source for irrigation.',
         'https://pmksy.gov.in', '011-24361669', date(2026, 8, 14)),
        ('Agriculture Infrastructure Fund (AIF)', 'कृषि अवसंरचना कोष (AIF)', 'Ministry of Agriculture', Scheme.Level.CENTRAL, 'All India',
         'Financing facility for post-harvest management infrastructure and community farming assets.',
         'गोदाम, कोल्ड स्टोरेज, ग्रेडिंग यूनिट व एग्री-लॉजिस्टिक्स की स्थापना हेतु रियायती ऋण।',
         '3% interest subvention per annum on institutional loans up to ₹2 Crore for a maximum tenure of 7 years, plus CGTMSE fee coverage.',
         '₹2 करोड़ तक के ऋण पर 3% वार्षिक ब्याज छूट और क्रेडिट गारंटी।',
         'Farmers, FPOs, Primary Agricultural Credit Societies (PACS), Agri-entrepreneurs, and Startups.',
         'https://agriinfra.dac.gov.in', '011-23381012', date(2026, 10, 5)),
    ]
    for name, hi, dept, lvl, st, obj, obj_hi, ben, ben_hi, elig, url, help_no, dt in schemes:
        Scheme.objects.get_or_create(
            name=name,
            defaults={
                'name_hi': hi,
                'department': dept,
                'level': lvl,
                'applicable_state': st,
                'objective': obj,
                'objective_hi': obj_hi,
                'benefits': ben,
                'benefits_hi': ben_hi,
                'eligibility_criteria': elig,
                'official_portal_url': url,
                'helpline_number': help_no,
                'last_verified_date': dt,
                'is_active': True,
            }
        )

    # 14. Logistics & Warehouses
    StorageFacility.objects.get_or_create(
        name='Haryana State Warehousing Corp (HSWC) - Karnal Hub',
        defaults={
            'facility_type': StorageFacility.FacilityType.WAREHOUSE,
            'state': 'Haryana',
            'district': 'Karnal',
            'location': 'Near APMC Yard, GT Road, Karnal',
            'total_capacity_mt': 8000.0,
            'available_capacity_mt': 2100.0,
            'monthly_rate_per_quintal': 12.00,
            'contact_phone': '0184-2258900',
            'is_wdra_accredited': True,
        }
    )
    StorageFacility.objects.get_or_create(
        name='Karnal Agro Cold Chain & Perishables Store',
        defaults={
            'facility_type': StorageFacility.FacilityType.COLD_STORAGE,
            'state': 'Haryana',
            'district': 'Karnal',
            'location': 'Taraori Industrial Zone, Karnal',
            'total_capacity_mt': 3500.0,
            'available_capacity_mt': 850.0,
            'monthly_rate_per_quintal': 35.00,
            'contact_phone': '+91 98120 77889',
            'is_wdra_accredited': True,
        }
    )

    Transporter.objects.get_or_create(
        transporter_name='Kisan Rath Rural Transport Service',
        defaults={
            'vehicle_type': Transporter.VehicleType.TRACTOR_TROLLEY,
            'capacity_quintals': 55.0,
            'rate_per_km': 25.00,
            'base_loading_charge': 250.00,
            'operating_district': 'Karnal',
            'contact_phone': '+91 98120 44556',
            'is_verified': True,
        }
    )
    Transporter.objects.get_or_create(
        transporter_name='Sher-e-Punjab Agri Highway Logistics',
        defaults={
            'vehicle_type': Transporter.VehicleType.MEDIUM_TRUCK,
            'capacity_quintals': 100.0,
            'rate_per_km': 42.00,
            'base_loading_charge': 500.00,
            'operating_district': 'Ludhiana',
            'contact_phone': '+91 98720 99887',
            'is_verified': True,
        }
    )

    # 15. Completed Transaction & Web3 Digital Receipt
    txn, _ = Transaction.objects.get_or_create(
        farmer=farmer_prof1,
        buyer=buyer_prof,
        crop=created_crops['Wheat'],
        quantity_quintals=40.0,
        defaults={
            'agreed_rate_per_quintal': 2360.00,
            'gross_amount': 40.0 * 2360.00, # ₹94,400.00
            'total_deductions_expenses': 850.00,
            'net_payable_to_farmer': 93550.00,
            'transaction_date': today - timedelta(days=2),
            'status': Transaction.Status.COMPLETED,
        }
    )
    # Generate on-chain receipt and anchor
    receipt = generate_digital_receipt(txn)
    print(f"Anchored Digital Receipt {receipt.receipt_code} on Web3 Ledger (Hash: {receipt.sha256_hash[:12]}...)")

    # 16. Notifications
    Notification.objects.get_or_create(
        user=farmer1,
        title="Payment Cleared for Wheat Procurement",
        defaults={
            'message': 'Shiva Agro Mills has disbursed ₹93,550.00 for 40 quintals. Digital receipt is anchored on Web3 Trust Ledger.',
            'category': Notification.Category.BUYER_QUOTE,
            'link_url': f'/web3/receipt/{receipt.receipt_code}/',
        }
    )
    Notification.objects.get_or_create(
        user=farmer1,
        title="Rabi Wheat Mandi Price Trend Alert",
        defaults={
            'message': 'Wheat modal rate touched ₹2,275/qtl in Karnal Mandi (+₹25 above MSP). Check net realization options.',
            'category': Notification.Category.PRICE_ALERT,
            'link_url': '/calculator/',
        }
    )

    print("KisanSAATHI 2.0 demonstration database seeded successfully!")

if __name__ == '__main__':
    seed_all()
