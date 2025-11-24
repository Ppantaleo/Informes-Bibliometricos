#!/usr/bin/env python3
"""
Script para obtener datos ampliados de OpenAlex específicamente para revistas chilenas activas
Basado en chile_juojs_activas.csv y ampliando los campos disponibles en OpenAlex
"""

import pandas as pd
import requests
import time
from tqdm import tqdm
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==========================================
# CONFIGURACIÓN
# ==========================================
INPUT_FILE = 'visualizations/chile_juojs_activas.csv'
OUTPUT_FILE = 'visualizations/13_chile_openalex_ampliado.csv'
EMAIL = 'tu_email@ejemplo.com'  # OpenAlex recomienda incluir email
RATE_LIMIT_DELAY = 0.15  # segundos entre requests (max ~6 req/seg)

def get_openalex_data_ampliado(issn, email=EMAIL):
    """
    Consulta OpenAlex API para obtener datos ampliados de una revista por ISSN
    """
    # Limpiar ISSN de posibles espacios o caracteres extraños
    issn_clean = str(issn).strip().replace('\n', ',')
    
    # OpenAlex puede tener múltiples ISSNs separados por salto de línea o punto y coma
    issn_list = issn_clean.replace(';', ',').split(',')
    
    results = {
        # Campos básicos existentes
        'issn_buscado': issn_clean,
        'openalex_id': None,
        'works_count': 0,
        'cited_by_count': 0,
        'h_index': 0,
        '2yr_mean_citedness': 0,
        'is_in_openalex': False,
        'error': None,
        
        # Campos ampliados solicitados
        'is_oa': False,                    # ¿Es completamente OA?
        'is_in_doaj': False,               # ¿Está en DOAJ?
        'apc_usd': None,                   # Costo APC en dólares
        'apc_prices': [],                  # APCs en diferentes monedas
        'host_organization_name': None,    # Nombre del publisher/institución
        'host_organization': None,         # ID del publisher
        'societies': [],                   # Sociedades científicas asociadas
        'i10_index': 0,                    # i10-index (artículos con 10+ citas)
        'is_core': False,                  # ¿Es fuente "core" según CWTS?
        'counts_by_year': [],              # Works y citas por año (últimos 10 años)
        'created_date': None,              # Fecha de creación en OpenAlex
        'updated_date': None,              # Última actualización
        
        # Campos adicionales útiles
        'display_name': None,              # Nombre de la revista en OpenAlex
        'homepage_url': None,              # URL de la revista
        'country_code': None,              # Código de país
        'type': None,                      # Tipo de fuente
        'abbreviated_title': None,         # Título abreviado
        'alternate_titles': []             # Títulos alternativos
    }
    
    # Intentar con cada ISSN si hay múltiples
    for issn_single in issn_list[:3]:  # Máximo 3 intentos
        issn_single = issn_single.strip()
        if not issn_single or len(issn_single) < 8 or issn_single == 'Sin ISSN':
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
                    
                    # Campos básicos
                    results['openalex_id'] = journal.get('id', '').replace('https://openalex.org/', '')
                    results['works_count'] = journal.get('works_count', 0)
                    results['cited_by_count'] = journal.get('cited_by_count', 0)
                    results['is_in_openalex'] = True
                    results['display_name'] = journal.get('display_name', '')
                    results['homepage_url'] = journal.get('homepage_url', '')
                    results['type'] = journal.get('type', '')
                    results['abbreviated_title'] = journal.get('abbreviated_title', '')
                    results['alternate_titles'] = journal.get('alternate_titles', [])
                    results['created_date'] = journal.get('created_date', '')
                    results['updated_date'] = journal.get('updated_date', '')
                    
                    # Summary stats
                    summary = journal.get('summary_stats', {})
                    if summary:
                        results['h_index'] = summary.get('h_index', 0)
                        results['2yr_mean_citedness'] = summary.get('2yr_mean_citedness', 0)
                        results['i10_index'] = summary.get('i10_index', 0)
                    
                    # Acceso abierto
                    results['is_oa'] = journal.get('is_oa', False)
                    results['is_in_doaj'] = journal.get('is_in_doaj', False)
                    
                    # APCs
                    apc_prices = journal.get('apc_prices', [])
                    results['apc_prices'] = apc_prices
                    # Buscar APC en USD
                    for apc in apc_prices:
                        if apc.get('currency') == 'USD':
                            results['apc_usd'] = apc.get('price')
                            break
                    
                    # Host organization
                    host_org = journal.get('host_organization')
                    if host_org:
                        results['host_organization'] = host_org.get('id', '').replace('https://openalex.org/', '')
                        results['host_organization_name'] = host_org.get('display_name', '')
                    
                    # Sociedades
                    societies = journal.get('societies', [])
                    results['societies'] = [s.get('display_name', '') for s in societies if s.get('display_name')]
                    
                    # País
                    host_org_country = journal.get('host_organization_country_code')
                    results['country_code'] = host_org_country
                    
                    # Core source
                    results['is_core'] = journal.get('is_core', False)
                    
                    # Counts by year (últimos 10 años)
                    counts_by_year = journal.get('counts_by_year', [])
                    # Filtrar últimos 10 años y formatear
                    recent_counts = []
                    for count in counts_by_year[-10:]:  # Últimos 10 años
                        recent_counts.append({
                            'year': count.get('year'),
                            'works_count': count.get('works_count', 0),
                            'cited_by_count': count.get('cited_by_count', 0)
                        })
                    results['counts_by_year'] = recent_counts
                    
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

