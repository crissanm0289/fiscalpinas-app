import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="SISTEMA DE GESTIÓN - FISCALPIÑAS", page_icon="⚡")

# --- VARIABLES DEL CONTRATO (ACTUALIZADAS) ---
MONTO_TOTAL_PROYECTO = 3899999.22
NOMBRE_FISCALIZADOR = "CONSORCIO FISCALPIÑAS"

# --- DATOS DE LA FICHA TÉCNICA ---
datos_ficha = {
    "Entidad": "CNEL EP - UNIDAD DE NEGOCIO EL ORO",
    "Categoría": "CONSTRUCCIÓN DE SUBESTACIONES ELÉCTRICAS DE ALTA Y EXTRA ALTA TENSIÓN",
    "Objeto": "EOR Construccion de la subestacion Pinas y su linea de subtransmision GD",
    "Código": "LICO-CNELEP-2025-1",
    "Plazo": "450 Días Calendario",
    "Contratista": "CONSORCIO PIÑAS INPI",
    "Rep_Legal": "PILEGGI CONSTRUCCIONES C.LTDA. (Procurador Común)",
    "Monto_Str": "$ 3,899,999.22",
    "Link": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/resumenAdjudicacion.cpe?solicitud=V_550at-6mzyMx9KwoPuuaByned8HAHsT3R-uscx9wE,"
}

# --- GESTIÓN DE MEMORIA (ESTADO) ---
if 'data_fiscalpinas' not in st.session_state:
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

def dibujar_ficha_tecnica():
    estilo_tabla = """
    <style>
        .ficha-tecnica {
            width: 100%; border-collapse: collapse; margin-bottom: 20px; 
            font-family: Arial, sans-serif; font-size: 13px; border: 1px solid #ddd;
        }
        .ficha-tecnica th {
            background-color: #1E3A8A; color: white; padding: 8px; 
            text-align: center; border: 1px solid #ddd; font-weight: bold;
        }
        .ficha-tecnica td {
            padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9; color: #333;
        }
        .label-cell { font-weight: bold; background-color: #eef2ff; width: 15%; }
    </style>
    """
    
    html_ficha = f"""
    {estilo_tabla}
    <table class="ficha-tecnica">
        <tr><th colspan="4">FICHA TÉCNICA DEL PROYECTO (CONTRATO DE OBRA)</th></tr>
        <tr>
            <td class="label-cell">Entidad:</td>
            <td width="35%">{datos_ficha['Entidad']}</td>
            <td class="label-cell">Categoría:</td>
            <td width="35%">{datos_ficha['Categoría']}</td>
        </tr>
        <tr>
            <td class="label-cell">Objeto:</td>
            <td colspan="3">{datos_ficha['Objeto']}</td>
        </tr>
        <tr>
            <td class="label-cell">Código:</td>
            <td>{datos_ficha['Código']}</td>
            <td class="label-cell">Plazo:</td>
            <td>{datos_ficha['Plazo']}</td>
        </tr>
        <tr>
            <td class="label-cell">Contratista:</td>
            <td>{datos_ficha['Contratista']}</td>
            <td class="label-cell">Rep. Legal:</td>
            <td>{datos_ficha['Rep_Legal']}</td>
        </tr>
        <tr>
            <td class="label-cell">Monto:</td>
            <td style="font-weight:bold; color:#b91c1c;">{datos_ficha['Monto_Str']}</td>
            <td class="label-cell">Enlace:</td>
            <td><a href="{datos_ficha['Link']}" target="_blank">Ver en SERCOP</a></td>
        </tr>
    </table>
    """
    st.markdown(html_ficha, unsafe_allow_html=True)

