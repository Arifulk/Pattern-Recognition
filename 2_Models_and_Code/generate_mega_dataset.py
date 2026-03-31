import pandas as pd
import numpy as np
import random
from datetime import datetime

print("="*70)
print("  🎲 GENERATING 1,000,000 REALISTIC REVIEW DATASET")
print("  This will take a few minutes...")
print("="*70)

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# Templates for GENUINE reviews (more specific, balanced)
genuine_templates = [
    "I bought this {period} and it {quality_good}. {detail_specific}",
    "The product {quality_good} but {minor_issue}. Overall {rating_word}.",
    "{quality_good} for the price. {delivery_comment}",
    "I've been using this for {period} and {quality_good}. {recommendation}",
    "The {product_feature} is {quality_good}. {specific_detail}",
    "{quality_neutral}. It works as described but {minor_issue}.",
    "Received it {delivery_time}. {quality_good} and {specific_detail}",
    "Good quality. {specific_use_case}. {minor_positive}",
    "{quality_good}. My {family_member} loves it. {specific_detail}",
    "Decent product. {quality_neutral} but {price_comment}",
    "The material feels {texture} and {quality_good}. {usage_comment}",
    "Works well for {use_case}. {minor_issue} but overall satisfied.",
    "I compared this with {comparison} and this is better. {specific_reason}",
    "{quality_good}. Easy to {action}. {minor_detail}",
    "After {period} of use, {quality_good}. {maintenance_comment}",
    "The {product_feature} exceeded my expectations. {specific_detail}",
    "Bought for {purpose}. {quality_good} and {delivery_comment}",
    "{quality_negative}. {reason_negative}. Will not buy again.",
    "The size is {size_comment}. {quality_neutral} otherwise.",
    "{quality_good} but arrived {delivery_issue}.",
]

# Templates for FAKE reviews (repetitive, generic, urgent)
fake_templates = [
    "{superlative} {superlative} {superlative}! {urgent_action}!",
    "Best product ever! {excitement} {excitement} {excitement}!!!",
    "{generic_praise} {generic_praise} {generic_praise}. Highly recommended!!!",
    "Amazing quality! {urgent_action}! {generic_praise}!",
    "{superlative} deal! Everyone should {urgent_action}!",
    "Perfect perfect perfect! {generic_praise} {generic_praise}!",
    "{excitement} {excitement}! Five stars! {urgent_action}!",
    "Excellent excellent quality! {superlative} product! Buy now!",
    "{generic_praise}! {superlative}! {urgent_action} immediately!",
    "Wonderful wonderful wonderful! {excitement}! {generic_praise}!",
    "{superlative} {superlative}! Best purchase ever! {urgent_action}!",
    "Outstanding! {generic_praise} {generic_praise}! Must buy!",
    "{excitement} {excitement} {excitement}! {superlative} product!",
    "Highly highly recommended! {urgent_action}! {generic_praise}!",
    "Best best best! {superlative}! Everyone buy this!",
    "{generic_praise}! {superlative} quality! {urgent_action} now!",
    "Perfect product! {excitement} {excitement}! {urgent_action}!",
    "Amazing amazing amazing! {generic_praise}! Five stars!",
    "{superlative}! {superlative}! {urgent_action} before too late!",
    "Incredible! {excitement}! {generic_praise} {generic_praise}!",
]

# Word lists for filling templates
word_lists = {
    'period': ['2 weeks ago', '3 months ago', 'last month', 'recently', 'a few days ago', 
               '6 months ago', 'last year', 'yesterday'],
    'quality_good': ['works great', 'is good quality', 'exceeded expectations', 
                     'is well made', 'does the job', 'is decent', 'works well',
                     'is satisfactory', 'meets my needs', 'is reliable'],
    'quality_neutral': ['It\'s okay', 'It\'s average', 'It\'s acceptable', 'Nothing special',
                        'What you would expect', 'Fairly standard'],
    'quality_negative': ['Disappointed', 'Not worth it', 'Poor quality', 'Broke quickly',
                         'Waste of money', 'Not as described', 'Very poor'],
    'minor_issue': ['the color was slightly off', 'delivery took longer than expected',
                    'packaging could be better', 'instructions were unclear',
                    'it\'s a bit small', 'it\'s slightly larger than expected'],
    'rating_word': ['satisfied', 'happy with it', 'good purchase', 'worth the money',
                    'glad I bought it', 'would recommend'],
    'detail_specific': ['The battery lasts about 8 hours.', 'It fits perfectly in my space.',
                        'The buttons are easy to press.', 'Setup took about 15 minutes.',
                        'The cord length is adequate.', 'It\'s lighter than I expected.'],
    'delivery_comment': ['Arrived on time.', 'Fast shipping.', 'Took 5 days to arrive.',
                         'Delivery was quick.', 'Came earlier than expected.'],
    'product_feature': ['design', 'build quality', 'functionality', 'size', 'color', 
                        'material', 'texture', 'weight'],
    'specific_detail': ['The handle is comfortable.', 'Easy to clean.',
                        'Fits in my drawer.', 'Looks good in my kitchen.',
                        'My kids can use it easily.', 'Doesn\'t take up much space.'],
    'specific_use_case': ['I use it daily for breakfast', 'Perfect for my home office',
                          'Great for camping trips', 'Works well in small apartments'],
    'minor_positive': ['No complaints so far', 'Does what it promises',
                       'Good value for money', 'Exactly as pictured'],
    'family_member': ['husband', 'wife', 'son', 'daughter', 'kids', 'family'],
    'texture': ['soft', 'smooth', 'sturdy', 'solid', 'lightweight', 'durable'],
    'usage_comment': ['Use it every day', 'Haven\'t had any issues',
                      'Still working perfectly', 'No problems yet'],
    'use_case': ['my morning routine', 'daily tasks', 'small spaces', 'beginners'],
    'comparison': ['other brands', 'the original', 'cheaper alternatives', 'similar products'],
    'specific_reason': ['Better quality material', 'More features', 'Easier to use', 'Lasts longer'],
    'action': ['install', 'clean', 'use', 'assemble', 'store', 'operate'],
    'minor_detail': ['Wish it came in more colors', 'Could be a bit larger', 'Price is fair'],
    'maintenance_comment': ['Easy to maintain', 'Cleaning is simple', 'Still like new', 'Holding up well'],
    'purpose': ['my kids', 'a gift', 'replacement', 'an upgrade', 'daily use'],
    'reason_negative': ['Broke after a week', 'Not durable', 'Cheap materials', 'Doesn\'t work properly'],
    'size_comment': ['perfect', 'smaller than expected', 'larger than needed', 'just right'],
    'delivery_issue': ['damaged', 'late', 'with missing parts', 'in poor packaging'],
    'price_comment': ['worth the price', 'a bit expensive', 'good value', 'fair price'],
    
    # Fake review words
    'superlative': ['Amazing', 'Incredible', 'Outstanding', 'Fantastic', 'Excellent',
                    'Perfect', 'Wonderful', 'Spectacular', 'Phenomenal', 'Superb'],
    'excitement': ['Love it', 'Best ever', 'So good', 'Awesome', 'Great'],
    'generic_praise': ['Excellent quality', 'Amazing product', 'Highly recommend',
                       'Five stars', 'Best purchase', 'Perfect item', 'Great deal'],
    'urgent_action': ['Buy now', 'Don\'t miss this', 'Get it today', 'Purchase immediately',
                      'Buy before it\'s gone', 'Order now', 'Must have'],
}

