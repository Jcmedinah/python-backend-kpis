<div align="center">
  <h1>📊 Inventory Analytics API</h1>
  <p>
    <strong>API RESTful de alto rendimiento para el análisis de inventarios y préstamos.</strong>
  </p>
  <p>
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  </p>
</div>

<hr />

## 💡 ¿Qué hace esta aplicación?

**Analytics API** es un motor de procesamiento de datos backend diseñado para integrarse directamente con Dashboards en React, Vue o cualquier otro framework de frontend. 

En lugar de delegar cálculos pesados al navegador del cliente, esta API se encarga de conectar con la base de datos PostgreSQL, leer las tablas crudas de inventarios y préstamos, y utilizar **Pandas** para limpiar, agrupar y transformar millones de registros instantáneamente. 

Entre sus capacidades clave destacan:
- **Agrupación Temporal:** Analiza historiales de préstamos mensuales (últimos 6 meses).
- **KPIs en Tiempo Real:** Calcula el inventario disponible, equipos dañados y préstamos atrasados.
- **Detección de Anomalías:** Genera alertas críticas de stock agotado (< 10% del total) y fechas de entrega vencidas.
- **Formato Listo para Graficar:** Devuelve la data estructurada en objetos JSON que encajan perfectamente en librerías como Recharts o Chart.js.

---

## 🚀 Instalación y Configuración

Sigue estos pasos para correr el motor analítico en tu máquina local.

### 1. Requisitos Previos
* **Python 3.11** o superior instalado en tu sistema.
* Una base de datos **PostgreSQL** activa (ya sea local usando pgAdmin o remota como Prisma/Supabase).

### 2. Clonar e Instalar
```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPO>
cd python-backend

# 2. Instalar dependencias 
pip install -r requirements.txt
```

### 3. Variables de Entorno
Por defecto, la API utiliza una conexión de prueba. Para conectarte a tu propia base de datos, configura la variable en tu terminal antes de ejecutar:

**En Windows (PowerShell):**
```powershell
$env:DATABASE_URL="postgresql://usuario:contraseña@localhost:5432/mi_base_de_datos"
```
*(Render inyectará esta variable automáticamente en producción).*

---

## 📖 Instructivo de Uso

Una vez instalado, levantar el proyecto y consumirlo es extremadamente simple.

### Iniciar el Servidor
Ejecuta el siguiente comando en tu terminal para arrancar Uvicorn con recarga en vivo (ideal para desarrollo):

```bash
uvicorn main:app --reload
```
Verás en consola que el servidor está escuchando en `http://127.0.0.1:8000`.

### Consumir la Documentación Interactiva (Swagger)
FastAPI genera documentación automática de clase mundial. Abre tu navegador y dirígete a:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Desde aquí puedes probar la API haciendo clic en **"Try it out"** en cualquiera de los siguientes endpoints:

| Endpoint | Método | ¿Para qué sirve? |
| :--- | :---: | :--- |
| `/` | `GET` / `HEAD` | **Health Check:** Verifica si el servidor está encendido (usado por Render). |
| `/analytics/kpis` | `GET` | **Métricas Globales:** Total de inventario, stock disponible y alertas generales. |
| `/analytics/category-distribution` | `GET` | **Gráficos de Tarta:** Devuelve la cantidad de inventario separada por categoría. |
| `/analytics/loan-history` | `GET` | **Gráfico de Líneas/Barras:** Historial de préstamos vs devoluciones en los últimos 6 meses. |
| `/analytics/top-articles` | `GET` | **Ranking:** Los 5 artículos con mayor cantidad de salidas/préstamos. |
| `/analytics/critical-alerts` | `GET` | **Tablas de Advertencia:** Equipos casi agotados y usuarios con fechas de préstamo vencidas. |

### Integración con tu Frontend
El proyecto tiene el **CORS configurado de forma abierta** (sin credenciales), lo que significa que desde tu proyecto en Vite/React puedes hacer peticiones `fetch()` directamente usando axios o la API Fetch nativa sin sufrir bloqueos del navegador.

```javascript
// Ejemplo en React
const response = await fetch("http://127.0.0.1:8000/analytics/kpis");
const data = await response.json();
console.log("Mis KPIs listos para graficar:", data);
```

---
<div align="center">
  <i>Construido con Python 🐍 y mucho café ☕</i>
</div>
