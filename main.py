from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os

app = FastAPI(title="نظام رزان للتحليل المالي")

# HTML مدمج في الكود
HTML_CONTENT = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>نظام رزان للتحليل المالي</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
            color: #FFD700;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { 
            text-align: center; 
            font-size: 2.5rem; 
            margin-bottom: 20px;
            color: #FFD700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }
        .card { 
            background: rgba(26, 26, 26, 0.9);
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #B8860B;
            margin: 20px 0;
        }
        .form-group { margin: 15px 0; }
        label { 
            display: block; 
            margin-bottom: 5px;
            color: #FFD700;
            font-weight: bold;
        }
        input, select, textarea { 
            width: 100%;
            padding: 10px;
            border: 2px solid #2d2d2d;
            border-radius: 5px;
            background: #000000;
            color: #ffffff;
        }
        button { 
            background: linear-gradient(45deg, #FFD700, #B8860B);
            color: #000;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            margin: 10px 5px;
        }
        button:hover { transform: translateY(-2px); }
        .results { 
            background: rgba(45, 45, 45, 0.8);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #DAA520;
            margin: 20px 0;
        }
        .result-item { margin: 10px 0; color: #DAA520; }
    </style>
</head>
<body>
    <div class="container">
        <h1>نظام رزان للتحليل المالي</h1>
        
        <div class="card">
            <h2 style="color: #FFD700; margin-bottom: 20px;">إدخال بيانات الشركة</h2>
            
            <div class="form-group">
                <label>اسم الشركة</label>
                <input type="text" id="companyName" placeholder="أدخل اسم الشركة">
            </div>
            
            <div class="form-group">
                <label>القطاع</label>
                <select id="industry">
                    <option value="technology">تكنولوجيا المعلومات</option>
                    <option value="banking">البنوك</option>
                    <option value="energy">الطاقة</option>
                    <option value="healthcare">الرعاية الصحية</option>
                    <option value="retail">التجارة</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>الإيرادات (السنة الحالية)</label>
                <input type="number" id="revenue" placeholder="1000000">
            </div>
            
            <div class="form-group">
                <label>صافي الربح</label>
                <input type="number" id="netIncome" placeholder="200000">
            </div>
            
            <div class="form-group">
                <label>إجمالي الأصول</label>
                <input type="number" id="totalAssets" placeholder="5000000">
            </div>
            
            <button onclick="analyzeData()">تحليل البيانات</button>
            <button onclick="clearData()">مسح البيانات</button>
        </div>
        
        <div id="results" class="card" style="display: none;">
            <h2 style="color: #FFD700;">نتائج التحليل</h2>
            <div id="analysisResults"></div>
        </div>
    </div>

    <script>
        function analyzeData() {
            const company = document.getElementById('companyName').value;
            const industry = document.getElementById('industry').value;
            const revenue = parseFloat(document.getElementById('revenue').value) || 0;
            const netIncome = parseFloat(document.getElementById('netIncome').value) || 0;
            const totalAssets = parseFloat(document.getElementById('totalAssets').value) || 0;
            
            if (!company || revenue === 0) {
                alert('يرجى إدخال اسم الشركة والإيرادات');
                return;
            }
            
            // حسابات بسيطة
            const netMargin = ((netIncome / revenue) * 100).toFixed(2);
            const roa = ((netIncome / totalAssets) * 100).toFixed(2);
            
            const results = `
                <div class="result-item"><strong>اسم الشركة:</strong> ${company}</div>
                <div class="result-item"><strong>القطاع:</strong> ${getIndustryName(industry)}</div>
                <div class="result-item"><strong>هامش الربح الصافي:</strong> ${netMargin}%</div>
                <div class="result-item"><strong>العائد على الأصول:</strong> ${roa}%</div>
                <div class="result-item"><strong>الإيرادات:</strong> ${revenue.toLocaleString()} ريال</div>
                <div class="result-item"><strong>صافي الربح:</strong> ${netIncome.toLocaleString()} ريال</div>
                <div class="result-item"><strong>التقييم:</strong> ${getPerformanceRating(parseFloat(netMargin))}</div>
            `;
            
            document.getElementById('analysisResults').innerHTML = results;
            document.getElementById('results').style.display = 'block';
        }
        
        function getIndustryName(value) {
            const industries = {
                'technology': 'تكنولوجيا المعلومات',
                'banking': 'البنوك',
                'energy': 'الطاقة',
                'healthcare': 'الرعاية الصحية',
                'retail': 'التجارة'
            };
            return industries[value] || value;
        }
        
        function getPerformanceRating(margin) {
            if (margin > 20) return 'ممتاز';
            if (margin > 15) return 'جيد جداً';
            if (margin > 10) return 'جيد';
            if (margin > 5) return 'متوسط';
            return 'ضعيف';
        }
        
        function clearData() {
            document.getElementById('companyName').value = '';
            document.getElementById('revenue').value = '';
            document.getElementById('netIncome').value = '';
            document.getElementById('totalAssets').value = '';
            document.getElementById('results').style.display = 'none';
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return HTML_CONTENT

@app.get("/health")
def health():
    return {"status": "ok", "message": "نظام رزان يعمل بنجاح"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
