#!/usr/bin/env python3
"""
Script para obtener datos ampliados de Crossref para revistas chilenas activas
Basado en chile_juojs_activas.csv y obteniendo métricas de cobertura, DOIs y versiones
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
OUTPUT_FILE = 'visualizations/14_chile_crossref_ampliado.csv'
EMAIL = 'tu_email@ejemplo.com'  # Crossref recomienda incluir email
RATE_LIMIT_DELAY = 0.2  # segundos entre requests
BASE_URL = 'https://api.crossref.org'

# Relaciones que indican versiones
RELATION_TYPES = {
    'is-preprint-of': 'Este DOI es preprint de...',
    'has-preprint': 'Este DOI tiene como preprint...',
    'is-version-of': 'Este DOI es versión de...',
    'has-version': 'Este DOI tiene versiones...',
    'is-same-as': 'Este DOI es el mismo que...',
    'is-replaced-by': 'Este DOI fue reemplazado por...',
    'replaces': 'Este DOI reemplaza a...',
}

def get_crossref_data_ampliado(issn, email=EMAIL):
    """
    Consulta Crossref API para obtener datos ampliados de una revista por ISSN
    """
    # Limpiar ISSN
    issn_clean = str(issn).strip().replace('\n', ',')
    issn_list = issn_clean.replace(';', ',').split(',')
    
    results = {
        # Campos básicos
        'issn_buscado': issn_clean,
        'crossref_id': None,
        'is_in_crossref': False,
        'error': None,
        'last_status_check_time': None,
        
        # Conteos de DOIs
        'current_dois': 0,
        'backfile_dois': 0,
        'total_dois': 0,
        
        # Cobertura actual (current)
        'affiliations_current': 0.0,
        'abstracts_current': 0.0,
        'licenses_current': 0.0,
        'orcids_current': 0.0,
        'update_policies_current': 0.0,
        'ror_ids_current': 0.0,
        'similarity_checking_current': 0.0,
        'funders_current': 0.0,
        'award_numbers_current': 0.0,
        'references_current': 0.0,
        
        # Cobertura histórica (backfile)
        'affiliations_backfile': 0.0,
        'abstracts_backfile': 0.0,
        'licenses_backfile': 0.0,
        'orcids_backfile': 0.0,
        'update_policies_backfile': 0.0,
        'ror_ids_backfile': 0.0,
        'similarity_checking_backfile': 0.0,
        'funders_backfile': 0.0,
        'award_numbers_backfile': 0.0,
        'references_backfile': 0.0,
        
        # Relaciones de versiones y preprints
        'has_preprints': 0,
        'is_preprint_count': 0,
        'has_versions': 0,
        'is_version_count': 0,
        'replacement_relations': 0,
        'same_as_relations': 0,
        'total_version_relations': 0,
        
        # Información adicional
        'title': None,
        'publisher': None,
        'subject': [],
        'flags': [],
        'breakdowns': {}
    }
    
    # Intentar con cada ISSN
    for issn_single in issn_list[:3]:
        issn_single = issn_single.strip()
        if not issn_single or len(issn_single) < 8 or issn_single == 'Sin ISSN':
            continue
            
        try:
            # Consultar información de la revista
            url = f"{BASE_URL}/journals/{issn_single}"
            headers = {'User-Agent': f'mailto:{email}'}
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'message' in data:
                    journal = data['message']
                    
                    # Información básica
                    results['crossref_id'] = issn_single
                    results['is_in_crossref'] = True
                    results['title'] = journal.get('title', '')
                    results['publisher'] = journal.get('publisher', '')
                    results['subject'] = journal.get('subject', [])
                    results['flags'] = journal.get('flags', [])
                    results['last_status_check_time'] = journal.get('last-status-check-time')
                    
                    # Conteos de DOIs
                    counts = journal.get('counts', {})
                    results['current_dois'] = counts.get('current-dois', 0)
                    results['backfile_dois'] = counts.get('backfile-dois', 0)
                    results['total_dois'] = counts.get('total-dois', 0)
                    
                    # Cobertura
                    coverage = journal.get('coverage', {})
                    
                    # Cobertura actual
                    results['affiliations_current'] = coverage.get('affiliations-current', 0.0)
                    results['abstracts_current'] = coverage.get('abstracts-current', 0.0)
                    results['licenses_current'] = coverage.get('licenses-current', 0.0)
                    results['orcids_current'] = coverage.get('orcids-current', 0.0)
                    results['update_policies_current'] = coverage.get('update-policies-current', 0.0)
                    results['ror_ids_current'] = coverage.get('ror-ids-current', 0.0)
                    results['similarity_checking_current'] = coverage.get('similarity-checking-current', 0.0)
                    results['funders_current'] = coverage.get('funders-current', 0.0)
                    results['award_numbers_current'] = coverage.get('award-numbers-current', 0.0)
                    results['references_current'] = coverage.get('references-current', 0.0)
                    
                    # Cobertura backfile
                    results['affiliations_backfile'] = coverage.get('affiliations-backfile', 0.0)
                    results['abstracts_backfile'] = coverage.get('abstracts-backfile', 0.0)
                    results['licenses_backfile'] = coverage.get('licenses-backfile', 0.0)
                    results['orcids_backfile'] = coverage.get('orcids-backfile', 0.0)
                    results['update_policies_backfile'] = coverage.get('update-policies-backfile', 0.0)
                    results['ror_ids_backfile'] = coverage.get('ror-ids-backfile', 0.0)
                    results['similarity_checking_backfile'] = coverage.get('similarity-checking-backfile', 0.0)
                    results['funders_backfile'] = coverage.get('funders-backfile', 0.0)
                    results['award_numbers_backfile'] = coverage.get('award-numbers-backfile', 0.0)
                    results['references_backfile'] = coverage.get('references-backfile', 0.0)
                    
                    # Breakdowns
                    results['breakdowns'] = journal.get('breakdowns', {})
                    
                    # Consultar relaciones de versiones (muestra de artículos)
                    if results['total_dois'] > 0:
                        version_stats = get_version_relations(issn_single, email)
                        results.update(version_stats)
                    
                    break
                    
            elif response.status_code == 404:
                results['error'] = 'Journal not found in Crossref'
            elif response.status_code == 429:
                results['error'] = 'Rate limit exceeded'
                time.sleep(5)
                
        except requests.exceptions.Timeout:
            results['error'] = 'Timeout'
        except requests.exceptions.RequestException as e:
            results['error'] = f'Request error: {str(e)}'
        except Exception as e:
            results['error'] = f'Unexpected error: {str(e)}'
    
    return results

def get_version_relations(issn, email, sample_size=50):
    """
    Analiza una muestra de artículos para detectar relaciones de versiones y preprints
    """
    version_stats = {
        'has_preprints': 0,
        'is_preprint_count': 0,
        'has_versions': 0,
        'is_version_count': 0,
        'replacement_relations': 0,
        'same_as_relations': 0,
        'total_version_relations': 0
    }
    
    try:
        # Consultar muestra de artículos de la revista
        url = f"{BASE_URL}/works"
        params = {
            'filter': f'issn:{issn}',
            'rows': sample_size,
            'mailto': email
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            works = data.get('message', {}).get('items', [])
            
            for work in works:
                relations = work.get('relation', {})
                
                for relation_type, relation_list in relations.items():
                    if relation_type in RELATION_TYPES and relation_list:
                        version_stats['total_version_relations'] += len(relation_list)
                        
                        if relation_type == 'has-preprint':
                            version_stats['has_preprints'] += len(relation_list)
                        elif relation_type == 'is-preprint-of':
                            version_stats['is_preprint_count'] += len(relation_list)
                        elif relation_type == 'has-version':
                            version_stats['has_versions'] += len(relation_list)
                        elif relation_type == 'is-version-of':
                            version_stats['is_version_count'] += len(relation_list)
                        elif relation_type in ['is-replaced-by', 'replaces']:
                            version_stats['replacement_relations'] += len(relation_list)
                        elif relation_type == 'is-same-as':
                            version_stats['same_as_relations'] += len(relation_list)
                            
    except Exception as e:
        print(f"Error obteniendo relaciones de versiones para {issn}: {e}")
    
    return version_stats

def main():
    """Función principal"""
    print("=" * 60)
    print("ANÁLISIS AMPLIADO DE CROSSREF - REVISTAS CHILENAS ACTIVAS")
    print("=" * 60)
    
    # Cargar datos de revistas chilenas activas
    try:
        df_revistas = pd.read_csv(INPUT_FILE)
        print(f"Cargadas {len(df_revistas)} revistas chilenas activas")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {INPUT_FILE}")
        return
    
    # Procesar cada revista
    resultados = []
    
    for idx, row in tqdm(df_revistas.iterrows(), total=len(df_revistas), desc="Consultando Crossref"):
        issn = row.get('issn', '')
        nombre_revista = row.get('context_name', 'Sin nombre')
        
        print(f"\nProcesando: {nombre_revista} (ISSN: {issn})")
        
        # Obtener datos de Crossref
        crossref_data = get_crossref_data_ampliado(issn)
        
        # Combinar con datos originales
        resultado = {
            'nombre_revista': nombre_revista,
            'issn_original': issn,
            'url_ojs': row.get('url', ''),
            'institucion': row.get('institucion', ''),
            'region': row.get('region', ''),
            **crossref_data
        }
        
        resultados.append(resultado)
        
        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)
    
    # Crear DataFrame con resultados
    df_resultados = pd.DataFrame(resultados)
    
    # Guardar CSV completo
    df_resultados.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"\nResultados guardados en: {OUTPUT_FILE}")
    
    # Generar análisis y gráficas
    generar_analisis_graficas(df_resultados)
    
    # Mostrar resumen
    mostrar_resumen(df_resultados)

def generar_analisis_graficas(df):
    """Genera gráficas y análisis de los datos de Crossref"""
    
    # Configurar estilo
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 1. Distribución de revistas en Crossref
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Análisis Crossref - Revistas Chilenas Activas', fontsize=16, fontweight='bold')
    
    # Gráfica 1: Presencia en Crossref
    crossref_counts = df['is_in_crossref'].value_counts()
    axes[0,0].pie(crossref_counts.values, labels=['En Crossref', 'No en Crossref'], 
                  autopct='%1.1f%%', startangle=90)
    axes[0,0].set_title('Presencia en Crossref')
    
    # Gráfica 2: Distribución de DOIs totales
    df_crossref = df[df['is_in_crossref'] == True]
    if len(df_crossref) > 0:
        axes[0,1].hist(df_crossref['total_dois'], bins=20, alpha=0.7, color='skyblue')
        axes[0,1].set_title('Distribución de DOIs Totales')
        axes[0,1].set_xlabel('Número de DOIs')
        axes[0,1].set_ylabel('Frecuencia')
    
    # Gráfica 3: Cobertura de metadatos (current)
    if len(df_crossref) > 0:
        cobertura_cols = ['abstracts_current', 'licenses_current', 'orcids_current', 
                         'affiliations_current', 'references_current']
        cobertura_means = df_crossref[cobertura_cols].mean() * 100
        
        axes[1,0].bar(range(len(cobertura_means)), cobertura_means.values, 
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
        axes[1,0].set_title('Cobertura Promedio de Metadatos (Actual)')
        axes[1,0].set_ylabel('Porcentaje (%)')
        axes[1,0].set_xticks(range(len(cobertura_means)))
        axes[1,0].set_xticklabels(['Resúmenes', 'Licencias', 'ORCIDs', 'Afiliaciones', 'Referencias'], 
                                  rotation=45, ha='right')
    
    # Gráfica 4: Relaciones de versiones
    if len(df_crossref) > 0:
        version_cols = ['has_preprints', 'is_preprint_count', 'has_versions', 'replacement_relations']
        version_totals = df_crossref[version_cols].sum()
        
        if version_totals.sum() > 0:
            axes[1,1].bar(range(len(version_totals)), version_totals.values, 
                          color=['#E17055', '#74B9FF', '#A29BFE', '#FD79A8'])
            axes[1,1].set_title('Relaciones de Versiones y Preprints')
            axes[1,1].set_ylabel('Cantidad Total')
            axes[1,1].set_xticks(range(len(version_totals)))
            axes[1,1].set_xticklabels(['Tiene Preprints', 'Es Preprint', 'Tiene Versiones', 'Reemplazos'], 
                                      rotation=45, ha='right')
        else:
            axes[1,1].text(0.5, 0.5, 'Sin relaciones\nde versiones', 
                          ha='center', va='center', transform=axes[1,1].transAxes)
            axes[1,1].set_title('Relaciones de Versiones y Preprints')
    
    plt.tight_layout()
    plt.savefig('visualizations/14_crossref_analisis_general.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Gráfica de cobertura comparativa (current vs backfile)
    if len(df_crossref) > 0:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        metrics = ['abstracts', 'licenses', 'orcids', 'affiliations', 'references']
        current_means = [df_crossref[f'{m}_current'].mean() * 100 for m in metrics]
        backfile_means = [df_crossref[f'{m}_backfile'].mean() * 100 for m in metrics]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        ax.bar(x - width/2, current_means, width, label='Actual', alpha=0.8, color='#3498db')
        ax.bar(x + width/2, backfile_means, width, label='Histórico', alpha=0.8, color='#e74c3c')
        
        ax.set_xlabel('Tipo de Metadato')
        ax.set_ylabel('Cobertura Promedio (%)')
        ax.set_title('Comparación de Cobertura: Actual vs Histórico')
        ax.set_xticks(x)
        ax.set_xticklabels(['Resúmenes', 'Licencias', 'ORCIDs', 'Afiliaciones', 'Referencias'])
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('visualizations/14_crossref_cobertura_comparativa.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # 3. Top revistas por DOIs
    if len(df_crossref) > 0:
        top_revistas = df_crossref.nlargest(10, 'total_dois')[['nombre_revista', 'total_dois', 'current_dois', 'backfile_dois']]
        
        if len(top_revistas) > 0:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            x = range(len(top_revistas))
            ax.barh(x, top_revistas['backfile_dois'], label='DOIs Históricos', color='#95a5a6')
            ax.barh(x, top_revistas['current_dois'], left=top_revistas['backfile_dois'], 
                   label='DOIs Actuales', color='#3498db')
            
            ax.set_yticks(x)
            ax.set_yticklabels([name[:30] + '...' if len(name) > 30 else name 
                               for name in top_revistas['nombre_revista']], fontsize=9)
            ax.set_xlabel('Número de DOIs')
            ax.set_title('Top 10 Revistas por Cantidad de DOIs en Crossref')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='x')
            
            plt.tight_layout()
            plt.savefig('visualizations/14_crossref_top_revistas_dois.png', dpi=300, bbox_inches='tight')
            plt.show()

def mostrar_resumen(df):
    """Muestra resumen estadístico de los resultados"""
    print("\n" + "="*60)
    print("RESUMEN DE RESULTADOS")
    print("="*60)
    
    total_revistas = len(df)
    en_crossref = df['is_in_crossref'].sum()
    porcentaje_crossref = (en_crossref / total_revistas) * 100
    
    print(f"Total de revistas analizadas: {total_revistas}")
    print(f"Revistas encontradas en Crossref: {en_crossref} ({porcentaje_crossref:.1f}%)")
    
    if en_crossref > 0:
        df_crossref = df[df['is_in_crossref'] == True]
        
        print(f"\nDOIs registrados:")
        print(f"  - Total de DOIs: {df_crossref['total_dois'].sum():,}")
        print(f"  - DOIs actuales: {df_crossref['current_dois'].sum():,}")
        print(f"  - DOIs históricos: {df_crossref['backfile_dois'].sum():,}")
        print(f"  - Promedio DOIs por revista: {df_crossref['total_dois'].mean():.1f}")
        
        print(f"\nCobertura promedio de metadatos (actuales):")
        print(f"  - Resúmenes: {df_crossref['abstracts_current'].mean()*100:.1f}%")
        print(f"  - Licencias: {df_crossref['licenses_current'].mean()*100:.1f}%")
        print(f"  - ORCIDs: {df_crossref['orcids_current'].mean()*100:.1f}%")
        print(f"  - Afiliaciones: {df_crossref['affiliations_current'].mean()*100:.1f}%")
        print(f"  - Referencias: {df_crossref['references_current'].mean()*100:.1f}%")
        
        print(f"\nRelaciones de versiones:")
        print(f"  - Artículos con preprints: {df_crossref['has_preprints'].sum()}")
        print(f"  - Artículos que son preprints: {df_crossref['is_preprint_count'].sum()}")
        print(f"  - Artículos con versiones: {df_crossref['has_versions'].sum()}")
        print(f"  - Total relaciones de versión: {df_crossref['total_version_relations'].sum()}")
        
        # Top 5 revistas por DOIs
        print(f"\nTop 5 revistas por cantidad de DOIs:")
        top5 = df_crossref.nlargest(5, 'total_dois')[['nombre_revista', 'total_dois']]
        for idx, row in top5.iterrows():
            print(f"  {row['nombre_revista'][:50]}: {row['total_dois']:,} DOIs")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()