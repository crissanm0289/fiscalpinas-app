import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="FISCALPIÑAS - GESTIÓN RDO", page_icon="🏗️")

# --- VARIABLES DEL CONTRATO (EDITAR AQUÍ) ---
MONTO_TOTAL_PROYECTO = 150000.00  # <--- COLOCAR EL MONTO EXACTO DEL CONTRATO AQUÍ
NOMBRE_CONSORCIO = "CONSORCIO FISCALPIÑAS"
OBJETO_CONTRATO = "Fiscalización y Construcción de Obras Civiles y Eléctricas"

# --- GESTIÓN DE ESTADO (MEMORIA) ---
if 'data_fiscalpinas' not in st.session_state:
    # Inicializamos con el día 0 (Inicio)
    st.session_state['data_fiscalpinas'] = pd.DataFrame({
        'Fecha': [date(2025, 1, 1)],
        'Día N': ['Inicio'],
        'Físico Diario (%)': [0.0],
        'Inversión Diaria ($)': [0.0],
        'Físico Acum (%)': [0.0],
        'Financiero Acum ($)': [0.0],
        'Hito Civil (%)': [0.0],
        'Hito Eléctrico (%)': [0.0],
        'CPI': [1.0],
        'SPI': [1.0],
        'Detalle': ['Inicio de Contrato'],
        'Fotos': [0]
    })

if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "RDO"

