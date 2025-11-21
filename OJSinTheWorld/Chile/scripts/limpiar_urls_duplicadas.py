import pandas as pd

# Leer el archivo línea por línea para manejar comentarios
with open('visualizations/chile_oai_urls.csv', 'r') as f:
    lines = f.readlines()

# Extraer solo las URLs (primera columna antes de cualquier coma)
urls = []
for line in lines[1:]:  # Saltar header
    if line.strip():
        url = line.split(',')[0].strip()
        urls.append(url)

# Crear DataFrame
df = pd.DataFrame({'oai_url': urls})

print(f"Total URLs originales: {len(df)}")

# Eliminar duplicados
urls_unicas = df['oai_url'].drop_duplicates()

print(f"URLs únicas encontradas: {len(urls_unicas)}")
print(f"URLs duplicadas eliminadas: {len(df) - len(urls_unicas)}")

# Crear DataFrame limpio
df_limpio = pd.DataFrame({'oai_url': urls_unicas})

# Guardar archivo limpio
df_limpio.to_csv('visualizations/chile_oai_urls_limpio.csv', index=False)

print(f"\nArchivo limpio guardado: visualizations/chile_oai_urls_limpio.csv")
print(f"Total URLs finales: {len(df_limpio)}")

# Mostrar algunas URLs duplicadas que se eliminaron
duplicadas = df['oai_url'].value_counts()
duplicadas_multiples = duplicadas[duplicadas > 1]
if len(duplicadas_multiples) > 0:
    print(f"\nURLs que aparecían múltiples veces:")
    for url, count in duplicadas_multiples.head(10).items():
        print(f"  {url} (aparecía {count} veces)")