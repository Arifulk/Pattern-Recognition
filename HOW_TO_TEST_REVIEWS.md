# 🎯 কিভাবে রিভিউ টেস্ট করবেন

আপনার কাছে **3টি সহজ উপায়** আছে রিভিউ টেস্ট করার জন্য:

---

## ✨ **সবচেয়ে সহজ উপায় - Batch Files ব্যবহার করুন!**

### অপশন 1: Simple Terminal Version

**Double-click করুন:** `run_simple.bat`

- Terminal খুলবে
- রিভিউ লিখুন
- Enter চাপুন
- ফলাফল দেখুন!

### অপশন 2: Web Browser Version (সবচেয়ে সুন্দর!) ⭐

**Double-click করুন:** `run_web.bat`

- Browser automatically খুলবে
- সুন্দর পেজ দেখবেন
- রিভিউ লিখুন বক্সে
- "বিশ্লেষণ করুন" বাটন ক্লিক করুন
- তাৎক্ষণিক ফলাফল!

### অপশন 3: Advanced Terminal Version

**Double-click করুন:** `run_advanced.bat`

- বিস্তারিত বিশ্লেষণ
- কেন Fake/Genuine তার কারণ
- Multiple reviews টেস্ট

---

## 📝 **অথবা Command দিয়ে চালান:**

### Terminal থেকে:

```bash
# Simple Version
.venv/Scripts/python.exe simple_predict.py

# Web Version (Best!)
.venv/Scripts/python.exe web_predictor.py

# Advanced Version
.venv/Scripts/python.exe predict_review.py
```

---

## 🎯 **উদাহরণ রিভিউ টেস্ট করার জন্য:**

### 🚩 Fake Review Examples:

1. `Best product ever!!! Buy now!!! Amazing amazing!!!`
2. `Perfect perfect perfect five stars highly recommended`
3. `Excellent quality buy immediately amazing deal`

### ✅ Genuine Review Examples:

1. `Good product. Works well for my needs. Had it for 3 months.`
2. `Decent quality but delivery took longer than expected`
3. `The battery life is good and the design is sleek`

---

## ⚡ **Quick Start (সবচেয়ে দ্রুত):**

1. **File Explorer** খুলুন
2. `E:\PR Project` ফোল্ডারে যান
3. **`run_web.bat`** ফাইলে double-click করুন
4. Browser খুলবে স্বয়ংক্রিয়ভাবে
5. রিভিউ লিখুন এবং ফলাফল দেখুন!

---

## 🌐 **Web Version এর বিশেষত্ব:**

✅ Beautiful graphical interface
✅ বাংলা ও ইংরেজি সাপোর্ট
✅ Animated results
✅ Example reviews - ক্লিক করে টেস্ট করুন
✅ Color-coded results (Red = Fake, Green = Genuine)
✅ Confidence percentage
✅ সন্দেহজনক/বিশ্বাসযোগ্য কারণ দেখায়

---

## ❓ **যদি কোনো সমস্যা হয়:**

### Error: "ModuleNotFoundError"

**সমাধান:** Batch file (.bat) ব্যবহার করুন, সরাসরি `python` command নয়

### Error: "Model not found"

**সমাধান:** প্রথমে model train করুন:

```bash
.venv/Scripts/python.exe 2_Models_and_Code/train_mega_model.py
```

### Web page খুলছে না

**সমাধান:**

1. `run_web.bat` চালান
2. Manually browser খুলে যান: `http://localhost:8080`

---

## 🎓 **Presentation এর জন্য:**

1. ✅ **`run_web.bat`** double-click করুন
2. ✅ Browser এ page খুলবে
3. ✅ Live demo দিন:
   - উদাহরণ review ক্লিক করুন
   - অথবা নিজের review লিখুন
   - তাৎক্ষণিক ফলাফল দেখান
4. ✅ Fake vs Genuine comparison দেখান

---

## 📊 **ফাইল গুলো:**

| File                | Purpose           | কিভাবে চালাবেন                               |
| ------------------- | ----------------- | -------------------------------------------- |
| `run_simple.bat`    | Simple terminal   | Double-click                                 |
| `run_web.bat`       | Web interface ⭐  | Double-click                                 |
| `run_advanced.bat`  | Advanced analysis | Double-click                                 |
| `simple_predict.py` | Python script     | `.venv/Scripts/python.exe simple_predict.py` |
| `web_predictor.py`  | Web server        | `.venv/Scripts/python.exe web_predictor.py`  |
| `predict_review.py` | Advanced script   | `.venv/Scripts/python.exe predict_review.py` |

---

## ✨ **সবচেয়ে ভালো অভিজ্ঞতার জন্য:**

🌟 **`run_web.bat` double-click করুন!** 🌟

এটাই সবচেয়ে সুন্দর এবং সহজ উপায়!

---

**🎉 এখনই টেস্ট করে দেখুন! আপনার রিভিউ Fake নাকি Genuine? 🚀**
