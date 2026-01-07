import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="FISCALPIÑAS - GESTIÓN INTEGRAL", page_icon="⚡")

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

# --- GESTIÓN DE MEMORIA (BASES DE DATOS) ---
# 1. Base RDO (Registro Diario)
if 'data_fiscalpinas' not in st.session_state:
    st.session_state['data_fiscalpinas'] = pd.DataFrame({
        'Fecha': [date(2025, 1, 1)], 'Día N': ['Inicio'],
        'Físico Diario (%)': [0.0], 'Inversión Diaria ($)': [0.0],
        'Físico Acum (%)': [0.0], 'Financiero Acum ($)': [0.0],
        'Hito Civil (%)': [0.0], 'Hito Eléctrico (%)': [0.0],
        'Horas Hombre': [0.0], 'Personal Detalle': ['Inicio'],
        'Incidentes': ['Sin Novedad'], 'Contratos Comp': ['Ninguno'],
        'Ordenes Trabajo': ['Ninguna'], 'Incremento Cant': ['0.00'],
        'Control Cantidades': ['SI'], 'CPI': [1.0], 'SPI': [1.0],
        'Detalle': ['Inicio de Contrato'], 'Fotos': [0]
    })

# 2. Base LDO (Días Libres)
if 'data_ldo' not in st.session_state:
    st.session_state['data_ldo'] = pd.DataFrame(columns=[
        'Funcionario', 'Cargo', 'Fecha Salida', 'Fecha Retorno', 
        'Días Totales', 'Reemplazo', 'Tipo', 'Estado'
    ])

# 3. Base Reportes de Gestión
if 'data_reportes' not in st.session_state:
    st.session_state['data_reportes'] = pd.DataFrame(columns=[
        'Periodo', 'Tipo', 'Hitos', 'Alertas', 'Fecha Emisión', 'Archivo'
    ])

# 4. Base LP (Libro de Pedidos)
if 'data_lp' not in st.session_state:
    st.session_state['data_lp'] = pd.DataFrame(columns=[
        'Folio', 'Fecha', 'Asunto', 'Instrucción', 
        'Ref. Técnica', 'Plazo', 'Estado'
    ])

# --- FUNCIONES AUXILIARES ---
def reset_app():
    keys = ['data_fiscalpinas', 'data_ldo', 'data_reportes', 'data_lp']
    for k in keys:
        if k in st.session_state: del st.session_state[k]
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
st.sidebar.title("SISTEMA FISCALPIÑAS")

menu = st.sidebar.radio(
    "Navegación:", 
    [
        "1. DASHBOARD (Gerencial)", 
        "2. RDO (Registro Diario)", 
        "3. LDO (Días Libres)", 
        "4. REPORTES DE GESTIÓN", 
        "5. LIBRO DE PEDIDO (LP)"
    ]
)

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ RESETEAR SISTEMA"): reset_app()

