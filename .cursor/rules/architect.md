# Project Chimera: Architect Rules
- **Constraint**: No local GPU. All heavy compute must be API-first.
- **Workflow**: Spec-Driven Development (SDD). NEVER implement a feature without a corresponding file in `/specs`.
- **Commerce**: All agents must be designed to interface with the `Banker Agent` (Coinbase AgentKit) for economic transactions.
- **Environment**: Use `uv` for all dependency management.