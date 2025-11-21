#!/usr/bin/env python3
"""
Separación de Beacon v6 por tipo de aplicación
Adaptado para beacon_v6.csv con nuevas columnas 2024-2025
"""

import pandas as pd

# Configuración
INPUT_FILE = '../../beacon_v6.csv'
OUTPUT_OJS = '../../beacon_v6_ojs.csv'
OUTPUT_OMP = '../../beacon_v6_omp.csv'

print("="*60)
print("SEPARANDO BEACON V6 POR TIPO DE APLICACIÓN")
print("="*60)

# Cargar datos
print(f"\nCargando {INPUT_FILE}...")
try:
    beacon = pd.read_csv(INPUT_FILE, low_memory=False)
except FileNotFoundError:
    print(f"❌ ERROR: No se encuentra {INPUT_FILE}")
    print("Verifica que el archivo beacon_v6.csv esté en la carpeta raíz")
    exit(1)

print(f"Total de registros: {len(beacon):,}")
print(f"Total de columnas: {len(beacon.columns)}")

# Verificar columna application
if 'application' not in beacon.columns:
    print("\n❌ ERROR: No se encuentra la columna 'application'")
    print(f"Columnas disponibles: {beacon.columns.tolist()}")
    exit(1)

# Distribución de aplicaciones
print("\n" + "-"*60)
print("DISTRIBUCIÓN POR TIPO DE APLICACIÓN")
print("-"*60)
app_counts = beacon['application'].value_counts()
print(app_counts)

# Filtrar OJS
print("\nFiltrando instalaciones OJS...")
beacon_ojs = beacon[beacon['application'] == 'ojs'].copy()
print(f"  ✓ Encontradas {len(beacon_ojs):,} instalaciones OJS ({len(beacon_ojs)/len(beacon)*100:.1f}%)")

# Filtrar OMP
print("Filtrando instalaciones OMP...")
beacon_omp = beacon[beacon['application'] == 'omp'].copy()
print(f"  ✓ Encontradas {len(beacon_omp):,} instalaciones OMP ({len(beacon_omp)/len(beacon)*100:.1f}%)")

# Estadísticas v6
print("\n" + "="*60)
print("ESTADÍSTICAS BEACON V6")
print("="*60)

# OJS
if len(beacon_ojs) > 0:
    print("\n📚 OJS (Open Journal Systems):")
    print(f"  - Total instalaciones: {len(beacon_ojs):,}")
    print(f"  - Con ISSN: {beacon_ojs['issn'].notna().sum():,}")
    print(f"  - Total histórico: {beacon_ojs['total_record_count'].sum():,}")
    
    # Nuevas métricas v6
    if 'record_count_2024' in beacon_ojs.columns:
        activas_2024 = (beacon_ojs['record_count_2024'] > 5).sum()
        pub_2024 = beacon_ojs['record_count_2024'].sum()
        print(f"  - Publicaciones 2024: {pub_2024:,}")
        print(f"  - Activas 2024 (>5 pub): {activas_2024:,}")
    
    if 'region' in beacon_ojs.columns:
        print(f"  - Top 3 regiones:")
        top_regions = beacon_ojs['region'].value_counts().head(3)
        for region, count in top_regions.items():
            print(f"    • {region}: {count:,}")

# OMP
if len(beacon_omp) > 0:
    print("\n📖 OMP (Open Monograph Press):")
    print(f"  - Total instalaciones: {len(beacon_omp):,}")
    print(f"  - Con ISSN: {beacon_omp['issn'].notna().sum():,}")
    print(f"  - Total histórico: {beacon_omp['total_record_count'].sum():,}")

# Verificación
print("\n" + "="*60)
print("VERIFICACIÓN")
print("="*60)
total_filtrado = len(beacon_ojs) + len(beacon_omp)
otros = len(beacon) - total_filtrado

print(f"\nTotal original: {len(beacon):,}")
print(f"OJS + OMP: {total_filtrado:,}")
print(f"Otros/sin clasificar: {otros:,}")

if otros > 0:
    print(f"\n⚠️  Hay {otros:,} registros con otros valores:")
    otros_apps = beacon[~beacon['application'].isin(['ojs', 'omp'])]['application'].value_counts()
    print(otros_apps)

# Guardar archivos
print("\n" + "="*60)
print("GUARDANDO ARCHIVOS V6")
print("="*60)

# Guardar OJS
if len(beacon_ojs) > 0:
    print(f"\nGuardando {OUTPUT_OJS}...")
    beacon_ojs.to_csv(OUTPUT_OJS, index=False)
    print(f"  ✓ Guardado: {OUTPUT_OJS}")
    print(f"    Tamaño: {len(beacon_ojs):,} filas × {len(beacon_ojs.columns)} columnas")

# Guardar OMP
if len(beacon_omp) > 0:
    print(f"\nGuardando {OUTPUT_OMP}...")
    beacon_omp.to_csv(OUTPUT_OMP, index=False)
    print(f"  ✓ Guardado: {OUTPUT_OMP}")
    print(f"    Tamaño: {len(beacon_omp):,} filas × {len(beacon_omp.columns)} columnas")

# Resumen final
print("\n" + "="*60)
print("✓ PROCESO COMPLETADO V6")
print("="*60)
print("\nArchivos generados:")
if len(beacon_ojs) > 0:
    print(f"  1. {OUTPUT_OJS} ({len(beacon_ojs):,} instalaciones)")
if len(beacon_omp) > 0:
    print(f"  2. {OUTPUT_OMP} ({len(beacon_omp):,} instalaciones)")

print("\nNuevas columnas v6 disponibles:")
nuevas_cols = ['record_count_2024', 'record_count_2025', 'region', 'admin_email', 'country_doaj']
for col in nuevas_cols:
    if col in beacon.columns:
        print(f"  ✓ {col}")

if __name__ == "__main__":
    pass