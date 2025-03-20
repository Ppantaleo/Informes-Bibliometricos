import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# Configuración
csv_path = '/home/patricio/Escritorio/DOAJ-Geo-Analysis/doaj_journals_complete.csv'
output_dir = '/home/patricio/Escritorio/DOAJ-Geo-Analysis/outputs'

# Crear directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directorio de salida creado: {output_dir}")

# Configuración para visualización
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 12

# Cargar el CSV
print(f"Cargando datos desde: {csv_path}")
try:
    df = pd.read_csv(csv_path)
    print(f"Archivo cargado exitosamente con {len(df)} registros")
except Exception as e:
    print(f"Error al cargar el archivo: {str(e)}")
    exit(1)

# Verificar la columna publisher_name
if 'publisher_name' not in df.columns:
    print("La columna 'publisher_name' no existe en el dataset.")
    
    # Buscar columnas alternativas
    publisher_cols = [col for col in df.columns if 'publisher' in col.lower()]
    if publisher_cols:
        publisher_col = publisher_cols[0]
        print(f"Usando columna alternativa: {publisher_col}")
    else:
        print("No se encontró ninguna columna relacionada con el editor.")
        exit(1)
else:
    publisher_col = 'publisher_name'

# Limpiar y analizar los datos de editores
print("\nAnalizando datos de editores...")

# Reemplazar valores nulos
df[publisher_col] = df[publisher_col].fillna("No especificado")

# Función para limpiar nombres de editores
def clean_publisher_name(name):
    if pd.isna(name) or name == "":
        return "No especificado"
    
    # Convertir a minúsculas para normalizar
    name = name.strip().lower()
    
    # Eliminar texto entre paréntesis
    name = re.sub(r'\([^)]*\)', '', name)
    
    # Eliminar caracteres especiales y normalizar espacios
    name = re.sub(r'[^\w\s]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Convertir primera letra a mayúscula
    if name:
        return name.capitalize()
    return "No especificado"

# Aplicar limpieza
df['publisher_cleaned'] = df[publisher_col].apply(clean_publisher_name)

# Contar por editor
publisher_counts = df['publisher_cleaned'].value_counts()

# Mostrar estadísticas
total_publishers = len(publisher_counts)
print(f"Total de editores únicos: {total_publishers}")

# Top editores
top_50_publishers = publisher_counts.head(50)
print("\nTop 50 editores por número de revistas:")
for i, (publisher, count) in enumerate(top_50_publishers.items(), 1):
    print(f"{i}. {publisher}: {count}")

# Calcular concentración de mercado
top_10_percentage = publisher_counts.head(10).sum() / len(df) * 100
top_20_percentage = publisher_counts.head(20).sum() / len(df) * 100
print(f"\nConcentración de mercado:")
print(f"Top 10 editores: {top_10_percentage:.2f}% de todas las revistas")
print(f"Top 20 editores: {top_20_percentage:.2f}% de todas las revistas")

# Agrupar editores más pequeños - MODIFICADO para mostrar top 20 individualmente
threshold = 20  # Mostrar top 20 individualmente
top_publishers = publisher_counts.head(threshold).index
df['publisher_group'] = df['publisher_cleaned'].apply(
    lambda x: x if x in top_publishers else "Otros editores")

# Contar por grupo
publisher_group_counts = df['publisher_group'].value_counts()

# Visualización: Top 20 editores + otros
plt.figure(figsize=(16, 12))  # Aumentado el tamaño para mejor visualización
ax = sns.barplot(x=publisher_group_counts.values, y=publisher_group_counts.index, palette="viridis")
plt.title('Top 20 Editores por Número de Revistas en DOAJ', fontsize=18)
plt.xlabel('Número de Revistas', fontsize=14)
plt.ylabel('Editor', fontsize=14)

# Añadir valores a las barras
for i, v in enumerate(publisher_group_counts.values):
    ax.text(v + 5, i, str(v), va='center')

plt.tight_layout()
output_file = os.path.join(output_dir, 'doaj_top20_publishers.jpg')
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nGráfico guardado como: {output_file}")

# Visualización: Distribución de tamaño de editores
plt.figure(figsize=(12, 8))
publisher_size_bins = [1, 2, 3, 5, 10, 20, 50, 100, 500, 1000, float('inf')]
publisher_size_labels = ['1', '2', '3-5', '6-10', '11-20', '21-50', '51-100', '101-500', '501-1000', '1000+']

# Contar editores por tamaño
size_counts = []
for i in range(len(publisher_size_bins)-1):
    min_val, max_val = publisher_size_bins[i], publisher_size_bins[i+1]
    count = len(publisher_counts[(publisher_counts >= min_val) & (publisher_counts < max_val)])
    size_counts.append(count)

# Crear gráfico de barras
plt.bar(publisher_size_labels, size_counts, color='skyblue')
plt.title('Distribución de Editores por Tamaño (Número de Revistas)', fontsize=16)
plt.xlabel('Número de Revistas', fontsize=14)
plt.ylabel('Número de Editores', fontsize=14)
plt.xticks(rotation=45)

for i, v in enumerate(size_counts):
    plt.text(i, v + 5, str(v), ha='center')

plt.tight_layout()
output_file = os.path.join(output_dir, 'doaj_publisher_size_distribution.jpg')
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Gráfico de distribución guardado como: {output_file}")

# Crear un gráfico de pastel para visualizar la concentración de mercado
plt.figure(figsize=(12, 12))
top20_values = publisher_counts.head(20).values
top20_labels = publisher_counts.head(20).index
others_value = publisher_counts[20:].sum()

# Combinar valores y etiquetas
values = list(top20_values) + [others_value]
labels = [f"{label} ({value})" for label, value in zip(top20_labels, top20_values)]
labels.append(f"Otros editores ({others_value})")

# Crear explode para destacar los primeros 3 editores
explode = [0.1, 0.05, 0.02] + [0] * 18 + [0]

# Generar el gráfico de pastel
plt.pie(values, labels=None, autopct='%1.1f%%', startangle=90, explode=explode, 
        shadow=True, colors=plt.cm.tab20.colors)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.title('Concentración del Mercado de Editores en DOAJ', fontsize=20)

# Añadir leyenda separada
plt.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
plt.tight_layout()

output_file = os.path.join(output_dir, 'doaj_publisher_market_share.jpg')
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Gráfico de participación de mercado guardado como: {output_file}")

# Guardar resultados en CSV
# Top 100 editores
top_100_df = pd.DataFrame({
    'Editor': publisher_counts.head(100).index,
    'Número de Revistas': publisher_counts.head(100).values,
    'Porcentaje': (publisher_counts.head(100).values / len(df) * 100).round(2)
})

csv_output = os.path.join(output_dir, 'doaj_top100_publishers.csv')
top_100_df.to_csv(csv_output, index=False)
print(f"\nDatos de top 100 editores exportados a: {csv_output}")

print("\nAnálisis de editores completado con éxito.")