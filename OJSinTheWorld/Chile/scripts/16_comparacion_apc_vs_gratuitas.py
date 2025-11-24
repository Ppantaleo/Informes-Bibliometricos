#!/usr/bin/env python3
"""
Comparación entre revistas que cobran APC vs revistas gratuitas
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cargar datos
df = pd.read_csv('visualizations/15_analisis_comparativo_cruzado.csv')

# Clasificar revistas
df['cobra_apc'] = df['apc_usd'].notna() & (df['apc_usd'] > 0)
df['tipo_revista'] = df['cobra_apc'].map({True: 'Con APC', False: 'Gratuitas'})

# Crear figura con 2 gráficos
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle('Comparación: Revistas con APC vs Gratuitas', fontsize=16, fontweight='bold')

# Colores
colors = {'Con APC': 'red', 'Gratuitas': 'lightblue'}

# 1. Comparación de métricas clave
ax1 = axes[0]
metricas = ['nivel1_completitud', 'nivel2_visibilidad', 'h_index', 'total_dois']
labels = ['Completitud\nMetadatos', 'Visibilidad\nAcadémica', 'H-Index', 'Total DOIs']

# Calcular promedios por tipo
apc_means = []
gratuitas_means = []

for metrica in metricas:
    apc_val = df[df['cobra_apc'] == True][metrica].mean()
    gratuitas_val = df[df['cobra_apc'] == False][metrica].mean()
    apc_means.append(apc_val if not pd.isna(apc_val) else 0)
    gratuitas_means.append(gratuitas_val if not pd.isna(gratuitas_val) else 0)

x = np.arange(len(labels))
width = 0.35

bars1 = ax1.bar(x - width/2, apc_means, width, label='Con APC', color='red', alpha=0.7)
bars2 = ax1.bar(x + width/2, gratuitas_means, width, label='Gratuitas', color='lightblue', alpha=0.7)

ax1.set_xlabel('Métricas')
ax1.set_ylabel('Valor Promedio')
ax1.set_title('Comparación de Métricas Clave')
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Añadir valores en las barras
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
             f'{height:.1f}', ha='center', va='bottom', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
             f'{height:.1f}', ha='center', va='bottom', fontsize=9)

# 2. Distribución por segmentos estratégicos
ax2 = axes[1]
segmento_counts = pd.crosstab(df['segmento'], df['tipo_revista'], normalize='columns') * 100

segmento_counts.plot(kind='bar', ax=ax2, color=['red', 'lightblue'], alpha=0.7)
ax2.set_xlabel('Segmento Estratégico')
ax2.set_ylabel('Porcentaje (%)')
ax2.set_title('Distribución por Segmento Estratégico')
ax2.legend(title='Tipo de Revista')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('visualizations/16_comparacion_apc_vs_gratuitas.png', dpi=300, bbox_inches='tight')
plt.show()

# Generar estadísticas
print("📊 ANÁLISIS COMPARATIVO: APC vs GRATUITAS")
print("="*50)

print(f"\n📈 CANTIDAD DE REVISTAS:")
print(f"   Con APC: {df['cobra_apc'].sum()} revistas")
print(f"   Gratuitas: {(~df['cobra_apc']).sum()} revistas")

print(f"\n💰 REVISTAS CON APC:")
apc_revistas = df[df['cobra_apc'] == True][['nombre_revista', 'apc_usd', 'h_index', 'segmento']]
for _, row in apc_revistas.iterrows():
    print(f"   • {row['nombre_revista']}: ${row['apc_usd']} (H-index: {row['h_index']}, {row['segmento']})")

print(f"\n📊 COMPARACIÓN DE PROMEDIOS:")
for i, metrica in enumerate(metricas):
    apc_avg = apc_means[i]
    gratuitas_avg = gratuitas_means[i]
    diferencia = ((apc_avg - gratuitas_avg) / gratuitas_avg * 100) if gratuitas_avg > 0 else 0
    print(f"   {labels[i]}: APC={apc_avg:.2f} vs Gratuitas={gratuitas_avg:.2f} ({diferencia:+.1f}%)")

print(f"\n🎯 DISTRIBUCIÓN POR SEGMENTOS:")
for segmento in df['segmento'].unique():
    apc_count = len(df[(df['segmento'] == segmento) & (df['cobra_apc'] == True)])
    gratuitas_count = len(df[(df['segmento'] == segmento) & (df['cobra_apc'] == False)])
    total_segmento = apc_count + gratuitas_count
    if total_segmento > 0:
        apc_pct = (apc_count / total_segmento) * 100
        print(f"   {segmento}: {apc_pct:.1f}% con APC ({apc_count}/{total_segmento})")

print(f"\n✅ Gráfico guardado: visualizations/16_comparacion_apc_vs_gratuitas.png")