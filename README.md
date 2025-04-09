# 📊 Análisis Financiero Corporativo - Streamlit App

Esta es una aplicación desarrollada en **Python** usando **Streamlit** para el análisis financiero de empresas del S&P 500. Permite consultar información bursátil, visualizar gráficos históricos, calcular indicadores de rendimiento y riesgo, así como indicadores técnicos como RSI y MACD.

---

## 🚀 Funcionalidades

- Búsqueda de cualquier ticker del S&P 500.
- Visualización del precio histórico de cierre con medias móviles (20, 50, 200 días).
- Cálculo del **rendimiento anualizado (CAGR)** a 1, 3 y 5 años.
- Comparación visual de rendimientos mediante gráfico de barras horizontal.
- Cálculo de **volatilidad anualizada** basada en rendimientos logarítmicos.
- Gráficos de **RSI (Índice de Fuerza Relativa)** y **MACD** para análisis técnico.

---

## 🧰 Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

---

## ▶️ Cómo ejecutar

Ejecuta la aplicación con:

```bash
streamlit run nombre_del_script.py
```

Cambia `nombre_del_script.py` por el nombre real del archivo.

---

## 📂 Estructura sugerida del repositorio

```
📁 analisis-financiero/
├── app.py
├── requirements.txt
└── README.md
```

---

## 📌 Notas

- Los datos son obtenidos en tiempo real desde [Yahoo Finance](https://finance.yahoo.com/) usando la librería `yfinance`.
- Este proyecto es ideal como base para construir dashboards más avanzados para análisis financiero.

---

## 📄 Licencia

Este proyecto es de uso educativo. Puedes adaptarlo, mejorar y personalizarlo según tus necesidades.