def main():
    print("=== CONSULTA AMPLIADA OPENALEX PARA REVISTAS CHILENAS ACTIVAS ===")
    
    # Cargar revistas chilenas activas
    print(f"\nCargando {INPUT_FILE}...")
    try:
        chile_activas = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"❌ Error: No se encuentra {INPUT_FILE}")
        return
    
    print(f"Total revistas chilenas activas: {len(chile_activas)}")
    
    # Filtrar solo revistas con ISSN válido
    chile_con_issn = chile_activas[
        (chile_activas['issn'].notna()) & 
        (chile_activas['issn'] != 'Sin ISSN')
    ].copy()
    
    print(f"Revistas con ISSN válido: {len(chile_con_issn)}")
    print(f"Revistas sin ISSN: {len(chile_activas) - len(chile_con_issn)}")
    
    # Consultar OpenAlex para cada revista
    print(f"\nConsultando OpenAlex API...")
    print("Esto puede tomar varios minutos...")
    
    openalex_results = []
    
    # Usar tqdm para mostrar progreso
    for idx, row in tqdm(chile_con_issn.iterrows(), total=len(chile_con_issn)):
        issn = row['issn']
        
        # Obtener datos ampliados de OpenAlex
        openalex_data = get_openalex_data_ampliado(issn)
        
        # Agregar datos de la revista original
        openalex_data['context_name'] = row['context_name']
        openalex_data['dominio'] = row['dominio']
        openalex_data['total_historico'] = row['total_historico']
        openalex_data['record_count_2023'] = row['record_count_2023']
        
        openalex_results.append(openalex_data)
        
        # Respetar rate limits
        time.sleep(RATE_LIMIT_DELAY)
        
        # Guardar progreso cada 50 revistas
        if len(openalex_results) % 50 == 0:
            temp_df = pd.DataFrame(openalex_results)
            temp_df.to_csv('chile_openalex_progress.csv', index=False)
            print(f"\n  Progreso guardado: {len(openalex_results)} revistas procesadas")
    
    # Crear DataFrame final
    print(f"\nProcesando resultados...")
    df_final = pd.DataFrame(openalex_results)
    
    # Calcular índices de visibilidad
    df_final['indice_visibilidad'] = (
        df_final['cited_by_count'] / 
        df_final['total_historico'].replace(0, 1)
    )
    
    df_final['tasa_indexacion_openalex'] = (
        df_final['works_count'] / 
        df_final['total_historico'].replace(0, 1)
    )
    
    # Guardar resultados
    df_final.to_csv(OUTPUT_FILE, index=False)
    
    # Estadísticas
    print(f"\n" + "="*60)
    print("ESTADÍSTICAS AMPLIADAS - REVISTAS CHILENAS")
    print("="*60)
    
    total_procesadas = len(df_final)
    indexadas = df_final['is_in_openalex'].sum()
    porcentaje_indexadas = (indexadas / total_procesadas) * 100
    
    print(f"\nTotal revistas procesadas: {total_procesadas}")
    print(f"Revistas encontradas en OpenAlex: {indexadas} ({porcentaje_indexadas:.1f}%)")
    print(f"Revistas NO encontradas: {total_procesadas - indexadas}")
    
    if indexadas > 0:
        indexadas_df = df_final[df_final['is_in_openalex']]
        
        print(f"\n--- MÉTRICAS BÁSICAS ---")
        print(f"Total artículos indexados: {indexadas_df['works_count'].sum():,}")
        print(f"Total citaciones: {indexadas_df['cited_by_count'].sum():,}")
        print(f"H-index promedio: {indexadas_df['h_index'].mean():.1f}")
        print(f"i10-index promedio: {indexadas_df['i10_index'].mean():.1f}")
        
        print(f"\n--- ACCESO ABIERTO ---")
        oa_count = indexadas_df['is_oa'].sum()
        doaj_count = indexadas_df['is_in_doaj'].sum()
        print(f"Revistas completamente OA: {oa_count} ({oa_count/indexadas*100:.1f}%)")
        print(f"Revistas en DOAJ: {doaj_count} ({doaj_count/indexadas*100:.1f}%)")
        
        print(f"\n--- APCs ---")
        con_apc = indexadas_df['apc_usd'].notna().sum()
        if con_apc > 0:
            apc_promedio = indexadas_df['apc_usd'].mean()
            print(f"Revistas con APC informado: {con_apc}")
            print(f"APC promedio (USD): ${apc_promedio:.0f}")
        else:
            print("No se encontraron APCs informados")
        
        print(f"\n--- CALIDAD ---")
        core_count = indexadas_df['is_core'].sum()
        print(f"Revistas 'core' (CWTS): {core_count} ({core_count/indexadas*100:.1f}%)")
        
        print(f"\n--- TOP 5 POR VISIBILIDAD ---")
        top_5 = indexadas_df.nlargest(5, 'indice_visibilidad')[
            ['context_name', 'indice_visibilidad', 'h_index', 'is_oa', 'is_in_doaj']
        ]
        for i, (_, row) in enumerate(top_5.iterrows(), 1):
            oa_status = "OA" if row['is_oa'] else "No-OA"
            doaj_status = "DOAJ" if row['is_in_doaj'] else "No-DOAJ"
            print(f"{i}. {row['context_name'][:50]}...")
            print(f"   Visibilidad: {row['indice_visibilidad']:.3f} | H-index: {row['h_index']} | {oa_status} | {doaj_status}")
    
    # Resumen de errores
    errores = df_final[df_final['error'].notna()]
    if len(errores) > 0:
        print(f"\n⚠ Advertencia: {len(errores)} revistas tuvieron errores en la consulta")
    
    # Generar gráficos
    print(f"\nGenerando gráficos...")
    generar_graficos(df_final)
    
    print(f"\n✅ Proceso completado exitosamente!")
    print(f"Archivo generado: {OUTPUT_FILE}")
    print(f"Total de columnas: {len(df_final.columns)}")
    print(f"\n📊 Gráficos generados:")
    print(f"  - 13_chile_openalex_distribucion.png")
    print(f"  - 13_chile_openalex_metricas.png")
    print(f"  - 13_chile_openalex_acceso_abierto.png")

