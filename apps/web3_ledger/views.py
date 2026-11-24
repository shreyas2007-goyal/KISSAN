from django.shortcuts import render, get_object_or_404
from .models import DigitalReceipt
from .service import verify_receipt_integrity

def verify_receipt_view(request):
    code = request.GET.get('code', '').strip()
    result = None
    if code:
        tamper_test = request.GET.get('tamper') == '1'
        receipt = DigitalReceipt.objects.filter(receipt_code=code).first()
        payload = None
        if receipt and tamper_test:
            # Simulate a tampered payload for testing
            import json
            data = json.loads(receipt.canonical_payload)
            data['net_payable_farmer'] = data['net_payable_farmer'] + 50000.00 # Maliciously altered
            payload = json.dumps(data)

        result = verify_receipt_integrity(code, payload_json_str=payload)

    sample_receipts = DigitalReceipt.objects.select_related('transaction__crop', 'transaction__farmer__user')[:5]

    return render(request, 'web3_ledger/verify.html', {
        'code': code,
        'result': result,
        'sample_receipts': sample_receipts,
    })

def receipt_detail_view(request, receipt_code):
    receipt = get_object_or_404(DigitalReceipt.objects.select_related('blockchain_anchor', 'transaction__farmer__user', 'transaction__crop'), receipt_code=receipt_code)
    result = verify_receipt_integrity(receipt_code)
    return render(request, 'web3_ledger/detail.html', {
        'receipt': receipt,
        'verification': result,
    })
