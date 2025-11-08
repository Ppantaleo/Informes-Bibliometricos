import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

# ==========================================
# CONFIGURACIÓN
# ==========================================
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['font.size'] = 10

# ==========================================
# CARGAR DATOS
# ==========================================
print("Cargando datos...")
map_df = pd.read_csv('visualizations/vosviewer_map.txt', sep='\t')
network_df = pd.read_csv('visualizations/vosviewer_network.txt', sep='\t', 
                         names=['source', 'target', 'weight'])

print(f"✓ {len(map_df)} países, {len(network_df)} conexiones")

# ==========================================
# CREAR GRAFO
# ==========================================
G = nx.Graph()

# Agregar nodos con atributos
for _, row in map_df.iterrows():
    G.add_node(row['id'], 
               label=row['label'],
               citations=row['weight<citations>'],
               journals=row['weight<journals>'],
               visibility=row['weight<visibility>'],
               h_index=row['weight<h_index>'],
               cluster=row['cluster'])

# Agregar aristas (solo las más fuertes para claridad)
network_df_filtered = network_df[network_df['weight'] > 15]  # Umbral más alto
for _, row in network_df_filtered.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['weight'])

print(f"✓ Grafo: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas")

# ==========================================
# ANÁLISIS DE RED
# ==========================================
# Calcular métricas
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

# Top países
top_n = 15
top_nodes = sorted(G.nodes(), 
                   key=lambda x: G.nodes[x]['citations'], 
                   reverse=True)[:top_n]

# ==========================================
# VISUALIZACIÓN 1: RED PRINCIPAL
# ==========================================
fig, axes = plt.subplots(2, 2, figsize=(24, 20))

# --- SUBPLOT 1: Red completa ---
ax1 = axes[0, 0]
pos = nx.spring_layout(G, k=3, iterations=100, seed=42)

# Tamaño por citaciones (escala logarítmica)
node_sizes = [np.log1p(G.nodes[node]['citations']) * 150 for node in G.nodes()]

# Color por índice de visibilidad
visibilities = [G.nodes[node]['visibility'] for node in G.nodes()]
norm = plt.Normalize(vmin=min(visibilities), vmax=max(visibilities))
colors = plt.cm.RdYlGn(norm(visibilities))

# Dibujar aristas con grosor variable
edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
nx.draw_networkx_edges(G, pos, alpha=0.3, width=[w/10 for w in weights], ax=ax1)

# Dibujar nodos
nodes = nx.draw_networkx_nodes(G, pos, 
                               node_size=node_sizes,
                               node_color=visibilities,
                               cmap='RdYlGn',
                               alpha=0.8,
                               edgecolors='black',
                               linewidths=1.5,
                               ax=ax1)

# Etiquetas solo para top países
labels = {node: G.nodes[node]['label'].upper() for node in top_nodes}
nx.draw_networkx_labels(G, pos, labels, font_size=11, font_weight='bold', 
                        font_family='sans-serif', ax=ax1)

ax1.set_title('Red de países por índice de visibilidad\n(Tamaño = citaciones, Color = visibilidad)', 
              fontsize=16, fontweight='bold', pad=20)
ax1.axis('off')

# Colorbar
sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax1, fraction=0.046, pad=0.04)
cbar.set_label('Índice de visibilidad', fontsize=12, fontweight='bold')

# --- SUBPLOT 2: Top 20 países por citaciones ---
ax2 = axes[0, 1]
top_20 = map_df.nlargest(20, 'weight<citations>')

colors_bar = ['#2ecc71' if vis > map_df['weight<visibility>'].median() else '#e74c3c' 
              for vis in top_20['weight<visibility>']]

bars = ax2.barh(range(len(top_20)), top_20['weight<citations>'], color=colors_bar, alpha=0.7)
ax2.set_yticks(range(len(top_20)))
ax2.set_yticklabels(top_20['label'].str.upper())
ax2.set_xlabel('Total de citaciones', fontsize=12, fontweight='bold')
ax2.set_title('Top 20 países por citaciones totales\n(Verde = alta visibilidad, Rojo = baja visibilidad)', 
              fontsize=14, fontweight='bold', pad=15)
ax2.grid(axis='x', alpha=0.3)
ax2.invert_yaxis()

# Añadir valores
for i, (idx, row) in enumerate(top_20.iterrows()):
    ax2.text(row['weight<citations>'], i, f" {row['weight<citations>']:,.0f}", 
            va='center', fontsize=9)

# --- SUBPLOT 3: Scatter plot citaciones vs visibilidad ---
ax3 = axes[1, 0]

# Filtrar países con al menos 20 revistas para claridad
map_filtered = map_df[map_df['weight<journals>'] >= 20]

