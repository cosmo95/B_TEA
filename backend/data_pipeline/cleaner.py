"""
Data Cleaner Module - Data Cleaning and Standardization
Cleans, validates, and standardizes transaction data
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Tuple, List
import re

from app.utils.logger import get_logger

logger = get_logger(__name__)


class DataCleaner:
    """
    Cleans and standardizes transaction data
    """
    
    # Currency symbols to remove
    CURRENCY_SYMBOLS = ['$', '€', '£', '¥', '₹', '₽', '₩', '₪', '₦', '₱', '₡', '₲', '₴', '₵']
    
    def __init__(self):
        self.logger = logger
        self.cleaning_report = {}
    
    def clean_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Clean and standardize transaction data
        
        Args:
            df: Raw transaction DataFrame
        
        Returns:
            Tuple of (cleaned_df, cleaning_report)
        """
        self.logger.info(f"Starting data cleaning: {len(df)} rows")
        
        initial_rows = len(df)
        cleaning_steps = {}
        
        # Step 1: Handle missing values
        df, report = self._handle_missing_values(df)
        cleaning_steps['handle_missing_values'] = report
        
        # Step 2: Standardize dates
        df, report = self._standardize_dates(df)
        cleaning_steps['standardize_dates'] = report
        
        # Step 3: Standardize amounts
        df, report = self._standardize_amounts(df)
        cleaning_steps['standardize_amounts'] = report
        
        # Step 4: Standardize descriptions
        df, report = self._standardize_descriptions(df)
        cleaning_steps['standardize_descriptions'] = report
        
        # Step 5: Remove duplicates
        df, report = self._remove_duplicates(df)
        cleaning_steps['remove_duplicates'] = report
        
        # Step 6: Validate data
        df, report = self._validate_data(df)
        cleaning_steps['validate_data'] = report
        
        final_rows = len(df)
        
        self.cleaning_report = {
            'initial_rows': initial_rows,
            'final_rows': final_rows,
            'rows_removed': initial_rows - final_rows,
            'steps': cleaning_steps,
            'completion_timestamp': datetime.now().isoformat()
        }
        
        self.logger.info(f"Data cleaning complete: {final_rows} rows remaining")
        return df, self.cleaning_report
    
    def _handle_missing_values(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Handle missing values in critical columns
        """
        self.logger.info("Handling missing values...")
        
        initial_missing = df.isnull().sum().sum()
        
        # Drop rows with missing critical columns
        critical_cols = ['date', 'amount']
        df = df.dropna(subset=critical_cols)
        
        # Fill missing description with 'Unknown'
        if 'description' in df.columns:
            df['description'] = df['description'].fillna('Unknown')
        
        # Fill missing category with 'Other'
        if 'category' in df.columns:
            df['category'] = df['category'].fillna('Other')
        
        final_missing = df.isnull().sum().sum()
        
        report = {
            'initial_missing_values': int(initial_missing),
            'final_missing_values': int(final_missing),
            'rows_removed': 0
        }
        
        self.logger.info(f"Missing values handled: {initial_missing} -> {final_missing}")
        return df, report
    
    def _standardize_dates(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Standardize date format
        """
        self.logger.info("Standardizing dates...")
        
        try:
            df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
            df = df.dropna(subset=['date'])
            
            report = {
                'date_format': 'YYYY-MM-DD HH:MM:SS',
                'min_date': df['date'].min().isoformat(),
                'max_date': df['date'].max().isoformat(),
                'date_range_days': (df['date'].max() - df['date'].min()).days
            }
            
            self.logger.info(f"Dates standardized. Range: {report['min_date']} to {report['max_date']}")
            return df, report
        except Exception as e:
            self.logger.error(f"Date standardization error: {str(e)}")
            raise
    
    def _standardize_amounts(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Standardize amount values (remove currency symbols, convert to float)
        """
        self.logger.info("Standardizing amounts...")
        
        try:
            # Remove currency symbols
            df['amount'] = df['amount'].astype(str)
            for symbol in self.CURRENCY_SYMBOLS:
                df['amount'] = df['amount'].str.replace(symbol, '', regex=False)
            
            # Remove commas and spaces
            df['amount'] = df['amount'].str.replace(',', '', regex=False)
            df['amount'] = df['amount'].str.replace(' ', '', regex=False)
            
            # Convert to float
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            
            # Remove rows with invalid amounts
            df = df.dropna(subset=['amount'])
            
            # Make amounts positive
            df['amount'] = df['amount'].abs()
            
            report = {
                'total_amount': float(df['amount'].sum()),
                'min_amount': float(df['amount'].min()),
                'max_amount': float(df['amount'].max()),
                'average_amount': float(df['amount'].mean()),
                'median_amount': float(df['amount'].median())
            }
            
            self.logger.info(f"Amounts standardized. Total: {report['total_amount']:.2f}")
            return df, report
        except Exception as e:
            self.logger.error(f"Amount standardization error: {str(e)}")
            raise
    
    def _standardize_descriptions(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Standardize description text
        """
        self.logger.info("Standardizing descriptions...")
        
        if 'description' not in df.columns:
            return df, {'status': 'no_description_column'}
        
        try:
            # Convert to lowercase
            df['description'] = df['description'].str.lower()
            
            # Remove extra whitespace
            df['description'] = df['description'].str.strip()
            df['description'] = df['description'].str.replace(r'\s+', ' ', regex=True)
            
            # Remove special characters but keep meaningful ones
            df['description'] = df['description'].str.replace(r'[^a-z0-9\s\-\.&]', '', regex=True)
            
            report = {
                'unique_descriptions': len(df['description'].unique()),
                'most_common_description': df['description'].value_counts().head(1).index[0],
                'status': 'standardized'
            }
            
            self.logger.info(f"Descriptions standardized: {report['unique_descriptions']} unique")
            return df, report
        except Exception as e:
            self.logger.error(f"Description standardization error: {str(e)}")
            raise
    
    def _remove_duplicates(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Remove duplicate transactions
        """
        self.logger.info("Removing duplicates...")
        
        initial_rows = len(df)
        
        # Consider rows duplicates if date, amount, and description match
        subset_cols = ['date', 'amount', 'description']
        df = df.drop_duplicates(subset=subset_cols, keep='first')
        
        duplicates_removed = initial_rows - len(df)
        
        report = {
            'duplicates_removed': duplicates_removed,
            'percentage_removed': round((duplicates_removed / initial_rows) * 100, 2)
        }
        
        self.logger.info(f"Duplicates removed: {duplicates_removed} rows")
        return df, report
    
    def _validate_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Validate cleaned data
        """
        self.logger.info("Validating data...")
        
        validation_issues = []
        
        # Check for required columns
        required_cols = ['date', 'amount']
        for col in required_cols:
            if col not in df.columns:
                validation_issues.append(f"Missing required column: {col}")
        
        # Check for negative amounts
        if 'amount' in df.columns and (df['amount'] < 0).any():
            validation_issues.append(f"Found {(df['amount'] < 0).sum()} negative amounts")
        
        # Check for future dates
        if 'date' in df.columns:
            future_dates = (df['date'] > datetime.now()).sum()
            if future_dates > 0:
                validation_issues.append(f"Found {future_dates} future dates")
        
        report = {
            'validation_passed': len(validation_issues) == 0,
            'issues': validation_issues,
            'total_rows': len(df),
            'total_amount': float(df['amount'].sum()) if 'amount' in df.columns else 0
        }
        
        self.logger.info(f"Data validation complete: {report['validation_passed']}")
        return df, report