# --- FUNCIONES AUXILIARES ---
def reset_app():
    if 'data_fiscalpinas' in st.session_state:
        del st.session_state['data_fiscalpinas']
    st.rerun()

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .main-header {font-size: 26px; font-weight: bold; color: #b91c1c; text-align: center; margin-bottom: 20px;}
    .sub-header {font-size: 18px; font-weight: bold; color: #1E3A8A; margin-top: 10px;}
    .stTextInput label, .stNumberInput label, .stDateInput label, .stSelectbox label, .stTextArea label {
        font-weight: bold !important; color: #333 !important;
    }
    .metric-card {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #b91c1c;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (BARRA LATERAL) ---
st.sidebar.title("🏗️ MENÚ DE OBRA")
st.sidebar.info(f"**Contratista:** {NOMBRE_CONSORCIO}")

opcion = st.sidebar.radio("Ir a:", ["RDO (Ingreso Diario)", "DASHBOARD (Reporte)"])

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ BORRAR TODOS LOS DATOS"):
    reset_app()

# ==============================================================================
# MÓDULO: RDO (Puntos 6 al 20)
# ==============================================================================
if opcion == "RDO (Ingreso Diario)":
    st.markdown(f'<div class="main-header">REGISTRO DIARIO DE OBRA (RDO)</div>', unsafe_allow_html=True)
    
    df = st.session_state['data_fiscalpinas']
    ultimo = df.iloc[-1]
    prev_acum_fisico = ultimo['Físico Acum (%)']
    prev_acum_financiero = ultimo['Financiero Acum ($)']

    st.warning("📝 Ingrese los datos del día. Los cálculos acumulados se harán automáticamente al guardar.")

    with st.form("formulario_rdo"):
        
        # --- BLOQUE 1: DATOS GENERALES ---
        st.markdown('<div class="sub-header">A. Datos Generales y Económicos</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        in_fecha = c1.date_input("6. Fechas de Ejecución", date.today())
        in_dia = c2.text_input("9. Día de ejecución", placeholder="Ej: Día 15")
        in_clima = c3.selectbox("10. Condiciones climáticas", ["Soleado", "Nublado", "Lluvia", "Lluvia Fuerte"])

        c4, c5 = st.columns(2)
        c4.text_input("7. Datos Económicos del Contrato", f"$ {MONTO_TOTAL_PROYECTO:,.2f}", disabled=True)
        c5.text_input("8. Dato Económico total del Proyecto", f"$ {MONTO_TOTAL_PROYECTO:,.2f}", disabled=True)

        # --- BLOQUE 2: AVANCE Y VALOR GANADO ---
        st.markdown('<div class="sub-header">B. Control de Avance y Valor Ganado</div>', unsafe_allow_html=True)
        
        col_av1, col_av2, col_av3 = st.columns(3)
        in_monto_diario = col_av1.number_input("11. $ de Avance DEL DÍA (Inversión)", min_value=0.0, step=100.0)
        
        # Calculo automático de % diario basado en el monto ingresado
        pct_diario_calc = (in_monto_diario / MONTO_TOTAL_PROYECTO) * 100 if MONTO_TOTAL_PROYECTO > 0 else 0
        col_av2.metric("11. Curva de Avance % (Diario)", f"{pct_diario_calc:.2f} %")

        # Calculo proyectado del acumulado para mostrar al usuario
        nuevo_acum_fin = prev_acum_financiero + in_monto_diario
        col_av3.metric("12. Avance Avaluado Acumulado ($)", f"$ {nuevo_acum_fin:,.2f}")

        st.markdown("**13. Avance prorrateado del proyecto por Hito**")
        ch1, ch2 = st.columns(2)
        in_hito_civil = ch1.number_input("Hito Civil (%)", min_value=0.0, max_value=100.0, step=0.1)
        in_hito_elec = ch2.number_input("Hito Eléctrico (%)", min_value=0.0, max_value=100.0, step=0.1)

        st.markdown("**14. Indicadores de Desempeño y estimaciones**")
        ci1, ci2 = st.columns(2)
        in_cpi = ci1.number_input("CPI (Costo Performance Index)", value=1.00, step=0.01)
        in_spi = ci2.number_input("SPI (Schedule Performance Index)", value=1.00, step=0.01)

        # 15. Simbología (Gráfico Pequeño de Referencia)
        st.markdown("**15. Curva de Avance – Valor Ganado (Referencia Visual)**")
        fig_ref = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = prev_acum_fisico + pct_diario_calc,
            title = {'text': "% Físico Acumulado"},
            gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#b91c1c"}}
        ))
        fig_ref.update_layout(height=150, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_ref, use_container_width=True)

        # --- BLOQUE 3: DETALLE DE CAMPO ---
        st.markdown('<div class="sub-header">C. Detalle Cualitativo</div>', unsafe_allow_html=True)
        
        in_activ = st.text_area("17. Actividades ejecutadas en el día", placeholder="- Excavación de plintos\n- Tendido de conductor...")
        in_obs_fis = st.text_area("16. Observaciones de fiscalización", placeholder="Sin novedades...")
        in_obs_gen = st.text_area("18. Observaciones Generales", placeholder="Material llegó a tiempo...")

        # --- BLOQUE 4: FOTOS Y FIRMAS ---
        st.markdown('<div class="sub-header">D. Cierre</div>', unsafe_allow_html=True)
        cf1, cf2 = st.columns(2)
        in_fotos = cf1.file_uploader("19. Registro fotográfico", accept_multiple_files=True)
        in_firmas = cf2.text_input("20. Firmas de responsabilidad", placeholder="Ing. Residente / Ing. Fiscalizador")

        # BOTÓN DE GUARDADO
        submitted = st.form_submit_button("💾 GUARDAR RDO")

        if submitted:
            if not in_dia or not in_activ or not in_firmas:
                st.error("⚠️ Faltan campos obligatorios (Día, Actividades o Firmas).")
            else:
                # Cálculos Finales
                pct_acum_final = prev_acum_fisico + pct_diario_calc
                if pct_acum_final > 100: pct_acum_final = 100.0
                
                fin_acum_final = prev_acum_financiero + in_monto_diario
                if fin_acum_final > MONTO_TOTAL_PROYECTO: fin_acum_final = MONTO_TOTAL_PROYECTO

                # Crear nuevo registro
                nuevo_registro = {
                    'Fecha': in_fecha,
                    'Día N': in_dia,
                    'Físico Diario (%)': pct_diario_calc,
                    'Inversión Diaria ($)': in_monto_diario,
                    'Físico Acum (%)': pct_acum_final,
                    'Financiero Acum ($)': fin_acum_final,
                    'Hito Civil (%)': in_hito_civil,
                    'Hito Eléctrico (%)': in_hito_elec,
                    'CPI': in_cpi,
                    'SPI': in_spi,
                    'Detalle': in_activ,
                    'Fotos': len(in_fotos) if in_fotos else 0
                }
                
                # Guardar en Session State
                st.session_state['data_fiscalpinas'] = pd.concat(
                    [df, pd.DataFrame([nuevo_registro])], ignore_index=True
                )
                st.success(f"✅ RDO del {in_dia} guardado correctamente.")

# ==============================================================================
# MÓDULO: DASHBOARD (Puntos 1 al 5)
# ==============================================================================
elif opcion == "DASHBOARD (Reporte)":
    st.markdown(f'<div class="main-header">DASHBOARD DE SEGUIMIENTO</div>', unsafe_allow_html=True)
    
    # CSS para impresión
    st.markdown("""
    <style>
    @media print {
        [data-testid="stSidebar"], .stButton, header, footer {display: none;}
        .block-container {padding-top: 0 !important;}
    }
    </style>
    """, unsafe_allow_html=True)

    df = st.session_state['data_fiscalpinas']

    # 1. FECHA DE EMISIÓN
    st.markdown(f"**1. Fecha de emisión:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.markdown("---")

    # 2. % DE AVANCE ACUMULADO POR COMPONENTES O HITOS
    st.markdown("### 2. % de Avance Acumulado (Tabla Detallada)")
    
    if len(df) > 1:
        ultimo = df.iloc[-1]
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Avance Físico Global", f"{ultimo['Físico Acum (%)']:.2f}%")
        col_m2.metric("Hito Civil", f"{ultimo['Hito Civil (%)']:.2f}%")
        col_m3.metric("Hito Eléctrico", f"{ultimo['Hito Eléctrico (%)']:.2f}%")
    else:
        st.info("No hay datos registrados aún.")

    st.dataframe(df[['Fecha', 'Día N', 'Físico Acum (%)', 'Financiero Acum ($)', 'CPI', 'SPI']].style.format({
        'Físico Acum (%)': "{:.2f}%",
        'Financiero Acum ($)': "$ {:,.2f}",
        'CPI': "{:.2f}",
        'SPI': "{:.2f}"
    }), use_container_width=True)

    st.markdown("---")

    # GRÁFICOS
    c_g1, c_g2 = st.columns(2)

    with c_g1:
        # 3. GRÁFICO DE RESUMEN DE AVANCE GLOBAL ACUMULADO
        st.subheader("3. Resumen Avance Global Acumulado")
        fig3 = px.area(df, x='Fecha', y='Físico Acum (%)', title="Curva S (Físico)", markers=True)
        fig3.update_traces(line_color='#1E3A8A', fill_color='rgba(30, 58, 138, 0.3)')
        st.plotly_chart(fig3, use_container_width=True)

    with c_g2:
        # 4. GRÁFICO DE AVANCE FÍSICO TOTAL POR MES
        st.subheader("4. Avance Físico Total por Mes")
        # Creamos una copia para manipular fechas
        df_mes = df.copy()
        df_mes['Fecha'] = pd.to_datetime(df_mes['Fecha'])
        df_mes['Mes'] = df_mes['Fecha'].dt.strftime('%Y-%m')
        # Agrupamos por mes sumando el avance del día
        df_agrupado = df_mes.groupby('Mes')['Físico Diario (%)'].sum().reset_index()
        
        fig4 = px.bar(df_agrupado, x='Mes', y='Físico Diario (%)', title="Producción Mensual (%)", text_auto='.2f')
        fig4.update_traces(marker_color='#b91c1c')
        st.plotly_chart(fig4, use_container_width=True)

    # 5. CURVA DE AVANCE DE OBRA – VALOR GANADO
    st.subheader("5. Curva de Avance de Obra – Valor Ganado ($)")
    fig5 = go.Figure()
    
    # Valor Ganado (EV) - Lo que realmente se ha hecho en dinero
    fig5.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Financiero Acum ($)'],
        mode='lines+markers', name='Valor Ganado (EV)',
        line=dict(color='green', width=3)
    ))
    
    # Línea de Presupuesto Total (Referencia)
    fig5.add_trace(go.Scatter(
        x=df['Fecha'], y=[MONTO_TOTAL_PROYECTO]*len(df),
        mode='lines', name='Presupuesto al finalizar (BAC)',
        line=dict(color='gray', dash='dash')
    ))

    fig5.update_layout(title="Análisis de Valor Ganado", yaxis_title="Monto USD ($)", legend=dict(x=0, y=1))
    st.plotly_chart(fig5, use_container_width=True)
