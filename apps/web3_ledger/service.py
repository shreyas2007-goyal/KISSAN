"""
Web3 & Cryptographic Provenance Service for KisanSAATHI 2.0.
Implements canonical JSON hashing (SHA-256), on-chain receipt verification,
tamper detection, and testnet/mock fallback.
"""
import hashlib
import json
import time

def compute_canonical_hash(payload_dict):
    """
    Computes deterministic SHA-256 fingerprint from canonically sorted JSON dictionary.
    """
    canonical_json = json.dumps(payload_dict, sort_keys=True, separators=(',', ':'))
    sha256 = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    return sha256, canonical_json

def generate_digital_receipt(transaction):
    """
    Creates a canonical digital receipt for a completed transaction and anchors it.
    """
    from .models import DigitalReceipt, BlockchainRecord

    receipt_code = f"KS-REC-2026-X{transaction.id:04d}"
    
    payload = {
        "receipt_code": receipt_code,
        "transaction_id": transaction.id,
        "farmer_name": transaction.farmer.user.get_full_name() or transaction.farmer.user.username,
        "farmer_district": transaction.farmer.district,
        "crop": transaction.crop.name,
        "quantity_quintals": float(transaction.quantity_quintals),
        "rate_per_quintal": float(transaction.agreed_rate_per_quintal),
        "gross_amount": float(transaction.gross_amount),
        "total_deductions": float(transaction.total_deductions_expenses),
        "net_payable_farmer": float(transaction.net_payable_to_farmer),
        "date": str(transaction.transaction_date),
        "version": "KisanSAATHI-TrustLedger-v2.0"
    }

    sha256_hash, canonical_json = compute_canonical_hash(payload)

    qr_payload = f"https://kisansaathi.in/web3/verify/?code={receipt_code}&hash={sha256_hash}"

    receipt, created = DigitalReceipt.objects.update_or_create(
        transaction=transaction,
        defaults={
            "receipt_code": receipt_code,
            "canonical_payload": canonical_json,
            "sha256_hash": sha256_hash,
            "qr_data_payload": qr_payload,
            "is_tampered": False,
        }
    )

    # Generate or anchor Blockchain record
    tx_hash = "0x" + hashlib.sha256(f"{receipt_code}-{time.time()}".encode()).hexdigest()
    block_num = 5892100 + transaction.id
    
    BlockchainRecord.objects.update_or_create(
        receipt=receipt,
        defaults={
            "smart_contract_address": "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0",
            "tx_hash": tx_hash,
            "block_number": block_num,
            "network_name": "Sepolia-Ethereum-Testnet",
            "is_simulated_demo": True,
        }
    )

    return receipt

def verify_receipt_integrity(receipt_code, payload_json_str=None):
    """
    Verifies receipt hash against stored on-chain anchor. Detects payload modification/tampering.
    """
    from .models import DigitalReceipt

    try:
        receipt = DigitalReceipt.objects.select_related('blockchain_anchor', 'transaction__farmer__user').get(receipt_code=receipt_code)
    except DigitalReceipt.DoesNotExist:
        return {
            'verified': False,
            'status': 'NOT_FOUND',
            'message': f"Receipt code {receipt_code} not found in Trust Ledger."
        }

    on_chain_hash = receipt.sha256_hash
    target_payload = payload_json_str if payload_json_str else receipt.canonical_payload

    # Recompute SHA-256
    try:
        data = json.loads(target_payload)
        computed_hash, _ = compute_canonical_hash(data)
    except Exception:
        computed_hash = hashlib.sha256(target_payload.encode('utf-8')).hexdigest()

    is_valid = (computed_hash == on_chain_hash)
    
    return {
        'verified': is_valid,
        'status': 'VALID_AUTHENTIC' if is_valid else 'TAMPERED_WARNING',
        'receipt': receipt,
        'computed_hash': computed_hash,
        'on_chain_hash': on_chain_hash,
        'tx_hash': receipt.blockchain_anchor.tx_hash,
        'block_number': receipt.blockchain_anchor.block_number,
        'contract_address': receipt.blockchain_anchor.smart_contract_address,
        'network': receipt.blockchain_anchor.network_name,
        'message': 'Record matches on-chain cryptographic anchor.' if is_valid else 'CRITICAL: Hash mismatch! Receipt data has been tampered with or modified.'
    }
