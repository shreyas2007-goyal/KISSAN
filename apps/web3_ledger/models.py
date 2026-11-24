from django.db import models
from apps.transactions.models import Transaction

class DigitalReceipt(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='receipt')
    receipt_code = models.CharField(max_length=64, unique=True, help_text="e.g. KS-REC-2026-X882")
    canonical_payload = models.TextField(help_text="Deterministic sorted JSON string used for cryptographic hashing")
    sha256_hash = models.CharField(max_length=64, unique=True, help_text="SHA-256 fingerprint of the digital receipt")
    qr_data_payload = models.TextField(help_text="Data encoded within the verification QR code")
    is_tampered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt: {self.receipt_code} [Hash: {self.sha256_hash[:10]}...]"

class BlockchainRecord(models.Model):
    receipt = models.OneToOneField(DigitalReceipt, on_delete=models.CASCADE, related_name='blockchain_anchor')
    smart_contract_address = models.CharField(max_length=42, default='0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0')
    tx_hash = models.CharField(max_length=66, unique=True, default='0x7b4a2e5d8f9c1a3b5e7d9f2a4c6e8b0d1f3a5c7e9b2d4f6a8c0e2b4d6f8a0c2e')
    block_number = models.PositiveIntegerField(default=5892144)
    network_name = models.CharField(max_length=50, default='Sepolia-Ethereum-Testnet')
    is_simulated_demo = models.BooleanField(default=True)
    anchored_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"On-Chain Record: {self.tx_hash[:12]}... (Block #{self.block_number})"
