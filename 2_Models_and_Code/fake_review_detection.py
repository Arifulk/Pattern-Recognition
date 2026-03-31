import pandas as pd
import numpy as np
import nltk
import string
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Set style for better plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

print("="*60)
print("  FAKE PRODUCT REVIEW DETECTION SYSTEM")
print("  Pattern Recognition Project")
print("="*60)

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Load dataset
data = pd.read_csv("fake_reviews.csv")
print(f"\n📊 Dataset loaded: {len(data)} reviews")
print(f"   - Genuine reviews: {len(data[data['label'] == 'genuine'])}")
print(f"   - Fake reviews: {len(data[data['label'] == 'fake'])}")
print("\n📝 Sample reviews:")
print(data.head())


# Text Preprocessing
print("\n" + "="*60)
print("  STEP 1: TEXT PREPROCESSING")
print("="*60)

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

data['cleaned_review'] = data['review'].apply(clean_text)
print("\n✅ Text cleaning completed!")
print("\n📋 Before and After cleaning:")
print(data[['review', 'cleaned_review']].head(3))


# Feature Extraction
print("\n" + "="*60)
print("  STEP 2: FEATURE EXTRACTION (TF-IDF)")
print("="*60)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['cleaned_review'])
y = data['label']

print(f"✅ Feature extraction completed!")
print(f"   - Feature matrix shape: {X.shape}")
print(f"   - Number of unique words: {len(vectorizer.get_feature_names_out())}")

# Train-Test Split
print("\n" + "="*60)
print("  STEP 3: TRAIN-TEST SPLIT")
print("="*60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✅ Data split completed!")
print(f"   - Training samples: {X_train.shape[0]}")
print(f"   - Testing samples: {X_test.shape[0]}")


# Model Training
print("\n" + "="*60)
print("  STEP 4: MODEL TRAINING (Naive Bayes)")
print("="*60)

model = MultinomialNB()
model.fit(X_train, y_train)

print("✅ Model training completed!")

# Model Evaluation
print("\n" + "="*60)
print("  STEP 5: MODEL EVALUATION")
print("="*60)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Accuracy: {accuracy * 100:.2f}%")
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Fake', 'Genuine'], 
            yticklabels=['Fake', 'Genuine'])
plt.title('Confusion Matrix - Fake Review Detection', fontsize=16, fontweight='bold')
plt.ylabel('Actual', fontsize=12)
plt.xlabel('Predicted', fontsize=12)
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
print("\n✅ Confusion matrix saved as 'confusion_matrix.png'")

# Dataset Distribution
plt.figure(figsize=(8, 6))
label_counts = data['label'].value_counts()
colors = ['#FF6B6B', '#4ECDC4']
plt.pie(label_counts, labels=label_counts.index, autopct='%1.1f%%', 
        colors=colors, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
plt.title('Dataset Distribution: Genuine vs Fake Reviews', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('dataset_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Dataset distribution saved as 'dataset_distribution.png'")


# Testing with new reviews
print("\n" + "="*60)
print("  STEP 6: TESTING WITH NEW REVIEWS")
print("="*60)

def predict_review(review):
    cleaned = clean_text(review)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0]
    
    return prediction, probability

# Test samples
test_reviews = [
    "Best product ever!!! I bought 5 of them!!!",
    "This product is amazing and works perfectly",
    "Excellent excellent excellent quality amazing amazing",
    "Good quality material and fast shipping service",
    "Buy buy buy now limited offer hurry up amazing"
]

print("\n🧪 Testing with sample reviews:\n")
for i, review in enumerate(test_reviews, 1):
    prediction, prob = predict_review(review)
    confidence = max(prob) * 100
    
    emoji = "🚩" if prediction == "fake" else "✅"
    print(f"{i}. Review: \"{review[:50]}...\"" if len(review) > 50 else f"{i}. Review: \"{review}\"")
    print(f"   {emoji} Prediction: {prediction.upper()} (Confidence: {confidence:.2f}%)\n")

print("="*60)
print("  PROJECT COMPLETED SUCCESSFULLY!")
print("="*60)
print("\n📁 Generated Files:")
print("   1. confusion_matrix.png")
print("   2. dataset_distribution.png")
print("\n✨ Your Fake Review Detection Model is ready!")
print("="*60)


