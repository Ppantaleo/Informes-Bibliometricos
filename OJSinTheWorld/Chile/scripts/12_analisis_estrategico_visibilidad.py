#!/usr/bin/env python3
"""
Script para análisis estratégico de visibilidad académica de revistas chilenas

Genera tablas y análisis para identificar:
- Revistas por rangos de visibilidad
- Oportunidades de mejora (alta productividad, baja visibilidad)
- Análisis institucional
- Recomendaciones estratégicas para indexación
"""

import pandas as pd
import numpy as np
import os
from urllib.parse import urlparse

# Asegurar que el directorio visualizations existe
os.makedirs('visualizations', exist_ok=True)

print("=== ANÁLISIS ESTRATÉGICO DE VISIBILIDAD ACADÉMICA ===")

# Cargar datos
print("\nCargando datos...")
chile_visibilidad = pd.read_csv('visualizations/chile_ojs_con_visibilidad.csv')

print(f"Total revistas chilenas con datos de visibilidad: {len(chile_visibilidad)}")

# Filtrar solo revistas indexadas en OpenAlex
indexadas = chile_visibilidad[chile_visibilidad['is_in_openalex'] == True].copy()
print(f"Revistas indexadas en OpenAlex: {len(indexadas)}")

# ==========================================
# 1. CATEGORIZACIÓN POR RANGOS DE VISIBILIDAD
# ==========================================
print("\n=== 1. CATEGORIZACIÓN POR RANGOS DE VISIBILIDAD ===")

def categorizar_visibilidad(indice):
    if indice >= 10:
        return "Muy Alta (≥10)"
    elif indice >= 5:
        return "Alta (5-9.99)"
    elif indice >= 1:
        return "Media (1-4.99)"
    elif indice > 0:
        return "Baja (0.01-0.99)"
    else:
        return "Sin citaciones (0)"

indexadas['categoria_visibilidad'] = indexadas['indice_visibilidad'].apply(categorizar_visibilidad)

# Tabla de distribución por rangos
rangos_visibilidad = indexadas['categoria_visibilidad'].value_counts().reset_index()
rangos_visibilidad.columns = ['Rango_Visibilidad', 'Num_Revistas']
rangos_visibilidad['Porcentaje'] = (rangos_visibilidad['Num_Revistas'] / len(indexadas) * 100).round(1)

print("Distribución por rangos de visibilidad:")
print(rangos_visibilidad.to_string(index=False))

# Guardar tabla
rangos_visibilidad.to_csv('visualizations/chile_rangos_visibilidad.csv', index=False)

# ==========================================
# 2. IDENTIFICACIÓN DE OPORTUNIDADES
# ==========================================
print("\n=== 2. IDENTIFICACIÓN DE OPORTUNIDADES ===")

# Revistas con alta productividad pero baja visibilidad (oportunidades)
oportunidades = indexadas[
    (indexadas['total_record_count'] >= 200) &  # Alta productividad
    (indexadas['indice_visibilidad'] < 1)       # Baja visibilidad
].copy()

oportunidades_tabla = oportunidades[[
    'context_name', 'issn', 'total_record_count', 'works_count', 
    'cited_by_count', 'indice_visibilidad', 'h_index'
]].sort_values('total_record_count', ascending=False)

print(f"Revistas con oportunidad de mejora (alta productividad, baja visibilidad): {len(oportunidades)}")
if len(oportunidades) > 0:
    print("\nTop 10 oportunidades:")
    print(oportunidades_tabla.head(10).to_string(index=False))

# Guardar tabla
oportunidades_tabla.to_csv('visualizations/chile_oportunidades_visibilidad.csv', index=False)

# ==========================================
# 3. ANÁLISIS INSTITUCIONAL
# ==========================================
print("\n=== 3. ANÁLISIS INSTITUCIONAL ===")

