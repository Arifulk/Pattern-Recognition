import pandas as pd
import numpy as np
import nltk
import string
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import time
from datetime import datetime
import joblib

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

print("="*70)
print("  🚀 MEGA MODEL TRAINING - 1 MILLION REVIEWS")
print("  Advanced Machine Learning Pipeline")
print("="*70)

# NLTK setup
print("\n📥 Setting up NLTK...")
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# STEP 1: Load Dataset
print("\n" + "="*70)
print("  STEP 1: LOADING MEGA DATASET")
print("="*70)
start_time = time.time()

data = pd.read_csv("mega_dataset_1million.csv")
load_time = time.time() - start_time

print(f"\n✅ Dataset loaded successfully!")
print(f"   - Total reviews: {len(data):,}")
print(f"   - CG (Computer Generated/Fake): {len(data[data['label'] == 'CG']):,}")
print(f"   - OR (Original/Genuine): {len(data[data['label'] == 'OR']):,}")
print(f"   - Categories: {data['category'].nunique()}")
print(f"   - Loading time: {load_time:.2f} seconds")
print(f"   - Dataset size: {data.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")

# Show sample
print("\n📝 Sample reviews:")
print(data[['label', 'rating', 'text_']].head(3))

# STEP 2: Text Preprocessing
print("\n" + "="*70)
print("  STEP 2: TEXT PREPROCESSING (1M REVIEWS)")
print("="*70)
start_time = time.time()

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """Clean and preprocess text"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

print("🔄 Cleaning 1,000,000 reviews (this may take 2-3 minutes)...")
print("   Progress updates every 200,000 reviews...")

batch_size = 200000
cleaned_texts = []

for i in range(0, len(data), batch_size):
    batch_end = min(i + batch_size, len(data))
    batch = data['text_'].iloc[i:batch_end]
    cleaned_batch = batch.apply(clean_text)
    cleaned_texts.extend(cleaned_batch.tolist())
    print(f"   Processed {batch_end:,} / {len(data):,} reviews ({batch_end/len(data)*100:.1f}%)")

data['cleaned_text'] = cleaned_texts
preprocess_time = time.time() - start_time

print(f"✅ Text preprocessing completed!")
print(f"   - Processing time: {preprocess_time:.2f} seconds ({preprocess_time/60:.2f} minutes)")

# Show examples
print("\n📋 Cleaning examples:")
for i in range(2):
    print(f"\n{i+1}. Original: {data['text_'].iloc[i][:60]}...")
    print(f"   Cleaned:  {data['cleaned_text'].iloc[i][:60]}...")

# STEP 3: Feature Extraction
print("\n" + "="*70)
print("  STEP 3: FEATURE EXTRACTION (TF-IDF)")
print("="*70)
start_time = time.time()

print("🔄 Extracting features from 1,000,000 reviews...")
vectorizer = TfidfVectorizer(max_features=10000, min_df=5, max_df=0.8)
X = vectorizer.fit_transform(data['cleaned_text'])
y = data['label']

feature_time = time.time() - start_time

print(f"✅ Feature extraction completed!")
print(f"   - Feature matrix shape: {X.shape}")
print(f"   - Number of features: {X.shape[1]:,}")
print(f"   - Matrix density: {X.nnz / (X.shape[0] * X.shape[1]) * 100:.2f}%")
print(f"   - Processing time: {feature_time:.2f} seconds")

# STEP 4: Train-Test Split
print("\n" + "="*70)
print("  STEP 4: TRAIN-TEST SPLIT")
print("="*70)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✅ Data split completed!")
print(f"   - Training samples: {X_train.shape[0]:,} (80%)")
print(f"   - Testing samples: {X_test.shape[0]:,} (20%)")

# STEP 5: Model Training (Naive Bayes)
print("\n" + "="*70)
print("  STEP 5: TRAINING NAIVE BAYES MODEL")
print("="*70)
start_time = time.time()

model_nb = MultinomialNB()
print(f"🔄 Training Naive Bayes on {X_train.shape[0]:,} samples...")
model_nb.fit(X_train, y_train)

nb_train_time = time.time() - start_time
print(f"✅ Naive Bayes training completed!")
print(f"   - Training time: {nb_train_time:.2f} seconds")

# STEP 6: Model Training (Logistic Regression)
print("\n" + "="*70)
print("  STEP 6: TRAINING LOGISTIC REGRESSION MODEL")
print("="*70)
start_time = time.time()

model_lr = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
print(f"🔄 Training Logistic Regression on {X_train.shape[0]:,} samples...")
model_lr.fit(X_train, y_train)

lr_train_time = time.time() - start_time
print(f"✅ Logistic Regression training completed!")
print(f"   - Training time: {lr_train_time:.2f} seconds")

# STEP 7: Model Evaluation
print("\n" + "="*70)
print("  STEP 7: MODEL EVALUATION")
print("="*70)

# Naive Bayes predictions
print("\n📊 Evaluating Naive Bayes...")
y_pred_nb_train = model_nb.predict(X_train)
y_pred_nb_test = model_nb.predict(X_test)
nb_train_acc = accuracy_score(y_train, y_pred_nb_train)
nb_test_acc = accuracy_score(y_test, y_pred_nb_test)

# Logistic Regression predictions
print("📊 Evaluating Logistic Regression...")
y_pred_lr_train = model_lr.predict(X_train)
y_pred_lr_test = model_lr.predict(X_test)
lr_train_acc = accuracy_score(y_train, y_pred_lr_train)
lr_test_acc = accuracy_score(y_test, y_pred_lr_test)

# Display results
print("\n" + "="*70)
print("  🎯 MODEL PERFORMANCE COMPARISON")
print("="*70)

print(f"\n📊 NAIVE BAYES:")
print(f"   - Training Accuracy: {nb_train_acc * 100:.2f}%")
print(f"   - Testing Accuracy:  {nb_test_acc * 100:.2f}%")

print(f"\n📊 LOGISTIC REGRESSION:")
print(f"   - Training Accuracy: {lr_train_acc * 100:.2f}%")
print(f"   - Testing Accuracy:  {lr_test_acc * 100:.2f}%")

# Detailed report for best model
best_model = model_lr if lr_test_acc > nb_test_acc else model_nb
best_name = "Logistic Regression" if lr_test_acc > nb_test_acc else "Naive Bayes"
best_pred = y_pred_lr_test if lr_test_acc > nb_test_acc else y_pred_nb_test

print(f"\n🏆 Best Model: {best_name}")
print("\n📊 Detailed Classification Report:")
print(classification_report(y_test, best_pred, 
                          target_names=['Computer Generated (Fake)', 'Original (Genuine)']))

# STEP 8: Visualizations
print("\n" + "="*70)
print("  STEP 8: GENERATING VISUALIZATIONS")
print("="*70)

# Confusion Matrix
cm = confusion_matrix(y_test, best_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='RdYlGn', 
            xticklabels=['CG (Fake)', 'OR (Genuine)'], 
            yticklabels=['CG (Fake)', 'OR (Genuine)'],
            cbar_kws={'label': 'Count'}, annot_kws={'size': 16})
plt.title(f'Confusion Matrix - {best_name}\n1,000,000 Reviews Training', 
          fontsize=18, fontweight='bold', pad=20)
plt.ylabel('Actual Label', fontsize=14, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('mega_confusion_matrix.png', dpi=300, bbox_inches='tight')
print("✅ Confusion matrix saved as 'mega_confusion_matrix.png'")

# Model Comparison
plt.figure(figsize=(12, 7))
models = ['Naive Bayes\nTrain', 'Naive Bayes\nTest', 
          'Logistic Reg\nTrain', 'Logistic Reg\nTest']
accuracies = [nb_train_acc * 100, nb_test_acc * 100, 
              lr_train_acc * 100, lr_test_acc * 100]
colors_bar = ['#4ECDC4', '#FF6B6B', '#95E1D3', '#F38181']

bars = plt.bar(models, accuracies, color=colors_bar, alpha=0.8, 
               edgecolor='black', linewidth=2)
plt.ylim([0, 105])
plt.ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
plt.title('Model Performance Comparison\n1 Million Reviews Dataset', 
          fontsize=18, fontweight='bold', pad=20)
plt.grid(axis='y', alpha=0.3)

for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{acc:.2f}%', ha='center', va='bottom', 
             fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('mega_model_comparison.png', dpi=300, bbox_inches='tight')
print("✅ Model comparison saved as 'mega_model_comparison.png'")

# Dataset distribution
plt.figure(figsize=(10, 8))
label_counts = data['label'].value_counts()
colors_pie = ['#FF6B6B', '#4ECDC4']
explode = (0.05, 0.05)
wedges, texts, autotexts = plt.pie(label_counts, 
                                     labels=['Computer Generated (Fake)', 'Original (Genuine)'], 
                                     autopct='%1.1f%%', colors=colors_pie, 
                                     startangle=90, explode=explode,
                                     textprops={'fontsize': 13, 'fontweight': 'bold'},
                                     shadow=True)
plt.title(f'Dataset Distribution\n{len(data):,} Total Reviews', 
          fontsize=18, fontweight='bold', pad=20)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(14)
plt.tight_layout()
plt.savefig('mega_dataset_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Dataset distribution saved as 'mega_dataset_distribution.png'")

# STEP 9: Save Model
print("\n" + "="*70)
print("  STEP 9: SAVING MODEL")
print("="*70)

print("💾 Saving trained model and vectorizer...")
joblib.dump(best_model, 'mega_model.pkl')
joblib.dump(vectorizer, 'mega_vectorizer.pkl')
print(f"✅ Model saved as 'mega_model.pkl'")
print(f"✅ Vectorizer saved as 'mega_vectorizer.pkl'")

# STEP 10: Test with examples
print("\n" + "="*70)
print("  STEP 10: TESTING WITH NEW REVIEWS")
print("="*70)

def predict_review(review, model, vectorizer):
    """Predict if a review is fake or genuine"""
    cleaned = clean_text(review)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0]
    
    label = "FAKE (Computer Generated)" if prediction == "CG" else "GENUINE (Original)"
    confidence = max(probability) * 100
    
    return label, confidence

test_reviews = [
    "Best product ever!!! I bought 5 of them!!! Amazing quality!!!",
    "I've been using this for 3 months and it works well. No issues so far.",
    "Excellent excellent excellent amazing wonderful perfect buy now",
    "The product arrived on time. Good quality for the price.",
    "Buy buy buy now limited offer hurry amazing deal",
    "Decent product but delivery took longer than expected.",
    "Perfect perfect perfect five stars highly recommended amazing",
    "Works as described. My kids like it. Would buy again.",
]

print("\n🧪 Testing with sample reviews:\n")
for i, review in enumerate(test_reviews, 1):
    label, confidence = predict_review(review, best_model, vectorizer)
    
    emoji = "🚩" if "FAKE" in label else "✅"
    print(f"{i}. \"{review[:55]}...\"" if len(review) > 55 else f"{i}. \"{review}\"")
    print(f"   {emoji} {label}")
    print(f"   📊 Confidence: {confidence:.2f}%\n")

# Final Summary
print("="*70)
print("  🎉 MEGA MODEL TRAINING COMPLETED!")
print("="*70)

print(f"\n📊 TRAINING SUMMARY:")
print(f"   - Dataset: 1,000,000 reviews")
print(f"   - Training samples: {X_train.shape[0]:,}")
print(f"   - Testing samples: {X_test.shape[0]:,}")
print(f"   - Features: {X.shape[1]:,}")
print(f"   - Best model: {best_name}")
print(f"   - Best test accuracy: {max(nb_test_acc, lr_test_acc) * 100:.2f}%")

print(f"\n⏱️  TIME BREAKDOWN:")
print(f"   - Data loading: {load_time:.2f}s")
print(f"   - Preprocessing: {preprocess_time:.2f}s ({preprocess_time/60:.2f}m)")
print(f"   - Feature extraction: {feature_time:.2f}s")
print(f"   - Naive Bayes training: {nb_train_time:.2f}s")
print(f"   - Logistic Reg training: {lr_train_time:.2f}s")

print(f"\n💾 SAVED FILES:")
print(f"   - mega_model.pkl")
print(f"   - mega_vectorizer.pkl")
print(f"   - mega_confusion_matrix.png")
print(f"   - mega_model_comparison.png")
print(f"   - mega_dataset_distribution.png")

print("\n✨ Your MEGA Fake Review Detection Model is production-ready!")
print("="*70)
