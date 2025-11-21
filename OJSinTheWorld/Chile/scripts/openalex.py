import pandas as pd
import requests
import time
from tqdm import tqdm
import json

# ==========================================
# CONFIGURACIÓN
# ==========================================
BEACON_FILE = '../../beacon_ojs.csv'
OUTPUT_FILE = 'visualizations/beacon_ojs_con_visibilidad.csv'
EMAIL = 'tu_email@ejemplo.com'  # OpenAlex recomienda incluir email
RATE_LIMIT_DELAY = 0.15  # segundos entre requests (max ~6 req/seg)

# ==========================================
# FUNCIÓN PARA CONSULTAR OPENALEX
# ==========================================
def get_openalex_data(issn, email=EMAIL):
    """
    Consulta OpenAlex API para obtener datos de una revista por ISSN
    """
    # Limpiar ISSN de posibles espacios o caracteres extraños
    issn_clean = str(issn).strip().replace('\n', ',')
    
    # OpenAlex puede tener múltiples ISSNs separados por salto de línea
    # Tomamos el primero
    issn_list = issn_clean.split(',')
    
    results = {
        'issn_buscado': issn_clean,
        'openalex_id': None,
        'works_count': 0,
        'cited_by_count': 0,
        'h_index': 0,
        '2yr_mean_citedness': 0,
        'is_in_openalex': False,
        'error': None
    }
    
    # Intentar con cada ISSN si hay múltiples
    for issn_single in issn_list[:3]:  # Máximo 3 intentos
        issn_single = issn_single.strip()
        if not issn_single or len(issn_single) < 8:
            continue
            
        try:
            url = f"https://api.openalex.org/sources"
            params = {
                'filter': f'issn:{issn_single}',
                'mailto': email
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('results') and len(data['results']) > 0:
                    journal = data['results'][0]
                    
                    results['openalex_id'] = journal.get('id', '').replace('https://openalex.org/', '')
                    results['works_count'] = journal.get('works_count', 0)
                    results['cited_by_count'] = journal.get('cited_by_count', 0)
                    results['is_in_openalex'] = True
                    
                    # Summary stats (pueden ser None)
                    summary = journal.get('summary_stats', {})
                    if summary:
                        results['h_index'] = summary.get('h_index', 0)
                        results['2yr_mean_citedness'] = summary.get('2yr_mean_citedness', 0)
                    
                    # Si encontramos datos, salimos del loop
                    break
                    
            elif response.status_code == 429:
                results['error'] = 'Rate limit exceeded'
                time.sleep(2)  # Esperar más si hay rate limit
                
        except requests.exceptions.Timeout:
            results['error'] = 'Timeout'
        except requests.exceptions.RequestException as e:
            results['error'] = f'Request error: {str(e)}'
        except Exception as e:
            results['error'] = f'Unexpected error: {str(e)}'
    
    return results

# ==========================================
# CARGAR DATOS DEL BEACON
# ==========================================
print("Cargando beacon.tab...")
beacon = pd.read_csv(BEACON_FILE, low_memory=False)

print(f"Total de revistas en beacon: {len(beacon)}")
print(f"Revistas con ISSN: {beacon['issn'].notna().sum()}")

# Filtrar solo revistas con ISSN válido
beacon_con_issn = beacon[beacon['issn'].notna()].copy()
print(f"Procesaremos {len(beacon_con_issn)} revistas")

# ==========================================
# CONSULTAR OPENALEX PARA CADA REVISTA
# ==========================================
print("\nConsultando OpenAlex API...")
print("Esto puede tomar varios minutos dependiendo del tamaño del dataset")

openalex_results = []

# Usar tqdm para mostrar progreso
for idx, row in tqdm(beacon_con_issn.iterrows(), total=len(beacon_con_issn)):
    issn = row['issn']
    
    # Obtener datos de OpenAlex
    openalex_data = get_openalex_data(issn)
    openalex_results.append(openalex_data)
    
    # Respetar rate limits
    time.sleep(RATE_LIMIT_DELAY)
    
    # Guardar progreso cada 1000 revistas
    if len(openalex_results) % 1000 == 0:
        temp_df = pd.DataFrame(openalex_results)
        temp_df.to_csv('openalex_progress.csv', index=False)
        print(f"\n  Progreso guardado: {len(openalex_results)} revistas procesadas")

# ==========================================
# COMBINAR DATOS Y CALCULAR ÍNDICES
# ==========================================
print("\nCombinando datos y calculando índices...")

# Crear DataFrame con resultados de OpenAlex
openalex_df = pd.DataFrame(openalex_results)

# Combinar con beacon original
beacon_enriched = pd.concat([
    beacon_con_issn.reset_index(drop=True),
    openalex_df
], axis=1)

# ==========================================
# CALCULAR ÍNDICE DE VISIBILIDAD
# ==========================================
print("\nCalculando índice de visibilidad...")

# Índice de visibilidad = citaciones / total de artículos publicados
beacon_enriched['indice_visibilidad'] = (
    beacon_enriched['cited_by_count'] / 
    beacon_enriched['total_record_count'].replace(0, 1)  # Evitar división por cero
)

# Índice de visibilidad ajustado = citaciones / artículos indexados en OpenAlex
beacon_enriched['indice_visibilidad_ajustado'] = (
    beacon_enriched['cited_by_count'] / 
    beacon_enriched['works_count'].replace(0, 1)
)

# Tasa de indexación en OpenAlex
beacon_enriched['tasa_indexacion_openalex'] = (
    beacon_enriched['works_count'] / 
    beacon_enriched['total_record_count'].replace(0, 1)
)

# ==========================================
# ESTADÍSTICAS DESCRIPTIVAS
# ==========================================
print("\n" + "="*60)
print("ESTADÍSTICAS GENERALES")
print("="*60)

total_revistas = len(beacon_enriched)
indexadas = beacon_enriched['is_in_openalex'].sum()
porcentaje = (indexadas / total_revistas) * 100

print(f"\nTotal de revistas procesadas: {total_revistas}")
print(f"Revistas encontradas en OpenAlex: {indexadas} ({porcentaje:.1f}%)")
print(f"Revistas NO encontradas: {total_revistas - indexadas}")

if indexadas > 0:
    print("\n" + "-"*60)
    print("MÉTRICAS DE REVISTAS INDEXADAS EN OPENALEX")
    print("-"*60)
    
    indexadas_df = beacon_enriched[beacon_enriched['is_in_openalex']]
    
    print(f"\nTotal de artículos indexados: {indexadas_df['works_count'].sum():,}")
    print(f"Total de citaciones: {indexadas_df['cited_by_count'].sum():,}")
    
    print(f"\nÍndice de visibilidad promedio: {indexadas_df['indice_visibilidad'].mean():.3f}")
    print(f"Índice de visibilidad mediano: {indexadas_df['indice_visibilidad'].median():.3f}")
    print(f"Índice de visibilidad máximo: {indexadas_df['indice_visibilidad'].max():.3f}")
    
    print(f"\nH-index promedio: {indexadas_df['h_index'].mean():.1f}")
    print(f"H-index mediano: {indexadas_df['h_index'].median():.1f}")
    print(f"H-index máximo: {indexadas_df['h_index'].max():.0f}")
    
    print(f"\nTasa de indexación promedio: {indexadas_df['tasa_indexacion_openalex'].mean():.1%}")

# ==========================================
# TOP REVISTAS POR VISIBILIDAD
# ==========================================
print("\n" + "="*60)
print("TOP 10 REVISTAS POR ÍNDICE DE VISIBILIDAD")
print("="*60)

top_visibility = beacon_enriched[
    beacon_enriched['is_in_openalex']
].nlargest(10, 'indice_visibilidad')[
    ['context_name', 'country_consolidated', 'total_record_count', 
     'cited_by_count', 'indice_visibilidad', 'h_index']
]

print(top_visibility.to_string(index=False))

# ==========================================
# GUARDAR RESULTADOS
# ==========================================
print(f"\nGuardando resultados en {OUTPUT_FILE}...")
beacon_enriched.to_csv(OUTPUT_FILE, index=False)

print("\n✓ Proceso completado exitosamente!")
print(f"\nArchivo generado: {OUTPUT_FILE}")
print(f"Total de columnas: {len(beacon_enriched.columns)}")

# ==========================================
# RESUMEN DE ERRORES
# ==========================================
errores = beacon_enriched[beacon_enriched['error'].notna()]
if len(errores) > 0:
    print(f"\n⚠ Advertencia: {len(errores)} revistas tuvieron errores en la consulta")
    print("Ver columna 'error' en el archivo de salida para detalles")