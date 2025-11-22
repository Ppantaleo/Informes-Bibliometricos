#!/usr/bin/env python3
"""
Script para análisis de políticas de acceso abierto de revistas chilenas
basado en datos disponibles (OJS, OpenAlex, Dialnet)

Genera un análisis inferido de políticas de acceso abierto considerando:
- Uso de OJS (plataforma de acceso abierto)
- Presencia en OpenAlex (visibilidad académica)
- Calidad editorial (Dialnet)
- Patrones institucionales
"""

import pandas as pd
import numpy as np
import os
from urllib.parse import urlparse

print("=== ANÁLISIS DE POLÍTICAS DE ACCESO ABIERTO CHILE ===")

# Cargar datos
print("\nCargando datasets...")
try:
    chile_activas = pd.read_csv('visualizations/chile_juojs_activas.csv')
    print(f"✓ Revistas chilenas activas: {len(chile_activas)}")
except:
    print("❌ Error cargando chile_juojs_activas.csv")
    exit(1)

try:
    chile_visibilidad = pd.read_csv('visualizations/chile_ojs_con_visibilidad.csv')
    print(f"✓ Revistas con datos OpenAlex: {len(chile_visibilidad)}")
except:
    print("⚠ No se encontró chile_ojs_con_visibilidad.csv")
    chile_visibilidad = pd.DataFrame()

try:
    dialnet_procesados = pd.read_csv('visualizations/dialnet_informes_procesados.csv')
    print(f"✓ Informes Dialnet procesados: {len(dialnet_procesados)}")
except:
    print("⚠ No se encontró dialnet_informes_procesados.csv")
    dialnet_procesados = pd.DataFrame()

# ==========================================
# 1. CLASIFICACIÓN DE POLÍTICAS DE ACCESO ABIERTO
# ==========================================
print("\n=== 1. CLASIFICACIÓN DE POLÍTICAS DE ACCESO ABIERTO ===")

def extraer_institucion(dominio):
    """Extrae institución del dominio"""
    instituciones_map = {
        'uc.cl': 'Pontificia Universidad Católica',
        'uchile.cl': 'Universidad de Chile', 
        'udec.cl': 'Universidad de Concepción',
        'uach.cl': 'Universidad Austral de Chile',
        'usach.cl': 'Universidad de Santiago',
        'uv.cl': 'Universidad de Valparaíso',
        'ucsc.cl': 'Universidad Católica de la Santísima Concepción',
        'udd.cl': 'Universidad del Desarrollo',
        'umce.cl': 'Universidad Metropolitana de Ciencias de la Educación'
    }
    
    for key, inst in instituciones_map.items():
        if key in dominio:
            return inst
    return 'Otra institución'

def clasificar_politica_oa(row):
    """Clasifica política de acceso abierto basada en datos disponibles"""
    score = 0
    categoria = "Desconocida"
    
    # Factor 1: Uso de OJS (+2 puntos - plataforma OA)
    score += 2
    
    # Factor 2: Visibilidad en OpenAlex
    if not pd.isna(row.get('indice_visibilidad', np.nan)):
        if row['indice_visibilidad'] > 5:
            score += 3  # Alta visibilidad internacional
        elif row['indice_visibilidad'] > 1:
            score += 2  # Media visibilidad
        else:
            score += 1  # Baja visibilidad pero presente
    
    # Factor 3: Productividad (proxy de política activa)
    total_articulos = row.get('total_historico', 0)
    if total_articulos > 1000:
        score += 2
    elif total_articulos > 500:
        score += 1
    
    # Factor 4: Calidad editorial (Dialnet)
    if not pd.isna(row.get('total_errores', np.nan)):
        if row['total_errores'] < 100:
            score += 2  # Buena calidad
        elif row['total_errores'] < 500:
            score += 1  # Calidad media
    
    # Factor 5: Institución (políticas institucionales conocidas)
    institucion = row.get('institucion', '')
    if 'Universidad de Chile' in institucion or 'Pontificia Universidad Católica' in institucion:
        score += 1  # Instituciones con políticas OA establecidas
    
    # Clasificación final
    if score >= 8:
        categoria = "Acceso Abierto Pleno"
    elif score >= 6:
        categoria = "Acceso Abierto Activo"
    elif score >= 4:
        categoria = "Acceso Abierto Básico"
    else:
        categoria = "Acceso Abierto Limitado"
    
    return categoria, score