def extraer_institucion(oai_url):
    """Extrae la institución principal del dominio"""
    try:
        domain = urlparse(oai_url).netloc.lower()
        
        # Mapeo de dominios a instituciones
        instituciones = {
            'uc.cl': 'Pontificia Universidad Católica',
            'uchile.cl': 'Universidad de Chile',
            'udec.cl': 'Universidad de Concepción',
            'uach.cl': 'Universidad Austral de Chile',
            'usach.cl': 'Universidad de Santiago',
            'uv.cl': 'Universidad de Valparaíso',
            'ucsc.cl': 'Universidad Católica de la Santísima Concepción',
            'udd.cl': 'Universidad del Desarrollo',
            'umce.cl': 'Universidad Metropolitana de Ciencias de la Educación',
            'ulagos.cl': 'Universidad de Los Lagos',
            'uct.cl': 'Universidad Católica de Temuco',
            'utalca.cl': 'Universidad de Talca',
            'ubiobio.cl': 'Universidad del Bío-Bío'
        }
        
        for key, inst in instituciones.items():
            if key in domain:
                return inst
        
        # Si no se encuentra, usar el dominio principal
        parts = domain.split('.')
        if len(parts) >= 2:
            return f"{parts[-2]}.{parts[-1]}"
        return domain
        
    except:
        return "Desconocida"

indexadas['institucion'] = indexadas['oai_url'].apply(extraer_institucion)

# Análisis por institución
analisis_institucional = indexadas.groupby('institucion').agg({
    'context_name': 'count',
    'total_record_count': 'sum',
    'works_count': 'sum',
    'cited_by_count': 'sum',
    'indice_visibilidad': 'mean',
    'h_index': 'mean'
}).round(2)

analisis_institucional.columns = [
    'Num_Revistas', 'Total_Articulos', 'Articulos_OpenAlex', 
    'Total_Citaciones', 'Indice_Visibilidad_Promedio', 'H_Index_Promedio'
]

analisis_institucional = analisis_institucional.sort_values('Total_Citaciones', ascending=False)

print("Análisis por institución (top 10):")
print(analisis_institucional.head(10).to_string())

# Guardar tabla
analisis_institucional.to_csv('visualizations/chile_analisis_institucional.csv')

# ==========================================
# 4. REVISTAS ESTRELLA Y EMERGENTES
# ==========================================
print("\n=== 4. REVISTAS ESTRELLA Y EMERGENTES ===")

# Revistas estrella (alta visibilidad y alto H-index)
estrellas = indexadas[
    (indexadas['indice_visibilidad'] >= 5) & 
    (indexadas['h_index'] >= 15)
].copy()

estrellas_tabla = estrellas[[
    'context_name', 'issn', 'indice_visibilidad', 'h_index', 
    'cited_by_count', 'works_count'
]].sort_values('indice_visibilidad', ascending=False)

print(f"Revistas estrella (alta visibilidad + alto H-index): {len(estrellas)}")
if len(estrellas) > 0:
    print(estrellas_tabla.to_string(index=False))

# Revistas emergentes (H-index bajo pero crecimiento reciente)
emergentes = indexadas[
    (indexadas['h_index'] <= 10) & 
    (indexadas['indice_visibilidad'] >= 1) &
    (indexadas['works_count'] >= 100)
].copy()

emergentes_tabla = emergentes[[
    'context_name', 'issn', 'indice_visibilidad', 'h_index', 
    'works_count', 'cited_by_count'
]].sort_values('indice_visibilidad', ascending=False)

print(f"\nRevistas emergentes (potencial de crecimiento): {len(emergentes)}")
if len(emergentes) > 0:
    print(emergentes_tabla.head(10).to_string(index=False))

# Guardar tablas
estrellas_tabla.to_csv('visualizations/chile_revistas_estrella.csv', index=False)
emergentes_tabla.to_csv('visualizations/chile_revistas_emergentes.csv', index=False)

# ==========================================
# 5. CORRELACIONES Y PATRONES
# ==========================================
print("\n=== 5. CORRELACIONES Y PATRONES ===")

