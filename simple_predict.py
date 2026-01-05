"""
🎯 FAKE REVIEW DETECTOR - SIMPLE VERSION
Just run this script and type your review!
"""

import joblib
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
import sys

# Setup
nltk.download('stopwords', quiet=True)
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

# Load model
print("\n" + "="*70)
print("  🎯 FAKE REVIEW DETECTOR")
print("="*70)
print("\n⏳ Loading model...")

try:
    if os.path.exists("2_Models_and_Code/mega_model.pkl"):
        model = joblib.load("2_Models_and_Code/mega_model.pkl")
        vectorizer = joblib.load("2_Models_and_Code/mega_vectorizer.pkl")
    else:
        model = joblib.load("mega_model.pkl")
        vectorizer = joblib.load("mega_vectorizer.pkl")
    print("✅ Model ready!\n")
except:
    print("❌ Model not found! Run train_mega_model.py first.")
    sys.exit(1)

# Examples
print("="*70)
print("📝 EXAMPLES TO TRY:")
print("="*70)
print("\n🚩 Fake Review Examples:")
print("  1. Best product ever!!! Buy now!!! Amazing!!!")
print("  2. Perfect perfect perfect five stars recommended")
print("  3. Excellent quality buy immediately amazing deal")

print("\n✅ Genuine Review Examples:")
print("  4. Good product. Works well. Had it for 3 months.")
print("  5. Decent quality but delivery was delayed")
print("  6. The battery life is good and design is nice")
print("="*70)

# Main loop
count = 0
while True:
    print("\n" + "-"*70)
    review = input("\n✍️  Type your review (or 'exit' to quit): ").strip()
    
    if review.lower() in ['exit', 'quit', 'q']:
        print(f"\n👋 Analyzed {count} reviews. Goodbye!")
        break
    
    if not review:
        continue
    
    # Predict
    cleaned = clean_text(review)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0]
    confidence = max(probability) * 100
    
    # Display result
    count += 1
    print("\n" + "="*70)
    print(f"  REVIEW #{count}: {review[:50]}..." if len(review) > 50 else f"  REVIEW #{count}: {review}")
    print("="*70)
    
    if prediction == "CG":
        print("\n  🚩 RESULT: FAKE (Computer Generated)")
        print(f"  📊 CONFIDENCE: {confidence:.2f}%")
        print("\n  ⚠️  This review shows patterns of fake reviews:")
        if "!!!" in review:
            print("     • Too many exclamation marks")
        if any(w*2 in review.lower() for w in ['best','amazing','perfect']):
            print("     • Repetitive praise words")
    else:
        print("\n  ✅ RESULT: GENUINE (Original)")
        print(f"  📊 CONFIDENCE: {confidence:.2f}%")
        print("\n  ✓ This review appears authentic:")
        if len(review.split()) > 10:
            print("     • Detailed and specific")
        if not "!!!" in review:
            print("     • Natural writing style")
    
    print("\n" + "="*70)
