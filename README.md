# Analytics API 🚀

Esta es una API Analítica construida con **FastAPI** y **Pandas** diseñada para conectarse a una base de datos PostgreSQL. Extrae, procesa y formatea datos de inventario y préstamos para ser consumidos directamente por librerías de gráficos en el frontend (como Recharts o Chart.js).

## 🛠️ Tecnologías

- **FastAPI**: Framework web asíncrono y de alto rendimiento.
- **Pandas**: Procesamiento y agregación de datos (agrupación mensual, contadores, alertas).
- **SQLAlchemy**: ORM para gestionar la conexión y lectura de datos.
- **Pydantic**: Validación de datos y generación de esquemas JSON estrictos.
- **PostgreSQL**: Base de datos relacional principal.

## ⚙️ Requisitos Previos

- Python 3.11+
- Base de datos PostgreSQL (local o en la nube como Prisma/Supabase)

## 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio y entrar en la carpeta:**
   ```bash
   cd python-backend
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar Variables de Entorno:**
   Configura la URL de tu base de datos (por defecto la app intentará usar la variable `DATABASE_URL`).
   ```bash
   # En Windows PowerShell
   $env:DATABASE_URL="postgresql://usuario:password@localhost:5432/tu_base_de_datos"
   ```

4. **Ejecutar el servidor local:**
   ```bash
   uvicorn main:app --reload
   ```
   La API estará corriendo en `http://127.0.0.1:8000`.

## ☁️ Despliegue en Render

El proyecto está pre-configurado para desplegarse fácilmente en [Render.com](https://render.com).

1. Conecta este repositorio en tu dashboard de Render creando un nuevo **Web Service**.
2. **Start Command**: `python main.py` (o alternativamente `uvicorn main:app --host 0.0.0.0 --port $PORT`).
3. **Environment Variables**:
   - `PYTHON_VERSION`: `3.11.6`
   - `DATABASE_URL`: Tu connection string de PostgreSQL (Ej. proporcionado por Prisma). *Nota: Si empieza por `postgres://`, la app lo convierte automáticamente a `postgresql://` para evitar errores.*
   - `FRONTEND_URL`: `*` (o la URL de tu Vercel/Netlify por seguridad).

## 📡 Endpoints Principales

Puedes probar todos los endpoints y ver sus respuestas exactas accediendo a la documentación interactiva Swagger UI:
👉 **`http://127.0.0.1:8000/docs`**

- `GET /` - Health check de la API.
- `GET /analytics/kpis` - Resumen general numérico (Inventario total, préstamos activos, etc.).
- `GET /analytics/category-distribution` - Distribución de inventario por categoría (Ideal para gráficos de tarta).
- `GET /analytics/loan-history` - Historial de los últimos 6 meses (Ideal para gráficos de barras/líneas).
- `GET /analytics/top-articles` - Top 5 de artículos más prestados.
- `GET /analytics/critical-alerts` - Alertas de stock bajo o préstamos atrasados.
