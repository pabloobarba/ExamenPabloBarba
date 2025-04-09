import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import timedelta
import numpy as np


# Configuración de la página
st.set_page_config(page_title="Análisis Financiero", layout="wide")

# -------- Sidebar --------
with st.sidebar:
    st.title("📊 Panel de Análisis")
    st.markdown("""
    <div style='font-size: 15px; color: #FFFFFF;'>
        Bienvenido al sistema de análisis financiero.<br>
        Ingrese un <b>ticker</b> perteneciente al índice <b>S&P 500</b> para comenzar el análisis.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    
    ticker_input = st.text_input("🔍 Ticker del S&P 500:", value="MSFT")

# -------- Encabezado principal --------
st.markdown("""
    <h1 style='text-align: center; color: #FFFFFF; font-family: Arial, sans-serif;'>
        Análisis Financiero Bursátil
    </h1>
    <p style='text-align: center; font-size: 20 px; color: #FFFFFF;'>
        Consulta profesional de información bursátil y datos históricos de mercado.
    </p>
""", unsafe_allow_html=True)

st.divider()

# -------- Funciones --------
@st.cache_data
def validar_ticker(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return not data.empty
    except:
        return False

@st.cache_data
def obtener_info_empresa(ticker):
    info = yf.Ticker(ticker).info
    nombre = info.get("longName", "Nombre no disponible")
    sector = info.get("sector", "Sector no disponible")
    descripcion = info.get("longBusinessSummary", "Descripción no disponible")
    return nombre, sector, descripcion

def calcular_cagr_1y(data):
    if data.empty or "Close" not in data.columns:
        return None
    fecha_final = data.index[-1]
    fecha_inicial = fecha_final - timedelta(days=365)
    data_filtrada = data[data.index >= fecha_inicial]
    if len(data_filtrada) < 2:
        return None

    precio_inicio = data_filtrada["Close"].iloc[0]
    precio_fin = data_filtrada["Close"].iloc[-1]

    if isinstance(precio_inicio, pd.Series):
        precio_inicio = precio_inicio.item()
    if isinstance(precio_fin, pd.Series):
        precio_fin = precio_fin.item()

    if pd.isna(precio_inicio) or pd.isna(precio_fin):
        return None

    cagr = (precio_fin / precio_inicio) ** (1 / 1) - 1
    return round(cagr * 100, 2)

def calcular_cagr_3y(data):
    if data.empty or "Close" not in data.columns:
        return None
    fecha_final = data.index[-1]
    fecha_inicial = fecha_final - timedelta(days=1095)
    data_filtrada = data[data.index >= fecha_inicial]
    if len(data_filtrada) < 2:
        return None

    precio_inicio = data_filtrada["Close"].iloc[0]
    precio_fin = data_filtrada["Close"].iloc[-1]

    if isinstance(precio_inicio, pd.Series):
        precio_inicio = precio_inicio.item()
    if isinstance(precio_fin, pd.Series):
        precio_fin = precio_fin.item()

    if pd.isna(precio_inicio) or pd.isna(precio_fin):
        return None

    cagr = (precio_fin / precio_inicio) ** (1 / 1) - 1
    return round(cagr * 100, 2)

def calcular_cagr_5y(data):
    if data.empty or "Close" not in data.columns:
        return None
    fecha_final = data.index[-1]
    fecha_inicial = fecha_final - timedelta(days=1825)
    data_filtrada = data[data.index >= fecha_inicial]
    if len(data_filtrada) < 2:
        return None

    precio_inicio = data_filtrada["Close"].iloc[0]
    precio_fin = data_filtrada["Close"].iloc[-1]

    if isinstance(precio_inicio, pd.Series):
        precio_inicio = precio_inicio.item()
    if isinstance(precio_fin, pd.Series):
        precio_fin = precio_fin.item()

    if pd.isna(precio_inicio) or pd.isna(precio_fin):
        return None

    cagr = (precio_fin / precio_inicio) ** (1 / 1) - 1
    return round(cagr * 100, 2)


# -------- Lógica principal --------
if ticker_input:
    ticker_input = ticker_input.upper()
    if validar_ticker(ticker_input):
        st.success(f"✅ Información encontrada para: **{ticker_input}**")
        
        st.divider()

        nombre, sector, descripcion = obtener_info_empresa(ticker_input)

        st.markdown(f"""
            <h2 style='text-align: center; color: #FFFFFF; font-family: Georgia, serif;'>Nombre: {nombre}</h2>
            <h3 style='text-align: center; color: #FFFFFF; font-family: Georgia, serif;'>🏭 Sector: {sector}</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style='background-color: #F4F6F7; padding: 25px; border-radius: 8px; margin: 30px auto; width: 85%;'>
                <p style='font-size: 16px; text-align: justify; color: #333; font-family: Georgia, serif; line-height: 1.6;'>
                    {descripcion}
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Descargar precios históricos de 5 años
        precios_5y = yf.download(ticker_input, period="5y")

        # Calcular medias móviles
        precios_5y["MA20"] = precios_5y["Close"].rolling(window=20).mean()
        precios_5y["MA50"] = precios_5y["Close"].rolling(window=50).mean()
        precios_5y["MA200"] = precios_5y["Close"].rolling(window=200).mean()

        # -------- Gráfica con medias móviles --------
        st.subheader("📉 Precio histórico de cierre con medias móviles")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(precios_5y.index, precios_5y["Close"], label="Precio de cierre", color="#1f77b4")
        ax.plot(precios_5y.index, precios_5y["MA20"], label="Media móvil 20 días", linestyle="--", color="#FF9900")
        ax.plot(precios_5y.index, precios_5y["MA50"], label="Media móvil 50 días", linestyle="--", color="#2ca02c")
        ax.plot(precios_5y.index, precios_5y["MA200"], label="Media móvil 200 días", linestyle="--", color="#d62728")

        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.tick_params(axis='x', rotation=45)

        ax.set_title(f"Precio histórico de cierre - {ticker_input} (últimos 5 años)", fontsize=14)
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precio USD")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        st.pyplot(fig)

        st.divider()

        # -------- Rendimiento anualizado (CAGR) --------
        st.subheader("📈 Cálculo de Rendimientos Anualizados")

        precios_1y = yf.download(ticker_input, period="1y")
        rendimiento_anual = calcular_cagr_1y(precios_1y)
 
        if rendimiento_anual is not None:
            st.markdown(f"""
            <div style="font-size: 22px; color: #FFFFFF;">
                <strong>Rendimiento anualizado (1 año) para {ticker_input}:</strong> 
                <span style="color: {'green' if rendimiento_anual >= 0 else 'red'};">
                    {'🔼' if rendimiento_anual >= 0 else '🔽'} {rendimiento_anual:.2f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

        precios_3y = yf.download(ticker_input, period="3y")
        rendimiento_anual = calcular_cagr_3y(precios_3y)
 
        if rendimiento_anual is not None:
            st.markdown(f"""
            <div style="font-size: 22px; color: #FFFFFF;">
                <strong>Rendimiento anualizado (3 años) para {ticker_input}:</strong> 
                <span style="color: {'green' if rendimiento_anual >= 0 else 'red'};">
                    {'🔼' if rendimiento_anual >= 0 else '🔽'} {rendimiento_anual:.2f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

        precios_5y = yf.download(ticker_input, period="5y")
        rendimiento_anual = calcular_cagr_5y(precios_5y)
 
        if rendimiento_anual is not None:
            st.markdown(f"""
            <div style="font-size: 22px; color: #FFFFFF;">
                <strong>Rendimiento anualizado (5 años) para {ticker_input}:</strong> 
                <span style="color: {'green' if rendimiento_anual >= 0 else 'red'};">
                    {'🔼' if rendimiento_anual >= 0 else '🔽'} {rendimiento_anual:.2f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background-color: #F0F3F4; padding: 15px; border-radius: 8px; font-size: 15px; color: #333; margin-top: 15px;">
                📌 <strong>Explicación:</strong> El rendimiento anualizado se calculó usando la fórmula del <em>Compound Annual Growth Rate (CAGR)</em>, 
                que representa el crecimiento promedio anual considerando interés compuesto.
            </div>
            """, unsafe_allow_html=True)

            st.divider()
        else:
            st.warning("No se pudo calcular el rendimiento anual. Puede que no haya suficientes datos disponibles.")
                     
        
         # -------- Gráfico comparativo de rendimientos (estético) --------
        st.subheader("📊 Comparación visual de rendimientos anualizados")

        # Crear listas de datos
        periodos = ["1 año", "3 años", "5 años"]
        rendimientos = []

        # Recalcular para asegurar consistencia
        rendimiento_1 = calcular_cagr_1y(precios_1y)
        rendimiento_3 = calcular_cagr_3y(precios_3y)
        rendimiento_5 = calcular_cagr_5y(precios_5y)

        for r in [rendimiento_1, rendimiento_3, rendimiento_5]:
            rendimientos.append(r if r is not None else 0)

        # Gráfico de barras horizontales
        fig_bar, ax = plt.subplots(figsize=(8, 2.5))
        colores = ["green" if r >= 0 else "red" for r in rendimientos]
        bars = ax.barh(periodos, rendimientos, color=colores, height=0.5)

        # Etiquetas
        for i, v in enumerate(rendimientos):
            ax.text(v + 0.5 if v >= 0 else v - 5, i, f"{v:.2f}%", va='center', fontsize=10, color='#333')

        ax.set_xlabel("Rendimiento (%)")
        ax.set_xlim(min(-10, min(rendimientos) - 5), max(10, max(rendimientos) + 5))
        ax.set_title(f"Rendimiento anualizado - {ticker_input}", fontsize=13)
        ax.axvline(0, color='gray', linewidth=0.8)
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.3)

        st.pyplot(fig_bar)

        st.divider()

        # -------- Cálculo del riesgo (volatilidad anualizada) --------
       
        st.subheader("📉 Volatilidad anualizada (riesgo del activo)")
        
         # Calcular rendimientos diarios logarítmicos
        precios_1y["LogRet"] = np.log(precios_1y["Close"] / precios_1y["Close"].shift(1))
        rendimientos_diarios = precios_1y["LogRet"].dropna()

        if not rendimientos_diarios.empty:
            volatilidad_anual = np.std(rendimientos_diarios) * np.sqrt(252)
            volatilidad_pct = round(volatilidad_anual * 100, 2)

            st.markdown(f"""
            <div style="font-size: 22px; color: #FFFFFF;">
                <strong>Volatilidad anualizada para {ticker_input}:</strong> 
                <span style="color:#0072B2;">{volatilidad_pct:.2f}%</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background-color: #F4F6F7; padding: 15px; border-radius: 8px; font-size: 15px; color: #333; margin-top: 15px;">
                📌 <strong>Explicación:</strong> Este valor representa la <em>volatilidad anual histórica</em> del activo, 
                medida por la desviación estándar de los rendimientos diarios logarítmicos. 
                Un valor más alto indica mayor incertidumbre o riesgo en el comportamiento del precio.
            </div>
            """, unsafe_allow_html=True)  

            st.divider()
            st.subheader("📉 Indicadores técnicos")

            # ==    = RSI ===
            delta = precios_1y["Close"].diff()
            ganancia = delta.where(delta > 0, 0)
            perdida = -delta.where(delta < 0, 0)
            avg_gain = ganancia.rolling(window=14).mean()
            avg_loss = perdida.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            precios_1y["RSI"] = rsi

            fig_rsi, ax_rsi = plt.subplots(figsize=(10, 2))
            ax_rsi.plot(precios_1y.index, precios_1y["RSI"], label="RSI", color="#FF9900")
            ax_rsi.axhline(70, linestyle="--", color="red", linewidth=1)
            ax_rsi.axhline(30, linestyle="--", color="green", linewidth=1)
            ax_rsi.set_title("Índice de Fuerza Relativa (RSI)")
            ax_rsi.set_ylim(0, 100)
            ax_rsi.grid(True, linestyle='--', alpha=0.3)
            st.pyplot(fig_rsi)

            # === MACD ===#
            exp1 = precios_1y["Close"].ewm(span=12, adjust=False).mean()
            exp2 = precios_1y["Close"].ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()
            precios_1y["MACD"] = macd
            precios_1y["Signal"] = signal

            fig_macd, ax_macd = plt.subplots(figsize=(10, 3))
            ax_macd.plot(precios_1y.index, macd, label="MACD", color="blue")
            ax_macd.plot(precios_1y.index, signal, label="Señal", color="orange")
            ax_macd.set_title("MACD - Media Móvil Convergente Divergente")
            ax_macd.axhline(0, color="gray", linewidth=0.8)
            ax_macd.legend(loc="upper left")
            ax_macd.grid(True, linestyle='--', alpha=0.3)
            st.pyplot(fig_macd)

            st.markdown("""
            <div style="background-color: #F4F6F7; padding: 15px; border-radius: 8px; font-size: 15px; color: #333; margin-top: 15px;">
                📌 <strong>Explicación:</strong> El RSI es un oscilador que mide la velocidad y el cambio de los movimientos de precios recientes. 
                Su valor oscila entre 0 y 100 y ayuda a identificar condiciones de sobrecompra o sobreventa en el mercado
            </div>
            """, unsafe_allow_html=True) 

            st.markdown("""
            <div style="background-color: #F4F6F7; padding: 15px; border-radius: 8px; font-size: 15px; color: #333; margin-top: 15px;">
                📌 <strong>Explicación:</strong> El MACD es un indicador de seguimiento de tendencia que muestra la relación entre dos medias móviles exponenciales (EMA) de distinto periodo
            </div>
            """, unsafe_allow_html=True) 

        else:
          st.warning("No se pudo calcular la volatilidad. Datos insuficientes de precios diarios.")

    else:
        st.error("❌ Ticker inválido, por favor revise e intente de nuevo.")

st.divider()
st.caption("Profe pongame 100 :)")











