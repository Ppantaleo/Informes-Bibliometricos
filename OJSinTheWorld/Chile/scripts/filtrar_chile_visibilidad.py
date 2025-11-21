import pandas as pd
import os

# Asegurar que el directorio visualizations existe
os.makedirs('visualizations', exist_ok=True)

# Cargar los archivos
beacon_visibilidad = pd.read_csv('visualizations/beacon_ojs_con_visibilidad.csv')
chile_activas = pd.read_csv('visualizations/chile_instalaciones_activas.csv')

# Filtrar solo las revistas de Chile del archivo de visibilidad
# Usar country_consolidated = 'cl' para identificar Chile
chile_visibilidad = beacon_visibilidad[beacon_visibilidad['country_consolidated'] == 'cl'].copy()

print(f"Total revistas en beacon_ojs_con_visibilidad: {len(beacon_visibilidad)}")
print(f"Revistas de Chile encontradas: {len(chile_visibilidad)}")

# Guardar el archivo filtrado
chile_visibilidad.to_csv('visualizations/chile_ojs_con_visibilidad.csv', index=False)

print(f"\nArchivo guardado: visualizations/chile_ojs_con_visibilidad.csv")
print(f"Columnas incluidas: {list(chile_visibilidad.columns)}")

# Mostrar algunas estadísticas
if len(chile_visibilidad) > 0:
    indexadas = chile_visibilidad['is_in_openalex'].sum()
    print(f"\nRevistas chilenas indexadas en OpenAlex: {indexadas} de {len(chile_visibilidad)} ({indexadas/len(chile_visibilidad)*100:.1f}%)")
    
    if indexadas > 0:
        indexadas_df = chile_visibilidad[chile_visibilidad['is_in_openalex']]
        print(f"Índice de visibilidad promedio: {indexadas_df['indice_visibilidad'].mean():.3f}")
        print(f"Total citaciones: {indexadas_df['cited_by_count'].sum():,}")