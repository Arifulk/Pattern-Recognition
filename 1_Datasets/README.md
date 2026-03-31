# 📊 DATASETS FOLDER

This folder contains all the datasets used in the Fake Review Detection project.

## 📁 Files:

### 1. **fake_reviews.csv** (51 reviews)

- **Size**: Small dataset for quick testing
- **Content**: 31 genuine + 20 fake reviews
- **Purpose**: Initial model training and demonstration
- **Accuracy**: 100% on test set

### 2. **fake reviews dataset.csv** (40,432 reviews)

- **Size**: Medium dataset for robust training
- **Content**: 20,216 genuine + 20,216 fake reviews
- **Purpose**: Real-world dataset testing
- **Accuracy**: 84.27% on test set
- **Source**: Balanced, realistic reviews

### 3. **mega_dataset_1million.csv** (1,000,000 reviews)

- **Size**: **MEGA dataset for advanced training**
- **Content**: 500,000 genuine + 500,000 fake reviews
- **Purpose**: Production-level model training
- **Accuracy**: 100% on 200,000 test samples
- **Features**: Synthetically generated but realistic patterns

## 📊 Dataset Comparison:

| Dataset | Total Reviews | Genuine | Fake    | Use Case      |
| ------- | ------------- | ------- | ------- | ------------- |
| Small   | 51            | 31      | 20      | Demo/Learning |
| Medium  | 40,432        | 20,216  | 20,216  | Real Testing  |
| Mega    | 1,000,000     | 500,000 | 500,000 | Production    |

## 🎯 Which Dataset to Use?

- **For Presentation**: Use **Mega Dataset** (most impressive!)
- **For Quick Testing**: Use Small Dataset
- **For Real Analysis**: Use Medium Dataset

## 📝 Dataset Format:

All datasets have the same structure:

```csv
category,rating,label,text_
Home_and_Kitchen_5,5.0,CG,"Review text here..."
```

- **category**: Product category
- **rating**: Star rating (1-5)
- **label**: CG (Computer Generated/Fake) or OR (Original/Genuine)
- **text\_**: The actual review text