# ==============================================================================
# MÓDULO 1: DASHBOARD
# ==============================================================================
if menu == "1. DASHBOARD (Gerencial)":
    st.markdown("### 📊 DASHBOARD DE DESEMPEÑO DEL PROYECTO")
    dibujar_ficha_tecnica()
    
    df = st.session_state['data_fiscalpinas']
    ultimo = df.iloc[-1]
    
    # Filtrar datos reales (sin fila de inicio)
    if len(df) > 1: df_real = df.iloc[1:].copy()
    else: df_real = df.copy()

    st.markdown(f"**Corte de Información:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # KPIs Principales
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Avance Físico", f"{ultimo['Físico Acum (%)']:.2f}%", delta_color="normal")
    k2.metric("Inversión Acumulada", f"$ {ultimo['Financiero Acum ($)']:,.0f}")
    k3.metric("SPI (Cronograma)", f"{ultimo['SPI']:.2f}", delta=f"{ultimo['SPI']-1:.2f}")
    k4.metric("CPI (Costo)", f"{ultimo['CPI']:.2f}", delta=f"{ultimo['CPI']-1:.2f}")

    st.markdown("---") 

    # --- FILA 1: CURVAS S ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Avance Global Acumulado (Curva S)")
        fig_global = px.area(df, x='Fecha', y='Físico Acum (%)')
        fig_global.update_traces(line_color='#1E3A8A', fillcolor='rgba(30, 58, 138, 0.3)')
        st.plotly_chart(fig_global, use_container_width=True)
    
    with c2:
        st.subheader("Valor Ganado vs Presupuesto")
        fig_ev = go.Figure()
        fig_ev.add_trace(go.Scatter(x=df['Fecha'], y=df['Financiero Acum ($)'], name='Valor Ganado (EV)', line=dict(color='green', width=3)))
        fig_ev.add_trace(go.Scatter(x=df['Fecha'], y=[MONTO_TOTAL_PROYECTO]*len(df), name='BAC (Presupuesto)', line=dict(dash='dash', color='red')))
        st.plotly_chart(fig_ev, use_container_width=True)

    st.markdown("---") 

    # --- FILA 2: PRODUCCIÓN ---
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Producción Física Mensual (%)")
        df_real['Mes'] = pd.to_datetime(df_real['Fecha']).dt.strftime('%Y-%m')
        df_mes_fis = df_real.groupby('Mes')['Físico Diario (%)'].sum().reset_index()
        fig_mes_fis = px.bar(df_mes_fis, x='Mes', y='Físico Diario (%)', text_auto='.2f')
        fig_mes_fis.update_traces(marker_color='#b91c1c')
        st.plotly_chart(fig_mes_fis, use_container_width=True)

    with c4:
        st.subheader("Pagos/Planillaje Mensual ($)")
        df_mes_din = df_real.groupby('Mes')['Inversión Diaria ($)'].sum().reset_index()
        fig_mes_din = px.bar(df_mes_din, x='Mes', y='Inversión Diaria ($)', text_auto='.2s')
        st.plotly_chart(fig_mes_din, use_container_width=True)

    st.markdown("---")
    
    # --- ESTADO ADMINISTRATIVO ---
    st.subheader("Estado Administrativo y Legal")
    col_adm1, col_adm2, col_adm3 = st.columns(3)
    col_adm1.info(f"📋 **Contratos Complementarios:**\n{ultimo['Contratos Comp']}")
    col_adm2.info(f"🛠️ **Órdenes de Trabajo:**\n{ultimo['Ordenes Trabajo']}")
    col_adm3.warning(f"📈 **Incremento de Cantidades:**\n{ultimo['Incremento Cant']}")

# ==============================================================================
# MÓDULO 2: RDO
# ==============================================================================
elif menu == "2. RDO (Registro Diario)":
    st.markdown("### 📝 REGISTRO DIARIO DE OBRA (RDO)")
    dibujar_ficha_tecnica()
    
    df = st.session_state['data_fiscalpinas']
    ultimo = df.iloc[-1]
    
    with st.form("rdo_form"):
        st.markdown("**A. Datos del Día**")
        c1, c2, c3 = st.columns(3)
        in_fecha = c1.date_input("Fecha", date.today())
        in_dia = c2.text_input("Día Ejecución (Ej: Día 45)")
        in_clima = c3.selectbox("Clima", ["Soleado", "Nublado", "Lluvia"])

        st.markdown("**B. Avances**")
        m1, m2 = st.columns(2)
        in_monto = m1.number_input("Inversión del Día ($)", min_value=0.0, step=100.0)
        pct_dia = (in_monto / MONTO_TOTAL_PROYECTO) * 100
        m2.metric("Avance Físico del Día", f"{pct_dia:.4f}%")
        
        st.markdown("**C. Hitos**")
        h1, h2 = st.columns(2)
        in_hc = h1.number_input("% Hito Civil", 0.0, 100.0)
        in_he = h2.number_input("% Hito Eléctrico", 0.0, 100.0)

        st.markdown("**D. Recursos y Seguridad**")
        r1, r2, r3 = st.columns(3)
        in_hh = r1.number_input("Horas Hombre", min_value=0.0)
        in_inc = r2.selectbox("Incidentes", ["Sin Novedad", "Leve", "Grave"])
        in_cont = r3.selectbox("Control Cantidades", ["SI", "NO"])
        
        st.markdown("**E. Administrativo**")
        a1, a2, a3 = st.columns(3)
        in_cc = a1.text_input("Cont. Complementarios", "Ninguno")
        in_ot = a2.text_input("Órdenes Trabajo", "Ninguna")
        in_ic = a3.text_input("Incr. Cantidades", "0.00%")

        st.markdown("**F. Detalles**")
        in_det = st.text_area("Actividades Ejecutadas")
        
        if st.form_submit_button("💾 GUARDAR RDO"):
            nuevo_fis = ultimo['Físico Acum (%)'] + pct_dia
            nuevo_fin = ultimo['Financiero Acum ($)'] + in_monto
            
            nuevo = {
                'Fecha': in_fecha, 'Día N': in_dia,
                'Físico Diario (%)': pct_dia, 'Inversión Diaria ($)': in_monto,
                'Físico Acum (%)': min(nuevo_fis, 100.0), 'Financiero Acum ($)': min(nuevo_fin, MONTO_TOTAL_PROYECTO),
                'Hito Civil (%)': in_hc, 'Hito Eléctrico (%)': in_he,
                'Horas Hombre': in_hh, 'Incidentes': in_inc, 'Control Cantidades': in_cont,
                'Contratos Comp': in_cc, 'Ordenes Trabajo': in_ot, 'Incremento Cant': in_ic,
                'Detalle': in_det, 'CPI': 1.0, 'SPI': 1.0, 'Personal Detalle': '', 'Fotos': 0
            }
            st.session_state['data_fiscalpinas'] = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            st.success("Registro guardado.")

# ==============================================================================
# MÓDULO 3: LDO (DÍAS LIBRES)
# ==============================================================================
elif menu == "3. LDO (Días Libres)":
    st.markdown("### 🗓️ GESTIÓN DE DÍAS LIBRES (LDO/DRO)")
    st.info("Control de turnos, bajadas de campo y reemplazos del personal de fiscalización.")
    
    col_form, col_tabla = st.columns([1, 2])
    
    with col_form:
        st.markdown("#### Nuevo Registro")
        with st.form("ldo_form"):
            ldo_func = st.text_input("Funcionario")
            ldo_cargo = st.selectbox("Cargo", ["Director", "Residente", "Especialista Elec.", "Especialista Civil", "Ambiental", "SISO"])
            ldo_inicio = st.date_input("Fecha Salida")
            ldo_fin = st.date_input("Fecha Retorno")
            ldo_reemplazo = st.text_input("Reemplazo Designado (Obligatorio)")
            ldo_tipo = st.selectbox("Motivo", ["Franco/Descanso", "Vacaciones", "Permiso Médico", "Calamidad"])
            ldo_estado = st.selectbox("Estado", ["Solicitado", "Aprobado", "Ejecutado"])
            
            if st.form_submit_button("Agendar LDO"):
                dias = (ldo_fin - ldo_inicio).days
                nuevo_ldo = {
                    'Funcionario': ldo_func, 'Cargo': ldo_cargo,
                    'Fecha Salida': ldo_inicio, 'Fecha Retorno': ldo_fin,
                    'Días Totales': dias, 'Reemplazo': ldo_reemplazo,
                    'Tipo': ldo_tipo, 'Estado': ldo_estado
                }
                st.session_state['data_ldo'] = pd.concat([st.session_state['data_ldo'], pd.DataFrame([nuevo_ldo])], ignore_index=True)
                st.success("Agendado.")

    with col_tabla:
        st.markdown("#### Calendario de Ausencias")
        if not st.session_state['data_ldo'].empty:
            st.dataframe(st.session_state['data_ldo'], use_container_width=True)
        else:
            st.info("No hay días libres programados.")

# ==============================================================================
# MÓDULO 4: REPORTES DE GESTIÓN
# ==============================================================================
elif menu == "4. REPORTES DE GESTIÓN":
    st.markdown("### 📑 REPORTES EJECUTIVOS")
    st.caption("Repositorio de informes semanales y mensuales enviados a la Entidad Contratante.")
    
    c_r1, c_r2 = st.columns([1, 2])
    
    with c_r1:
        with st.form("reporte_form"):
            rep_periodo = st.text_input("Periodo (Ej: Enero 2026)")
            rep_tipo = st.selectbox("Tipo", ["Informe Semanal", "Informe Mensual", "Informe Especial"])
            rep_hitos = st.text_area("Hitos Principales")
            rep_alertas = st.text_area("Alertas / Riesgos")
            rep_file = st.file_uploader("Cargar PDF Firmado")
            
            if st.form_submit_button("Subir Reporte"):
                nuevo_rep = {
                    'Periodo': rep_periodo, 'Tipo': rep_tipo,
                    'Hitos': rep_hitos, 'Alertas': rep_alertas,
                    'Fecha Emisión': date.today(), 'Archivo': "Cargado" if rep_file else "Pendiente"
                }
                st.session_state['data_reportes'] = pd.concat([st.session_state['data_reportes'], pd.DataFrame([nuevo_rep])], ignore_index=True)
                st.success("Reporte registrado.")

    with c_r2:
        st.markdown("#### Histórico de Informes")
        if not st.session_state['data_reportes'].empty:
            st.dataframe(st.session_state['data_reportes'], use_container_width=True)
        else:
            st.info("No hay reportes cargados.")

# ==============================================================================
# MÓDULO 5: LIBRO DE PEDIDO (LP)
# ==============================================================================
elif menu == "5. LIBRO DE PEDIDO (LP)":
    st.markdown("### 📖 LIBRO DE PEDIDO (LIBRO DE OBRA)")
    st.warning("⚠️ Las instrucciones aquí registradas tienen carácter contractual y legal.")
    
    with st.expander("➕ NUEVA INSTRUCCIÓN / ASIENTO DE OBRA", expanded=True):
        with st.form("lp_form"):
            c_lp1, c_lp2 = st.columns(2)
            lp_folio = c_lp1.text_input("No. de Folio / Asiento", placeholder="001")
            lp_fecha = c_lp2.date_input("Fecha de Instrucción")
            
            lp_asunto = st.text_input("Asunto (Título de la Orden)")
            lp_instruccion = st.text_area("Instrucción Técnica Detallada", height=100)
            
            c_lp3, c_lp4, c_lp5 = st.columns(3)
            lp_ref = c_lp3.text_input("Ref. Plano/Espec.", placeholder="Plano E-04")
            lp_plazo = c_lp4.text_input("Plazo Cumplimiento", placeholder="24 Horas")
            lp_estado = c_lp5.selectbox("Estado", ["Abierto (Pendiente)", "Cerrado (Cumplido)", "Anulado"])
            
            if st.form_submit_button("📜 REGISTRAR EN LIBRO DE OBRA"):
                nuevo_lp = {
                    'Folio': lp_folio, 'Fecha': lp_fecha,
                    'Asunto': lp_asunto, 'Instrucción': lp_instruccion,
                    'Ref. Técnica': lp_ref, 'Plazo': lp_plazo, 'Estado': lp_estado
                }
                st.session_state['data_lp'] = pd.concat([st.session_state['data_lp'], pd.DataFrame([nuevo_lp])], ignore_index=True)
                st.success(f"Folio {lp_folio} registrado exitosamente.")

    st.markdown("---")
    st.markdown("#### 📂 VISUALIZACIÓN DE ASIENTOS")
    
    df_lp = st.session_state['data_lp']
    if not df_lp.empty:
        for index, row in df_lp.iterrows():
            color_estado = "red" if "Abierto" in row['Estado'] else "green"
            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; border-left: 5px solid {color_estado}; margin-bottom: 10px;">
                    <strong>FOLIO: {row['Folio']}</strong> | 📅 {row['Fecha']} <br>
                    <h4 style="margin: 5px 0;">{row['Asunto']}</h4>
                    <p>{row['Instrucción']}</p>
                    <hr>
                    <small><strong>Ref:</strong> {row['Ref. Técnica']} | <strong>Plazo:</strong> {row['Plazo']} | <strong>Estado:</strong> {row['Estado']}</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("El Libro de Obra está vacío.")
