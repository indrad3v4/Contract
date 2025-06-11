# DAODISEO Clean Architecture

## Overview

DAODISEO follows Clean Architecture principles with strict separation of concerns and dependency rule enforcement. The system enables real estate tokenization through blockchain integration and AI-powered investment analysis.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    External Interfaces                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Flask Routes│ │   Vue UI    │ │ AI Agents   │           │
│  │             │ │             │ │ (o3-mini)   │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                  Interface Adapters                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  Gateways   │ │Repositories │ │ Presenters  │           │
│  │             │ │             │ │             │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                     Use Cases                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Dashboard   │ │Investment   │ │Orchestrator │           │
│  │ Analytics   │ │ Analysis    │ │  Control    │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                      Entities                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │   Asset     │ │   Wallet    │ │ Validator   │           │
│  │   Model     │ │   Model     │ │   Model     │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## Component Flow

### Request Flow
```
Vue Component → Flask Route → Use Case → Entity
     ↑                                     ↓
Presenter ← Interface Adapter ← Repository ←
```

### AI Analysis Flow
```
User Action → Orchestrator Use Case → o3-mini Agent → Analysis Result
     ↑                                                        ↓
UI Component ← Presenter ← Interface Adapter ← Processing ←
```

## Directory Structure

```
src/
├── entities/                    # Core business objects
│   ├── asset.py                # Real estate asset models
│   ├── wallet.py               # Wallet and transaction models
│   └── validator.py            # Blockchain validator models
│
├── use_cases/                   # Application logic
│   ├── dashboard_analytics.py  # Dashboard data orchestration
│   ├── investment_analysis.py  # Property investment logic
│   └── orchestrator_control.py # AI agent coordination
│
├── interface_adapters/          # Gateways and repositories
│   ├── gateways/
│   │   ├── blockchain_gateway.py    # RPC blockchain access
│   │   └── ai_gateway.py            # OpenAI API access
│   ├── repositories/
│   │   ├── asset_repository.py      # Asset data management
│   │   └── wallet_repository.py     # Wallet state management
│   └── presenters/
│       ├── dashboard_presenter.py   # Dashboard data formatting
│       └── analysis_presenter.py    # AI analysis formatting
│
└── external_interfaces/         # Controllers and UI
    ├── flask_routes/
    │   ├── dashboard_routes.py      # Main dashboard endpoints
    │   └── api_routes.py            # API endpoint controllers
    ├── vue_components/
    │   ├── dashboard.vue            # Main dashboard component
    │   └── bim_viewer.vue           # BIM analysis component
    └── ai_agents/
        └── orchestrator.py          # o3-mini integration
```

## Data Flow

### Blockchain Data
1. **RPC Gateway** → fetches from `testnet-rpc.daodiseo.chaintools.tech`
2. **Repository** → processes and caches data
3. **Use Case** → applies business logic
4. **Presenter** → formats for UI consumption
5. **Vue Component** → renders user interface

### AI Analysis
1. **User Trigger** → button click or data load
2. **Orchestrator Use Case** → coordinates analysis request
3. **AI Gateway** → sends prompt to o3-mini
4. **Analysis Presenter** → formats AI response
5. **Component Update** → displays inline results

## API Endpoints

### Core Endpoints
- `/api/rpc/validators` - Validator data from blockchain
- `/api/rpc/network-status` - Network health metrics
- `/api/rpc/transactions` - Transaction history

### Analysis Endpoints
- `/api/orchestrator/token-metrics` - Token analysis via o3-mini
- `/api/orchestrator/staking-metrics` - Staking analysis
- `/api/orchestrator/analyze-property` - Property investment analysis
- `/api/orchestrator/investment-analysis` - Investment opportunity analysis

## Dependency Rules

1. **Entities** have no dependencies on outer layers
2. **Use Cases** depend only on Entities
3. **Interface Adapters** depend on Use Cases and Entities
4. **External Interfaces** depend on all inner layers

## AI Integration

### o3-mini Orchestrator
Located in `src/external_interfaces/ai_agents/orchestrator.py`

**Capabilities:**
- Real-time blockchain data analysis
- Property investment scoring
- Market trend identification
- Risk assessment calculations

**Response Format:**
```json
{
  "analysis": "Detailed AI analysis text",
  "confidence": 0.85,
  "metrics": {
    "investment_score": "8.2/10",
    "roi_projection": "12.5% annually"
  }
}
```

## Security

- Rate limiting on all API endpoints
- CSRF protection for form submissions
- Secure headers applied to all responses
- Wallet address validation for transactions

## Performance

- Component-level lazy loading
- On-demand AI analysis (click-to-load)
- Efficient data caching in repositories
- Throttled API requests to prevent rate limits