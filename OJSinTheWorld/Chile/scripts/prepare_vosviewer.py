import pandas as pd
import numpy as np

# ==========================================
# CONFIGURACIÓN
# ==========================================
INPUT_FILE = 'visualizations/beacon_ojs_con_visibilidad.csv'

# Archivos de salida para VOSviewer
OUTPUT_MAP = 'visualizations/vosviewer_map.txt'
OUTPUT_NETWORK = 'visualizations/vosviewer_network.txt'

print("="*60)
print("PREPARANDO DATOS PARA VOSVIEWER")
print("="*60)

# ==========================================
# CARGAR DATOS
# ==========================================
print(f"\nCargando {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE, low_memory=False)

print(f"Total de registros: {len(df):,}")
print(f"Registros en OpenAlex: {df['is_in_openalex'].sum():,}")

# Filtrar solo revistas indexadas en OpenAlex
df_openalex = df[df['is_in_openalex'] == True].copy()
print(f"Trabajaremos con {len(df_openalex):,} revistas indexadas")

# ==========================================
# OPCIÓN 1: MAPA DE PAÍSES
# ==========================================
print("\n" + "-"*60)
print("CREANDO MAPA DE PAÍSES")
print("-"*60)

# Agrupar por país
paises = df_openalex.groupby('country_consolidated').agg({
    'context_name': 'count',  # Número de revistas
    'cited_by_count': 'sum',  # Total citaciones
    'works_count': 'sum',  # Total artículos indexados
    'indice_visibilidad': 'mean',  # Promedio visibilidad
    'h_index': 'mean'  # Promedio h-index
}).rename(columns={'context_name': 'num_revistas'})

# Filtrar países con al menos 5 revistas
paises = paises[paises['num_revistas'] >= 5].copy()
paises = paises.sort_values('cited_by_count', ascending=False)

print(f"\nPaíses con ≥5 revistas: {len(paises)}")
print("\nTop 10 países por citaciones:")
print(paises.head(10))

# Guardar mapa de países para VOSviewer
paises_vos = paises.reset_index()
paises_vos['id'] = range(1, len(paises_vos) + 1)
paises_vos['cluster'] = (paises_vos['indice_visibilidad'] > paises_vos['indice_visibilidad'].median()).astype(int) + 1

# Formato VOSviewer map file
vos_map = paises_vos[['id', 'country_consolidated', 'cluster', 'cited_by_count', 'num_revistas', 'indice_visibilidad', 'h_index']]
vos_map.columns = ['id', 'label', 'cluster', 'weight<citations>', 'weight<journals>', 'weight<visibility>', 'weight<h_index>']

# Guardar
vos_map.to_csv(OUTPUT_MAP, sep='\t', index=False)
print(f"\n✓ Archivo mapa guardado: {OUTPUT_MAP}")
print(f"  → Importar en VOSviewer: 'Create map based on bibliographic data' → 'Read data from reference manager files'")
print(f"  → O usar 'Create map based on a map and network file' → seleccionar {OUTPUT_MAP}")

# ==========================================
# OPCIÓN 2: RED DE PAÍSES (Co-ocurrencia)
# ==========================================
print("\n" + "-"*60)
print("CREANDO RED DE PAÍSES")
print("-"*60)

# Preparar datos
df_network = df_openalex[df_openalex['country_consolidated'].notna()].copy()

# Top 30 países por número de revistas
top_countries = df_network['country_consolidated'].value_counts().head(30).index.tolist()
df_network = df_network[df_network['country_consolidated'].isin(top_countries)]

# Calcular promedios por país
country_stats = df_network.groupby('country_consolidated').agg({
    'indice_visibilidad': 'mean',
    'h_index': 'mean',
    'cited_by_count': 'sum'
}).reset_index()

# Crear mapeo de país a ID (antes de renombrar columnas)
country_to_id = dict(zip(paises_vos['country_consolidated'], paises_vos['id']))

# Crear enlaces basados en similitud de índice de visibilidad
edges = []
countries_list = country_stats['country_consolidated'].tolist()

for i, country1 in enumerate(countries_list):
    vis1 = country_stats[country_stats['country_consolidated'] == country1]['indice_visibilidad'].values[0]
    
    for j, country2 in enumerate(countries_list):
        if i < j:  # Evitar duplicados
            vis2 = country_stats[country_stats['country_consolidated'] == country2]['indice_visibilidad'].values[0]
            
            # Calcular similitud (inverso de la diferencia)
            diff = abs(vis1 - vis2)
            if diff < 2.0:  # Solo conectar países con visibilidad similar
                similarity = 1 / (1 + diff)
                weight = int(similarity * 100)  # Escalar a enteros
                
                if weight > 10:  # Umbral mínimo
                    # Mapear a IDs usando el diccionario
                    if country1 in country_to_id and country2 in country_to_id:
                        id1 = country_to_id[country1]
                        id2 = country_to_id[country2]
                        edges.append([id1, id2, weight])

# Crear DataFrame de red
network_df = pd.DataFrame(edges, columns=['source', 'target', 'weight'])
network_df = network_df.sort_values('weight', ascending=False)

# Guardar
network_df.to_csv(OUTPUT_NETWORK, sep='\t', index=False, header=False)
print(f"\n✓ Archivo red guardado: {OUTPUT_NETWORK}")
print(f"  Enlaces creados: {len(network_df)}")

if len(network_df) > 0:
    print(f"\nTop 10 conexiones más fuertes:")
    # Crear diccionario inverso para mostrar nombres
    id_to_country = {v: k for k, v in country_to_id.items()}
    
    for idx, row in network_df.head(10).iterrows():
        c1 = id_to_country.get(row['source'], 'Unknown')
        c2 = id_to_country.get(row['target'], 'Unknown')
        print(f"  {c1} ↔ {c2} (peso: {row['weight']})")
else:
    print("\n⚠️  No se crearon conexiones. Intenta ajustar los umbrales.")

# ==========================================
# ESTADÍSTICAS FINALES
# ==========================================
print("\n" + "="*60)
print("ESTADÍSTICAS DE LA RED")
print("="*60)
print(f"\nNodos (países): {len(paises_vos)}")
print(f"Enlaces (conexiones): {len(network_df)}")
print(f"Densidad de red: {len(network_df) / (len(paises_vos) * (len(paises_vos)-1) / 2) * 100:.2f}%")

# ==========================================
# INSTRUCCIONES PARA VOSVIEWER
# ==========================================
print("\n" + "="*60)
print("CÓMO USAR EN VOSVIEWER")
print("="*60)

print("""
PASO 1: Abrir VOSviewer
  → Descarga: https://www.vosviewer.com/

PASO 2: Crear visualización
  → Menú: File → Create...
  → Seleccionar: "Create a map based on a map and network file"
  → Click: Next

PASO 3: Cargar archivos
  → Map file: seleccionar 'vosviewer_map.txt'
  → Network file: seleccionar 'vosviewer_network.txt'
  → Click: Finish

PASO 4: Personalizar visualización
  → Pestaña "Visualization"
  → Opciones disponibles:
    • Weights: seleccionar qué métrica usar para el tamaño
      - weight<citations>: tamaño por citaciones
      - weight<journals>: tamaño por número de revistas
      - weight<visibility>: tamaño por índice de visibilidad
      - weight<h_index>: tamaño por h-index promedio
    • Colors: cluster automático por similitud
    • Layout: Force Atlas 2 (recomendado)

PASO 5: Ajustar visualización
  → Scale: ajustar tamaño de nodos
  → Attraction/Repulsion: ajustar dispersión
  → Zoom: acercar/alejar

PASO 6: Exportar
  → File → Save map... (formato PNG o SVG)
  → Recomendado: PNG con DPI alto (300+) para publicación
""")

print("\n" + "="*60)
print("ARCHIVOS GENERADOS")
print("="*60)
print(f"\n1. {OUTPUT_MAP}")
print(f"   - {len(paises_vos)} países")
print(f"   - Pesos: citaciones, revistas, visibilidad, h-index")

print(f"\n2. {OUTPUT_NETWORK}")
print(f"   - {len(network_df)} conexiones")
print(f"   - Basadas en similitud de índice de visibilidad")

print("\n✓ ¡Archivos listos para VOSviewer!")
print("\nPara visualización rápida en Python, ejecuta:")
print("  python3 visualize_network.py")