"""
File Parser Module - CSV and PDF Parsing
Extracts transaction data from various file formats
"""

import pandas as pd
import pdfplumber
from typing import List, Dict, Tuple
from datetime import datetime
import os

from app.utils.logger import get_logger

logger = get_logger(__name__)


class FileParser:
    """
    Parses CSV and PDF files to extract transaction data
    """
    
    # Common column name patterns
    DATE_PATTERNS = ['date', 'transaction_date', 'trans_date', 'posted_date', 'day']
    AMOUNT_PATTERNS = ['amount', 'value', 'transaction_amount', 'debit', 'credit']
    DESCRIPTION_PATTERNS = ['description', 'merchant', 'note', 'reference', 'detail']
    CATEGORY_PATTERNS = ['category', 'type', 'transaction_type', 'category_code']
    
    def __init__(self):
        self.logger = logger
    
    def parse_file(self, file_path: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Parse CSV or PDF file and return transactions dataframe
        
        Args:
            file_path: Path to CSV or PDF file
        
        Returns:
            Tuple of (DataFrame, metadata_dict)
        
        Raises:
            ValueError: If file format not supported
            Exception: If parsing fails
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.csv':
                return self._parse_csv(file_path)
            elif file_ext == '.pdf':
                return self._parse_pdf(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
        except Exception as e:
            self.logger.error(f"Error parsing file {file_path}: {str(e)}")
            raise
    
    def _parse_csv(self, file_path: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Parse CSV file
        
        Args:
            file_path: Path to CSV file
        
        Returns:
            Tuple of (DataFrame, metadata)
        """
        self.logger.info(f"Parsing CSV file: {file_path}")
        
        try:
            # Read CSV with various encodings
            df = None
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    self.logger.info(f"CSV read successfully with encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("Could not read CSV with any encoding")
            
            # Standardize column names
            df.columns = [col.strip().lower() for col in df.columns]
            
            # Detect and rename columns
            df = self._standardize_columns(df)
            
            metadata = {
                'file_type': 'csv',
                'rows_parsed': len(df),
                'columns': list(df.columns),
                'parse_timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"CSV parsed successfully: {len(df)} rows")
            return df, metadata
        
        except Exception as e:
            self.logger.error(f"CSV parsing error: {str(e)}")
            raise
    
    def _parse_pdf(self, file_path: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Parse PDF file (assumes tabular data)
        
        Args:
            file_path: Path to PDF file
        
        Returns:
            Tuple of (DataFrame, metadata)
        """
        self.logger.info(f"Parsing PDF file: {file_path}")
        
        try:
            all_tables = []
            
            with pdfplumber.open(file_path) as pdf:
                self.logger.info(f"PDF has {len(pdf.pages)} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            df_table = pd.DataFrame(table[1:], columns=table[0])
                            all_tables.append(df_table)
                        self.logger.info(f"Extracted {len(tables)} table(s) from page {page_num}")
            
            if not all_tables:
                raise ValueError("No tables found in PDF")
            
            # Combine all tables
            df = pd.concat(all_tables, ignore_index=True)
            
            # Standardize columns
            df.columns = [col.strip().lower() for col in df.columns]
            df = self._standardize_columns(df)
            
            metadata = {
                'file_type': 'pdf',
                'rows_parsed': len(df),
                'pages_parsed': len(pdf.pages),
                'columns': list(df.columns),
                'parse_timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"PDF parsed successfully: {len(df)} rows")
            return df, metadata
        
        except Exception as e:
            self.logger.error(f"PDF parsing error: {str(e)}")
            raise
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names to known patterns
        
        Args:
            df: DataFrame with columns to standardize
        
        Returns:
            DataFrame with standardized column names
        """
        column_mapping = {}
        
        for col in df.columns:
            col_lower = col.lower()
            
            # Match date column
            if any(pattern in col_lower for pattern in self.DATE_PATTERNS):
                if 'date' not in column_mapping:
                    column_mapping[col] = 'date'
            
            # Match amount column
            elif any(pattern in col_lower for pattern in self.AMOUNT_PATTERNS):
                if 'amount' not in column_mapping:
                    column_mapping[col] = 'amount'
            
            # Match description column
            elif any(pattern in col_lower for pattern in self.DESCRIPTION_PATTERNS):
                if 'description' not in column_mapping:
                    column_mapping[col] = 'description'
            
            # Match category column
            elif any(pattern in col_lower for pattern in self.CATEGORY_PATTERNS):
                if 'category' not in column_mapping:
                    column_mapping[col] = 'category'
        
        df = df.rename(columns=column_mapping)
        self.logger.info(f"Column mapping applied: {column_mapping}")
        
        return df