# Product categories
categories = ['Home_and_Kitchen', 'Electronics', 'Sports_and_Outdoors', 'Books',
              'Clothing', 'Toys_and_Games', 'Beauty', 'Health', 'Automotive', 'Pet_Supplies']

def fill_template(template, word_lists):
    """Fill template with random words from word lists"""
    result = template
    for key, values in word_lists.items():
        placeholder = '{' + key + '}'
        while placeholder in result:
            result = result.replace(placeholder, random.choice(values), 1)
    return result

def generate_genuine_review():
    """Generate a realistic genuine review"""
    template = random.choice(genuine_templates)
    review = fill_template(template, word_lists)
    rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 15, 35, 35])[0]
    return review, rating, 'OR'

def generate_fake_review():
    """Generate a realistic fake review"""
    template = random.choice(fake_templates)
    review = fill_template(template, word_lists)
    rating = random.choices([4, 5], weights=[20, 80])[0]  # Fake reviews mostly 5 stars
    return review, rating, 'CG'

# Generate dataset
print("\n🔄 Generating reviews...")
print("   - Target: 1,000,000 reviews")
print("   - Genuine: 500,000")
print("   - Fake: 500,000")

start_time = datetime.now()
data = []

batch_size = 10000
total_reviews = 1000000
genuine_count = 500000
fake_count = 500000

for i in range(0, genuine_count, batch_size):
    batch_end = min(i + batch_size, genuine_count)
    for _ in range(batch_end - i):
        review, rating, label = generate_genuine_review()
        category = random.choice(categories)
        data.append({
            'category': category,
            'rating': float(rating),
            'label': label,
            'text_': review
        })
    
    if (i + batch_size) % 50000 == 0:
        print(f"   Generated {i + batch_size:,} genuine reviews...")

print(f"   ✅ Generated {genuine_count:,} genuine reviews")

for i in range(0, fake_count, batch_size):
    batch_end = min(i + batch_size, fake_count)
    for _ in range(batch_end - i):
        review, rating, label = generate_fake_review()
        category = random.choice(categories)
        data.append({
            'category': category,
            'rating': float(rating),
            'label': label,
            'text_': review
        })
    
    if (i + batch_size) % 50000 == 0:
        print(f"   Generated {genuine_count + i + batch_size:,} total reviews...")

print(f"   ✅ Generated {fake_count:,} fake reviews")

# Shuffle the data
print("\n🔀 Shuffling dataset...")
random.shuffle(data)

# Create DataFrame
print("📊 Creating DataFrame...")
df = pd.DataFrame(data)

# Save to CSV
print("\n💾 Saving to CSV file...")
filename = 'mega_dataset_1million.csv'
df.to_csv(filename, index=False)

end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

print("\n" + "="*70)
print("  ✅ DATASET GENERATION COMPLETED!")
print("="*70)

print(f"\n📊 Dataset Statistics:")
print(f"   - Total reviews: {len(df):,}")
print(f"   - Genuine (OR): {len(df[df['label'] == 'OR']):,}")
print(f"   - Fake (CG): {len(df[df['label'] == 'CG']):,}")
print(f"   - Categories: {df['category'].nunique()}")
print(f"   - File size: ~{df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB in memory")

print(f"\n⏱️  Generation time: {duration:.2f} seconds ({duration/60:.2f} minutes)")

print(f"\n💾 Saved as: {filename}")

print("\n📝 Sample reviews:")
print(df[['label', 'rating', 'text_']].sample(5))

print("\n✅ Ready for training! Run 'train_mega_model.py' next.")
print("="*70)
