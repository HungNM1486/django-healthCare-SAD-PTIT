# chatbot/nlp.py
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os

class NLPProcessor:
    def __init__(self):
        self.vietnamese_stopwords = [
            'và', 'của', 'có', 'là', 'để', 'trong', 'với', 'cho', 'được', 
            'người', 'này', 'nhưng', 'mà', 'không', 'một', 'các', 'những',
            'thì', 'bị', 'cũng', 'như', 'làm', 'gì', 'nào', 'đó', 'rất',
            'ở', 'đi', 'đến', 'từ', 'về', 'lên', 'xuống', 'ra', 'vào'
        ]
        
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),  # Use unigrams and bigrams
            max_features=5000,
            min_df=1
        )
        
        self.model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml_models')
        os.makedirs(self.model_dir, exist_ok=True)
        
        self.model_file = os.path.join(self.model_dir, 'tfidf_model.pkl')
        self.intent_file = os.path.join(self.model_dir, 'intents.pkl')
        
        # Load model if exists
        if os.path.exists(self.model_file) and os.path.exists(self.intent_file):
            self.load_model()
        else:
            self.X_train_tfidf = None
            self.training_data = []
            self.intents = []
    
    def preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation but keep Vietnamese diacritics
        text = re.sub(r'[^\w\s\u00C0-\u024FÀ-ỹ]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove stopwords
        tokens = text.split()
        tokens = [token for token in tokens if token not in self.vietnamese_stopwords]
        
        return ' '.join(tokens)
    
    def train_model(self, training_phrases, intents):
        # Preprocess training phrases
        self.training_data = [self.preprocess_text(phrase) for phrase in training_phrases]
        self.intents = intents
        
        # Create TF-IDF vectors
        self.X_train_tfidf = self.vectorizer.fit_transform(self.training_data)
        
        # Save model
        with open(self.model_file, 'wb') as f:
            pickle.dump((self.vectorizer, self.X_train_tfidf), f)
        
        with open(self.intent_file, 'wb') as f:
            pickle.dump((self.training_data, self.intents), f)
    
    def load_model(self):
        with open(self.model_file, 'rb') as f:
            self.vectorizer, self.X_train_tfidf = pickle.load(f)
        
        with open(self.intent_file, 'rb') as f:
            self.training_data, self.intents = pickle.load(f)
    
    def predict_intent(self, text, threshold=0.3):
        if not self.training_data:
            return None, 0
            
        # Preprocess input text
        processed_text = self.preprocess_text(text)
        
        # Transform input text using trained vectorizer
        X_input_tfidf = self.vectorizer.transform([processed_text])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(X_input_tfidf, self.X_train_tfidf)[0]
        
        # Get the index of the highest similarity score
        max_score_index = np.argmax(similarity_scores)
        max_score = similarity_scores[max_score_index]
        
        # Return the predicted intent if score is above threshold
        if max_score >= threshold:
            return self.intents[max_score_index], max_score
        else:
            return None, max_score