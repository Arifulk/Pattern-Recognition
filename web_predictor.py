"""
🎯 FAKE REVIEW DETECTOR - WEB VERSION
Simple HTML interface - just open in browser!
"""

import joblib
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json

# Setup
nltk.download('stopwords', quiet=True)
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Load model
print("⏳ Loading model...")
try:
    if os.path.exists("2_Models_and_Code/mega_model.pkl"):
        model = joblib.load("2_Models_and_Code/mega_model.pkl")
        vectorizer = joblib.load("2_Models_and_Code/mega_vectorizer.pkl")
    else:
        model = joblib.load("mega_model.pkl")
        vectorizer = joblib.load("mega_vectorizer.pkl")
    print("✅ Model loaded!")
except:
    print("❌ Model not found!")
    exit(1)

def clean_text(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fake Review Detector - ML Powered</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 700px;
            width: 100%;
            padding: 40px;
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        textarea {
            width: 100%;
            min-height: 150px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            margin-top: 20px;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        #result {
            margin-top: 30px;
            padding: 25px;
            border-radius: 10px;
            display: none;
            animation: slideIn 0.5s;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fake {
            background: #ffebee;
            border: 2px solid #ef5350;
        }
        .genuine {
            background: #e8f5e9;
            border: 2px solid #66bb6a;
        }
        .result-header {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .fake .result-header {
            color: #c62828;
        }
        .genuine .result-header {
            color: #2e7d32;
        }
        .confidence {
            font-size: 20px;
            margin: 10px 0;
        }
        .reasons {
            margin-top: 15px;
            padding: 15px;
            background: rgba(255,255,255,0.5);
            border-radius: 8px;
        }
        .reasons li {
            margin: 8px 0;
            padding-left: 10px;
        }
        .examples {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        .examples h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        .example-item {
            background: white;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .example-item:hover {
            background: #e3f2fd;
        }.loading {
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
        }.code-box {
            background: #282c34;
            color: #abb2bf;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            margin-top: 5px;
            word-wrap: break-word;
        }
        
        /* Chart Styles */
        .chart-container {
            width: 100%;
            max-width: 400px;
            margin: 20px auto;
            position: relative;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <h1>🎯 Fake Review Detector</h1>
        <p class="subtitle">আপনার রিভিউ লিখুন - তাৎক্ষণিক ফলাফল পান!</p>
        
        <textarea id="reviewText" placeholder="এখানে রিভিউ লিখুন... (ইংরেজিতে)

উদাহরণ:
✅ Good product. Works well for my needs. Had it for 3 months.
🚩 Best product ever!!! Buy now!!! Amazing amazing!!!"></textarea>
        
        <button onclick="analyzeReview()">🔍 রিভিউ বিশ্লেষণ করুন</button>
        
        <div class="loading" id="loading">⏳ বিশ্লেষণ করা হচ্ছে...</div>
        
        <div id="result"></div>
        
        <div class="examples">
            <h3>📝 উদাহরণ রিভিউ (ক্লিক করে টেস্ট করুন):</h3>
            
            <div class="example-item" onclick="setExample(this)">
                🚩 Best product ever!!! I bought 5 of them!!! Amazing quality!!!
            </div>
            <div class="example-item" onclick="setExample(this)">
                ✅ Good product. Works well for my needs. Had it for 3 months.
            </div>
            <div class="example-item" onclick="setExample(this)">
                🚩 Perfect perfect perfect five stars highly recommended amazing
            </div>
            <div class="example-item" onclick="setExample(this)">
                ✅ Decent quality but delivery took longer than expected.
            </div>
            <div class="example-item" onclick="setExample(this)">
                🚩 Buy buy buy now limited offer hurry amazing deal
            </div>
            <div class="example-item" onclick="setExample(this)">
                ✅ The battery life is good and the design is sleek.
            </div>
        </div>
    </div>
    
    <script>
        function setExample(element) {
            const text = element.textContent.substring(2).trim();
            document.getElementById('reviewText').value = text;
        }
        
        async function analyzeReview() {
            const review = document.getElementById('reviewText').value.trim();
            
            if (!review) {
                alert('⚠️ দয়া করে একটি রিভিউ লিখুন!');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({review: review})
                });
                
                const data = await response.json();
                displayResult(data, review);
            } catch (error) {
                alert('❌ Error: ' + error);
            }
            
            document.getElementById('loading').style.display = 'none';
        }
        
        let currentChart = null;
        
        function displayResult(data, review) {
            const resultDiv = document.getElementById('result');
            const isFake = data.prediction === 'CG' || data.prediction === 'fake';
            
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
            
            // Generate standard keys to deal with default CSV vs Mega CSV logic
            let fakeProb = 0;
            let genuineProb = 0;
            if(data.probabilities['CG']) {
                fakeProb = data.probabilities['CG'];
                genuineProb = data.probabilities['OR'];
            } else if (data.probabilities['fake']) {
                fakeProb = data.probabilities['fake'];
                genuineProb = data.probabilities['genuine'];
            }
            
            // Add Dashboard Process Flow and Chart
            html += `
                <div class="process-flow">
                    <h3>🔍 Analysis Dashboard</h3>
                    
                    <div class="dashboard-step">
                        <h4>1️⃣ Original Input</h4>
                        <div style="color: #666; font-style: italic;">"${review}"</div>
                    </div>
                    
                    <div class="dashboard-step">
                        <h4>2️⃣ Text Preprocessing</h4>
                        <p style="font-size: 13px; color: #555;">Punctuation Removed + Lowercase + Stemming</p>
                        <div class="code-box">${data.cleaned_text || '(Empty)'}</div>
                    </div>
                    
                    <div class="dashboard-step">
                        <h4>3️⃣ Keywords detected by the model</h4>
                        <div class="code-box">[ ${data.extracted_features.join(', ')} ]</div>
                    </div>
                    
                    <div class="dashboard-step">
                        <h4>4️⃣ Model Prediction Probability (Visual)</h4>
                        <div class="chart-container">
                            <canvas id="predictionChart"></canvas>
                        </div>
                    </div>
                </div>
            `;
            
            resultDiv.innerHTML = html;
            resultDiv.style.display = 'block';
            
            // Render Chart
            const ctx = document.getElementById('predictionChart').getContext('2d');
            
            if (currentChart) {
                currentChart.destroy();
            }
            
            currentChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Fake', 'Genuine'],
                    datasets: [{
                        data: [fakeProb, genuineProb],
                        backgroundColor: [
                            'rgba(2ef, 83, 80, 0.8)', // Red
                            'rgba(102, 187, 106, 0.8)' // Green
                        ],
                        borderColor: [
                            'rgba(239, 83, 80, 1)',
                            'rgba(102, 187, 106, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    </script>
</body>
</html>
'''

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))
    
    def do_POST(self):
        if self.path == '/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            review = data['review']
            # Predict
            cleaned = clean_text(review)
            vector = vectorizer.transform([cleaned])
            prediction = model.predict(vector)[0]
            probability = model.predict_proba(vector)[0]
            confidence = float(max(probability) * 100)
            
            # Identify class orders
            classes = model.classes_
            prob_dict = {str(classes[i]): float(probability[i] * 100) for i in range(len(classes))}
            
            # Get extracted features
            feature_names = vectorizer.get_feature_names_out()
            nonzero_indices = vector.nonzero()[1]
            extracted_features = [feature_names[i] for i in nonzero_indices]
            
            # Generate reasons
            
            reasons = []
            review_lower = review.lower()
            
            if prediction == "CG":
                if "!!!" in review or review.count("!") > 3:
                    reasons.append("অতিরিক্ত exclamation marks (!)")
                if any(word * 2 in review_lower for word in ['best', 'amazing', 'perfect']):
                    reasons.append("একই শব্দের পুনরাবৃত্তি")
                if any(p in review_lower for p in ['buy now', 'limited offer', 'hurry']):
                    reasons.append("জরুরি ক্রয়ের ভাষা")
            else:
                if any(word in review_lower for word in ['months', 'weeks', 'days']):
                    reasons.append("ব্যবহারের সময়কাল উল্লেখ")
                if any(word in review_lower for word in ['but', 'however', 'although']):
                    reasons.append("সুষম মতামত (ভালো এবং খারাপ)")
                if len(review.split()) > 15:
                    reasons.append("বিস্তারিত এবং নির্দিষ্ট")
            result = {
                'prediction': prediction,
                'confidence': confidence,
                'reasons': reasons,
                'cleaned_text': cleaned,
                'extracted_features': extracted_features,
                'probabilities': prob_dict
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
    
    def log_message(self, format, *args):
        pass  # Suppress logs

if __name__ == '__main__':
    PORT = 8080
    server = HTTPServer(('localhost', PORT), RequestHandler)
    print("\n" + "="*70)
    print("  🌐 WEB SERVER STARTED!")
    print("="*70)
    print(f"\n  ✅ Open your browser and go to:")
    print(f"\n     👉 http://localhost:{PORT}")
    print(f"\n  📝 Write a review and see instant results!")
    print(f"\n  🛑 Press Ctrl+C to stop the server")
    print("\n" + "="*70 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        server.shutdown()
