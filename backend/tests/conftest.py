"""
Pytest configuration and fixtures
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
import os


@pytest.fixture
def sample_transactions_df():
    """
    Create sample transaction dataframe for testing
    """
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    
    data = {
        'date': dates,
        'amount': [
            45.99, 12.50, 3.99, 85.00, 150.00,  # Food, Small purchases
            22.00, 55.00, 18.50, 95.00, 200.00,  # Transport, Bills
            15.99, 29.99, 120.00, 40.00, 60.00,  # Entertainment, Shopping
            35.00, 14.99, 75.00, 9.99, 110.00,   # Healthcare, Subscriptions
            50.00, 25.00, 88.00, 19.99, 130.00,
            48.00, 21.50, 92.00, 11.99, 140.00,
            52.00, 23.00, 85.50, 13.99, 125.00,
            46.00, 24.99, 90.00, 15.99, 135.00,
            49.00, 22.50, 87.00, 10.99, 145.00,
            51.00, 26.00, 89.00, 14.99, 128.00,
            47.00, 20.00, 86.00, 12.50, 132.00,
            50.50, 25.50, 91.00, 16.50, 138.00,
            45.50, 23.50, 84.00, 11.50, 126.00,
            48.50, 24.50, 88.50, 13.50, 131.00,
            52.50, 27.00, 93.00, 17.00, 142.00,
            46.50, 21.50, 85.50, 12.00, 129.00,
            49.50, 22.00, 89.50, 14.00, 137.00,
            51.50, 25.00, 92.00, 15.50, 141.00,
            44.50, 19.50, 83.00, 10.50, 124.00,
            50.00, 26.50, 90.50, 16.00, 140.00
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
    
    return pd.DataFrame(data)


@pytest.fixture
def csv_test_file(tmp_path, sample_transactions_df):
    """
    Create a temporary CSV file for testing
    """
    csv_path = tmp_path / "test_transactions.csv"
    sample_transactions_df.to_csv(csv_path, index=False)
    return str(csv_path)


@pytest.fixture
def test_data_dir(tmp_path):
    """
    Create a temporary directory for test data
    """
    return str(tmp_path)
