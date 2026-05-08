"""
Analytics Engine Module - Data Analysis and Insights Generation
Calculates metrics, detects patterns, and generates insights
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

from app.utils.logger import get_logger

logger = get_logger(__name__)


class AnalyticsEngine:
    """
    Analyzes transaction data and generates insights
    """
    
    def __init__(self):
        self.logger = logger
    
    def analyze(self, df: pd.DataFrame) -> Dict:
        """
        Perform comprehensive analysis on transaction data
        
        Args:
            df: Cleaned and categorized transaction DataFrame
        
        Returns:
            Dictionary with all analytics results
        """
        self.logger.info(f"Starting analysis on {len(df)} transactions...")
        
        try:
            analytics = {
                'basic_metrics': self._calculate_basic_metrics(df),
                'category_analysis': self._analyze_by_category(df),
                'time_analysis': self._analyze_by_time(df),
                'merchant_analysis': self._analyze_merchants(df),
                'anomalies': self._detect_anomalies(df),
                'subscriptions': self._detect_subscriptions(df),
                'trends': self._analyze_trends(df),
                'recommendations': self._generate_recommendations(df),
                'forecast': self._forecast_spending(df)
            }
            
            self.logger.info("Analysis complete")
            return analytics
        except Exception as e:
            self.logger.error(f"Analysis error: {str(e)}")
            raise
    
    def _calculate_basic_metrics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate basic spending metrics
        """
        self.logger.info("Calculating basic metrics...")
        
        total_spent = float(df['amount'].sum())
        num_transactions = len(df)
        avg_transaction = float(df['amount'].mean())
        median_transaction = float(df['amount'].median())
        date_range = (df['date'].max() - df['date'].min()).days + 1
        days_with_spending = df['date'].dt.date.nunique()
        
        return {
            'total_spent': total_spent,
            'num_transactions': num_transactions,
            'average_transaction': avg_transaction,
            'median_transaction': median_transaction,
            'max_transaction': float(df['amount'].max()),
            'min_transaction': float(df['amount'].min()),
            'date_range_days': date_range,
            'days_with_spending': days_with_spending,
            'daily_average': total_spent / date_range if date_range > 0 else 0,
            'transactions_per_day': num_transactions / date_range if date_range > 0 else 0
        }
    
    def _analyze_by_category(self, df: pd.DataFrame) -> Dict:
        """
        Analyze spending by category
        """
        self.logger.info("Analyzing by category...")
        
        category_stats = df.groupby('predicted_category').agg({
            'amount': ['sum', 'mean', 'count', 'min', 'max']
        }).round(2)
        
        category_analysis = {}
        for category in category_stats.index:
            stats = category_stats.loc[category]
            category_analysis[category] = {
                'total': float(stats[('amount', 'sum')]),
                'average': float(stats[('amount', 'mean')]),
                'count': int(stats[('amount', 'count')]),
                'min': float(stats[('amount', 'min')]),
                'max': float(stats[('amount', 'max')]),
                'percentage': float((stats[('amount', 'sum')] / df['amount'].sum()) * 100)
            }
        
        # Sort by total spending
        category_analysis = dict(sorted(
            category_analysis.items(),
            key=lambda x: x[1]['total'],
            reverse=True
        ))
        
        return category_analysis
    
    def _analyze_by_time(self, df: pd.DataFrame) -> Dict:
        """
        Analyze spending patterns over time
        """
        self.logger.info("Analyzing time patterns...")
        
        # Daily analysis
        daily_spending = df.groupby(df['date'].dt.date)['amount'].sum()
        
        # Weekly analysis
        df['week'] = df['date'].dt.isocalendar().week
        weekly_spending = df.groupby('week')['amount'].sum()
        
        # Monthly analysis (if data spans multiple months)
        df['month'] = df['date'].dt.to_period('M')
        monthly_spending = df.groupby('month')['amount'].sum()
        
        # Day of week analysis
        df['day_of_week'] = df['date'].dt.day_name()
        dow_spending = df.groupby('day_of_week')['amount'].agg(['sum', 'count', 'mean'])
        
        return {
            'daily_average': float(daily_spending.mean()),
            'daily_max': float(daily_spending.max()),
            'daily_min': float(daily_spending.min()),
            'weekly_average': float(weekly_spending.mean()),
            'monthly_average': float(monthly_spending.mean()),
            'day_of_week_spending': dow_spending.to_dict() if len(dow_spending) > 0 else {}
        }
    
    def _analyze_merchants(self, df: pd.DataFrame) -> Dict:
        """
        Analyze top merchants
        """
        self.logger.info("Analyzing merchants...")
        
        if 'description' not in df.columns:
            return {'status': 'no_merchant_data'}
        
        merchant_stats = df.groupby('description').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2).sort_values(by=('amount', 'sum'), ascending=False).head(10)
        
        top_merchants = {}
        for merchant in merchant_stats.index:
            stats = merchant_stats.loc[merchant]
            top_merchants[merchant] = {
                'total': float(stats[('amount', 'sum')]),
                'count': int(stats[('amount', 'count')]),
                'average': float(stats[('amount', 'mean')])
            }
        
        return top_merchants
    
    def _detect_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect unusual transactions
        """
        self.logger.info("Detecting anomalies...")
        
        anomalies = []
        
        # Detect unusually large transactions (> 2 std dev from mean)
        mean_amount = df['amount'].mean()
        std_amount = df['amount'].std()
        threshold = mean_amount + (2 * std_amount)
        
        large_transactions = df[df['amount'] > threshold]
        
        for idx, row in large_transactions.iterrows():
            anomalies.append({
                'type': 'large_transaction',
                'date': row['date'].strftime('%Y-%m-%d'),
                'amount': float(row['amount']),
                'description': row['description'],
                'category': row['predicted_category'],
                'deviation': float((row['amount'] - mean_amount) / std_amount)
            })
        
        return anomalies
    
    def _detect_subscriptions(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect recurring subscriptions
        """
        self.logger.info("Detecting subscriptions...")
        
        subscriptions = []
        
        # Group by description and amount
        recurring = df.groupby(['description', 'amount']).size().reset_index(name='count')
        recurring = recurring[recurring['count'] >= 2]  # At least 2 occurrences
        
        for idx, row in recurring.iterrows():
            matching_rows = df[(df['description'] == row['description']) & 
                              (df['amount'] == row['amount'])]
            
            # Check if dates are approximately monthly
            dates = sorted(matching_rows['date'].unique())
            if len(dates) >= 2:
                date_diffs = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
                avg_diff = np.mean(date_diffs)
                
                if 20 <= avg_diff <= 35:  # Approximately monthly
                    subscriptions.append({
                        'merchant': row['description'],
                        'amount': float(row['amount']),
                        'frequency': 'monthly',
                        'occurrences': int(row['count']),
                        'annual_cost': float(row['amount'] * 12),
                        'first_date': dates[0].strftime('%Y-%m-%d'),
                        'last_date': dates[-1].strftime('%Y-%m-%d')
                    })
        
        return subscriptions
    
    def _analyze_trends(self, df: pd.DataFrame) -> Dict:
        """
        Analyze spending trends
        """
        self.logger.info("Analyzing trends...")
        
        df['month'] = df['date'].dt.to_period('M')
        monthly_by_category = df.groupby(['month', 'predicted_category'])['amount'].sum().unstack(fill_value=0)
        
        trends = {}
        for category in monthly_by_category.columns:
            values = monthly_by_category[category].values
            if len(values) >= 2:
                trend_direction = 'increasing' if values[-1] > values[0] else 'decreasing'
                trend_percent = ((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0
                trends[category] = {
                    'direction': trend_direction,
                    'percent_change': float(trend_percent)
                }
        
        return trends
    
    def _generate_recommendations(self, df: pd.DataFrame) -> List[str]:
        """
        Generate actionable recommendations
        """
        self.logger.info("Generating recommendations...")
        
        recommendations = []
        
        # Recommendation 1: High spending categories
        top_category = df.groupby('predicted_category')['amount'].sum().idxmax()
        top_amount = df.groupby('predicted_category')['amount'].sum().max()
        total = df['amount'].sum()
        percentage = (top_amount / total) * 100
        
        if percentage > 30:
            recommendations.append(
                f"Your {top_category} spending accounts for {percentage:.1f}% of total expenses. "
                "Consider setting a budget for this category."
            )
        
        # Recommendation 2: Many transactions
        if len(df) > 100:
            recommendations.append(
                f"You have {len(df)} transactions. Focus on reducing frequency of small purchases "
                "to save more."
            )
        
        # Recommendation 3: Subscriptions
        subscriptions = self._detect_subscriptions(df)
        if len(subscriptions) > 0:
            total_subscriptions = sum(s['amount'] for s in subscriptions)
            annual_subscriptions = total_subscriptions * 12
            recommendations.append(
                f"Found {len(subscriptions)} recurring subscriptions costing ${annual_subscriptions:.2f}/year. "
                "Review which ones are still active."
            )
        
        return recommendations
    
    def _forecast_spending(self, df: pd.DataFrame) -> Dict:
        """
        Forecast next month's spending
        """
        self.logger.info("Forecasting spending...")
        
        df['month'] = df['date'].dt.to_period('M')
        monthly_totals = df.groupby('month')['amount'].sum()
        
        if len(monthly_totals) >= 2:
            avg_monthly = monthly_totals.mean()
            std_monthly = monthly_totals.std()
        else:
            avg_monthly = df['amount'].sum()
            std_monthly = 0
        
        # By category
        category_forecast = {}
        for category in df['predicted_category'].unique():
            category_df = df[df['predicted_category'] == category]
            category_monthly = category_df.groupby('month')['amount'].sum()
            
            if len(category_monthly) >= 2:
                forecast_amount = category_monthly.mean()
            else:
                forecast_amount = category_df['amount'].sum()
            
            category_forecast[category] = float(forecast_amount)
        
        return {
            'next_month_forecast': float(avg_monthly),
            'forecast_lower_bound': float(avg_monthly - std_monthly),
            'forecast_upper_bound': float(avg_monthly + std_monthly),
            'confidence_level': 0.75,
            'by_category': category_forecast
        }
