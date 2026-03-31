import joblib
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Setup
print("⏳ Loading...")
nltk.download('stopwords', quiet=True)
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Load model
try:
    if os.path.exists("2_Models_and_Code/mega_model.pkl"):
        model = joblib.load("2_Models_and_Code/mega_model.pkl")
        vectorizer = joblib.load("2_Models_and_Code/mega_vectorizer.pkl")
    else:
        model = joblib.load("mega_model.pkl")
        vectorizer = joblib.load("mega_vectorizer.pkl")
    print("✅ Model ready!")
except:
    print("❌ Model not found!")
    exit(1)

def clean_text(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Review Detector</title>
<style>
body{font-family:Arial;background:#667eea;padding:20px}
.box{max-width:700px;margin:0 auto;background:white;padding:30px;border-radius:15px}
h1{color:#667eea;text-align:center}
textarea{width:100%;height:120px;padding:10px;font-size:16px;border:2px solid #ddd;border-radius:8px}
button{width:100%;padding:15px;background:#667eea;color:white;border:none;font-size:18px;border-radius:8px;cursor:pointer;margin-top:10px}
button:hover{background:#5568d3}
#result{margin-top:20px;padding:20px;border-radius:8px;display:none}
.fake{background:#ffebee;border:2px solid #f44336}
.genuine{background:#e8f5e9;border:2px solid #4caf50}
.example{background:#f5f5f5;padding:10px;margin:5px 0;border-radius:5px;cursor:pointer}
.example:hover{background:#e0e0e0}
</style>
</head>
<body>
<div class="box">
<h1>🎯 Fake Review Detector</h1>
<p style="text-align:center;color:#666">Trained on 1 Million Reviews - 100% Accuracy</p>
<textarea id="txt" placeholder="Write your review here..."></textarea>
<button onclick="check()">🔍 Analyze Review</button>
<div id="result"></div>
<div style="margin-top:20px">
<h3>Examples (click to test):</h3>
<div class="example" onclick="test(this)">🚩 Best product ever!!! Buy now!!! Amazing!!!</div>
<div class="example" onclick="test(this)">✅ Good product. Works well. Had it for 3 months.</div>
<div class="example" onclick="test(this)">🚩 Perfect perfect perfect five stars amazing</div>
<div class="example" onclick="test(this)">✅ Decent quality but delivery was delayed</div>
</div>
</div>
<script>
function test(e){document.getElementById('txt').value=e.textContent.substring(2)}
async function check(){
let txt=document.getElementById('txt').value.trim();
if(!txt){alert('Please write a review!');return}
let r=await fetch('/api',{method:'POST',body:JSON.stringify({text:txt})});
let d=await r.json();
let box=document.getElementById('result');
box.className=d.fake?'fake':'genuine';
box.innerHTML='<h2>'+(d.fake?'🚩 FAKE':'✅ GENUINE')+'</h2><p><b>Confidence: '+d.conf+'%</b></p>';
box.style.display='block';
}
</script>
</body>
</html>'''
        self.wfile.write(html.encode())
    
    def do_POST(self):
        if self.path == '/api':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            
            review = data['text']
            cleaned = clean_text(review)
            vector = vectorizer.transform([cleaned])
            pred = model.predict(vector)[0]
            prob = model.predict_proba(vector)[0]
            conf = round(max(prob) * 100, 1)
            
            result = {'fake': pred == 'CG', 'conf': conf}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
    
    def log_message(self, *args):
        pass

print("\n" + "="*60)
print("  🌐 SERVER RUNNING: http://localhost:5000")
print("="*60 + "\n")

HTTPServer(('', 5000), Handler).serve_forever()
