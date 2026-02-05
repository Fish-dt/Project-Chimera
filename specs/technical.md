# Technical Specification & Data Contracts

## 1. Agent Handshake Schema
All internal communication between the Planner and Worker agents must validate against this Pydantic-ready JSON schema:
{
  "request_id": "UUID",
  "priority": "LOW | MEDIUM | HIGH",
  "payload": {
    "action": "string",
    "params": "object"
  },
  "max_cost_usdc": "float"
}

## 2. Database ERD (Conceptual)
- **Table: `influencer_state`**: Stores current persona, followers, and engagement metrics.
- **Table: `wallet_ledger`**: ACID-compliant logs of all AgentKit transactions.
- **Vector Store**: Semantic embeddings of previous posts to maintain persona consistency.

## 3. Wallet Manager Skill Contract
- **Module**: `skills.wallet`
- **Class**: `WalletManager`
- **Purpose**: Enforces daily spend limits for AgentKit transactions while delegating actual signing to Coinbase AgentKit.
- **Constructor**:
  - `daily_limit: float` — maximum total spend allowed per 24h window, in USDC.
- **Methods**:
  - `execute_transaction(amount: float, target: str) -> None`
    - **Preconditions**:
      - `amount` must be a positive float.
      - `target` must be a non-empty string.
    - **Behavior**:
      - Validates inputs using Pydantic models.
      - If `amount` exceeds `daily_limit`, raises `PermissionError("DAILY_LIMIT_EXCEEDED")`.
      - Otherwise, records an entry in `wallet_ledger` (persistence stub is allowed) and returns `None`.
    - **Resilience**:
      - Any downstream AgentKit/network failures must surface as a subclass of `RuntimeError`.