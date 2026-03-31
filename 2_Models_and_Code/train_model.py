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
import time

# Set style for plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

print("="*70)
print("  🎯 FAKE REVIEW DETECTION - ADVANCED MODEL TRAINING")
print("  Large Dataset Training System")
print("="*70)

# Download NLTK data
print("\n📥 Setting up NLTK...")
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Load dataset
print("\n" + "="*70)
print("  STEP 1: LOADING DATASET")
print("="*70)
start_time = time.time()

data = pd.read_csv("fake reviews dataset.csv")
print(f"\n✅ Dataset loaded successfully!")
print(f"   - Total reviews: {len(data):,}")
print(f"   - CG (Computer Generated/Fake): {len(data[data['label'] == 'CG']):,}")
print(f"   - OR (Original/Genuine): {len(data[data['label'] == 'OR']):,}")
print(f"   - Categories: {data['category'].nunique()}")
print(f"   - Loading time: {time.time() - start_time:.2f} seconds")

# Show sample data
print("\n📝 Sample reviews:")
print(data[['label', 'rating', 'text_']].head(3))

# Text Preprocessing
print("\n" + "="*70)
print("  STEP 2: TEXT PREPROCESSING")
print("="*70)
start_time = time.time()

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """Clean and preprocess text data"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

print("🔄 Cleaning text data (this may take a minute)...")
data['cleaned_text'] = data['text_'].apply(clean_text)
print(f"✅ Text preprocessing completed!")
print(f"   - Processing time: {time.time() - start_time:.2f} seconds")

print("\n📋 Before and After cleaning:")
for i in range(2):
    print(f"\n{i+1}. Original: {data['text_'].iloc[i][:60]}...")
    print(f"   Cleaned:  {data['cleaned_text'].iloc[i][:60]}...")

# Feature Extraction
print("\n" + "="*70)
print("  STEP 3: FEATURE EXTRACTION (TF-IDF)")
print("="*70)
start_time = time.time()

vectorizer = TfidfVectorizer(max_features=5000)  # Top 5000 most important words
X = vectorizer.fit_transform(data['cleaned_text'])
y = data['label']

print(f"✅ Feature extraction completed!")
print(f"   - Feature matrix shape: {X.shape}")
print(f"   - Number of features: {X.shape[1]:,}")
print(f"   - Processing time: {time.time() - start_time:.2f} seconds")

# Train-Test Split
print("\n" + "="*70)
print("  STEP 4: TRAIN-TEST SPLIT")
print("="*70)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✅ Data split completed!")
print(f"   - Training samples: {X_train.shape[0]:,} (80%)")
print(f"   - Testing samples: {X_test.shape[0]:,} (20%)")

# Model Training
print("\n" + "="*70)
print("  STEP 5: MODEL TRAINING (Naive Bayes)")
print("="*70)
start_time = time.time()

model = MultinomialNB()
print("🔄 Training model on {:,} samples...".format(X_train.shape[0]))
model.fit(X_train, y_train)

training_time = time.time() - start_time
print(f"✅ Model training completed!")
print(f"   - Training time: {training_time:.2f} seconds")

# Model Evaluation
print("\n" + "="*70)
print("  STEP 6: MODEL EVALUATION")
print("="*70)
start_time = time.time()

# Predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Calculate accuracy
train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"\n🎯 MODEL PERFORMANCE:")
print(f"   - Training Accuracy: {train_accuracy * 100:.2f}%")
print(f"   - Testing Accuracy:  {test_accuracy * 100:.2f}%")
print(f"   - Prediction time: {time.time() - start_time:.2f} seconds")

print("\n📊 Detailed Classification Report (Test Set):")
print(classification_report(y_test, y_pred_test, 
                          target_names=['Computer Generated (Fake)', 'Original (Genuine)']))

# Confusion Matrix
print("\n" + "="*70)
print("  STEP 7: GENERATING VISUALIZATIONS")
print("="*70)

cm = confusion_matrix(y_test, y_pred_test)

# Plot confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['CG (Fake)', 'OR (Genuine)'], 
            yticklabels=['CG (Fake)', 'OR (Genuine)'],
            cbar_kws={'label': 'Count'})
plt.title('Confusion Matrix - Fake Review Detection\n(40,432 Reviews)', 
          fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Actual Label', fontsize=12, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('advanced_confusion_matrix.png', dpi=300, bbox_inches='tight')
print("✅ Confusion matrix saved as 'advanced_confusion_matrix.png'")

# Plot dataset distribution
plt.figure(figsize=(10, 8))
label_counts = data['label'].value_counts()
colors = ['#FF6B6B', '#4ECDC4']
explode = (0.05, 0.05)
plt.pie(label_counts, labels=['Computer Generated (Fake)', 'Original (Genuine)'], 
        autopct='%1.1f%%', colors=colors, startangle=90, explode=explode,
        textprops={'fontsize': 12, 'fontweight': 'bold'},
        shadow=True)
plt.title(f'Dataset Distribution\n{len(data):,} Total Reviews', 
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('advanced_dataset_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Dataset distribution saved as 'advanced_dataset_distribution.png'")

# Plot accuracy comparison
plt.figure(figsize=(10, 6))
accuracies = [train_accuracy * 100, test_accuracy * 100]
labels = ['Training\nAccuracy', 'Testing\nAccuracy']
colors_bar = ['#4ECDC4', '#FF6B6B']
bars = plt.bar(labels, accuracies, color=colors_bar, alpha=0.8, edgecolor='black', linewidth=2)
plt.ylim([0, 105])
plt.ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
plt.title('Model Performance Comparison', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{acc:.2f}%',
             ha='center', va='bottom', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('advanced_accuracy_comparison.png', dpi=300, bbox_inches='tight')
print("✅ Accuracy comparison saved as 'advanced_accuracy_comparison.png'")

# Testing with new reviews
print("\n" + "="*70)
print("  STEP 8: TESTING WITH NEW REVIEWS")
print("="*70)

def predict_review(review):
    """Predict if a review is fake or genuine"""
    cleaned = clean_text(review)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0]
    
    label = "FAKE (Computer Generated)" if prediction == "CG" else "GENUINE (Original)"
    confidence = max(probability) * 100
    
    return label, confidence

# Test samples
test_reviews = [
    "Best product ever!!! I bought 5 of them!!! Amazing quality!!!",
    "This product works well for my needs. Had it for 3 months.",
    "Excellent excellent excellent amazing wonderful perfect buy now",
    "Good quality material and fast shipping. Works as described.",
    "Buy buy buy now limited offer hurry amazing deal",
    "The product arrived on time and meets my expectations.",
    "Perfect perfect perfect five stars highly recommended amazing",
    "Decent product for the price but delivery was delayed"
]

print("\n🧪 Testing with sample reviews:\n")
for i, review in enumerate(test_reviews, 1):
    label, confidence = predict_review(review)
    
    emoji = "🚩" if "FAKE" in label else "✅"
    print(f"{i}. Review: \"{review[:55]}...\"" if len(review) > 55 else f"{i}. Review: \"{review}\"")
    print(f"   {emoji} Prediction: {label}")
    print(f"   📊 Confidence: {confidence:.2f}%\n")

# Summary
print("="*70)
print("  🎉 PROJECT TRAINING COMPLETED SUCCESSFULLY!")
print("="*70)

print(f"\n📊 FINAL STATISTICS:")
print(f"   - Total reviews processed: {len(data):,}")
print(f"   - Training samples: {X_train.shape[0]:,}")
print(f"   - Testing samples: {X_test.shape[0]:,}")
print(f"   - Training accuracy: {train_accuracy * 100:.2f}%")
print(f"   - Testing accuracy: {test_accuracy * 100:.2f}%")
print(f"   - Number of features: {X.shape[1]:,}")

print(f"\n📁 Generated Files:")
print(f"   1. advanced_confusion_matrix.png")
print(f"   2. advanced_dataset_distribution.png")
print(f"   3. advanced_accuracy_comparison.png")

print("\n✨ Your Advanced Fake Review Detection Model is ready!")
print("="*70)
