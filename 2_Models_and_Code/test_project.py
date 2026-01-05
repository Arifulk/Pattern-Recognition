# TEST YOUR PROJECT - Quick Verification Script
# Run this to make sure everything works before your presentation!

print("="*70)
print("🔍 PROJECT VERIFICATION TEST")
print("="*70)

# Test 1: Check imports
print("\n✓ Testing imports...")
try:
    import pandas as pd
    import numpy as np
    import nltk
    import sklearn
    import matplotlib
    import seaborn
    print("  ✅ All libraries imported successfully!")
except ImportError as e:
    print(f"  ❌ Import error: {e}")
    exit(1)

# Test 2: Check dataset file
print("\n✓ Testing dataset...")
try:
    data = pd.read_csv("fake_reviews.csv")
    print(f"  ✅ Dataset loaded: {len(data)} reviews")
    print(f"     - Genuine: {len(data[data['label'] == 'genuine'])}")
    print(f"     - Fake: {len(data[data['label'] == 'fake'])}")
except Exception as e:
    print(f"  ❌ Dataset error: {e}")
    exit(1)

# Test 3: Check NLTK data
print("\n✓ Testing NLTK stopwords...")
try:
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    print(f"  ✅ NLTK stopwords available: {len(stop_words)} words")
except Exception as e:
    print("  ⚠️  Downloading stopwords...")
    nltk.download('stopwords', quiet=True)
    from nltk.corpus import stopwords
    print("  ✅ NLTK stopwords downloaded!")

# Test 4: Check visualization files
print("\n✓ Checking visualization files...")
import os
files_to_check = ['confusion_matrix.png', 'dataset_distribution.png']
for file in files_to_check:
    if os.path.exists(file):
        print(f"  ✅ {file} exists")
    else:
        print(f"  ⚠️  {file} not found (will be created when you run main code)")

# Test 5: Quick model test
print("\n✓ Testing ML model...")
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.model_selection import train_test_split
    
    # Quick preprocessing
    data['cleaned'] = data['review'].str.lower()
    
    # Quick model test
    vectorizer = TfidfVectorizer(max_features=50)
    X = vectorizer.fit_transform(data['cleaned'])
    y = data['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = MultinomialNB()
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"  ✅ Model trained successfully!")
    print(f"     Quick test accuracy: {score*100:.1f}%")
    
except Exception as e:
    print(f"  ❌ Model error: {e}")
    exit(1)

# Test 6: Test prediction
print("\n✓ Testing prediction function...")
try:
    test_review = "Best product ever buy now"
    test_cleaned = test_review.lower()
    test_vector = vectorizer.transform([test_cleaned])
    prediction = model.predict(test_vector)[0]
    print(f"  ✅ Prediction works!")
    print(f"     Test: \"{test_review}\"")
    print(f"     Prediction: {prediction}")
except Exception as e:
    print(f"  ❌ Prediction error: {e}")
    exit(1)

# Final summary
print("\n" + "="*70)
print("🎉 ALL TESTS PASSED!")
print("="*70)
print("\n✅ Your project is ready to run!")
print("✅ All components working correctly!")
print("✅ You can present with confidence!")
print("\n💡 Next step: Run 'python fake_review_detection.py' for full output")
print("="*70)
