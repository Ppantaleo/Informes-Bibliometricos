import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx
import numpy as np

print("="*60)
print("CREANDO VISUALIZACIÓN INTERACTIVA HTML")
print("="*60)

# ==========================================
# CARGAR DATOS
# ==========================================
print("\nCargando datos...")
df = pd.read_csv('visualizations/beacon_ojs_con_visibilidad.csv', low_memory=False)
df_openalex = df[df['is_in_openalex'] == True].copy()

map_df = pd.read_csv('visualizations/vosviewer_map.txt', sep='\t')
network_df = pd.read_csv('visualizations/vosviewer_network.txt', sep='\t', 
                         names=['source', 'target', 'weight'])

print(f"✓ {len(df_openalex)} revistas indexadas")
print(f"✓ {len(map_df)} países")

# ==========================================
# CREAR GRAFO PARA LAYOUT
# ==========================================
G = nx.Graph()
for _, row in map_df.iterrows():
    G.add_node(row['id'], **row.to_dict())

network_df_filtered = network_df[network_df['weight'] > 15]
for _, row in network_df_filtered.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['weight'])

pos = nx.spring_layout(G, k=3, iterations=100, seed=42)

# ==========================================
# FIGURA PRINCIPAL CON SUBPLOTS
# ==========================================
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Red de países (interactiva)',
        'Top 20 países por citaciones',
        'Relación citaciones vs visibilidad',
        'Distribución de índice de visibilidad'
    ),
    specs=[
        [{"type": "scatter"}, {"type": "bar"}],
        [{"type": "scatter"}, {"type": "histogram"}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.10
)

# ==========================================
# SUBPLOT 1: RED INTERACTIVA
# ==========================================
print("\nCreando red interactiva...")

# Aristas
edge_traces = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    weight = G[edge[0]][edge[1]]['weight']
    
    edge_trace = go.Scatter(
        x=[x0, x1, None],
        y=[y0, y1, None],
        mode='lines',
        line=dict(width=weight/15, color='rgba(125,125,125,0.3)'),
        hoverinfo='skip',
        showlegend=False
    )
    edge_traces.append(edge_trace)

for trace in edge_traces:
    fig.add_trace(trace, row=1, col=1)

# Nodos
node_x = []
node_y = []
node_text = []
node_size = []
node_color = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    
    node_data = G.nodes[node]
    country = node_data['label']
    citations = int(node_data['weight<citations>'])
    journals = int(node_data['weight<journals>'])
    visibility = node_data['weight<visibility>']
    h_index = node_data['weight<h_index>']
    
    node_text.append(
        f"<b>{country.upper()}</b><br>" +
        f"Revistas: {journals:,}<br>" +
        f"Citaciones: {citations:,}<br>" +
        f"Visibilidad: {visibility:.2f}<br>" +
        f"H-index: {h_index:.1f}"
    )
    
    node_size.append(np.log1p(citations) * 3)
    node_color.append(visibility)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=[G.nodes[node]['label'].upper()[:2] for node in G.nodes()],
    textposition="middle center",
    textfont=dict(size=8, color='white', family='Arial Black'),
    hovertext=node_text,
    hoverinfo='text',
    marker=dict(
        size=node_size,
        color=node_color,
        colorscale='RdYlGn',
        showscale=True,
        colorbar=dict(
            title="Visibilidad",
            thickness=15,
            len=0.4,
            x=0.46,
            y=0.85
        ),
        line=dict(width=2, color='white')
    ),
    showlegend=False
)

fig.add_trace(node_trace, row=1, col=1)

fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, row=1, col=1)
fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, row=1, col=1)

# ==========================================
# SUBPLOT 2: TOP 20 PAÍSES
# ==========================================
print("Creando gráfico de barras...")

top_20 = map_df.nlargest(20, 'weight<citations>').sort_values('weight<citations>')

colors_bar = ['#2ecc71' if vis > map_df['weight<visibility>'].median() else '#e74c3c' 
              for vis in top_20['weight<visibility>']]

