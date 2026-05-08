"""
Auto-Categorizer Module - ML-based Transaction Categorization
Automatically categorizes transactions based on description and patterns
"""

import pandas as pd
import re
from typing import Tuple, Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from app.utils.logger import get_logger

logger = get_logger(__name__)


class Categorizer:
    """
    Auto-categorizes transactions using keyword matching and ML
    """
    
    # Keyword-based category mapping (fallback method)
    CATEGORY_KEYWORDS = {
        'Food & Dining': [
            'restaurant', 'cafe', 'coffee', 'pizza', 'burger', 'food', 'grocery',
            'supermarket', 'bakery', 'diner', 'pub', 'bar', 'lunch', 'dinner',
            'breakfast', 'delivery', 'uber eats', 'doordash', 'grubhub', 'starbucks'
        ],
        'Transportation': [
            'uber', 'lyft', 'taxi', 'gas', 'fuel', 'parking', 'toll', 'metro',
            'transit', 'bus', 'train', 'airline', 'flight', 'hotel', 'airbnb',
            'car rental', 'vehicle', 'auto', 'mechanic', 'repair'
        ],
        'Bills & Utilities': [
            'electric', 'water', 'gas', 'internet', 'phone', 'mobile', 'utility',
            'bill', 'payment', 'insurance', 'mortgage', 'rent', 'lease'
        ],
        'Entertainment': [
            'movie', 'cinema', 'netflix', 'spotify', 'hulu', 'disney', 'game',
            'gaming', 'concert', 'ticket', 'theater', 'entertainment', 'streaming',
            'youtube', 'music', 'show', 'event'
        ],
        'Shopping': [
            'amazon', 'ebay', 'walmart', 'target', 'mall', 'store', 'shop',
            'retail', 'clothing', 'apparel', 'fashion', 'nike', 'adidas',
            'zara', 'h&m', 'uniqlo', 'department store'
        ],
        'Healthcare': [
            'doctor', 'hospital', 'pharmacy', 'medical', 'dental', 'clinic',
            'health', 'medicine', 'prescription', 'cvs', 'walgreens', 'therapist',
            'gym', 'fitness', 'surgeon'
        ],
        'Education': [
            'school', 'university', 'college', 'education', 'tuition', 'course',
            'training', 'lesson', 'book', 'study', 'udemy', 'coursera', 'teacher'
        ],
        'Personal Care': [
            'salon', 'haircut', 'barber', 'spa', 'beauty', 'cosmetic', 'massage',
            'grooming', 'laundry', 'cleaning', 'personal'
        ],
        'Subscriptions': [
            'subscription', 'monthly', 'renewal', 'recurring', 'membership',
            'premium', 'netflix', 'spotify', 'aws', 'app store', 'play store'
        ]
    }
    
    CATEGORIES = list(CATEGORY_KEYWORDS.keys())
    
    def __init__(self):
        self.logger = logger
        self.vectorizer = None
        self.model = None
    
    def categorize_transactions(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Categorize all transactions in dataframe
        
        Args:
            df: DataFrame with 'description' column
        
        Returns:
            Tuple of (df_with_categories, categorization_report)
        """
        self.logger.info(f"Categorizing {len(df)} transactions...")
        
        if 'description' not in df.columns:
            raise ValueError("DataFrame must have 'description' column")
        
        # Apply keyword-based categorization
        df['predicted_category'] = df['description'].apply(self._categorize_by_keywords)
        df['category_confidence'] = 0.5  # Default confidence for keyword matching
        
        # Count categories
        category_counts = df['predicted_category'].value_counts().to_dict()
        
        report = {
            'total_transactions': len(df),
            'categorized_transactions': len(df),
            'category_distribution': category_counts,
            'uncategorized': len(df[df['predicted_category'] == 'Other']),
            'method': 'keyword_matching',
            'average_confidence': float(df['category_confidence'].mean())
        }
        
        self.logger.info(f"Categorization complete. Distribution: {category_counts}")
        return df, report
    
    def _categorize_by_keywords(self, description: str) -> str:
        """
        Categorize transaction by matching keywords in description
        
        Args:
            description: Transaction description
        
        Returns:
            Category name
        """
        if not description or not isinstance(description, str):
            return 'Other'
        
        description_lower = description.lower()
        
        # Check each category's keywords
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in description_lower:
                    return category
        
        return 'Other'
    
    def get_category_list(self) -> List[str]:
        """
        Get list of available categories
        
        Returns:
            List of category names
        """
        return self.CATEGORIES
    
    def train_model(self, descriptions: List[str], categories: List[str]) -> Dict:
        """
        Train ML model on labeled data (for future enhancement)
        
        Args:
            descriptions: List of transaction descriptions
            categories: List of corresponding categories
        
        Returns:
            Training report
        """
        self.logger.info(f"Training categorization model on {len(descriptions)} samples...")
        
        try:
            # Vectorize descriptions
            self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            X = self.vectorizer.fit_transform(descriptions)
            
            # Train model
            self.model = MultinomialNB()
            self.model.fit(X, categories)
            
            report = {
                'status': 'success',
                'samples_trained': len(descriptions),
                'features': len(self.vectorizer.get_feature_names_out()),
                'categories': len(set(categories))
            }
            
            self.logger.info(f"Model training complete: {report}")
            return report
        except Exception as e:
            self.logger.error(f"Model training failed: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def predict_with_model(self, descriptions: List[str]) -> List[Tuple[str, float]]:
        """
        Predict categories using trained ML model
        
        Args:
            descriptions: List of transaction descriptions
        
        Returns:
            List of (category, confidence) tuples
        """
        if not self.model or not self.vectorizer:
            self.logger.warning("Model not trained, falling back to keyword matching")
            return [(self._categorize_by_keywords(desc), 0.5) for desc in descriptions]
        
        try:
            X = self.vectorizer.transform(descriptions)
            predictions = self.model.predict(X)
            confidences = self.model.predict_proba(X).max(axis=1)
            
            return list(zip(predictions, confidences))
        except Exception as e:
            self.logger.error(f"Prediction failed: {str(e)}")
            return [(self._categorize_by_keywords(desc), 0.5) for desc in descriptions]