scatter = ax3.scatter(map_filtered['weight<citations>'], 
                     map_filtered['weight<visibility>'],
                     s=map_filtered['weight<journals>'] * 3,
                     c=map_filtered['weight<h_index>'],
                     cmap='plasma',
                     alpha=0.6,
                     edgecolors='black',
                     linewidth=1)

# Etiquetar países destacados
for _, row in map_filtered.nlargest(15, 'weight<citations>').iterrows():
    ax3.annotate(row['label'].upper(), 
                (row['weight<citations>'], row['weight<visibility>']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))

ax3.set_xlabel('Total de citaciones', fontsize=12, fontweight='bold')
ax3.set_ylabel('Índice de visibilidad promedio', fontsize=12, fontweight='bold')
ax3.set_title('Relación entre citaciones y visibilidad\n(Tamaño = número de revistas, Color = h-index)', 
             fontsize=14, fontweight='bold', pad=15)
ax3.grid(True, alpha=0.3)
ax3.set_xscale('log')

# Colorbar
cbar2 = plt.colorbar(scatter, ax=ax3)
cbar2.set_label('H-index promedio', fontsize=11, fontweight='bold')

# --- SUBPLOT 4: Estadísticas por cluster ---
ax4 = axes[1, 1]

# Agrupar por cluster
cluster_stats = map_df.groupby('cluster').agg({
    'label': 'count',
    'weight<citations>': 'sum',
    'weight<journals>': 'sum',
    'weight<visibility>': 'mean',
    'weight<h_index>': 'mean'
}).rename(columns={'label': 'num_paises'})

cluster_stats = cluster_stats.reset_index()

# Crear tabla
table_data = []
for _, row in cluster_stats.iterrows():
    table_data.append([
        f"Cluster {int(row['cluster'])}",
        f"{int(row['num_paises'])}",
        f"{int(row['weight<citations>']):,}",
        f"{int(row['weight<journals>']):,}",
        f"{row['weight<visibility>']:.2f}",
        f"{row['weight<h_index>']:.1f}"
    ])

table = ax4.table(cellText=table_data,
                 colLabels=['Cluster', 'Países', 'Citaciones', 'Revistas', 'Visibilidad', 'H-index'],
                 cellLoc='center',
                 loc='center',
                 bbox=[0, 0.3, 1, 0.6])

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2)

# Estilo de tabla
for i in range(len(cluster_stats) + 1):
    for j in range(6):
        cell = table[(i, j)]
        if i == 0:
            cell.set_facecolor('#3498db')
            cell.set_text_props(weight='bold', color='white')
        else:
            cell.set_facecolor('#ecf0f1' if i % 2 == 0 else 'white')

ax4.axis('off')
ax4.set_title('Estadísticas por cluster\n(Agrupación por similitud de visibilidad)', 
             fontsize=14, fontweight='bold', pad=15)

# Añadir interpretación
interpretation = (
    "Interpretación:\n"
    "• Cluster 1: Países con BAJA visibilidad relativa\n"
    "• Cluster 2: Países con ALTA visibilidad relativa\n\n"
    "La visibilidad se calcula como:\n"
    "citaciones totales / artículos publicados"
)
ax4.text(0.5, 0.15, interpretation, transform=ax4.transAxes,
        fontsize=11, verticalalignment='top', horizontalalignment='center',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ==========================================
# AJUSTES FINALES Y GUARDAR
# ==========================================
plt.suptitle('Análisis de visibilidad de revistas OJS por país', 
            fontsize=20, fontweight='bold', y=0.995)
plt.tight_layout(rect=[0, 0, 1, 0.99])

output_file = 'visualizations/network_countries_enhanced.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\n✓ Visualización mejorada guardada: {output_file}")

plt.show()

# ==========================================
# ESTADÍSTICAS ADICIONALES
# ==========================================
print("\n" + "="*60)
print("ESTADÍSTICAS DE RED")
print("="*60)

print(f"\nDensidad de red: {nx.density(G):.4f}")
print(f"Componentes conectados: {nx.number_connected_components(G)}")
print(f"Diámetro (mayor componente): {nx.diameter(max(nx.connected_components(G), key=len))}")

print("\nTop 10 países por centralidad de grado:")
top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
for node, cent in top_degree:
    country = G.nodes[node]['label']
    journals = G.nodes[node]['journals']
    print(f"  {country}: {cent:.3f} ({int(journals)} revistas)")

print("\nTop 10 países por centralidad de intermediación:")
top_between = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
for node, cent in top_between:
    country = G.nodes[node]['label']
    print(f"  {country}: {cent:.3f}")