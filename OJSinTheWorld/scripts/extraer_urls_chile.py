import pandas as pd

# Cargar el archivo de Chile con visibilidad
chile_visibilidad = pd.read_csv('visualizations/chile_ojs_con_visibilidad.csv')

# Extraer solo la columna oai_url
urls_chile = chile_visibilidad[['oai_url']].copy()

# Guardar el archivo con solo las URLs
urls_chile.to_csv('visualizations/chile_oai_urls.csv', index=False)

print(f"Total URLs de OAI extraídas: {len(urls_chile)}")
print(f"Archivo guardado: visualizations/chile_oai_urls.csv")