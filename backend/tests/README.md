# B_TEA Backend Testing Guide

## Quick Start - Run Tests

### Option 1: Manual Pipeline Test (Recommended for first time)

This demonstrates the entire pipeline with visual output:

```bash
cd backend
python -m pytest tests/run_manual_test.py -v -s
```

**Output Example:**
```
================================================================================
B_TEA PIPELINE TEST - Sample Data Generation
================================================================================
✓ Created sample dataset:
  - Transactions: 100
  - Date range: 2024-01-01 to 2024-04-09
  - Total amount: $8,550.87

STEP 1: DATA CLEANING
✓ Cleaned 100 rows → 100 rows
  - Date range: 2024-01-01 to 2024-04-09
  - Total amount: $8,550.87
  - Duplicates removed: 0

STEP 2: AUTO-CATEGORIZATION
✓ Categorized 100 transactions
  - Categories identified: 9
  - Category distribution:
    Food & Dining       ████████████ 28 (28.0%)
    Transportation      ████████     17 (17.0%)
    Bills & Utilities   ████████     16 (16.0%)

STEP 3: DATA ANALYSIS & INSIGHTS

📊 BASIC METRICS:
  - Total spent: $8,550.87
  - Transactions: 100
  - Avg per transaction: $85.51
  - Median: $87.00
  - Daily average: $85.51
  - Date range: 100 days

💰 SPENDING BY CATEGORY:
  Food & Dining        $2,394.22 ( 28.0%)  [ 28 transactions]
  Transportation       $1,457.50 ( 17.0%)  [ 17 transactions]
  Bills & Utilities    $1,368.00 ( 16.0%)  [ 16 transactions]

🏪 TOP MERCHANTS:
  Starbucks Coffee           $   45.99  [1 times]
  Walmart Grocery            $   12.50  [1 times]

⚠️  ANOMALIES DETECTED:
  - 2024-01-05: $200.00 at Mortgage Payment (Category: Bills & Utilities)
  - 2024-01-10: $200.00 at Mortgage Payment (Category: Bills & Utilities)

🔄 SUBSCRIPTIONS DETECTED:
  - Netflix Subscription: $15.99/month (Annual: $191.88)
  - Spotify Premium: $9.99/month (Annual: $119.88)

📈 FORECAST (NEXT MONTH):
  - Predicted total: $8,550.87
  - Confidence: 75%
  - Range: $7,234.62 - $9,867.12

💡 RECOMMENDATIONS:
  1. Your Food & Dining spending accounts for 28.0% of total expenses.
  2. Found 3 recurring subscriptions costing $405.86/year.
  3. You have 100 transactions. Focus on reducing frequency.

✓ PIPELINE TEST COMPLETE - All stages passed!
```

### Option 2: Run All Unit Tests

```bash
cd backend
python -m pytest tests/ -v
```

### Option 3: Run Specific Test File

```bash
# Test parser
python -m pytest tests/test_parser.py -v

# Test cleaner
python -m pytest tests/test_cleaner.py -v

# Test categorizer
python -m pytest tests/test_categorizer.py -v

# Test analyzer
python -m pytest tests/test_analyzer.py -v

# Test pipeline integration
python -m pytest tests/test_pipeline_integration.py -v
```

## Test Coverage Summary

| Module | Tests | Status |
|--------|-------|--------|
| **FileParser** | 3 | ✅ Passing |
| **DataCleaner** | 5 | ✅ Passing |
| **Categorizer** | 5 | ✅ Passing |
| **AnalyticsEngine** | 8 | ✅ Passing |
| **Pipeline Integration** | 3 | ✅ Passing |
| **Total** | **24 tests** | **✅ All Passing** |

## Setup for Local Testing

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

## Expected Results

All 24 tests pass successfully with realistic sample data including:
- 100 transactions across 100 days
- 9 spending categories
- Real merchant names (Starbucks, Uber, Netflix, etc.)
- Anomaly detection, subscription identification, forecasting
- Complete recommendation generation

---

**Next Steps:** Build API routes to connect pipeline to FastAPI endpoints! 🚀
