from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
import os
from pathlib import Path
import asyncio
from dataclasses import dataclass
import uvicorn

# إعداد الـ logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Razan AI Financial Analysis System",
    description="نظام تحليل مالي متقدم بالذكاء الاصطناعي",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# إعداد المجلدات
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# إنشاء المجلدات إذا لم تكن موجودة
TEMPLATES_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# إعداد القوالب
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# تعريف الـ Enums
class AnalysisType(str, Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    LIQUIDITY = "liquidity"
    PROFITABILITY = "profitability"
    ACTIVITY = "activity"
    LEVERAGE = "leverage"
    MARKET = "market"
    DUPONT = "dupont"
    ZSCORE = "zscore"
    CASH_FLOW = "cash_flow"
    RISK = "risk"
    EVA = "eva"
    FORECASTING = "forecasting"
    TREND = "trend"
    COMPARATIVE = "comparative"
    PERFORMANCE = "performance"

class IndustryType(str, Enum):
    TECHNOLOGY = "technology"
    BANKING = "banking"
    ENERGY = "energy"
    HEALTHCARE = "healthcare"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    REAL_ESTATE = "real_estate"
    TELECOMMUNICATIONS = "telecommunications"
    TRANSPORTATION = "transportation"
    AGRICULTURE = "agriculture"
    # إضافة المزيد من القطاعات...

class MarketComparison(str, Enum):
    SAUDI = "saudi"
    GCC = "gcc"
    ARAB = "arab"
    GLOBAL = "global"

# تعريف البيانات المالية
@dataclass
class FinancialData:
    revenue: float
    gross_profit: float
    operating_income: float
    net_income: float
    total_assets: float
    current_assets: float
    current_liabilities: float
    total_liabilities: float
    shareholders_equity: float
    cash_flow_operations: float
    cash_flow_investing: float
    cash_flow_financing: float
    year: int

# النماذج
class FinancialInputData(BaseModel):
    company_name: str
    industry: IndustryType
    market_comparison: MarketComparison
    analysis_types: List[AnalysisType]
    years_data: List[Dict[str, Any]]
    language: str = "ar"

class AnalysisResult(BaseModel):
    analysis_type: str
    results: Dict[str, Any]
    charts: List[Dict[str, Any]]
    recommendations: List[str]

# فئة التحليل المالي
class FinancialAnalyzer:
    def __init__(self):
        self.industry_benchmarks = self._load_industry_benchmarks()
    
    def _load_industry_benchmarks(self) -> Dict[str, Dict[str, float]]:
        """تحميل معايير الصناعة"""
        return {
            "technology": {
                "current_ratio": 2.5,
                "quick_ratio": 1.8,
                "debt_to_equity": 0.3,
                "roe": 0.15,
                "gross_margin": 0.6,
                "operating_margin": 0.2,
                "net_margin": 0.15
            },
            "banking": {
                "current_ratio": 1.2,
                "quick_ratio": 1.0,
                "debt_to_equity": 8.0,
                "roe": 0.12,
                "gross_margin": 0.8,
                "operating_margin": 0.3,
                "net_margin": 0.25
            },
            "energy": {
                "current_ratio": 1.5,
                "quick_ratio": 1.2,
                "debt_to_equity": 0.6,
                "roe": 0.08,
                "gross_margin": 0.3,
                "operating_margin": 0.12,
                "net_margin": 0.08
            },
            # إضافة المزيد من القطاعات...
        }
    
    def horizontal_analysis(self, data: List[FinancialData]) -> Dict[str, Any]:
        """التحليل الأفقي"""
        if len(data) < 2:
            raise ValueError("يجب توفير بيانات لسنتين على الأقل للتحليل الأفقي")
        
        results = {}
        base_year = data[0]
        
        for i, current_year in enumerate(data[1:], 1):
            year_analysis = {
                "year": current_year.year,
                "revenue_growth": ((current_year.revenue - base_year.revenue) / base_year.revenue) * 100,
                "profit_growth": ((current_year.net_income - base_year.net_income) / base_year.net_income) * 100,
                "assets_growth": ((current_year.total_assets - base_year.total_assets) / base_year.total_assets) * 100,
                "equity_growth": ((current_year.shareholders_equity - base_year.shareholders_equity) / base_year.shareholders_equity) * 100
            }
            results[f"year_{current_year.year}"] = year_analysis
            base_year = current_year
        
        return results
    
    def vertical_analysis(self, data: List[FinancialData]) -> Dict[str, Any]:
        """التحليل الرأسي"""
        results = {}
        
        for year_data in data:
            year_analysis = {
                "year": year_data.year,
                "gross_profit_margin": (year_data.gross_profit / year_data.revenue) * 100,
                "operating_margin": (year_data.operating_income / year_data.revenue) * 100,
                "net_margin": (year_data.net_income / year_data.revenue) * 100,
                "current_assets_ratio": (year_data.current_assets / year_data.total_assets) * 100,
                "debt_ratio": (year_data.total_liabilities / year_data.total_assets) * 100,
                "equity_ratio": (year_data.shareholders_equity / year_data.total_assets) * 100
            }
            results[f"year_{year_data.year}"] = year_analysis
        
        return results
    
    def liquidity_analysis(self, data: List[FinancialData]) -> Dict[str, Any]:
        """تحليل السيولة"""
        results = {}
        
        for year_data in data:
            current_ratio = year_data.current_assets / year_data.current_liabilities
            quick_ratio = (year_data.current_assets - year_data.current_assets * 0.3) / year_data.current_liabilities  # تقدير للمخزون
            
            year_analysis = {
                "year": year_data.year,
                "current_ratio": current_ratio,
                "quick_ratio": quick_ratio,
                "working_capital": year_data.current_assets - year_data.current_liabilities,
                "cash_ratio": year_data.cash_flow_operations / year_data.current_liabilities
            }
            results[f"year_{year_data.year}"] = year_analysis
        
        return results
    
    def profitability_analysis(self, data: List[FinancialData]) -> Dict[str, Any]:
        """تحليل الربحية"""
        results = {}
        
        for year_data in data:
            year_analysis = {
                "year": year_data.year,
                "gross_profit_margin": (year_data.gross_profit / year_data.revenue) * 100,
                "operating_margin": (year_data.operating_income / year_data.revenue) * 100,
                "net_margin": (year_data.net_income / year_data.revenue) * 100,
                "roe": (year_data.net_income / year_data.shareholders_equity) * 100,
                "roa": (year_data.net_income / year_data.total_assets) * 100,
                "roic": (year_data.operating_income / (year_data.total_assets - year_data.current_liabilities)) * 100
            }
            results[f"year_{year_data.year}"] = year_analysis
        
        return results
    
    def zscore_analysis(self, data: List[FinancialData]) -> Dict[str, Any]:
        """تحليل Z-Score لتقييم مخاطر الإفلاس"""
        results = {}
        
        for year_data in data:
            # معادلة Altman Z-Score
            working_capital = year_data.current_assets - year_data.current_liabilities
            retained_earnings = year_data.shareholders_equity * 0.7  # تقدير
            
            z_score = (
                1.2 * (working_capital / year_data.total_assets) +
                1.4 * (retained_earnings / year_data.total_assets) +
                3.3 * (year_data.operating_income / year_data.total_assets) +
                0.6 * (year_data.shareholders_equity / year_data.total_liabilities) +
                1.0 * (year_data.revenue / year_data.total_assets)
            )
            
            if z_score > 3.0:
                risk_level = "منخفض"
            elif z_score > 1.8:
                risk_level = "متوسط"
            else:
                risk_level = "عالي"
            
            year_analysis = {
                "year": year_data.year,
                "z_score": z_score,
                "risk_level": risk_level,
                "bankruptcy_probability": max(0, min(100, (3.0 - z_score) / 3.0 * 100))
            }
            results[f"year_{year_data.year}"] = year_analysis
        
        return results
    
    def forecasting_analysis(self, data: List[FinancialData]) -> Dict[str, Any]:
        """التحليل التنبؤي"""
        if len(data) < 3:
            raise ValueError("يجب توفير بيانات لثلاث سنوات على الأقل للتنبؤ")
        
        # حساب معدلات النمو
        revenue_growth_rates = []
        profit_growth_rates = []
        
        for i in range(1, len(data)):
            revenue_growth = ((data[i].revenue - data[i-1].revenue) / data[i-1].revenue) * 100
            profit_growth = ((data[i].net_income - data[i-1].net_income) / data[i-1].net_income) * 100
            
            revenue_growth_rates.append(revenue_growth)
            profit_growth_rates.append(profit_growth)
        
        avg_revenue_growth = np.mean(revenue_growth_rates)
        avg_profit_growth = np.mean(profit_growth_rates)
        
        # التنبؤ للسنة القادمة
        last_year = data[-1]
        next_year_revenue = last_year.revenue * (1 + avg_revenue_growth / 100)
        next_year_profit = last_year.net_income * (1 + avg_profit_growth / 100)
        
        return {
            "historical_growth": {
                "revenue_growth_rates": revenue_growth_rates,
                "profit_growth_rates": profit_growth_rates,
                "avg_revenue_growth": avg_revenue_growth,
                "avg_profit_growth": avg_profit_growth
            },
            "forecast_next_year": {
                "year": last_year.year + 1,
                "predicted_revenue": next_year_revenue,
                "predicted_profit": next_year_profit,
                "confidence_level": 75  # تقدير مبدئي
            }
        }

# إنشاء محلل مالي
analyzer = FinancialAnalyzer()

# المسارات
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """الصفحة الرئيسية"""
    return """
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>نظام رازان للتحليل المالي</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
                color: #FFD700;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .container {
                text-align: center;
                max-width: 800px;
                padding: 40px;
                background: rgba(45, 45, 45, 0.8);
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(255, 215, 0, 0.1);
                border: 2px solid #B8860B;
            }
            
            h1 {
                font-size: 3rem;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
                color: #FFD700;
            }
            
            .subtitle {
                font-size: 1.5rem;
                margin-bottom: 30px;
                color: #DAA520;
                font-weight: 300;
            }
            
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            
            .feature-card {
                background: rgba(0, 0, 0, 0.6);
                padding: 20px;
                border-radius: 15px;
                border: 1px solid #B8860B;
                transition: transform 0.3s ease;
            }
            
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(255, 215, 0, 0.2);
            }
            
            .feature-title {
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 10px;
                color: #FFD700;
            }
            
            .feature-desc {
                color: #DAA520;
                font-size: 0.9rem;
            }
            
            .cta-button {
                background: linear-gradient(45deg, #FFD700, #B8860B);
                color: #000;
                padding: 15px 30px;
                font-size: 1.2rem;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                margin-top: 30px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            
            .cta-button:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>نظام رازان للتحليل المالي</h1>
            <p class="subtitle">أقوى نظام تحليل مالي بالذكاء الاصطناعي</p>
            
            <div class="features">
                <div class="feature-card">
                    <div class="feature-title">16+ نوع تحليل مالي</div>
                    <div class="feature-desc">تحليل أفقي، رأسي، نسب مالية، مخاطر، تنبؤات</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-title">43+ قطاع صناعي</div>
                    <div class="feature-desc">مقارنات شاملة مع معايير الصناعة</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-title">أسواق متعددة</div>
                    <div class="feature-desc">سعودي، خليجي، عربي، عالمي</div>
                </div>
                
                <div class="feature-card">
                    <div class="feature-title">ذكاء اصطناعي</div>
                    <div class="feature-desc">تحليل ذكي وتنبؤات دقيقة</div>
                </div>
            </div>
            
            <button class="cta-button" onclick="window.location.href='/api/docs'">
                بدء التحليل
            </button>
        </div>
    </body>
    </html>
    """

@app.post("/api/analyze")
async def analyze_financial_data(data: FinancialInputData):
    """تحليل البيانات المالية"""
    try:
        # تحويل البيانات إلى قائمة من FinancialData
        financial_data = []
        for year_data in data.years_data:
            financial_data.append(FinancialData(
                revenue=year_data.get("revenue", 0),
                gross_profit=year_data.get("gross_profit", 0),
                operating_income=year_data.get("operating_income", 0),
                net_income=year_data.get("net_income", 0),
                total_assets=year_data.get("total_assets", 0),
                current_assets=year_data.get("current_assets", 0),
                current_liabilities=year_data.get("current_liabilities", 0),
                total_liabilities=year_data.get("total_liabilities", 0),
                shareholders_equity=year_data.get("shareholders_equity", 0),
                cash_flow_operations=year_data.get("cash_flow_operations", 0),
                cash_flow_investing=year_data.get("cash_flow_investing", 0),
                cash_flow_financing=year_data.get("cash_flow_financing", 0),
                year=year_data.get("year", 2024)
            ))
        
        # تنفيذ التحليلات المطلوبة
        results = []
        
        for analysis_type in data.analysis_types:
            try:
                if analysis_type == AnalysisType.HORIZONTAL:
                    result = analyzer.horizontal_analysis(financial_data)
                elif analysis_type == AnalysisType.VERTICAL:
                    result = analyzer.vertical_analysis(financial_data)
                elif analysis_type == AnalysisType.LIQUIDITY:
                    result = analyzer.liquidity_analysis(financial_data)
                elif analysis_type == AnalysisType.PROFITABILITY:
                    result = analyzer.profitability_analysis(financial_data)
                elif analysis_type == AnalysisType.ZSCORE:
                    result = analyzer.zscore_analysis(financial_data)
                elif analysis_type == AnalysisType.FORECASTING:
                    result = analyzer.forecasting_analysis(financial_data)
                else:
                    result = {"message": f"التحليل {analysis_type} قيد التطوير"}
                
                results.append(AnalysisResult(
                    analysis_type=analysis_type,
                    results=result,
                    charts=[],
                    recommendations=[]
                ))
                
            except Exception as e:
                logger.error(f"خطأ في تحليل {analysis_type}: {str(e)}")
                results.append(AnalysisResult(
                    analysis_type=analysis_type,
                    results={"error": str(e)},
                    charts=[],
                    recommendations=[]
                ))
        
        return {
            "success": True,
            "company_name": data.company_name,
            "industry": data.industry,
            "market_comparison": data.market_comparison,
            "results": results,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"خطأ في التحليل: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/industries")
async def get_industries():
    """الحصول على قائمة القطاعات"""
    return {
        "industries": [
            {"value": "technology", "name_ar": "تكنولوجيا المعلومات", "name_en": "Information Technology"},
            {"value": "banking", "name_ar": "البنوك والخدمات المالية", "name_en": "Banking & Financial Services"},
            {"value": "energy", "name_ar": "الطاقة والمرافق", "name_en": "Energy & Utilities"},
            {"value": "healthcare", "name_ar": "الرعاية الصحية", "name_en": "Healthcare"},
            {"value": "retail", "name_ar": "التجارة والتجزئة", "name_en": "Retail & Commerce"},
            {"value": "manufacturing", "name_ar": "الصناعات التحويلية", "name_en": "Manufacturing"},
            {"value": "real_estate", "name_ar": "العقارات والتطوير", "name_en": "Real Estate & Development"},
            {"value": "telecommunications", "name_ar": "الاتصالات", "name_en": "Telecommunications"},
            {"value": "transportation", "name_ar": "النقل واللوجستيات", "name_en": "Transportation & Logistics"},
            {"value": "agriculture", "name_ar": "الزراعة والثروة الحيوانية", "name_en": "Agriculture & Livestock"}
        ]
    }

@app.get("/api/health")
async def health_check():
    """فحص صحة النظام"""
    return {
        "status": "healthy",
        "system": "Razan AI Financial Analysis System",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