# Correlación entre productividad y visibilidad
correlacion_prod_vis = indexadas['total_record_count'].corr(indexadas['indice_visibilidad'])
correlacion_h_vis = indexadas['h_index'].corr(indexadas['indice_visibilidad'])
correlacion_works_cit = indexadas['works_count'].corr(indexadas['cited_by_count'])

print(f"Correlación productividad total vs visibilidad: {correlacion_prod_vis:.3f}")
print(f"Correlación H-index vs visibilidad: {correlacion_h_vis:.3f}")
print(f"Correlación artículos OpenAlex vs citaciones: {correlacion_works_cit:.3f}")

# ==========================================
# 6. RECOMENDACIONES ESTRATÉGICAS
# ==========================================
print("\n=== 6. RECOMENDACIONES ESTRATÉGICAS ===")

# Priorización para Dialnet
def calcular_prioridad_dialnet(row):
    """Calcula prioridad para indexación en Dialnet"""
    score = 0
    
    # Alta productividad (+2)
    if row['total_record_count'] >= 300:
        score += 2
    elif row['total_record_count'] >= 100:
        score += 1
    
    # Visibilidad internacional (+3)
    if row['indice_visibilidad'] >= 5:
        score += 3
    elif row['indice_visibilidad'] >= 1:
        score += 2
    elif row['indice_visibilidad'] > 0:
        score += 1
    
    # H-index (+2)
    if row['h_index'] >= 20:
        score += 2
    elif row['h_index'] >= 10:
        score += 1
    
    # Tasa de indexación (+1)
    if row['tasa_indexacion_openalex'] >= 0.5:
        score += 1
    
    return score

indexadas['prioridad_dialnet'] = indexadas.apply(calcular_prioridad_dialnet, axis=1)

# Top revistas por prioridad
priorizacion = indexadas[[
    'context_name', 'issn', 'prioridad_dialnet', 'indice_visibilidad', 
    'h_index', 'total_record_count', 'cited_by_count'
]].sort_values('prioridad_dialnet', ascending=False)

print("Top 15 revistas priorizadas para Dialnet:")
print(priorizacion.head(15).to_string(index=False))

# Guardar tabla de priorización
priorizacion.to_csv('visualizations/chile_priorizacion_dialnet.csv', index=False)

# ==========================================
# 7. RESUMEN EJECUTIVO
# ==========================================
print("\n=== 7. RESUMEN EJECUTIVO ===")

total_revistas = len(chile_visibilidad)
indexadas_count = len(indexadas)
alta_visibilidad = len(indexadas[indexadas['indice_visibilidad'] >= 5])
oportunidades_count = len(oportunidades)
estrellas_count = len(estrellas)

resumen = {
    'Total_Revistas_Chilenas': total_revistas,
    'Indexadas_OpenAlex': indexadas_count,
    'Porcentaje_Indexadas': round(indexadas_count/total_revistas*100, 1),
    'Alta_Visibilidad': alta_visibilidad,
    'Revistas_Estrella': estrellas_count,
    'Oportunidades_Mejora': oportunidades_count,
    'Total_Citaciones': int(indexadas['cited_by_count'].sum()),
    'Visibilidad_Promedio': round(indexadas['indice_visibilidad'].mean(), 3),
    'H_Index_Promedio': round(indexadas['h_index'].mean(), 1)
}

print("Métricas clave:")
for key, value in resumen.items():
    print(f"  {key.replace('_', ' ')}: {value}")

# Guardar resumen
pd.DataFrame([resumen]).to_csv('visualizations/chile_resumen_visibilidad.csv', index=False)

print(f"\n✅ Análisis completado. Archivos generados:")
print("  - chile_rangos_visibilidad.csv")
print("  - chile_oportunidades_visibilidad.csv") 
print("  - chile_analisis_institucional.csv")
print("  - chile_revistas_estrella.csv")
print("  - chile_revistas_emergentes.csv")
print("  - chile_priorizacion_dialnet.csv")
print("  - chile_resumen_visibilidad.csv")