# Preparar dataset combinado
dataset_combinado = chile_activas.copy()
dataset_combinado['institucion'] = dataset_combinado['dominio'].apply(extraer_institucion)

# Combinar con datos de visibilidad si están disponibles
if not chile_visibilidad.empty:
    # Hacer merge por ISSN
    visibilidad_merge = chile_visibilidad[['issn', 'indice_visibilidad', 'h_index', 'cited_by_count']].copy()
    visibilidad_merge = visibilidad_merge.rename(columns={'issn': 'issn_merge'})
    
    # Preparar ISSNs para merge
    def preparar_issn_merge(issn_str):
        if pd.isna(issn_str) or issn_str == 'Sin ISSN':
            return None
        return str(issn_str).split(';')[0].strip()
    
    dataset_combinado['issn_merge'] = dataset_combinado['issn'].apply(preparar_issn_merge)
    visibilidad_merge['issn_merge'] = visibilidad_merge['issn_merge'].apply(preparar_issn_merge)
    
    dataset_combinado = dataset_combinado.merge(visibilidad_merge, on='issn_merge', how='left')

# Combinar con datos de Dialnet si están disponibles
if not dialnet_procesados.empty:
    dialnet_merge = dialnet_procesados[['dominio', 'errores_total', 'errores_alta']].copy()
    dialnet_merge = dialnet_merge.rename(columns={'errores_total': 'total_errores', 'errores_alta': 'errores_alta_gravedad'})
    dataset_combinado = dataset_combinado.merge(dialnet_merge, on='dominio', how='left')

# Aplicar clasificación
print("Clasificando políticas de acceso abierto...")
clasificaciones = dataset_combinado.apply(
    lambda row: clasificar_politica_oa(row), axis=1
)

dataset_combinado['politica_oa'] = [c[0] for c in clasificaciones]
dataset_combinado['score_oa'] = [c[1] for c in clasificaciones]

# ==========================================
# 2. ESTADÍSTICAS DE POLÍTICAS
# ==========================================
print("\n=== 2. DISTRIBUCIÓN DE POLÍTICAS DE ACCESO ABIERTO ===")

distribucion_politicas = dataset_combinado['politica_oa'].value_counts()
print("Distribución por tipo de política:")
for politica, count in distribucion_politicas.items():
    porcentaje = (count / len(dataset_combinado)) * 100
    print(f"  {politica}: {count} revistas ({porcentaje:.1f}%)")

# ==========================================
# 3. ANÁLISIS POR INSTITUCIÓN
# ==========================================
print("\n=== 3. ANÁLISIS POR INSTITUCIÓN ===")

analisis_institucional = dataset_combinado.groupby('institucion').agg({
    'context_name': 'count',
    'score_oa': 'mean',
    'total_historico': 'sum'
}).round(2)

analisis_institucional.columns = ['Num_Revistas', 'Score_OA_Promedio', 'Total_Articulos']
analisis_institucional = analisis_institucional.sort_values('Score_OA_Promedio', ascending=False)

print("Top instituciones por score de acceso abierto:")
print(analisis_institucional.head(10).to_string())

# ==========================================
# 4. REVISTAS MODELO DE ACCESO ABIERTO
# ==========================================
print("\n=== 4. REVISTAS MODELO DE ACCESO ABIERTO ===")

revistas_modelo = dataset_combinado[
    dataset_combinado['politica_oa'] == 'Acceso Abierto Pleno'
].copy()

