import os
import shutil

print("="*70)
print("  📁 ORGANIZING PROJECT INTO 3 CATEGORIES")
print("="*70)

base_path = "e:/PR Project"

# Define file categories
file_organization = {
    "1_Datasets": [
        "fake_reviews.csv",
        "fake reviews dataset.csv",
        "mega_dataset_1million.csv"
    ],
    "2_Models_and_Code": [
        "fake_review_detection.py",
        "train_model.py",
        "train_mega_model.py",
        "generate_mega_dataset.py",
        "test_project.py",
        "mega_model.pkl",
        "mega_vectorizer.pkl"
    ],
    "3_Results_and_Visualizations": [
        "confusion_matrix.png",
        "dataset_distribution.png",
        "advanced_confusion_matrix.png",
        "advanced_dataset_distribution.png",
        "advanced_accuracy_comparison.png",
        "mega_confusion_matrix.png",
        "mega_model_comparison.png",
        "mega_dataset_distribution.png"
    ]
}

# Move files
for folder, files in file_organization.items():
    folder_path = os.path.join(base_path, folder)
    print(f"\n📂 {folder}:")
    
    for file in files:
        src = os.path.join(base_path, file)
        dst = os.path.join(folder_path, file)
        
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                print(f"   ✅ {file}")
            except Exception as e:
                print(f"   ⚠️  {file} - {e}")
        else:
            print(f"   ⏭️  {file} (not found or already moved)")

print("\n" + "="*70)
print("  ✅ PROJECT ORGANIZATION COMPLETED!")
print("="*70)

# Show final structure
print("\n📁 Final Project Structure:")
for folder in file_organization.keys():
    folder_path = os.path.join(base_path, folder)
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        print(f"\n{folder}/ ({len(files)} files)")
        for f in sorted(files)[:5]:  # Show first 5
            print(f"  ├── {f}")
        if len(files) > 5:
            print(f"  └── ... and {len(files)-5} more files")

print("\n✨ All files organized successfully!")
