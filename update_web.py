import re

with open("web_predictor.py", "r", encoding="utf-8") as f:
    content = f.read()

# Modify the Post handler to extract and return features
new_backend_code = """
            # Predict
            cleaned = clean_text(review)
            vector = vectorizer.transform([cleaned])
            prediction = model.predict(vector)[0]
            probability = model.predict_proba(vector)[0]
            confidence = float(max(probability) * 100)
            
            # Get extracted features
            feature_names = vectorizer.get_feature_names_out()
            nonzero_indices = vector.nonzero()[1]
            extracted_features = [feature_names[i] for i in nonzero_indices]
            
            # Generate reasons
"""
content = content.replace("""
            # Predict
            cleaned = clean_text(review)
            vector = vectorizer.transform([cleaned])
            prediction = model.predict(vector)[0]
            probability = model.predict_proba(vector)[0]
            confidence = float(max(probability) * 100)
            
            # Generate reasons""", new_backend_code.strip())

new_result_dict = """
            result = {
                'prediction': prediction,
                'confidence': confidence,
                'reasons': reasons,
                'cleaned_text': cleaned,
                'extracted_features': extracted_features
            }"""
content = content.replace("""
            result = {
                'prediction': prediction,
                'confidence': confidence,
                'reasons': reasons
            }""", new_result_dict.strip())

# Modify the frontend CSS
new_css = """
        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
            color: #667eea;
            font-size: 18px;
        }
        
        /* New Dashboard CSS */
        .dashboard-step {
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
            font-size: 15px;
        }
        .dashboard-step h4 {
            color: #333;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .process-flow {
            margin-top: 20px;
            border-top: 2px dashed #ddd;
            padding-top: 20px;
        }
        .code-box {
            background: #282c34;
            color: #abb2bf;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            margin-top: 5px;
            word-wrap: break-word;
        }
    </style>
"""
content = content.replace("""
        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
            color: #667eea;
            font-size: 18px;
        }
    </style>""", new_css.strip())

# Modify the JS to display the dashboard
new_js = """
        function displayResult(data, review) {
            const resultDiv = document.getElementById('result');
            const isFake = data.prediction === 'CG';
            
            resultDiv.className = isFake ? 'fake' : 'genuine';
            
            let html = `
                <div class="result-header">
                    ${isFake ? '🚩 FAKE (Computer Generated)' : '✅ GENUINE (Original)'}
                </div>
                <div class="confidence">
                    📊 Confidence: ${data.confidence.toFixed(2)}%
                </div>
            `;
            
            if (data.reasons && data.reasons.length > 0) {
                html += '<div class="reasons">';
                html += isFake ? '<strong>⚠️ সন্দেহজনক প্যাটার্ন (Suspicious Patterns):</strong>' : '<strong>✓ বিশ্বাসযোগ্য প্যাটার্ন (Trustworthy Patterns):</strong>';
                html += '<ul>';
                data.reasons.forEach(reason => {
                    html += `<li>${reason}</li>`;
                });
                html += '</ul></div>';
            }
            
            // Add Dashboard Process Flow
            html += `
                <div class="process-flow">
                    <h3>🔍 Analysis Dashboard (কিভাবে কাজ করলো?)</h3>
                    
                    <div class="dashboard-step">
                        <h4>1️⃣ Original Input (মডেল এ দেয়ার আগে)</h4>
                        <div style="color: #666; font-style: italic;">"${review}"</div>
                    </div>
                    
                    <div class="dashboard-step">
                        <h4>2️⃣ Text Preprocessing (ক্লিনিং এবং স্টপ-ওয়ার্ড রিমুভাল)</h4>
                        <p style="font-size: 13px; color: #555;">Punctuation Removed + Lowercase + Stemming</p>
                        <div class="code-box">${data.cleaned_text || '(Empty)'}</div>
                    </div>
                    
                    <div class="dashboard-step">
                        <h4>3️⃣ Feature Extraction (TF-IDF Vectorization)</h4>
                        <p style="font-size: 13px; color: #555;">মডেল যে শব্দগুলো থেকে প্যাটার্ন খুঁজছে (Keywords detected):</p>
                        <div class="code-box">[ ${data.extracted_features.join(', ')} ]</div>
                    </div>
                    
                    <div class="dashboard-step">
                        <h4>4️⃣ Model Prediction (মেশিন লার্নিং সিদ্ধান্ত)</h4>
                        <p style="font-size: 13px; color: #555;">Naive Bayes Algorithm Analysis:</p>
                        <div class="code-box">${isFake ? 'Class: Computer Generated (Fake) | ' : 'Class: Original (Genuine) | '} Probability: ${data.confidence.toFixed(2)}%</div>
                    </div>
                </div>
            `;
            
            resultDiv.innerHTML = html;
            resultDiv.style.display = 'block';
        }
"""
# We extract the entire displayResult function and replace it
content = re.sub(
    r"function displayResult\(data, review\).*?resultDiv.style.display = 'block';\s*}", 
    new_js.strip(), 
    content, 
    flags=re.DOTALL
)

with open("web_predictor.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated web_predictor.py successfully!")
