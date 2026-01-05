import joblib
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os

# Download NLTK data
nltk.download('stopwords', quiet=True)

print("="*70)
print("  🎯 FAKE REVIEW DETECTION - INTERACTIVE SYSTEM")
print("  Write a review and get instant prediction!")
print("="*70)

# Load model and vectorizer
print("\n⏳ Loading trained model...")

model_path = "mega_model.pkl"
vectorizer_path = "mega_vectorizer.pkl"

# Check if in Models folder
if not os.path.exists(model_path):
    model_path = "2_Models_and_Code/mega_model.pkl"
    vectorizer_path = "2_Models_and_Code/mega_vectorizer.pkl"

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ Error: Model files not found!")
    print("   Please run 'train_mega_model.py' first to create the model.")
    exit(1)

# Initialize preprocessing tools
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """Clean and preprocess review text"""
    if not text or text.strip() == "":
        return ""
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

def predict_review(review_text):
    """Predict if review is fake or genuine"""
    # Clean the text
    cleaned = clean_text(review_text)
    
    if not cleaned:
        return None, None, "empty"
    
    # Transform to vector
    vector = vectorizer.transform([cleaned])
    
    # Predict
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0]
    
    # Format result
    if prediction == "CG":
        label = "FAKE (Computer Generated)"
        emoji = "🚩"
        color = "RED"
    else:
        label = "GENUINE (Original)"
        emoji = "✅"
        color = "GREEN"
    
    confidence = max(probability) * 100
    
    return label, confidence, emoji

def display_result(review, label, confidence, emoji):
    """Display prediction result beautifully"""
    print("\n" + "="*70)
    print("  📝 YOUR REVIEW:")
    print("="*70)
    print(f"\"{review}\"")
    
    print("\n" + "="*70)
    print("  🎯 PREDICTION RESULT:")
    print("="*70)
    print(f"\n  {emoji} Status: {label}")
    print(f"  📊 Confidence: {confidence:.2f}%")
    
    if confidence > 90:
        certainty = "Very High Confidence"
    elif confidence > 75:
        certainty = "High Confidence"
    elif confidence > 60:
        certainty = "Moderate Confidence"
    else:
        certainty = "Low Confidence"
    
    print(f"  🎚️  Certainty: {certainty}")
    print("\n" + "="*70)

# Main interactive loop
print("\n" + "="*70)
print("  💡 HOW TO USE:")
print("="*70)
print("  1. Type or paste a review")
print("  2. Press Enter")
print("  3. See instant prediction!")
print("  4. Type 'quit' or 'exit' to stop")
print("="*70)

# Sample reviews for reference
print("\n📌 Sample Reviews to Test:")
print("\n  Fake Examples:")
print("    - Best product ever!!! Buy now!!! Amazing amazing!!!")
print("    - Perfect perfect perfect five stars highly recommended")
print("\n  Genuine Examples:")
print("    - Good product. Works well for my needs. Had it for 3 months.")
print("    - Decent quality but delivery took longer than expected")
print("="*70)

# Interactive loop
review_count = 0

while True:
    print("\n" + "-"*70)
    review = input("\n✍️  Enter your review: ").strip()
    
    # Check for exit
    if review.lower() in ['quit', 'exit', 'q', 'stop', '']:
        if review.lower() in ['quit', 'exit', 'q', 'stop']:
            print("\n" + "="*70)
            print("  👋 Thank you for using Fake Review Detection System!")
            print(f"  📊 Total reviews analyzed: {review_count}")
            print("="*70)
            break
        else:
            print("⚠️  Please enter a review or type 'quit' to exit.")
            continue
    
    # Predict
    print("\n⏳ Analyzing...")
    label, confidence, emoji = predict_review(review)
    
    if label:
        review_count += 1
        display_result(review, label, confidence, emoji)
        
        # Additional insights
        if "FAKE" in label:
            print("\n💡 Why might this be fake?")
            review_lower = review.lower()
            reasons = []
            
            if "!!!" in review or review.count("!") > 3:
                reasons.append("   • Excessive exclamation marks")
            if any(word * 2 in review_lower for word in ['best', 'amazing', 'perfect', 'excellent']):
                reasons.append("   • Repetitive words")
            if any(phrase in review_lower for phrase in ['buy now', 'limited offer', 'hurry', 'must buy']):
                reasons.append("   • Urgent buying language")
            if len(review.split()) < 10 and review.count('!') > 2:
                reasons.append("   • Short with excessive excitement")
            
            if reasons:
                for reason in reasons:
                    print(reason)
        else:
            print("\n💡 Why might this be genuine?")
            review_lower = review.lower()
            reasons = []
            
            if any(word in review_lower for word in ['months', 'weeks', 'days', 'years']):
                reasons.append("   • Mentions time period of usage")
            if any(word in review_lower for word in ['but', 'however', 'although']):
                reasons.append("   • Balanced opinion (pros and cons)")
            if len(review.split()) > 15:
                reasons.append("   • Detailed and specific")
            if not "!!!" in review:
                reasons.append("   • Natural writing style")
            
            if reasons:
                for reason in reasons:
                    print(reason)
    else:
        print("⚠️  Empty review. Please enter some text.")
    
    print("\n" + "-"*70)
    continue_choice = input("🔄 Test another review? (Press Enter to continue, 'quit' to exit): ").strip()
    if continue_choice.lower() in ['quit', 'exit', 'q', 'stop', 'n', 'no']:
        print("\n" + "="*70)
        print("  👋 Thank you for using Fake Review Detection System!")
        print(f"  📊 Total reviews analyzed: {review_count}")
        print("="*70)
        break
