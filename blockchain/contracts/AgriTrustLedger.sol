// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title AgriTrustLedger
 * @dev KisanSAATHI 2.0 Web3 Agricultural Transaction & Provenance Ledger.
 * Stores tamper-proof SHA-256 cryptographic fingerprints of agricultural receipts and batches.
 * Sensitive commercial and personal information is kept off-chain.
 */
contract AgriTrustLedger {
    address public immutable authority;

    struct AnchorRecord {
        bytes32 receiptHash;
        string receiptCode;
        uint256 timestamp;
        uint256 blockNumber;
        address recorder;
        bool exists;
    }

    // Mapping from receiptCode to AnchorRecord
    mapping(string => AnchorRecord) private records;

    // Mapping from receiptHash to verification status
    mapping(bytes32 => bool) public isHashRegistered;

    event ReceiptAnchored(
        string indexed receiptCode,
        bytes32 indexed receiptHash,
        uint256 timestamp,
        address indexed recorder
    );

    modifier onlyAuthority() {
        require(msg.sender == authority, "AgriTrustLedger: Unauthorized caller");
        _;
    }

    constructor() {
        authority = msg.sender;
    }

    /**
     * @dev Anchors a canonical receipt hash onto the blockchain
     */
    function anchorReceipt(string calldata receiptCode, bytes32 receiptHash) external onlyAuthority {
        require(!records[receiptCode].exists, "AgriTrustLedger: Receipt already anchored");
        require(receiptHash != bytes32(0), "AgriTrustLedger: Invalid hash");

        records[receiptCode] = AnchorRecord({
            receiptHash: receiptHash,
            receiptCode: receiptCode,
            timestamp: block.timestamp,
            blockNumber: block.number,
            recorder: msg.sender,
            exists: true
        });

        isHashRegistered[receiptHash] = true;

        emit ReceiptAnchored(receiptCode, receiptHash, block.timestamp, msg.sender);
    }

    /**
     * @dev Verifies whether a given receipt payload hash matches the on-chain anchor
     */
    function verifyReceipt(string calldata receiptCode, bytes32 computedHash)
        external
        view
        returns (
            bool isValid,
            bytes32 onChainHash,
            uint256 anchorTimestamp,
            uint256 blockNumber
        )
    {
        AnchorRecord memory rec = records[receiptCode];
        if (!rec.exists) {
            return (false, bytes32(0), 0, 0);
        }
        bool valid = (rec.receiptHash == computedHash);
        return (valid, rec.receiptHash, rec.timestamp, rec.blockNumber);
    }
}
