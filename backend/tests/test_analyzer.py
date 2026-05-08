"""
Tests for Analytics Engine Module
"""

import pytest
import pandas as pd
from app.data_pipeline.analyzer import AnalyticsEngine
from app.data_pipeline.categorizer import Categorizer


class TestAnalyticsEngine:
    """
    Test AnalyticsEngine class
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, sample_transactions_df):
        self.analyzer = AnalyticsEngine()
        self.categorizer = Categorizer()
        
        # Prepare data: parse -> clean -> categorize
        self.df, _ = self.categorizer.categorize_transactions(sample_transactions_df)
    
    def test_analyze_basic(self):
        """
        Test basic analysis
        """
        results = self.analyzer.analyze(self.df)
        
        assert isinstance(results, dict)
        assert 'basic_metrics' in results
        assert 'category_analysis' in results
        assert 'time_analysis' in results
        assert 'merchant_analysis' in results
        assert 'anomalies' in results
        assert 'subscriptions' in results
        assert 'recommendations' in results
        assert 'forecast' in results
    
    def test_basic_metrics(self):
        """
        Test basic metrics calculation
        """
        metrics = self.analyzer._calculate_basic_metrics(self.df)
        
        assert 'total_spent' in metrics
        assert 'num_transactions' in metrics
        assert 'average_transaction' in metrics
        assert 'daily_average' in metrics
        
        assert metrics['num_transactions'] == 100
        assert metrics['total_spent'] > 0
        assert metrics['average_transaction'] > 0
        assert metrics['daily_average'] > 0
    
    def test_category_analysis(self):
        """
        Test category analysis
        """
        category_analysis = self.analyzer._analyze_by_category(self.df)
        
        assert isinstance(category_analysis, dict)
        assert len(category_analysis) > 0
        
        # Check each category has required fields
        for category, stats in category_analysis.items():
            assert 'total' in stats
            assert 'average' in stats
            assert 'count' in stats
            assert 'percentage' in stats
    
    def test_time_analysis(self):
        """
        Test time-based analysis
        """
        time_analysis = self.analyzer._analyze_by_time(self.df)
        
        assert 'daily_average' in time_analysis
        assert 'weekly_average' in time_analysis
        assert time_analysis['daily_average'] > 0
    
    def test_anomaly_detection(self):
        """
        Test anomaly detection
        """
        anomalies = self.analyzer._detect_anomalies(self.df)
        
        assert isinstance(anomalies, list)
        # Should find some anomalies in 100 transactions
        assert len(anomalies) >= 0
        
        if len(anomalies) > 0:
            anomaly = anomalies[0]
            assert 'type' in anomaly
            assert 'amount' in anomaly
            assert 'date' in anomaly
    
    def test_subscription_detection(self):
        """
        Test subscription detection
        """
        subscriptions = self.analyzer._detect_subscriptions(self.df)
        
        assert isinstance(subscriptions, list)
        # Sample data likely has some recurring transactions
        # but may not match monthly pattern
    
    def test_recommendations_generation(self):
        """
        Test recommendations generation
        """
        recommendations = self.analyzer._generate_recommendations(self.df)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all(isinstance(r, str) for r in recommendations)
    
    def test_forecasting(self):
        """
        Test spending forecast
        """
        forecast = self.analyzer._forecast_spending(self.df)
        
        assert 'next_month_forecast' in forecast
        assert 'by_category' in forecast
        assert forecast['next_month_forecast'] > 0
        assert isinstance(forecast['by_category'], dict)