if len(revistas_modelo) > 0:
    modelo_tabla = revistas_modelo[[
        'context_name', 'issn', 'institucion', 'score_oa', 'total_historico'
    ]].sort_values('score_oa', ascending=False)
    
    print(f"Revistas con Acceso Abierto Pleno ({len(revistas_modelo)}):")
    print(modelo_tabla.head(10).to_string(index=False))
else:
    print("No se identificaron revistas con Acceso Abierto Pleno")

# ==========================================
# 5. OPORTUNIDADES DE MEJORA
# ==========================================
print("\n=== 5. OPORTUNIDADES DE MEJORA ===")

oportunidades = dataset_combinado[
    (dataset_combinado['total_historico'] > 200) &
    (dataset_combinado['politica_oa'].isin(['Acceso Abierto Limitado', 'Acceso Abierto Básico']))
].copy()

if len(oportunidades) > 0:
    oportunidades_tabla = oportunidades[[
        'context_name', 'issn', 'institucion', 'politica_oa', 'total_historico'
    ]].sort_values('total_historico', ascending=False)
    
    print(f"Revistas con potencial de mejora ({len(oportunidades)}):")
    print(oportunidades_tabla.head(10).to_string(index=False))

# ==========================================
# 6. RECOMENDACIONES ESTRATÉGICAS
# ==========================================
print("\n=== 6. RECOMENDACIONES ESTRATÉGICAS ===")

# Calcular métricas clave
total_revistas = len(dataset_combinado)
oa_pleno = len(dataset_combinado[dataset_combinado['politica_oa'] == 'Acceso Abierto Pleno'])
oa_activo = len(dataset_combinado[dataset_combinado['politica_oa'] == 'Acceso Abierto Activo'])
score_promedio = dataset_combinado['score_oa'].mean()

print(f"Métricas del ecosistema chileno:")
print(f"  Total revistas analizadas: {total_revistas}")
print(f"  Acceso Abierto Pleno: {oa_pleno} ({oa_pleno/total_revistas*100:.1f}%)")
print(f"  Acceso Abierto Activo: {oa_activo} ({oa_activo/total_revistas*100:.1f}%)")
print(f"  Score promedio: {score_promedio:.2f}/10")

print(f"\nRecomendaciones:")
print(f"1. Fortalecer {len(oportunidades)} revistas con alto potencial")
print(f"2. Promover mejores prácticas de las {oa_pleno} revistas modelo")
print(f"3. Implementar políticas institucionales en universidades con score bajo")
print(f"4. Mejorar visibilidad internacional de revistas con baja presencia en OpenAlex")

# ==========================================
# 7. GUARDAR RESULTADOS
# ==========================================
print(f"\n=== 7. GUARDANDO RESULTADOS ===")

# Dataset completo con clasificaciones
dataset_final = dataset_combinado[[
    'context_name', 'dominio', 'issn', 'institucion', 'politica_oa', 
    'score_oa', 'total_historico', 'indice_visibilidad', 'total_errores'
]].copy()

dataset_final.to_csv('visualizations/chile_politicas_acceso_abierto.csv', index=False)

# Resumen por políticas
resumen_politicas = distribucion_politicas.reset_index()
resumen_politicas.columns = ['Politica_OA', 'Num_Revistas']
resumen_politicas['Porcentaje'] = (resumen_politicas['Num_Revistas'] / total_revistas * 100).round(1)
resumen_politicas.to_csv('visualizations/chile_resumen_politicas_oa.csv', index=False)

# Análisis institucional
analisis_institucional.to_csv('visualizations/chile_instituciones_politicas_oa.csv')

print(f"✅ Archivos generados:")
print(f"  - chile_politicas_acceso_abierto.csv (dataset completo)")
print(f"  - chile_resumen_politicas_oa.csv (resumen por políticas)")
print(f"  - chile_instituciones_politicas_oa.csv (análisis institucional)")

print(f"\n✅ Análisis de políticas de acceso abierto completado")