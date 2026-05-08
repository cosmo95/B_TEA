"""
Tests for File Parser Module
"""

import pytest
import pandas as pd
from app.data_pipeline.parser import FileParser


class TestFileParser:
    """
    Test FileParser class
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.parser = FileParser()
    
    def test_parse_csv_basic(self, csv_test_file):
        """
        Test basic CSV parsing
        """
        df, metadata = self.parser.parse_file(csv_test_file)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 100
        assert 'date' in df.columns
        assert 'amount' in df.columns
        assert 'description' in df.columns
        assert metadata['file_type'] == 'csv'
        assert metadata['rows_parsed'] == 100
    
    def test_csv_column_standardization(self, csv_test_file):
        """
        Test that CSV columns are standardized
        """
        df, metadata = self.parser.parse_file(csv_test_file)
        
        # Check that columns are lowercase
        assert all(col.islower() for col in df.columns)
        
        # Check that expected columns exist
        expected_cols = {'date', 'amount', 'description'}
        assert expected_cols.issubset(set(df.columns))
    
    def test_unsupported_file_format(self, tmp_path):
        """
        Test error handling for unsupported file format
        """
        unsupported_file = tmp_path / "test.txt"
        unsupported_file.write_text("test content")
        
        with pytest.raises(ValueError, match="Unsupported file format"):
            self.parser.parse_file(str(unsupported_file))
