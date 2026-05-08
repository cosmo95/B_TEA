# B_TEA - Intelligent Expense Analysis Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![React 18+](https://img.shields.io/badge/React-18+-61dafb.svg)](https://react.dev/)

## 🎯 Overview

**B_TEA** is an AI-powered financial analysis platform that transforms raw expense data into actionable insights. Upload your financial documents (CSV/PDF) and get professional-grade analysis, visualization, and forecasting—automatically.

### Problem
Users struggle to understand their spending patterns without tedious manual analysis.

### Solution
**One-click upload → Comprehensive analytics dashboard** with insights a financial analyst would provide.

### Why B_TEA?
- ✅ **Better than Splitwise**: Automatic parsing, real insights (vs manual logging)
- ✅ **Better than Bank Apps**: Privacy-first, smarter analysis, actionable recommendations
- ✅ **Affordable**: $5/month vs $500+ for real analyst

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+ (for local development)
- Node 18+ (for frontend development)

### Option 1: Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/cosmo95/B_TEA.git
cd B_TEA

# Start all services
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm start
```

---

## 📋 Features (MVP - Phase 1)

### ✨ Core Capabilities
- 📤 **File Upload**: CSV & PDF parsing with auto-detection
- 🧹 **Data Cleaning**: Standardization, deduplication, currency handling
- 🤖 **Auto-Categorization**: ML-powered transaction categorization
- 📊 **Analytics Dashboard**: Beautiful charts, spending breakdown, trends
- 💡 **Smart Insights**: Subscriptions, anomalies, behavioral patterns
- 📈 **Forecasting**: Next month predictions with confidence intervals
- 💬 **Recommendations**: Actionable suggestions to optimize spending
- 📄 **Export**: PDF reports & cleaned CSV data

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (React 18)    │
└────────┬────────┘
         │ HTTP/REST API
┌────────▼─────────────────────────────┐
│   FastAPI Backend                    │
│  ┌──────────────────────────────┐   │
│  │ Data Processing Pipeline:    │   │
│  │ • Parser (CSV/PDF)           │   │
│  │ • Cleaner                    │   │
│  │ • Categorizer (ML)           │   │
│  │ • Analyzer (Insights)        │   │
│  │ • Forecaster                 │   │
│  └──────────────────────────────┘   │
└────────┬──────────────────┬──────────┘
         │                  │
    ┌────▼───┐         ┌────▼──────┐
    │   DB   │         │   Redis   │
    │(PostgreSQL)      │ (Caching) │
    └────────┘         └───────────┘
```

### Tech Stack

**Backend:**
- FastAPI (API framework)
- Pandas & NumPy (data processing)
- Scikit-learn (ML categorization)
- pdfplumber (PDF parsing)
- SQLAlchemy (ORM)
- PostgreSQL (database)
- Redis (caching)
- Celery (async tasks)

**Frontend:**
- React 18 (UI framework)
- Recharts (data visualization)
- TailwindCSS (styling)
- Axios (API client)
- TypeScript (type safety)

---

## 📁 Project Structure

```
B_TEA/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app initialization
│   │   ├── api/
│   │   │   ├── routes/          # API endpoints
│   │   │   └── models/          # Pydantic schemas
│   │   ├── database/            # SQLAlchemy models
│   │   └── utils/               # Config, logging, helpers
│   ├── data_pipeline/
│   │   ├── parser.py            # CSV/PDF parsing
│   │   ├── cleaner.py           # Data cleaning
│   │   ├── categorizer.py       # Auto-categorization
│   │   └── analyzer.py          # Analytics & insights
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API calls
│   │   ├── types/               # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
├── PRD.txt                      # Product Requirements Document
└── README.md
```

---

## 🔌 API Endpoints (MVP)

### Health Check
```
GET /health
→ Returns: { status: "healthy" }
```

### File Upload & Analysis
```
POST /api/v1/analysis/upload
Body: { file: File }
→ Returns: { analysis_id: UUID, status: "processing" }

GET /api/v1/analysis/{analysis_id}
→ Returns: { transactions, metrics, status }

GET /api/v1/insights/{analysis_id}
→ Returns: { subscriptions, anomalies, trends, recommendations }

GET /api/v1/forecast/{analysis_id}
→ Returns: { predictions by category, confidence }

GET /api/v1/report/{analysis_id}
→ Returns: PDF file download
```

---

## 📊 Data Pipeline

```
1. File Upload
   ↓
2. Validation & Parsing (CSV/PDF)
   ↓
3. Data Cleaning (standardization, deduplication)
   ↓
4. Auto-Categorization (ML model)
   ↓
5. Analytics (metrics, patterns, anomalies)
   ↓
6. Forecasting (next month predictions)
   ↓
7. Report Generation (PDF + JSON)
```

---

## 💡 Key Features Explained

### Auto-Categorization
ML model trained on common transaction patterns automatically assigns categories:
- Food & Dining
- Transportation
- Bills & Utilities
- Entertainment
- Shopping
- Healthcare
- Education
- Personal Care
- Subscriptions
- Other

### Smart Insights
- **Subscriptions**: Detect recurring monthly charges (Netflix, Spotify, gym)
- **Anomalies**: Flag unusual spending spikes
- **Trends**: Show category growth/decline over time
- **Behavioral**: Weekend vs weekday patterns
- **Recommendations**: Actionable suggestions to save money

### Forecasting
- Next month spending prediction
- Category-wise forecasts
- Confidence intervals
- Seasonal adjustment

---

## 🔐 Security

- ✅ Encrypted file upload (AES-256 at rest)
- ✅ HTTPS for all communication
- ✅ Automatic file deletion (30 days)
- ✅ Rate limiting on API
- ✅ Optional user authentication
- ✅ GDPR-compliant data retention

---

## 📈 Roadmap

### Phase 1 (MVP) - Months 1-2 ⚡
- ✅ File parsing & cleaning
- ✅ Auto-categorization
- ✅ Analytics dashboard
- ✅ Insights generation
- ✅ PDF reports

### Phase 2 (Polish) - Months 3-4 🎨
- User accounts
- Save/manage analyses
- Mobile responsive
- Performance optimization

### Phase 3 (Monetization) - Months 5-6 💰
- Freemium launch
- Stripe integration
- API for Business tier

### Phase 4 (Growth) - Months 7+ 🚀
- Bank API integrations
- Budget planning
- Mobile apps
- 10k+ users

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Cosmo** - [GitHub](https://github.com/cosmo95)

---

## 🚀 Getting Help

- 📖 Read the [PRD.txt](PRD.txt) for detailed product specifications
- 🐛 Report bugs in [Issues](https://github.com/cosmo95/B_TEA/issues)
- 💬 Discuss ideas in [Discussions](https://github.com/cosmo95/B_TEA/discussions)
- 📧 Contact via email (if available)

---

**Made with ❤️ for open source**
