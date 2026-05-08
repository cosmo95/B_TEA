"""
Tests for Data Cleaner Module
"""

import pytest
import pandas as pd
from datetime import datetime
from app.data_pipeline.cleaner import DataCleaner


class TestDataCleaner:
    """
    Test DataCleaner class
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.cleaner = DataCleaner()
    
    def test_clean_data_basic(self, sample_transactions_df):
        """
        Test basic data cleaning
        """
        df, report = self.cleaner.clean_data(sample_transactions_df)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'date' in df.columns
        assert 'amount' in df.columns
        assert isinstance(report, dict)
        assert 'initial_rows' in report
        assert 'final_rows' in report
    
    def test_date_standardization(self, sample_transactions_df):
        """
        Test that dates are properly standardized
        """
        df, report = self.cleaner.clean_data(sample_transactions_df)
        
        # Check that all dates are datetime
        assert pd.api.types.is_datetime64_any_dtype(df['date'])
        
        # Check report contains date info
        assert 'standardize_dates' in report['steps']
        assert 'min_date' in report['steps']['standardize_dates']
        assert 'max_date' in report['steps']['standardize_dates']
    
    def test_amount_standardization(self, sample_transactions_df):
        """
        Test that amounts are properly standardized
        """
        df, report = self.cleaner.clean_data(sample_transactions_df)
        
        # Check that all amounts are numeric and positive
        assert pd.api.types.is_numeric_dtype(df['amount'])
        assert (df['amount'] >= 0).all()
        
        # Check report contains amount stats
        assert 'standardize_amounts' in report['steps']
        assert 'total_amount' in report['steps']['standardize_amounts']
    
    def test_duplicate_removal(self):
        """
        Test that duplicates are removed
        """
        # Create dataframe with duplicates
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-01', '2024-01-02'],
            'amount': [50.0, 50.0, 75.0],
            'description': ['Starbucks', 'Starbucks', 'Restaurant']
        })
        
        cleaned_df, report = self.cleaner.clean_data(df)
        
        # Check that duplicate was removed
        assert len(cleaned_df) == 2
        assert report['steps']['remove_duplicates']['duplicates_removed'] == 1
    
    def test_missing_values_handling(self):
        """
        Test that missing values are handled
        """
        # Create dataframe with missing values
        df = pd.DataFrame({
            'date': ['2024-01-01', None, '2024-01-03'],
            'amount': [50.0, 75.0, None],
            'description': ['Starbucks', 'Restaurant', 'Shop']
        })
        
        cleaned_df, report = self.cleaner.clean_data(df)
        
        # Check that rows with missing critical data are removed
        assert len(cleaned_df) <= len(df)
        assert cleaned_df[['date', 'amount']].isnull().sum().sum() == 0
