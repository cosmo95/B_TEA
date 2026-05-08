"""
Tests for Categorizer Module
"""

import pytest
from app.data_pipeline.categorizer import Categorizer


class TestCategorizer:
    """
    Test Categorizer class
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.categorizer = Categorizer()
    
    def test_categorize_transactions(self, sample_transactions_df):
        """
        Test transaction categorization
        """
        df, report = self.categorizer.categorize_transactions(sample_transactions_df)
        
        assert 'predicted_category' in df.columns
        assert 'category_confidence' in df.columns
        assert len(df) == len(sample_transactions_df)
        assert report['total_transactions'] == 100
        assert report['categorized_transactions'] == 100
    
    def test_category_keywords(self):
        """
        Test keyword-based categorization
        """
        test_descriptions = {
            'Starbucks Coffee': 'Food & Dining',
            'Uber Ride': 'Transportation',
            'Netflix Subscription': 'Entertainment',
            'Whole Foods Market': 'Food & Dining',
            'Electric Bill': 'Bills & Utilities',
            'Amazon Purchase': 'Shopping',
            'Doctor Visit': 'Healthcare',
            'Gym Membership': 'Healthcare',
            'Pizza Restaurant': 'Food & Dining',
            'Target Shopping': 'Shopping'
        }
        
        for description, expected_category in test_descriptions.items():
            category = self.categorizer._categorize_by_keywords(description)
            assert category == expected_category, f"Failed for {description}: got {category}, expected {expected_category}"
    
    def test_category_distribution(self, sample_transactions_df):
        """
        Test that all transactions are categorized
        """
        df, report = self.categorizer.categorize_transactions(sample_transactions_df)
        
        # Check that all rows have a category
        assert df['predicted_category'].notna().all()
        
        # Check that categories are from the defined list
        valid_categories = set(self.categorizer.CATEGORIES)
        df_categories = set(df['predicted_category'].unique())
        assert df_categories.issubset(valid_categories.union({'Other'}))
        
        # Check report
        assert len(report['category_distribution']) > 0
        assert sum(report['category_distribution'].values()) == 100
    
    def test_unknown_description(self):
        """
        Test handling of unknown descriptions
        """
        category = self.categorizer._categorize_by_keywords('xyz123abc')
        assert category == 'Other'
    
    def test_get_category_list(self):
        """
        Test getting available categories
        """
        categories = self.categorizer.get_category_list()
        assert isinstance(categories, list)
        assert len(categories) == 9
        assert 'Food & Dining' in categories
        assert 'Transportation' in categories
