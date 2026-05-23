from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class KPIs(BaseModel):
    total_inventory: int
    available_stock: int
    damaged_items: int
    active_loans: int
    overdue_loans_count: int

class CategoryDistribution(BaseModel):
    category: str
    count: int

class MonthlyLoanHistory(BaseModel):
    month: str
    loans: int
    returns: int

class TopArticle(BaseModel):
    name: str
    loan_count: int

class ArticleAlert(BaseModel):
    item_id: int
    name: str
    quantity_available: int
    quantity_total: int

class LoanAlert(BaseModel):
    loan_id: int
    user_id: int
    item_id: int
    due_date: date
    status: str

class CriticalAlerts(BaseModel):
    articles: List[ArticleAlert]
    loans: List[LoanAlert]