def generar_graficos(df):
    """Genera gráficos de análisis de OpenAlex para revistas chilenas"""
    
    # Configurar estilo
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Filtrar solo revistas indexadas
    indexadas = df[df['is_in_openalex'] == True]
    
    # Gráfico 1: Distribución de indexación y acceso abierto
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1.1 Indexación en OpenAlex
    indexacion_data = ['Indexadas', 'No indexadas']
    indexacion_values = [len(indexadas), len(df) - len(indexadas)]
    colors1 = ['#2ecc71', '#e74c3c']
    
    ax1.pie(indexacion_values, labels=indexacion_data, autopct='%1.1f%%', 
            colors=colors1, startangle=90)
    ax1.set_title('Indexación en OpenAlex\n(316 revistas chilenas activas)', fontweight='bold')
    
    # 1.2 Acceso Abierto (solo indexadas)
    if len(indexadas) > 0:
        oa_data = ['Acceso Abierto', 'No OA']
        oa_values = [indexadas['is_oa'].sum(), len(indexadas) - indexadas['is_oa'].sum()]
        colors2 = ['#f39c12', '#95a5a6']
        
        ax2.pie(oa_values, labels=oa_data, autopct='%1.1f%%', 
                colors=colors2, startangle=90)
        ax2.set_title('Políticas de Acceso Abierto\n(revistas indexadas)', fontweight='bold')
    
    # 1.3 DOAJ (solo indexadas)
    if len(indexadas) > 0:
        doaj_data = ['En DOAJ', 'No DOAJ']
        doaj_values = [indexadas['is_in_doaj'].sum(), len(indexadas) - indexadas['is_in_doaj'].sum()]
        colors3 = ['#9b59b6', '#bdc3c7']
        
        ax3.pie(doaj_values, labels=doaj_data, autopct='%1.1f%%', 
                colors=colors3, startangle=90)
        ax3.set_title('Indexación en DOAJ\n(revistas indexadas)', fontweight='bold')
    
    # 1.4 Fuentes Core
    if len(indexadas) > 0:
        core_data = ['Core', 'No Core']
        core_values = [indexadas['is_core'].sum(), len(indexadas) - indexadas['is_core'].sum()]
        colors4 = ['#1abc9c', '#ecf0f1']
        
        ax4.pie(core_values, labels=core_data, autopct='%1.1f%%', 
                colors=colors4, startangle=90)
        ax4.set_title('Fuentes Core (CWTS)\n(revistas indexadas)', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('visualizations/13_chile_openalex_distribucion.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Gráfico 2: Métricas de impacto
    if len(indexadas) > 0:
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 2.1 Distribución H-index
        h_index_data = indexadas[indexadas['h_index'] > 0]['h_index']
        if len(h_index_data) > 0:
            ax1.hist(h_index_data, bins=20, color='#3498db', alpha=0.7, edgecolor='black')
            ax1.set_xlabel('H-index')
            ax1.set_ylabel('Número de revistas')
            ax1.set_title('Distribución del H-index', fontweight='bold')
            ax1.axvline(h_index_data.mean(), color='red', linestyle='--', 
                       label=f'Promedio: {h_index_data.mean():.1f}')
            ax1.legend()
        
        # 2.2 Distribución i10-index
        i10_data = indexadas[indexadas['i10_index'] > 0]['i10_index']
        if len(i10_data) > 0:
            ax2.hist(i10_data, bins=20, color='#e67e22', alpha=0.7, edgecolor='black')
            ax2.set_xlabel('i10-index')
            ax2.set_ylabel('Número de revistas')
            ax2.set_title('Distribución del i10-index', fontweight='bold')
            ax2.axvline(i10_data.mean(), color='red', linestyle='--', 
                       label=f'Promedio: {i10_data.mean():.1f}')
            ax2.legend()
        
        # 2.3 Índice de visibilidad
        vis_data = indexadas[indexadas['indice_visibilidad'] > 0]['indice_visibilidad']
        if len(vis_data) > 0:
            ax3.hist(vis_data, bins=20, color='#2ecc71', alpha=0.7, edgecolor='black')
            ax3.set_xlabel('Índice de Visibilidad')
            ax3.set_ylabel('Número de revistas')
            ax3.set_title('Distribución del Índice de Visibilidad', fontweight='bold')
            ax3.axvline(vis_data.mean(), color='red', linestyle='--', 
                       label=f'Promedio: {vis_data.mean():.3f}')
            ax3.legend()
        
        # 2.4 Scatter: H-index vs Visibilidad
        scatter_data = indexadas[(indexadas['h_index'] > 0) & (indexadas['indice_visibilidad'] > 0)]
        if len(scatter_data) > 0:
            ax4.scatter(scatter_data['h_index'], scatter_data['indice_visibilidad'], 
                       alpha=0.6, color='#9b59b6')
            ax4.set_xlabel('H-index')
            ax4.set_ylabel('Índice de Visibilidad')
            ax4.set_title('H-index vs Índice de Visibilidad', fontweight='bold')
            
            # Línea de tendencia
            if len(scatter_data) > 1:
                z = np.polyfit(scatter_data['h_index'], scatter_data['indice_visibilidad'], 1)
                p = np.poly1d(z)
                ax4.plot(scatter_data['h_index'], p(scatter_data['h_index']), "r--", alpha=0.8)
        
        plt.tight_layout()
        plt.savefig('visualizations/13_chile_openalex_metricas.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # Gráfico 3: Top revistas por categorías
    if len(indexadas) > 0:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # 3.1 Top 10 por H-index
        top_h = indexadas.nlargest(10, 'h_index')[['context_name', 'h_index']]
        if len(top_h) > 0:
            # Truncar nombres largos
            top_h['nombre_corto'] = top_h['context_name'].str[:30] + '...'
            
            bars1 = ax1.barh(range(len(top_h)), top_h['h_index'], color='#3498db')
            ax1.set_yticks(range(len(top_h)))
            ax1.set_yticklabels(top_h['nombre_corto'], fontsize=9)
            ax1.set_xlabel('H-index')
            ax1.set_title('Top 10 Revistas por H-index', fontweight='bold')
            ax1.invert_yaxis()
            
            # Agregar valores en las barras
            for i, bar in enumerate(bars1):
                width = bar.get_width()
                ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                        f'{int(width)}', ha='left', va='center', fontsize=8)
        
        # 3.2 Top 10 por Visibilidad
        top_vis = indexadas.nlargest(10, 'indice_visibilidad')[['context_name', 'indice_visibilidad']]
        if len(top_vis) > 0:
            # Truncar nombres largos
            top_vis['nombre_corto'] = top_vis['context_name'].str[:30] + '...'
            
            bars2 = ax2.barh(range(len(top_vis)), top_vis['indice_visibilidad'], color='#2ecc71')
            ax2.set_yticks(range(len(top_vis)))
            ax2.set_yticklabels(top_vis['nombre_corto'], fontsize=9)
            ax2.set_xlabel('Índice de Visibilidad')
            ax2.set_title('Top 10 Revistas por Visibilidad', fontweight='bold')
            ax2.invert_yaxis()
            
            # Agregar valores en las barras
            for i, bar in enumerate(bars2):
                width = bar.get_width()
                ax2.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                        f'{width:.3f}', ha='left', va='center', fontsize=8)
        
        plt.tight_layout()
        plt.savefig('visualizations/13_chile_openalex_acceso_abierto.png', dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    main()