from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime

from database import engine, Base
import schemas

# Inicializar Base (crear tablas si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Analytics API")

@app.get("/")
@app.head("/")
def read_root():
    return {"status": "API corriendo correctamente"}

# Configuración CORS global para aceptar todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analytics/kpis", response_model=schemas.KPIs)
def get_kpis():
    articles_df = pd.read_sql("SELECT * FROM articles", engine)
    loans_df = pd.read_sql("SELECT * FROM loans", engine)
    
    total_inventory = int(articles_df['quantity_total'].sum()) if not articles_df.empty else 0
    available_stock = int(articles_df['quantity_available'].sum()) if not articles_df.empty else 0
    damaged_items = int(articles_df['quantity_damaged'].sum()) if not articles_df.empty else 0
    
    active_loans = 0
    overdue_loans = 0
    
    if not loans_df.empty:
        # La BD utiliza true/false para el estado del préstamo
        status_limpio = loans_df['status'].astype(str).str.strip().str.lower()
        active_loans = int(len(loans_df[status_limpio == 'true']))
        
        hoy = pd.Timestamp.now().date()
        loans_df['due_date'] = pd.to_datetime(loans_df['due_date']).dt.date
        overdue_loans = int(len(loans_df[(status_limpio == 'true') & (loans_df['due_date'] < hoy)]))
    
    return schemas.KPIs(
        total_inventory=total_inventory,
        available_stock=available_stock,
        damaged_items=damaged_items,
        active_loans=active_loans,
        overdue_loans_count=overdue_loans
    )

@app.get("/analytics/category-distribution", response_model=list[schemas.CategoryDistribution])
def get_category_distribution():
    query = """
        SELECT c.category_name as category, a.quantity_total 
        FROM articles a
        JOIN categories c ON a.category_id = c.category_id
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        return []
        
    dist = df.groupby('category')['quantity_total'].sum().reset_index()
    
    return [
        {"category": str(row['category']), "count": int(row['quantity_total'])} 
        for _, row in dist.iterrows()
    ]

@app.get("/analytics/loan-history", response_model=list[schemas.MonthlyLoanHistory])
def get_loan_history():
    df = pd.read_sql("SELECT loan_date, return_date FROM loans", engine)
    if df.empty:
        return []
        
    df['loan_date'] = pd.to_datetime(df['loan_date'])
    df['return_date'] = pd.to_datetime(df['return_date'])
    
    # Manejar los valores nulos en return_date usando .fillna()
    df['return_date'] = df['return_date'].fillna(pd.NaT)
    
    try:
        # Pandas >= 2.2 prefiere 'ME' (Month End)
        df_loans = df.set_index('loan_date').resample('ME').size().rename('loans')
        df_returns = df.dropna(subset=['return_date']).set_index('return_date').resample('ME').size().rename('returns')
    except ValueError:
        # Fallback para versiones de Pandas más antiguas
        df_loans = df.set_index('loan_date').resample('M').size().rename('loans')
        df_returns = df.dropna(subset=['return_date']).set_index('return_date').resample('M').size().rename('returns')
    
    # Unir ambos DataFrames y rellenar nulos
    history = pd.concat([df_loans, df_returns], axis=1).fillna(0)
    
    # Obtener los últimos 6 meses
    history = history.tail(6)
    
    # Nombres de meses en español
    meses_es = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun', 
                7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
    
    result = []
    for date_idx, row in history.iterrows():
        result.append({
            "month": meses_es[date_idx.month],
            "loans": int(row['loans']),
            "returns": int(row['returns'])
        })
    return result

@app.get("/analytics/top-articles", response_model=list[schemas.TopArticle])
def get_top_articles():
    loans_df = pd.read_sql("SELECT item_id FROM loans", engine)
    articles_df = pd.read_sql("SELECT item_id, name FROM articles", engine)
    
    if loans_df.empty or articles_df.empty:
        return []
        
    # Realizar merge entre LOANS y ARTICLES
    merged = pd.merge(loans_df, articles_df, on="item_id")
    
    # Usar value_counts() sobre el nombre del artículo
    top_counts = merged['name'].value_counts().head(5)
    
    result = []
    for name, count in top_counts.items():
        result.append({
            "name": str(name),
            "loan_count": int(count)
        })
    return result

@app.get("/analytics/critical-alerts", response_model=schemas.CriticalAlerts)
def get_critical_alerts():
    articles_df = pd.read_sql("SELECT item_id, name, quantity_available, quantity_total FROM articles", engine)
    loans_df = pd.read_sql("SELECT loan_id, user_id, item_id, due_date, status FROM loans", engine)
    
    articles_list = []
    if not articles_df.empty:
        critical_articles = articles_df[articles_df['quantity_available'] < (articles_df['quantity_total'] * 0.1)]
        articles_list = critical_articles.to_dict(orient='records')
        
    loans_list = []
    if not loans_df.empty:
        hoy = pd.Timestamp.now().date()
        loans_df['due_date'] = pd.to_datetime(loans_df['due_date']).dt.date
        status_limpio = loans_df['status'].astype(str).str.strip().str.lower()
        critical_loans = loans_df[(status_limpio == 'true') & (loans_df['due_date'] < hoy)]
        loans_list = critical_loans.to_dict(orient='records')
        
    return {
        "articles": articles_list,
        "loans": loans_list
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