# --- ESTILOS CSS GENERALES ---
st.markdown("""
<style>
    .main-header {font-size: 24px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px;}
    .sub-header {font-size: 18px; font-weight: bold; color: #b91c1c; margin-top: 15px; border-bottom: 1px solid #ccc;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Logotipo_de_CNEL.svg", width=140)
st.sidebar.title("MENÚ DE CONTROL")
st.sidebar.info(f"**Fiscalización:**\n{NOMBRE_FISCALIZADOR}")

opcion = st.sidebar.radio("Navegación:", ["MÓDULO 1: RDO (Ingreso)", "MÓDULO 2: DASHBOARD (Reporte)"])

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ RESETEAR DATOS"):
    reset_app()

# ==============================================================================
# MÓDULO 1: RDO
# ==============================================================================
if opcion == "MÓDULO 1: RDO (Ingreso)":
    st.markdown('<div class="main-header">MÓDULO 1: REGISTRO DIARIO DE OBRA (RDO)</div>', unsafe_allow_html=True)
    
    # DIBUJAR FICHA TÉCNICA
    dibujar_ficha_tecnica()
    
    df = st.session_state['data_fiscalpinas']
    ultimo = df.iloc[-1]
    prev_acum_fisico = ultimo['Físico Acum (%)']
    prev_acum_financiero = ultimo['Financiero Acum ($)']

    with st.form("formulario_rdo"):
        st.markdown('<div class="sub-header">A. Datos Generales</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        in_fecha = c1.date_input("1. Fechas de Ejecución", date.today())
        in_dia = c2.text_input("9. Día de ejecución", placeholder="Ej: Día 120")
        in_clima = c3.selectbox("10. Condiciones climáticas", ["Soleado", "Nublado", "Lluvia", "Tormenta"])

        c4, c5 = st.columns(2)
        c4.text_input("7. Datos Económicos del Contrato (Fiscalización)", "Variable según contrato", disabled=True)
        c5.text_input("8. Dato Económico total del Proyecto (Obra)", datos_ficha['Monto_Str'], disabled=True)

        st.markdown('<div class="sub-header">B. Control de Avance</div>', unsafe_allow_html=True)
        
        col_av1, col_av2, col_av3 = st.columns(3)
        in_monto_diario = col_av1.number_input("11. $ de Avance DEL DÍA (Inversión)", min_value=0.0, step=1000.0)
        
        # Cálculos automáticos visuales
        pct_diario_calc = (in_monto_diario / MONTO_TOTAL_PROYECTO) * 100
        nuevo_acum_fin = prev_acum_financiero + in_monto_diario
        
        col_av2.metric("11. Curva de Avance % (Diario)", f"{pct_diario_calc:.4f} %")
        col_av3.metric("12. Avance Avaluado Acumulado ($)", f"$ {nuevo_acum_fin:,.2f}")

        st.markdown("**13. Avance prorrateado del proyecto por Hito**")
        ch1, ch2 = st.columns(2)
        in_hito_civil = ch1.number_input("Hito Civil (%)", min_value=0.0, max_value=100.0, step=0.01)
        in_hito_elec = ch2.number_input("Hito Eléctrico (%)", min_value=0.0, max_value=100.0, step=0.01)

        st.markdown("**14. Indicadores de Desempeño y estimaciones**")
        ci1, ci2 = st.columns(2)
        in_cpi = ci1.number_input("CPI (Costo)", value=1.00, step=0.01)
        in_spi = ci2.number_input("SPI (Cronograma)", value=1.00, step=0.01)

        st.markdown("**15. Curva de Avance – Simbología (Ref.)**")
        st.progress(min(int(prev_acum_fisico + pct_diario_calc), 100))

        st.markdown('<div class="sub-header">C. Detalle de Campo</div>', unsafe_allow_html=True)
        in_activ = st.text_area("17. Actividades ejecutadas en el día", height=100)
        in_obs_fis = st.text_area("16. Observaciones de fiscalización", height=70)
        in_obs_gen = st.text_area("18. Observaciones Generales", height=70)

        st.markdown('<div class="sub-header">D. Cierre</div>', unsafe_allow_html=True)
        cf1, cf2 = st.columns(2)
        in_fotos = cf1.file_uploader("19. Registro fotográfico", accept_multiple_files=True)
        in_firmas = cf2.text_input("20. Firmas de responsabilidad")

        submitted = st.form_submit_button("💾 GUARDAR REGISTRO")

        if submitted:
            if not in_dia or not in_activ or not in_firmas:
                st.error("⚠️ Complete Día, Actividades y Firmas.")
            else:
                pct_acum_final = prev_acum_fisico + pct_diario_calc
                fin_acum_final = prev_acum_financiero + in_monto_diario
                
                # Tope lógico
                if fin_acum_final > MONTO_TOTAL_PROYECTO: fin_acum_final = MONTO_TOTAL_PROYECTO
                if pct_acum_final > 100.0: pct_acum_final = 100.0

                nuevo_registro = {
                    'Fecha': in_fecha, 'Día N': in_dia,
                    'Físico Diario (%)': pct_diario_calc, 'Inversión Diaria ($)': in_monto_diario,
                    'Físico Acum (%)': pct_acum_final, 'Financiero Acum ($)': fin_acum_final,
                    'Hito Civil (%)': in_hito_civil, 'Hito Eléctrico (%)': in_hito_elec,
                    'CPI': in_cpi, 'SPI': in_spi,
                    'Detalle': in_activ, 'Fotos': len(in_fotos) if in_fotos else 0
                }
                
                st.session_state['data_fiscalpinas'] = pd.concat(
                    [df, pd.DataFrame([nuevo_registro])], ignore_index=True
                )
                st.success("✅ RDO Guardado Exitosamente.")

# ==============================================================================
# MÓDULO 2: DASHBOARD
# ==============================================================================
elif opcion == "MÓDULO 2: DASHBOARD (Reporte)":
    st.markdown('<div class="main-header">MÓDULO 2: DASHBOARD DE DESEMPEÑO</div>', unsafe_allow_html=True)
    
    # Estilo para ocultar cosas al imprimir
    st.markdown("""<style>@media print {[data-testid="stSidebar"], .stButton, header, footer {display: none;}}</style>""", unsafe_allow_html=True)

    # DIBUJAR FICHA TÉCNICA
    dibujar_ficha_tecnica()
    
    df = st.session_state['data_fiscalpinas']
    
    st.markdown(f"**1. Fecha de emisión:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.markdown("---")

    # 2. TABLA DETALLADA
    st.subheader("2. % de Avance Acumulado (Tabla)")
    st.dataframe(df[['Fecha', 'Día N', 'Físico Acum (%)', 'Financiero Acum ($)', 'CPI', 'SPI']].style.format({
        'Físico Acum (%)': "{:.4f}%", 'Financiero Acum ($)': "$ {:,.2f}", 'CPI': "{:.2f}", 'SPI': "{:.2f}"
    }), use_container_width=True)

    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("3. Resumen Avance Global Acumulado")
        fig3 = px.area(df, x='Fecha', y='Físico Acum (%)', title="Curva 'S' Física")
        fig3.update_traces(line_color='#1E3A8A')
        st.plotly_chart(fig3, use_container_width=True)
        
        st.subheader("5. Curva Avance de Obra - Valor Ganado ($)")
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=df['Fecha'], y=df['Financiero Acum ($)'], name='Valor Ganado (EV)', line=dict(color='green', width=3)))
        fig5.add_trace(go.Scatter(x=df['Fecha'], y=[MONTO_TOTAL_PROYECTO]*len(df), name='Presupuesto (BAC)', line=dict(dash='dash', color='red')))
        st.plotly_chart(fig5, use_container_width=True)

    with c2:
        st.subheader("4. Avance Físico Total por Mes")
        # Agrupación Mensual
        df_copia = df.copy()
        df_copia['Mes'] = pd.to_datetime(df_copia['Fecha']).dt.strftime('%Y-%m')
        df_agrupado = df_copia.groupby('Mes')['Físico Diario (%)'].sum().reset_index()
        
        fig4 = px.bar(df_agrupado, x='Mes', y='Físico Diario (%)', title="Producción Mensual (%)", text_auto='.2f')
        fig4.update_traces(marker_color='#b91c1c')
        st.plotly_chart(fig4, use_container_width=True)
