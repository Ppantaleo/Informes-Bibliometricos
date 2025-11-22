#!/usr/bin/env python3
"""
Script para filtrar datos de visibilidad OpenAlex específicamente para las revistas
chilenas activas identificadas en el análisis JUOJS

Filtra el dataset global de visibilidad usando como criterio las 319 revistas
que aparecen en chile_juojs_activas.csv
"""

import pandas as pd
import os

# Asegurar que el directorio visualizations existe
os.makedirs('visualizations', exist_ok=True)

print("=== FILTRADO DE VISIBILIDAD PARA REVISTAS CHILENAS ACTIVAS ===")

# Cargar los archivos
print("\nCargando archivos...")
beacon_visibilidad = pd.read_csv('visualizations/beacon_ojs_con_visibilidad.csv')
chile_activas = pd.read_csv('visualizations/chile_juojs_activas.csv')

print(f"Total revistas en beacon_ojs_con_visibilidad: {len(beacon_visibilidad):,}")
print(f"Revistas chilenas activas (JUOJS): {len(chile_activas)}")

# Crear conjunto de ISSNs de las revistas chilenas activas para matching
# Manejar casos donde ISSN puede tener múltiples valores separados por ;
issns_chile = set()
for issn_raw in chile_activas['issn'].dropna():
    if issn_raw != 'Sin ISSN':
        # Dividir por ; y limpiar espacios
        issns = [issn.strip() for issn in str(issn_raw).split(';')]
        issns_chile.update(issns)

print(f"ISSNs únicos de revistas chilenas activas: {len(issns_chile)}")

# Función para verificar si una revista está en la lista de Chile
def es_revista_chile_activa(issn_beacon):
    if pd.isna(issn_beacon):
        return False
    
    # El beacon puede tener ISSNs separados por salto de línea o coma
    issns_beacon = str(issn_beacon).replace('\n', ',').split(',')
    issns_beacon = [issn.strip() for issn in issns_beacon if issn.strip()]
    
    # Verificar si algún ISSN del beacon coincide con los de Chile
    return any(issn in issns_chile for issn in issns_beacon)

# Filtrar revistas de Chile usando los ISSNs
beacon_visibilidad['es_chile_activa'] = beacon_visibilidad['issn'].apply(es_revista_chile_activa)
chile_visibilidad = beacon_visibilidad[beacon_visibilidad['es_chile_activa']].copy()

print(f"\nRevistas chilenas encontradas en beacon de visibilidad: {len(chile_visibilidad)}")

# Guardar el archivo filtrado
chile_visibilidad.to_csv('visualizations/chile_ojs_con_visibilidad.csv', index=False)

print(f"\nArchivo guardado: visualizations/chile_ojs_con_visibilidad.csv")
print(f"Columnas incluidas: {len(chile_visibilidad.columns)}")

# Mostrar estadísticas detalladas
if len(chile_visibilidad) > 0:
    indexadas = chile_visibilidad['is_in_openalex'].sum()
    porcentaje_indexadas = (indexadas / len(chile_visibilidad)) * 100
    
    print(f"\n=== ESTADÍSTICAS DE VISIBILIDAD CHILE ===")
    print(f"Revistas chilenas indexadas en OpenAlex: {indexadas} de {len(chile_visibilidad)} ({porcentaje_indexadas:.1f}%)")
    print(f"Revistas chilenas NO indexadas: {len(chile_visibilidad) - indexadas}")
    
    if indexadas > 0:
        indexadas_df = chile_visibilidad[chile_visibilidad['is_in_openalex']]
        
        print(f"\n=== MÉTRICAS AGREGADAS ===")
        print(f"Total artículos indexados en OpenAlex: {indexadas_df['works_count'].sum():,}")
        print(f"Total citaciones recibidas: {indexadas_df['cited_by_count'].sum():,}")
        print(f"Índice de visibilidad promedio: {indexadas_df['indice_visibilidad'].mean():.4f}")
        print(f"Índice de visibilidad mediano: {indexadas_df['indice_visibilidad'].median():.4f}")
        print(f"H-index promedio: {indexadas_df['h_index'].mean():.1f}")
        print(f"H-index mediano: {indexadas_df['h_index'].median():.1f}")
        
        print(f"\n=== TOP 5 REVISTAS POR VISIBILIDAD ===")
        top_visibilidad = indexadas_df.nlargest(5, 'indice_visibilidad')[[
            'context_name', 'issn', 'works_count', 'cited_by_count', 'indice_visibilidad', 'h_index'
        ]]
        
        for i, (_, row) in enumerate(top_visibilidad.iterrows(), 1):
            print(f"{i}. {row['context_name'][:50]}...")
            print(f"   ISSN: {row['issn']}")
            print(f"   Artículos: {row['works_count']:,} | Citaciones: {row['cited_by_count']:,}")
            print(f"   Índice visibilidad: {row['indice_visibilidad']:.4f} | H-index: {row['h_index']}")
            print()
else:
    print("\n⚠ No se encontraron revistas chilenas en el dataset de visibilidad")

print("\n✅ Filtrado completado exitosamente")