fig.add_trace(
    go.Bar(
        y=top_20['label'].str.upper(),
        x=top_20['weight<citations>'],
        orientation='h',
        marker=dict(color=colors_bar),
        text=top_20['weight<citations>'].apply(lambda x: f'{x:,.0f}'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Citaciones: %{x:,.0f}<extra></extra>',
        showlegend=False
    ),
    row=1, col=2
)

fig.update_xaxes(title_text="Citaciones totales", row=1, col=2)

# ==========================================
# SUBPLOT 3: SCATTER CITACIONES VS VISIBILIDAD
# ==========================================
print("Creando scatter plot...")

map_filtered = map_df[map_df['weight<journals>'] >= 20]

fig.add_trace(
    go.Scatter(
        x=map_filtered['weight<citations>'],
        y=map_filtered['weight<visibility>'],
        mode='markers+text',
        text=map_filtered['label'].str.upper(),
        textposition='top center',
        textfont=dict(size=8),
        marker=dict(
            size=map_filtered['weight<journals>'] * 0.5,
            color=map_filtered['weight<h_index>'],
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(
                title="H-index",
                thickness=15,
                len=0.4,
                x=0.46,
                y=0.25
            ),
            line=dict(width=1, color='white')
        ),
        hovertemplate='<b>%{text}</b><br>' +
                     'Citaciones: %{x:,.0f}<br>' +
                     'Visibilidad: %{y:.2f}<br>' +
                     '<extra></extra>',
        showlegend=False
    ),
    row=2, col=1
)

fig.update_xaxes(title_text="Citaciones totales", type='log', row=2, col=1)
fig.update_yaxes(title_text="Índice de visibilidad", row=2, col=1)

# ==========================================
# SUBPLOT 4: HISTOGRAMA DE VISIBILIDAD
# ==========================================
print("Creando histograma...")

fig.add_trace(
    go.Histogram(
        x=map_df['weight<visibility>'],
        nbinsx=30,
        marker=dict(
            color='rgba(52, 152, 219, 0.7)',
            line=dict(color='white', width=1)
        ),
        hovertemplate='Visibilidad: %{x:.2f}<br>Países: %{y}<extra></extra>',
        showlegend=False
    ),
    row=2, col=2
)

# Añadir línea de mediana
median_vis = map_df['weight<visibility>'].median()
fig.add_vline(
    x=median_vis,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Mediana: {median_vis:.2f}",
    annotation_position="top",
    row=2, col=2
)

fig.update_xaxes(title_text="Índice de visibilidad", row=2, col=2)
fig.update_yaxes(title_text="Número de países", row=2, col=2)

# ==========================================
# LAYOUT GENERAL
# ==========================================
fig.update_layout(
    title=dict(
        text='<b>Análisis interactivo de visibilidad de revistas OJS por país</b>',
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    height=1000,
    showlegend=False,
    hovermode='closest',
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# ==========================================
# GUARDAR FIGURA
# ==========================================
output_html = 'visualizations/dashboard_interactivo.html'
fig.write_html(output_html)

print(f"✓ Dashboard interactivo guardado: {output_html}")
print("="*60)
print("✓ PROCESO COMPLETADO")
print("="*60)
print("Abre el archivo en tu navegador:")
print("  firefox visualizations/dashboard_interactivo.html")
print("  google-chrome visualizations/dashboard_interactivo.html")
print("O simplemente haz doble click en el archivo.")

# ==========================================
# CREAR PÁGINA HTML COMPLETA CON TABLA
# ==========================================
print("\nCreando página HTML completa con tabla...")

html_template = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard OJS - Análisis de Visibilidad</title>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        #dashboard {{
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }}
        th:hover {{
            background-color: #2980b9;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .search-box {{
            margin: 20px 0;
            padding: 10px;
            width: 100%;
            font-size: 16px;
            border: 2px solid #3498db;
            border-radius: 5px;
        }}
        .footer {{
            text-align: center;
            color: #7f8c8d;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Análisis de visibilidad de revistas OJS</h1>
        <p class="subtitle">Basado en {len(df_openalex):,} revistas indexadas en OpenAlex</p>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{len(map_df)}</div>
                <div class="stat-label">Países</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(df_openalex):,}</div>
                <div class="stat-label">Revistas indexadas</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{df_openalex['cited_by_count'].sum():,.0f}</div>
                <div class="stat-label">Citaciones totales</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{df_openalex['indice_visibilidad'].mean():.2f}</div>
                <div class="stat-label">Visibilidad promedio</div>
            </div>
        </div>
        
        <div id="dashboard"></div>
        
        <h2>🔍 Tabla de datos por país</h2>
        <input type="text" id="searchInput" class="search-box" placeholder="Buscar país...">
        
        <table id="dataTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">País ▼</th>
                    <th onclick="sortTable(1)">Revistas ▼</th>
                    <th onclick="sortTable(2)">Citaciones ▼</th>
                    <th onclick="sortTable(3)">Visibilidad ▼</th>
                    <th onclick="sortTable(4)">H-index ▼</th>
                </tr>
            </thead>
            <tbody>
"""

# Añadir filas de datos
for _, row in map_df.sort_values('weight<citations>', ascending=False).iterrows():
    html_template += f"""
                <tr>
                    <td><b>{row['label'].upper()}</b></td>
                    <td>{int(row['weight<journals>']):,}</td>
                    <td>{int(row['weight<citations>']):,}</td>
                    <td>{row['weight<visibility>']:.2f}</td>
                    <td>{row['weight<h_index>']:.1f}</td>
                </tr>
"""

html_template += """
            </tbody>
        </table>
        
        <div class="footer">
            <p>Generado con Python + Plotly | Datos de OpenAlex + PKP Beacon</p>
            <p>© 2025 - Análisis bibliométrico OJS</p>
        </div>
    </div>
    
    <script>
        // Cargar el dashboard de Plotly
        fetch('dashboard_interactivo.html')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const plotlyDiv = doc.querySelector('body > div');
                document.getElementById('dashboard').innerHTML = plotlyDiv.innerHTML;
                
                // Re-ejecutar scripts de Plotly
                const scripts = doc.querySelectorAll('script');
                scripts.forEach(script => {
                    if (script.innerHTML) {
                        eval(script.innerHTML);
                    }
                });
            });
        
        // Búsqueda en tabla
        document.getElementById('searchInput').addEventListener('keyup', function() {
            const filter = this.value.toUpperCase();
            const table = document.getElementById('dataTable');
            const tr = table.getElementsByTagName('tr');
            
            for (let i = 1; i < tr.length; i++) {
                const td = tr[i].getElementsByTagName('td')[0];
                if (td) {
                    const txtValue = td.textContent || td.innerText;
                    tr[i].style.display = txtValue.toUpperCase().indexOf(filter) > -1 ? '' : 'none';
                }
            }
        });
        
        // Ordenar tabla
        function sortTable(n) {
            const table = document.getElementById('dataTable');
            let switching = true;
            let dir = 'asc';
            let switchcount = 0;
            
            while (switching) {
                switching = false;
                const rows = table.rows;
                
                for (let i = 1; i < (rows.length - 1); i++) {
                    let shouldSwitch = false;
                    const x = rows[i].getElementsByTagName('TD')[n];
                    const y = rows[i + 1].getElementsByTagName('TD')[n];
                    
                    let xValue = x.innerHTML.replace(/,/g, '').replace(/<b>|<\\/b>/g, '');
                    let yValue = y.innerHTML.replace(/,/g, '').replace(/<b>|<\\/b>/g, '');
                    
                    if (!isNaN(xValue) && !isNaN(yValue)) {
                        xValue = parseFloat(xValue);
                        yValue = parseFloat(yValue);
                    }
                    
                    if (dir == 'asc') {
                        if (xValue > yValue) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == 'desc') {
                        if (xValue < yValue) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                }
                
                if (shouldSwitch) {
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount++;
                } else {
                    if (switchcount == 0 && dir == 'asc') {
                        dir = 'desc';
                        switching = true;
                    }
                }
            }
        }
    </script>
</body>
</html>
"""

# Guardar HTML completo
output_html_full = 'visualizations/dashboard_completo.html'
with open(output_html_full, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"✓ Dashboard completo guardado: {output_html_full}")
print("\n" + "="*60)
print("ARCHIVOS GENERADOS:")
print("="*60)
print(f"1. {output_html} - Gráficos interactivos")
print(f"2. {output_html_full} - Dashboard completo con tabla")
print("\n¡Abre cualquiera de los dos en tu navegador!")