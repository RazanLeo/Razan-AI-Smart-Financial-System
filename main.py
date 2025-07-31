from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from enum import Enum
import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging
import os
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
            "healthcare": {
                "current_ratio": 2.0,
                "quick_ratio": 1.5,
                "debt_to_equity": 0.4,
                "roe": 0.13,
                "gross_margin": 0.7,
                "operating_margin": 0.18,
                "net_margin": 0.12
            },
            "retail": {
                "current_ratio": 1.8,
                "quick_ratio": 0.9,
                "debt_to_equity": 0.7,
                "roe": 0.11,
                "gross_margin": 0.35,
                "operating_margin": 0.08,
                "net_margin": 0.05
            }
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
            quick_ratio = (year_data.current_assets - year_data.current_assets * 0.3) / year_data.current_liabilities
            
            year_analysis = {
                "year": year_data.year,
                "current_ratio": round(current_ratio, 2),
                "quick_ratio": round(quick_ratio, 2),
                "working_capital": year_data.current_assets - year_data.current_liabilities,
                "cash_ratio": round(year_data.cash_flow_operations / year_data.current_liabilities, 2)
            }
            results[f"year_{year_data.year}"] = year_analysis
        
        return results
    
    def profitability_analysis(self, data: List[FinancialData]) -> Dict[str, Any]:
        """تحليل الربحية"""
        results = {}
        
        for year_data in data:
            year_analysis = {
                "year": year_data.year,
                "gross_profit_margin": round((year_data.gross_profit / year_data.revenue) * 100, 2),
                "operating_margin": round((year_data.operating_income / year_data.revenue) * 100, 2),
                "net_margin": round((year_data.net_income / year_data.revenue) * 100, 2),
                "roe": round((year_data.net_income / year_data.shareholders_equity) * 100, 2),
                "roa": round((year_data.net_income / year_data.total_assets) * 100, 2),
                "roic": round((year_data.operating_income / (year_data.total_assets - year_data.current_liabilities)) * 100, 2)
            }
            results[f"year_{year_data.year}"] = year_analysis
        
        return results
    
    def zscore_analysis(self, data: List[FinancialData]) -> Dict[str, Any]:
        """تحليل Z-Score لتقييم مخاطر الإفلاس"""
        results = {}
        
        for year_data in data:
            working_capital = year_data.current_assets - year_data.current_liabilities
            retained_earnings = year_data.shareholders_equity * 0.7
            
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
                "z_score": round(z_score, 2),
                "risk_level": risk_level,
                "bankruptcy_probability": max(0, min(100, round((3.0 - z_score) / 3.0 * 100, 2)))
            }
            results[f"year_{year_data.year}"] = year_analysis
        
        return results
    
    def forecasting_analysis(self, data: List[FinancialData]) -> Dict[str, Any]:
        """التحليل التنبؤي"""
        if len(data) < 3:
            raise ValueError("يجب توفير بيانات لثلاث سنوات على الأقل للتنبؤ")
        
        revenue_growth_rates = []
        profit_growth_rates = []
        
        for i in range(1, len(data)):
            revenue_growth = ((data[i].revenue - data[i-1].revenue) / data[i-1].revenue) * 100
            profit_growth = ((data[i].net_income - data[i-1].net_income) / data[i-1].net_income) * 100
            
            revenue_growth_rates.append(revenue_growth)
            profit_growth_rates.append(profit_growth)
        
        avg_revenue_growth = np.mean(revenue_growth_rates)
        avg_profit_growth = np.mean(profit_growth_rates)
        
        last_year = data[-1]
        next_year_revenue = last_year.revenue * (1 + avg_revenue_growth / 100)
        next_year_profit = last_year.net_income * (1 + avg_profit_growth / 100)
        
        return {
            "historical_growth": {
                "revenue_growth_rates": [round(rate, 2) for rate in revenue_growth_rates],
                "profit_growth_rates": [round(rate, 2) for rate in profit_growth_rates],
                "avg_revenue_growth": round(avg_revenue_growth, 2),
                "avg_profit_growth": round(avg_profit_growth, 2)
            },
            "forecast_next_year": {
                "year": last_year.year + 1,
                "predicted_revenue": round(next_year_revenue, 2),
                "predicted_profit": round(next_year_profit, 2),
                "confidence_level": 75
            }
        }

# إنشاء محلل مالي
analyzer = FinancialAnalyzer()

# المسارات
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """الصفحة الرئيسية"""
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()

@app.post("/api/analyze")
async def analyze_financial_data(data: FinancialInputData):
    """تحليل البيانات المالية"""
    try:
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
