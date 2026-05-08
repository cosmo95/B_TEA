"""
Integration tests for complete data pipeline
"""

import pytest
import pandas as pd
from app.data_pipeline.parser import FileParser
from app.data_pipeline.cleaner import DataCleaner
from app.data_pipeline.categorizer import Categorizer
from app.data_pipeline.analyzer import AnalyticsEngine


class TestPipelineIntegration:
    """
    Test complete pipeline: Parse -> Clean -> Categorize -> Analyze
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.parser = FileParser()
        self.cleaner = DataCleaner()
        self.categorizer = Categorizer()
        self.analyzer = AnalyticsEngine()
    
    def test_complete_pipeline_csv(self, csv_test_file):
        """
        Test complete pipeline with CSV file
        """
        # Step 1: Parse
        print("\n[1/4] PARSING...")
        df, parse_metadata = self.parser.parse_file(csv_test_file)
        print(f"✓ Parsed: {len(df)} rows, columns: {list(df.columns)}")
        
        # Step 2: Clean
        print("\n[2/4] CLEANING...")
        df, clean_report = self.cleaner.clean_data(df)
        print(f"✓ Cleaned: {len(df)} rows remaining")
        print(f"  - Date range: {clean_report['steps']['standardize_dates']['min_date']} to {clean_report['steps']['standardize_dates']['max_date']}")
        print(f"  - Total spent: ${clean_report['steps']['standardize_amounts']['total_amount']:.2f}")
        
        # Step 3: Categorize
        print("\n[3/4] CATEGORIZING...")
        df, cat_report = self.categorizer.categorize_transactions(df)
        print(f"✓ Categorized: All {len(df)} transactions")
        print(f"  - Distribution: {cat_report['category_distribution']}")
        
        # Step 4: Analyze
        print("\n[4/4] ANALYZING...")
        results = self.analyzer.analyze(df)
        print(f"✓ Analysis complete")
        print(f"  - Total spent: ${results['basic_metrics']['total_spent']:.2f}")
        print(f"  - Avg transaction: ${results['basic_metrics']['average_transaction']:.2f}")
        print(f"  - Transactions: {results['basic_metrics']['num_transactions']}")
        print(f"  - Top category: {list(results['category_analysis'].keys())[0]}")
        print(f"  - Recommendations: {len(results['recommendations'])}")
        
        # Assertions
        assert len(df) > 0
        assert 'predicted_category' in df.columns
        assert results['basic_metrics']['total_spent'] > 0
        assert len(results['recommendations']) > 0
        assert len(results['category_analysis']) > 0
    
    def test_pipeline_data_consistency(self, sample_transactions_df):
        """
        Test that data remains consistent through pipeline
        """
        initial_count = len(sample_transactions_df)
        
        # Clean
        df, _ = self.cleaner.clean_data(sample_transactions_df)
        assert len(df) <= initial_count
        
        # Categorize
        df, _ = self.categorizer.categorize_transactions(df)
        assert len(df) > 0
        
        # Analyze
        results = self.analyzer.analyze(df)
        assert results['basic_metrics']['num_transactions'] == len(df)
    
    def test_pipeline_output_format(self, sample_transactions_df):
        """
        Test that pipeline outputs are properly formatted
        """
        # Clean
        df, _ = self.cleaner.clean_data(sample_transactions_df)
        
        # Categorize
        df, _ = self.categorizer.categorize_transactions(df)
        
        # Analyze
        results = self.analyzer.analyze(df)
        
        # Verify output format
        assert isinstance(results['basic_metrics'], dict)
        assert isinstance(results['category_analysis'], dict)
        assert isinstance(results['anomalies'], list)
        assert isinstance(results['recommendations'], list)
        assert isinstance(results['forecast'], dict)
        
        # Verify numeric types
        for key, val in results['basic_metrics'].items():
            if isinstance(val, (int, float)):
                assert val >= 0
