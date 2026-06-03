"""
Manual integration test to demonstrate the pipeline
Run with: python -m backend.tests.run_manual_test
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from datetime import datetime, timedelta
from data_pipeline.parser import FileParser
from data_pipeline.cleaner import DataCleaner
from data_pipeline.categorizer import Categorizer
from data_pipeline.analyzer import AnalyticsEngine
import json


def create_sample_data():
    """
    Create comprehensive sample transaction data
    """
    print("\n" + "="*80)
    print("B_TEA PIPELINE TEST - Sample Data Generation")
    print("="*80)
    
    # Generate 100 realistic transactions over 3 months
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    
    transactions = {
        'date': dates,
        'amount': [
            45.99, 12.50, 3.99, 85.00, 150.00, 22.00, 55.00, 18.50, 95.00, 200.00,
            15.99, 29.99, 120.00, 40.00, 60.00, 35.00, 14.99, 75.00, 9.99, 110.00,
            50.00, 25.00, 88.00, 19.99, 130.00, 48.00, 21.50, 92.00, 11.99, 140.00,
            52.00, 23.00, 85.50, 13.99, 125.00, 46.00, 24.99, 90.00, 15.99, 135.00,
            49.00, 22.50, 87.00, 10.99, 145.00, 51.00, 26.00, 89.00, 14.99, 128.00,
            47.00, 20.00, 86.00, 12.50, 132.00, 50.50, 25.50, 91.00, 16.50, 138.00,
            45.50, 23.50, 84.00, 11.50, 126.00, 48.50, 24.50, 88.50, 13.50, 131.00,
            52.50, 27.00, 93.00, 17.00, 142.00, 46.50, 21.50, 85.50, 12.00, 129.00,
            49.50, 22.00, 89.50, 14.00, 137.00, 51.50, 25.00, 92.00, 15.50, 141.00,
            44.50, 19.50, 83.00, 10.50, 124.00, 50.00, 26.50, 90.50, 16.00, 140.00
        ],
        'description': [
            'Starbucks Coffee', 'Walmart Grocery', 'Fast Food', 'Amazon Purchase', 'Whole Foods Market',
            'Uber Ride', 'Gas Station', 'Movie Tickets', 'Electric Bill', 'Mortgage Payment',
            'Netflix Subscription', 'Pizza Restaurant', 'Target Shopping', 'Gym Membership', 'Doctor Visit',
            'Restaurant Dinner', 'Coffee Shop', 'Furniture Store', 'Spotify Premium', 'Hotel Stay',
            'Grocery Store', 'Pharmacy Prescription', 'Restaurant Lunch', 'App Store Purchase', 'Airline Ticket',
            'Cafe Coffee', 'Fast Food Lunch', 'Retail Store', 'Subscription Service', 'Train Fare',
            'Restaurant Dinner', 'Book Purchase', 'Mall Shopping', 'Laundry Service', 'Car Repair',
            'Cafe Breakfast', 'Supermarket', 'Restaurant Lunch', 'Gaming PC Parts', 'Vacation Hotel',
            'Restaurant Dinner', 'Pharmacy', 'Shopping Center', 'Hair Salon', 'Concert Tickets',
            'Coffee Shop', 'Grocery Delivery', 'Restaurant', 'Beauty Products', 'Flight Booking',
            'Restaurant Lunch', 'Retail Store', 'Restaurant Dinner', 'Movie Theatre', 'Dental Visit',
            'Supermarket Grocery', 'Coffee Shop', 'Restaurant Dinner', 'Rideshare', 'Medical Appointment',
            'Restaurant Breakfast', 'Fast Food', 'Shopping Mall', 'Parking Garage', 'Hotel Check-in',
            'Cafe Coffee', 'Restaurant Lunch', 'Retail Purchase', 'Pet Store', 'Insurance Payment',
            'Grocery Store', 'Pharmacy', 'Restaurant Dinner', 'Electronics Store', 'Library Fine',
            'Restaurant Lunch', 'Shopping Center', 'Restaurant Dinner', 'Fitness Class', 'Airline Booking',
            'Coffee Shop', 'Supermarket', 'Restaurant Lunch', 'Clothing Store', 'Subscription Service',
            'Restaurant Dinner', 'Fast Food', 'Shopping Mall', 'Haircut', 'Car Maintenance',
            'Cafe Coffee', 'Grocery Delivery', 'Restaurant Lunch', 'Electronics', 'Hotel Booking',
            'Restaurant Dinner', 'Retail Store', 'Restaurant Breakfast', 'Music Lessons', 'Travel Booking'
        ]
    }
    
    df = pd.DataFrame(transactions)
    print(f"\n✓ Created sample dataset:")
    print(f"  - Transactions: {len(df)}")
    print(f"  - Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"  - Total amount: ${df['amount'].sum():.2f}")
    
    return df


def run_pipeline_test():
    """
    Run complete pipeline test
    """
    print("\n" + "="*80)
    print("RUNNING COMPLETE PIPELINE TEST")
    print("="*80)
    
    # Initialize modules
    parser = FileParser()
    cleaner = DataCleaner()
    categorizer = Categorizer()
    analyzer = AnalyticsEngine()
    
    # Create sample data
    raw_data = create_sample_data()
    
    # STEP 1: Clean data
    print("\n" + "-"*80)
    print("STEP 1: DATA CLEANING")
    print("-"*80)
    cleaned_df, clean_report = cleaner.clean_data(raw_data)
    print(f"✓ Cleaned {len(raw_data)} rows → {len(cleaned_df)} rows")
    print(f"  - Date range: {clean_report['steps']['standardize_dates']['min_date']} to {clean_report['steps']['standardize_dates']['max_date']}")
    print(f"  - Total amount: ${clean_report['steps']['standardize_amounts']['total_amount']:.2f}")
    print(f"  - Duplicates removed: {clean_report['steps']['remove_duplicates']['duplicates_removed']}")
    
    # STEP 2: Categorize transactions
    print("\n" + "-"*80)
    print("STEP 2: AUTO-CATEGORIZATION")
    print("-"*80)
    categorized_df, cat_report = categorizer.categorize_transactions(cleaned_df)
    print(f"✓ Categorized {len(categorized_df)} transactions")
    print(f"  - Categories identified: {len(cat_report['category_distribution'])}")
    print(f"  - Category distribution:")
    for category, count in sorted(cat_report['category_distribution'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(categorized_df)) * 100
        bar = '█' * int(percentage / 5)
        print(f"    {category:20} {bar:20} {count:3} ({percentage:5.1f}%)")
    
    # STEP 3: Analyze data
    print("\n" + "-"*80)
    print("STEP 3: DATA ANALYSIS & INSIGHTS")
    print("-"*80)
    results = analyzer.analyze(categorized_df)
    
    # Display basic metrics
    print("\n📊 BASIC METRICS:")
    metrics = results['basic_metrics']
    print(f"  - Total spent: ${metrics['total_spent']:.2f}")
    print(f"  - Transactions: {metrics['num_transactions']}")
    print(f"  - Avg per transaction: ${metrics['average_transaction']:.2f}")
    print(f"  - Median: ${metrics['median_transaction']:.2f}")
    print(f"  - Daily average: ${metrics['daily_average']:.2f}")
    print(f"  - Date range: {metrics['date_range_days']} days")
    
    # Display category breakdown
    print("\n💰 SPENDING BY CATEGORY:")
    for category, stats in list(results['category_analysis'].items())[:5]:
        print(f"  {category:20} ${stats['total']:8.2f} ({stats['percentage']:5.1f}%)  [{stats['count']:3} transactions]")
    
    # Display top merchants
    print("\n🏪 TOP MERCHANTS:")
    for merchant, stats in list(results['merchant_analysis'].items())[:5]:
        print(f"  {merchant:30} ${stats['total']:8.2f}  [{stats['count']} times]")
    
    # Display anomalies
    print("\n⚠️  ANOMALIES DETECTED:")
    anomalies = results['anomalies']
    if len(anomalies) > 0:
        for anomaly in anomalies[:3]:
            print(f"  - {anomaly['date']}: ${anomaly['amount']:.2f} at {anomaly['description']} (Category: {anomaly['category']})")
    else:
        print("  - No significant anomalies found")
    
    # Display subscriptions
    print("\n🔄 SUBSCRIPTIONS DETECTED:")
    subscriptions = results['subscriptions']
    if len(subscriptions) > 0:
        for sub in subscriptions:
            print(f"  - {sub['merchant']}: ${sub['amount']:.2f}/month (Annual: ${sub['annual_cost']:.2f})")
    else:
        print("  - No recurring subscriptions detected")
    
    # Display forecast
    print("\n📈 FORECAST (NEXT MONTH):")
    forecast = results['forecast']
    print(f"  - Predicted total: ${forecast['next_month_forecast']:.2f}")
    print(f"  - Confidence: {forecast['confidence_level']*100:.0f}%")
    print(f"  - Range: ${forecast['forecast_lower_bound']:.2f} - ${forecast['forecast_upper_bound']:.2f}")
    
    # Display recommendations
    print("\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print("\n" + "="*80)
    print("✓ PIPELINE TEST COMPLETE - All stages passed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_pipeline_test()
