import pandas as pd

# ==========================================
# CONFIGURACIÓN
# ==========================================
INPUT_FILE = '../beacon.csv'
OUTPUT_OJS = '../beacon_ojs.csv'
OUTPUT_OMP = '../beacon_omp.csv'

print("="*60)
print("SEPARANDO BEACON POR TIPO DE APLICACIÓN")
print("="*60)

# ==========================================
# CARGAR DATOS
# ==========================================
print(f"\nCargando {INPUT_FILE}...")
beacon = pd.read_csv(INPUT_FILE, low_memory=False)

print(f"Total de registros: {len(beacon):,}")
print(f"Total de columnas: {len(beacon.columns)}")

# ==========================================
# VERIFICAR COLUMNA APPLICATION
# ==========================================
if 'application' not in beacon.columns:
    print("\n❌ ERROR: No se encuentra la columna 'application'")
    print(f"Columnas disponibles: {beacon.columns.tolist()}")
    exit(1)

# Ver distribución de aplicaciones
print("\n" + "-"*60)
print("DISTRIBUCIÓN POR TIPO DE APLICACIÓN")
print("-"*60)
app_counts = beacon['application'].value_counts()
print(app_counts)
print()

# ==========================================
# FILTRAR POR OJS
# ==========================================
print("Filtrando revistas OJS...")
beacon_ojs = beacon[beacon['application'] == 'ojs'].copy()
print(f"  ✓ Encontradas {len(beacon_ojs):,} revistas OJS ({len(beacon_ojs)/len(beacon)*100:.1f}%)")

# ==========================================
# FILTRAR POR OMP
# ==========================================
print("Filtrando revistas OMP...")
beacon_omp = beacon[beacon['application'] == 'omp'].copy()
print(f"  ✓ Encontradas {len(beacon_omp):,} revistas OMP ({len(beacon_omp)/len(beacon)*100:.1f}%)")

# ==========================================
# ESTADÍSTICAS ADICIONALES
# ==========================================
print("\n" + "="*60)
print("ESTADÍSTICAS COMPARATIVAS")
print("="*60)

# OJS
if len(beacon_ojs) > 0:
    print("\n📚 OJS (Open Journal Systems):")
    print(f"  - Total revistas: {len(beacon_ojs):,}")
    print(f"  - Con ISSN: {beacon_ojs['issn'].notna().sum():,}")
    print(f"  - Total artículos: {beacon_ojs['total_record_count'].sum():,}")
    print(f"  - Promedio artículos/revista: {beacon_ojs['total_record_count'].mean():.1f}")
    
    if 'country_consolidated' in beacon_ojs.columns:
        top_countries_ojs = beacon_ojs['country_consolidated'].value_counts().head(5)
        print(f"  - Top 5 países:")
        for country, count in top_countries_ojs.items():
            print(f"    • {country}: {count:,} revistas")

# OMP
if len(beacon_omp) > 0:
    print("\n📖 OMP (Open Monograph Press):")
    print(f"  - Total revistas: {len(beacon_omp):,}")
    print(f"  - Con ISSN: {beacon_omp['issn'].notna().sum():,}")
    print(f"  - Total artículos: {beacon_omp['total_record_count'].sum():,}")
    print(f"  - Promedio artículos/revista: {beacon_omp['total_record_count'].mean():.1f}")
    
    if 'country_consolidated' in beacon_omp.columns:
        top_countries_omp = beacon_omp['country_consolidated'].value_counts().head(5)
        print(f"  - Top 5 países:")
        for country, count in top_countries_omp.items():
            print(f"    • {country}: {count:,} revistas")

# ==========================================
# VERIFICACIÓN DE DATOS
# ==========================================
print("\n" + "="*60)
print("VERIFICACIÓN")
print("="*60)
total_filtrado = len(beacon_ojs) + len(beacon_omp)
otros = len(beacon) - total_filtrado

print(f"\nTotal original: {len(beacon):,}")
print(f"OJS + OMP: {total_filtrado:,}")
print(f"Otros/sin clasificar: {otros:,}")

if otros > 0:
    print(f"\n⚠️  Hay {otros:,} registros con otros valores en 'application':")
    otros_apps = beacon[~beacon['application'].isin(['ojs', 'omp'])]['application'].value_counts()
    print(otros_apps)

# ==========================================
# GUARDAR ARCHIVOS
# ==========================================
print("\n" + "="*60)
print("GUARDANDO ARCHIVOS")
print("="*60)

# Guardar OJS
if len(beacon_ojs) > 0:
    print(f"\nGuardando {OUTPUT_OJS}...")
    beacon_ojs.to_csv(OUTPUT_OJS, index=False)
    print(f"  ✓ Guardado: {OUTPUT_OJS}")
    print(f"    Tamaño: {len(beacon_ojs):,} filas × {len(beacon_ojs.columns)} columnas")
else:
    print(f"\n⚠️  No hay datos OJS para guardar")

# Guardar OMP
if len(beacon_omp) > 0:
    print(f"\nGuardando {OUTPUT_OMP}...")
    beacon_omp.to_csv(OUTPUT_OMP, index=False)
    print(f"  ✓ Guardado: {OUTPUT_OMP}")
    print(f"    Tamaño: {len(beacon_omp):,} filas × {len(beacon_omp.columns)} columnas")
else:
    print(f"\n⚠️  No hay datos OMP para guardar")

# ==========================================
# RESUMEN FINAL
# ==========================================
print("\n" + "="*60)
print("✓ PROCESO COMPLETADO")
print("="*60)
print("\nArchivos generados:")
if len(beacon_ojs) > 0:
    print(f"  1. {OUTPUT_OJS} ({len(beacon_ojs):,} revistas)")
if len(beacon_omp) > 0:
    print(f"  2. {OUTPUT_OMP} ({len(beacon_omp):,} revistas)")

print("\nPuedes usar estos archivos con openalex.py cambiando:")
print("  BEACON_FILE = 'beacon_ojs.csv'  # Para analizar solo OJS")
print("  BEACON_FILE = 'beacon_omp.csv'  # Para analizar solo OMP")