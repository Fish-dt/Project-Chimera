# Agent Skills Catalog

## 1. `skill-trend-scout`
- **Purpose**: Uses Tavily/Google Search MCP to find viral topics in real-time.
- **Output**: A ranked list of 3 trends with "Viral Potential" scores.

## 2. `skill-wallet-manager`
- **Purpose**: Interfaces with Coinbase AgentKit to sign transactions.
- **Constraint**: Requires a `GOVERNOR_APPROVAL` token for any spend > 2.0 USDC.

## 3. `skill-media-orchestrator`
- **Purpose**: Routes prompts to either Gemini (Image) or Kling (Video) based on the budget.