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