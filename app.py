import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="FISCALPIÑAS - SISTEMA INTEGRAL", page_icon="⚡")

# --- VARIABLES DEL CONTRATO ---
MONTO_TOTAL_PROYECTO = 3899999.22
NOMBRE_FISCALIZADOR = "CONSORCIO FISCALPIÑAS"

# --- DATOS FICHA TÉCNICA ---
datos_ficha = {
    "Entidad": "CNEL EP - UNIDAD DE NEGOCIO EL ORO",
    "Categoría": "CONSTRUCCIÓN DE SUBESTACIONES ELÉCTRICAS",
    "Objeto": "EOR Construccion de la subestacion Pinas y su linea de subtransmision GD",
    "Código": "LICO-CNELEP-2025-1",
    "Plazo": "450 Días Calendario",
    "Contratista": "CONSORCIO PIÑAS INPI",
    "Rep_Legal": "PILEGGI CONSTRUCCIONES C.LTDA.",
    "Monto_Str": "$ 3,899,999.22",
    "Link": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/resumenAdjudicacion.cpe?solicitud=V_550at-6mzyMx9KwoPuuaByned8HAHsT3R-uscx9wE,"
}

# --- GESTIÓN DE MEMORIA (DATAFRAME EXPANDIDO) ---
if 'data_fiscalpinas' not in st.session_state:
    # Columnas nuevas añadidas para cumplir requerimientos
    st.session_state['data_fiscalpinas'] = pd.DataFrame({
        'Fecha': [date(2025, 1, 1)],
        'Día N': ['Inicio'],
        'Físico Diario (%)': [0.0],
        'Inversión Diaria ($)': [0.0],
        'Físico Acum (%)': [0.0],
        'Financiero Acum ($)': [0.0],
        'Hito Civil (%)': [0.0],
        'Hito Eléctrico (%)': [0.0],
        'Horas Hombre': [0.0],          # Nuevo
        'Personal Detalle': ['Inicio'], # Nuevo
        'Incidentes': ['Sin Novedad'],  # Nuevo
        'Contratos Comp': ['Ninguno'],  # Nuevo
        'Ordenes Trabajo': ['Ninguna'], # Nuevo
        'Incremento Cant': ['0.00'],    # Nuevo
        'Control Cantidades': ['SI'],   # Nuevo
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
        .ficha-tecnica {width: 100%; border-collapse: collapse; margin-bottom: 20px; font-family: Arial, sans-serif; font-size: 13px; border: 1px solid #ddd;}
        .ficha-tecnica th {background-color: #1E3A8A; color: white; padding: 8px; text-align: center; border: 1px solid #ddd;}
        .ficha-tecnica td {padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9; color: #333;}
        .label-cell {font-weight: bold; background-color: #eef2ff; width: 15%;}
    </style>
    """
    html_ficha = f"""
    {estilo_tabla}
    <table class="ficha-tecnica">
        <tr><th colspan="4">FICHA TÉCNICA DEL PROYECTO (CONTRATO DE OBRA)</th></tr>
        <tr>
            <td class="label-cell">Entidad:</td><td width="35%">{datos_ficha['Entidad']}</td>
            <td class="label-cell">Categoría:</td><td width="35%">{datos_ficha['Categoría']}</td>
        </tr>
        <tr><td class="label-cell">Objeto:</td><td colspan="3">{datos_ficha['Objeto']}</td></tr>
        <tr>
            <td class="label-cell">Código:</td><td>{datos_ficha['Código']}</td>
            <td class="label-cell">Plazo:</td><td>{datos_ficha['Plazo']}</td>
        </tr>
        <tr>
            <td class="label-cell">Contratista:</td><td>{datos_ficha['Contratista']}</td>
            <td class="label-cell">Rep. Legal:</td><td>{datos_ficha['Rep_Legal']}</td>
        </tr>
        <tr>
            <td class="label-cell">Monto:</td><td style="font-weight:bold; color:#b91c1c;">{datos_ficha['Monto_Str']}</td>
            <td class="label-cell">Enlace:</td><td><a href="{datos_ficha['Link']}" target="_blank">Ver en SERCOP</a></td>
        </tr>
    </table>
    """
    st.markdown(html_ficha, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Logotipo_de_CNEL.svg", width=140)
st.sidebar.title("CONTROL DE OBRA")
opcion = st.sidebar.radio("Navegación:", ["MÓDULO 1: RDO (Ingreso)", "MÓDULO 2: DASHBOARD (Reporte)"])
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ BORRAR TODO"): reset_app()

# ==============================================================================
# MÓDULO 1: RDO (INGRESO DE DATOS)
# ==============================================================================
if opcion == "MÓDULO 1: RDO (Ingreso)":
    st.markdown("### MÓDULO 1: REGISTRO DIARIO DE OBRA (RDO)")
    dibujar_ficha_tecnica()
    
    df = st.session_state['data_fiscalpinas']
    ultimo = df.iloc[-1]
    prev_acum_fin = ultimo['Financiero Acum ($)']
    prev_acum_fis = ultimo['Físico Acum (%)']

    with st.form("formulario_rdo"):
        # --- SECCIÓN A: GENERALES ---
        st.info("A. Datos Generales y Económicos")
        c1, c2, c3 = st.columns(3)
        in_fecha = c1.date_input("1. Fecha de Emisión", date.today())
        in_dia = c2.text_input("9. Día de ejecución", placeholder="Ej: Día 12")
        in_clima = c3.selectbox("10. Condiciones climáticas", ["Soleado", "Nublado", "Lluvia", "Tormenta"])

        c4, c5 = st.columns(2)
        c4.text_input("7. Datos Económicos del Contrato", "Fiscalización (Variable)", disabled=True)
        c5.text_input("8. Dato Económico total del Proyecto", datos_ficha['Monto_Str'], disabled=True)

        # --- SECCIÓN B: AVANCE (CORREGIDO PUNTOS 11 y 15) ---
        st.info("B. Control de Avance y Valor Ganado")
        
        # PUNTO 11: INPUT
        col_m1, col_m2 = st.columns(2)
        in_monto_diario = col_m1.number_input("11. Curva de Avance $ ($ de Avance del día)", min_value=0.0, step=1000.0)
        
        # CÁLCULOS
        pct_diario = (in_monto_diario / MONTO_TOTAL_PROYECTO) * 100
        nuevo_acum_fin = prev_acum_fin + in_monto_diario
        nuevo_acum_fis = prev_acum_fis + pct_diario
        if nuevo_acum_fis > 100: nuevo_acum_fis = 100.0

        col_m2.metric("Avance Acumulado Proyectado", f"{nuevo_acum_fis:.4f} %", f"$ {nuevo_acum_fin:,.2f}")

        # PUNTO 15: SIMBOLOGÍA VISUAL
        st.markdown("**15. Curva de Avance – Valor Ganado – Simbología**")
        st.caption("Referencia visual del estado actual:")
        leyenda_col1, leyenda_col2, leyenda_col3 = st.columns(3)
        leyenda_col1.markdown("🟦 **Planificado (PV)**: Línea Base")
        leyenda_col2.markdown("🟩 **Ejecutado (EV)**: Valor Ganado Real")
        leyenda_col3.markdown("🟥 **Costo Real (AC)**: Gasto Realizado")
        st.progress(int(nuevo_acum_fis))

        # OTROS INDICADORES DE AVANCE
        st.markdown("**13. Avance prorrateado por Hito**")
        ch1, ch2 = st.columns(2)
        in_hito_civ = ch1.number_input("Hito Civil (%)", 0.0, 100.0, step=0.01)
        in_hito_ele = ch2.number_input("Hito Eléctrico (%)", 0.0, 100.0, step=0.01)

        # --- SECCIÓN C: ADMINISTRATIVO Y RECURSOS (NUEVOS CAMPOS) ---
        st.info("C. Recursos, Seguridad y Administrativo")
        
        col_rec1, col_rec2, col_rec3 = st.columns(3)
        in_hh = col_rec1.number_input("Reg. Horas Hombre (Diario)", min_value=0.0, step=1.0)
        in_incidente = col_rec2.selectbox("Reg. de Incidentes", ["Sin Novedad", "Incidente Leve", "Accidente con Baja", "Daño Material"])
        in_control = col_rec3.selectbox("Control Tabla de Cantidades", ["SI - Verificado", "NO - Pendiente", "Con Observaciones"])

        in_personal = st.text_area("Personal y Equipos (Detalle)", placeholder="Ej: 1 Ing. Residente, 5 Linieros, 1 Grúa...", height=70)

        # CAMPOS ADMINISTRATIVOS
        ca1, ca2, ca3 = st.columns(3)
        in_contratos_comp = ca1.text_input("Reg. Contratos Complementarios", "Ninguno")
        in_ordenes = ca2.text_input("Reg. Órdenes de Trabajo", "Ninguna")
        in_incremento = ca3.text_input("Reg. Incremento Cantidades", "0.00 %")

        # --- SECCIÓN D: DETALLE Y CIERRE ---
        st.info("D. Detalle Cualitativo y Firmas")
        col_ind1, col_ind2 = st.columns(2)
        in_cpi = col_ind1.number_input("14. CPI (Costo)", 1.00)
        in_spi = col_ind2.number_input("14. SPI (Cronograma)", 1.00)
        
        st.text_input("Porcentaje total del proyecto (Calculado)", f"{nuevo_acum_fis:.4f}%", disabled=True)

        in_actividades = st.text_area("17. Actividades ejecutadas", height=80)
        in_obs_fis = st.text_area("16. Observaciones Fiscalización", height=60)
        in_obs_gen = st.text_area("18. Observaciones Generales", height=60)
        
        cf1, cf2 = st.columns(2)
        in_fotos = cf1.file_uploader("19. Registro Fotográfico", accept_multiple_files=True)
        in_firmas = cf2.text_input("20. Firmas de Responsabilidad")

        if st.form_submit_button("💾 GUARDAR RDO DIARIO"):
            if not in_dia or not in_actividades or not in_firmas:
                st.error("⚠️ Faltan campos obligatorios.")
            else:
                nuevo_reg = {
                    'Fecha': in_fecha, 'Día N': in_dia,
                    'Físico Diario (%)': pct_diario, 'Inversión Diaria ($)': in_monto_diario,
                    'Físico Acum (%)': nuevo_acum_fis, 'Financiero Acum ($)': nuevo_acum_fin,
                    'Hito Civil (%)': in_hito_civ, 'Hito Eléctrico (%)': in_hito_ele,
                    'Horas Hombre': in_hh, 'Personal Detalle': in_personal,
                    'Incidentes': in_incidente, 'Contratos Comp': in_contratos_comp,
                    'Ordenes Trabajo': in_ordenes, 'Incremento Cant': in_incremento,
                    'Control Cantidades': in_control, 'CPI': in_cpi, 'SPI': in_spi,
                    'Detalle': in_actividades, 'Fotos': len(in_fotos) if in_fotos else 0
                }
                st.session_state['data_fiscalpinas'] = pd.concat([df, pd.DataFrame([nuevo_reg])], ignore_index=True)
                st.success("✅ RDO GUARDADO CORRECTAMENTE")

# ==============================================================================
# MÓDULO 2: DASHBOARD
# ==============================================================================
elif opcion == "MÓDULO 2: DASHBOARD (Reporte)":
    st.markdown("### MÓDULO 2: DASHBOARD DE SEGUIMIENTO Y CONTROL")
    st.markdown("""<style>@media print {[data-testid="stSidebar"], header, footer, .stButton {display: none;}}</style>""", unsafe_allow_html=True)
    
    dibujar_ficha_tecnica()
    df = st.session_state['data_fiscalpinas']
    
    if len(df) > 1:
        df_real = df.iloc[1:].copy() # Ignoramos fila de inicio para gráficas
    else:
        df_real = df.copy()

    st.markdown(f"**Fecha de Emisión:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # 2. TABLA RESUMEN (% Avance Acumulado)
    st.subheader("2. Resumen de Avance Acumulado")
    cols_view = ['Fecha', 'Día N', 'Físico Acum (%)', 'Financiero Acum ($)', 'Horas Hombre', 'Incidentes']
    st.dataframe(df[cols_view].style.format({
        'Físico Acum (%)': "{:.3f}%", 
        'Financiero Acum ($)': "$ {:,.2f}",
        'Horas Hombre': "{:.1f}"
    }), use_container_width=True, height=200)

    st.markdown("---")
    
    # --- FILA 1 DE GRÁFICOS ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**3. Gráfico de Avance de Pagos (Acumulado $)**")
        fig_pagos = px.area(df, x='Fecha', y='Financiero Acum ($)', markers=True)
        fig_pagos.update_traces(line_color='green', fill_color='rgba(0,128,0,0.2)')
        st.plotly_chart(fig_pagos, use_container_width=True)

    with c2:
        st.markdown("**4. Gráfico de Avance Porcentual vs USD (Doble Eje)**")
        fig_dual = go.Figure()
        fig_dual.add_trace(go.Bar(x=df['Fecha'], y=df['Inversión Diaria ($)'], name='Inversión ($)', marker_color='#90cdf4'))
        fig_dual.add_trace(go.Scatter(x=df['Fecha'], y=df['Físico Acum (%)'], name='% Acumulado', yaxis='y2', line=dict(color='#b91c1c', width=3)))
        fig_dual.update_layout(
            yaxis=dict(title="Inversión Diaria USD"),
            yaxis2=dict(title="% Avance Acumulado", overlaying='y', side='right'),
            legend=dict(x=0, y=1.1, orientation='h')
        )
        st.plotly_chart(fig_dual, use_container_width=True)

    # --- FILA 2 DE GRÁFICOS ---
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**5. Pagos Mensuales y Devengo de Anticipo**")
        # Procesar datos mensuales
        df_real['Mes'] = pd.to_datetime(df_real['Fecha']).dt.strftime('%Y-%m')
        df_mes = df_real.groupby('Mes')['Inversión Diaria ($)'].sum().reset_index()
        
        fig_mes = px.bar(df_mes, x='Mes', y='Inversión Diaria ($)', text_auto='.2s', title="Planillado Mensual")
        fig_mes.add_hline(y=df_mes['Inversión Diaria ($)'].mean(), line_dash="dot", annotation_text="Promedio")
        st.plotly_chart(fig_mes, use_container_width=True)

    with c4:
        st.markdown("**6. Horas Hombre y Equipos (Acumulado)**")
        fig_hh = px.line(df, x='Fecha', y='Horas Hombre', markers=True, title="Recurso Humano Diario")
        # Simular acumulación para la visualización
        df['HH_Acum'] = df['Horas Hombre'].cumsum()
        fig_hh.add_trace(go.Scatter(x=df['Fecha'], y=df['HH_Acum'], name='HH Acumuladas', fill='tozeroy', line=dict(dash='dot')))
        st.plotly_chart(fig_hh, use_container_width=True)

    # --- FILA 3 DE GRÁFICOS ---
    c5, c6 = st.columns(2)
    with c5:
        st.markdown("**7. Frecuencia de Incidentes/Accidentes**")
        conteo_inc = df_real['Incidentes'].value_counts().reset_index()
        conteo_inc.columns = ['Tipo', 'Cantidad']
        fig_seg = px.pie(conteo_inc, values='Cantidad', names='Tipo', hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_seg, use_container_width=True)

    with c6:
        st.markdown("**8. Estado de Contratos y Órdenes**")
        st.info(f"**Contratos Complementarios:** {ultimo['Contratos Comp']}")
        st.info(f"**Órdenes de Trabajo:** {ultimo['Ordenes Trabajo']}")
        st.warning(f"**Incremento de Cantidades:** {ultimo['Incremento Cant']}")
