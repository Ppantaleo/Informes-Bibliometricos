#!/usr/bin/env python3
"""
Script para análisis comparativo cruzado entre Dialnet, OpenAlex y Crossref
Identifica variables novedosas y patrones de correlación entre las tres fuentes
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# CONFIGURACIÓN
# ==========================================
DIALNET_FILE = 'visualizations/dialnet_informes_procesados.csv'
OPENALEX_FILE = 'visualizations/13_chile_openalex_ampliado.csv'
CROSSREF_FILE = 'visualizations/14_chile_crossref_ampliado.csv'
OUTPUT_FILE = 'visualizations/15_analisis_comparativo_cruzado.csv'

def load_and_prepare_data():
    """Carga y prepara los datos de las tres fuentes"""
    
    # Cargar datos
    try:
        df_dialnet = pd.read_csv(DIALNET_FILE)
        print(f"Dialnet: {len(df_dialnet)} revistas cargadas")
    except FileNotFoundError:
        print("Archivo Dialnet no encontrado")
        df_dialnet = pd.DataFrame()
    
    try:
        df_openalex = pd.read_csv(OPENALEX_FILE)
        print(f"OpenAlex: {len(df_openalex)} revistas cargadas")
    except FileNotFoundError:
        print("Archivo OpenAlex no encontrado")
        df_openalex = pd.DataFrame()
    
    try:
        df_crossref = pd.read_csv(CROSSREF_FILE)
        print(f"Crossref: {len(df_crossref)} revistas cargadas")
    except FileNotFoundError:
        print("Archivo Crossref no encontrado")
        df_crossref = pd.DataFrame()
    
    return df_dialnet, df_openalex, df_crossref

def create_unified_dataset(df_dialnet, df_openalex, df_crossref):
    """Crea dataset unificado con variables de las tres fuentes"""
    
    # Preparar datos base de Crossref (más completo)
    crossref_cols = ['nombre_revista', 'issn_original', 'is_in_crossref', 
                    'total_dois', 'current_dois', 'backfile_dois',
                    'abstracts_current', 'licenses_current', 'orcids_current',
                    'affiliations_current', 'references_current', 'title']
    
    # Verificar columnas disponibles
    available_crossref_cols = [col for col in crossref_cols if col in df_crossref.columns]
    base_df = df_crossref[available_crossref_cols].copy()
    
    # Usar la columna 'title' como nombre de revista si está disponible
    if 'title' in base_df.columns:
        base_df['nombre_revista'] = base_df['title'].fillna(base_df.get('issn_original', 'Sin identificador'))
    elif 'nombre_revista' not in base_df.columns:
        base_df['nombre_revista'] = base_df.get('issn_original', 'Sin identificador')
    else:
        # Si nombre_revista existe pero está vacío o es "Sin nombre", usar title
        if 'title' in base_df.columns:
            mask = (base_df['nombre_revista'].isna()) | (base_df['nombre_revista'] == 'Sin nombre') | (base_df['nombre_revista'] == '')
            base_df.loc[mask, 'nombre_revista'] = base_df.loc[mask, 'title']
    
    # Agregar datos OpenAlex
    if not df_openalex.empty:
        openalex_cols = ['issn_buscado', 'display_name', 'works_count', 'cited_by_count',
                        'h_index', 'i10_index', 'is_oa', 'is_in_doaj', 'apc_usd']
        
        # Verificar columnas disponibles en OpenAlex
        available_openalex_cols = [col for col in openalex_cols if col in df_openalex.columns]
        
        if 'issn_buscado' in available_openalex_cols:
            openalex_merge = df_openalex[available_openalex_cols].copy()
            openalex_merge = openalex_merge.rename(columns={'issn_buscado': 'issn_original'})
            
            # Convertir tipos de datos para compatibilidad
            base_df['issn_original'] = base_df['issn_original'].astype(str)
            openalex_merge['issn_original'] = openalex_merge['issn_original'].astype(str)
            
            # Merge con OpenAlex
            base_df = base_df.merge(openalex_merge, on='issn_original', how='left')
            
            # Usar nombre de OpenAlex si está disponible y mejor que el actual
            if 'display_name' in base_df.columns:
                # Si el nombre actual es "Sin nombre", vacío o NaN, usar el de OpenAlex
                mask = ((base_df['nombre_revista'] == 'Sin nombre') | 
                       (base_df['nombre_revista'].isna()) | 
                       (base_df['nombre_revista'] == '')) & base_df['display_name'].notna()
                base_df.loc[mask, 'nombre_revista'] = base_df.loc[mask, 'display_name']
                
                # Si aún no hay nombre, usar display_name como fallback
                base_df['nombre_revista'] = base_df['nombre_revista'].fillna(base_df['display_name'])
    
    # Agregar datos Dialnet (simplificado por compatibilidad)
    if not df_dialnet.empty:
        # Agregar estadísticas generales de Dialnet
        dialnet_stats = {
            'total_errores_promedio': df_dialnet['errores_total'].mean(),
            'porcentaje_resumenes_promedio': df_dialnet['resumenes_pct'].mean(),
            'porcentaje_palabras_clave_promedio': df_dialnet['palabras_clave_pct'].mean(),
            'porcentaje_referencias_promedio': df_dialnet['referencias_pct'].mean(),
            'porcentaje_afiliaciones_promedio': df_dialnet['afiliaciones_pct'].mean()
        }
        
        # Asignar valores promedio a todas las revistas (aproximación)
        base_df['total_errores'] = dialnet_stats['total_errores_promedio']
        base_df['porcentaje_resumenes'] = dialnet_stats['porcentaje_resumenes_promedio']
        base_df['porcentaje_palabras_clave'] = dialnet_stats['porcentaje_palabras_clave_promedio']
        base_df['porcentaje_referencias'] = dialnet_stats['porcentaje_referencias_promedio']
        base_df['porcentaje_afiliaciones'] = dialnet_stats['porcentaje_afiliaciones_promedio']
    
    # Limpiar nombres finales - si aún quedan "Sin nombre", usar ISSN
    mask = (base_df['nombre_revista'] == 'Sin nombre') | (base_df['nombre_revista'].isna()) | (base_df['nombre_revista'] == '')
    base_df.loc[mask, 'nombre_revista'] = base_df.loc[mask, 'issn_original']
    
    # Eliminar la columna title si existe (ya no la necesitamos)
    if 'title' in base_df.columns:
        base_df = base_df.drop('title', axis=1)
    
    return base_df

def calculate_novel_variables(df):
    """Calcula variables novedosas combinando las tres fuentes"""
    
    # Variables de calidad editorial
    if 'total_errores' in df.columns:
        df['calidad_dialnet_score'] = np.where(
            df['total_errores'].notna(),
            100 - (df['total_errores'] / df['total_errores'].max() * 100),
            50  # Valor por defecto
        )
    else:
        df['calidad_dialnet_score'] = 50
    
    # Índice de completitud de metadatos (promedio de Dialnet)
    metadatos_cols = ['porcentaje_resumenes', 'porcentaje_palabras_clave', 
                     'porcentaje_referencias', 'porcentaje_afiliaciones']
    existing_metadatos = [col for col in metadatos_cols if col in df.columns]
    if existing_metadatos:
        df['completitud_metadatos_dialnet'] = df[existing_metadatos].mean(axis=1)
    else:
        df['completitud_metadatos_dialnet'] = 0.5
    
    # Variables de visibilidad académica
    df['visibilidad_openalex'] = np.where(
        (df['works_count'].notna()) & (df['works_count'] > 0),
        df['cited_by_count'] / df['works_count'],
        0
    )
    
    # Variables de infraestructura DOI
    df['densidad_doi'] = np.where(
        df['total_dois'].notna() & (df['total_dois'] > 0),
        df['current_dois'] / df['total_dois'],
        0
    )
    
    # Índice de modernización Crossref
    crossref_modern_cols = ['abstracts_current', 'licenses_current', 'orcids_current']
    df['modernizacion_crossref'] = df[crossref_modern_cols].mean(axis=1)
    
    # Variables combinadas novedosas
    
    # 1. Índice de Madurez Editorial (combina DOIs históricos + calidad)
    df['madurez_editorial'] = np.where(
        (df['backfile_dois'].notna()) & (df['calidad_dialnet_score'].notna()),
        (np.log1p(df['backfile_dois']) * 0.6 + df['calidad_dialnet_score'] * 0.4) / 100,
        0.0
    ).astype(float)
    
    # 2. Brecha de Visibilidad (diferencia entre potencial y realidad)
    df['brecha_visibilidad'] = np.where(
        (df['total_dois'] > 0) & (df['works_count'].notna()),
        (df['total_dois'] - df['works_count']) / df['total_dois'],
        0.0
    ).astype(float)
    
    # 3. Índice de Coherencia de Metadatos (Dialnet vs Crossref)
    df['coherencia_resumenes'] = np.where(
        (df['porcentaje_resumenes'].notna()) & (df['abstracts_current'].notna()),
        1 - abs(df['porcentaje_resumenes']/100 - df['abstracts_current']),
        0.5
    ).astype(float)
    
    # 4. Potencial de Indexación (combina calidad + visibilidad + infraestructura)
    df['potencial_indexacion'] = np.where(
        (df['calidad_dialnet_score'].notna()) & (df['visibilidad_openalex'].notna()) & (df['modernizacion_crossref'].notna()),
        (df['calidad_dialnet_score'] * 0.4 + 
         np.log1p(df['visibilidad_openalex']) * 20 * 0.3 + 
         df['modernizacion_crossref'] * 100 * 0.3) / 100,
        0.0
    ).astype(float)
    
    # 5. Índice de Acceso Abierto Integral
    df['acceso_abierto_integral'] = 0
    if 'is_oa' in df.columns:
        df['acceso_abierto_integral'] += df['is_oa'].fillna(0) * 0.4
    if 'is_in_doaj' in df.columns:
        df['acceso_abierto_integral'] += df['is_in_doaj'].fillna(0) * 0.3
    if 'licenses_current' in df.columns:
        df['acceso_abierto_integral'] += df['licenses_current'].fillna(0) * 0.3
    
    return df

def calculate_three_levels(df):
    """Calcula los tres niveles de análisis"""
    
    # NIVEL 1: CALIDAD DE METADATOS
    df['nivel1_completitud'] = df[['completitud_metadatos_dialnet', 'modernizacion_crossref']].mean(axis=1)
    df['nivel1_coherencia'] = df['coherencia_resumenes'].fillna(0.5)
    
    # NIVEL 2: VISIBILIDAD Y ACCESO ABIERTO
    df['eficiencia_apc'] = np.where(
        (df['apc_usd'].notna()) & (df['apc_usd'] > 0) & (df['h_index'].notna()),
        df['h_index'] / np.log1p(df['apc_usd']),
        0.0
    ).astype(float)
    df['nivel2_visibilidad'] = df[['visibilidad_openalex', 'acceso_abierto_integral']].mean(axis=1)
    
    # NIVEL 3: MADUREZ E INFRAESTRUCTURA
    df['nivel3_madurez'] = df[['madurez_editorial', 'densidad_doi']].mean(axis=1)
    df['oportunidad_mejora'] = np.where(
        df['brecha_visibilidad'] > 0.3,
        1 - df['brecha_visibilidad'],
        df['potencial_indexacion']
    ).astype(float)
    
    return df

def create_strategic_segments(df):
    """Crea segmentación estratégica"""
    
    # Definir umbrales
    high_quality = df['nivel1_completitud'] > df['nivel1_completitud'].quantile(0.7)
    high_visibility = df['nivel2_visibilidad'] > df['nivel2_visibilidad'].quantile(0.7)
    high_maturity = df['nivel3_madurez'] > df['nivel3_madurez'].quantile(0.7)
    
    # Segmentación
    df['segmento'] = 'Básico'
    df.loc[high_quality & high_visibility & high_maturity, 'segmento'] = 'Estrella'
    df.loc[high_quality & ~high_visibility, 'segmento'] = 'Oportunidad'
    df.loc[~high_quality & high_visibility, 'segmento'] = 'Problema'
    df.loc[high_maturity & ~high_quality & ~high_visibility, 'segmento'] = 'Veterana'
    
    return df

def generate_outputs(df):
    """Genera los 8 outputs específicos"""
    
    outputs = {}
    
    # 1. TOP 10 REVISTAS POR POTENCIAL COMBINADO
    df['potencial_combinado'] = df[['nivel1_completitud', 'nivel2_visibilidad', 'nivel3_madurez']].mean(axis=1).astype(float)
    top10 = df.nlargest(10, 'potencial_combinado')[['nombre_revista', 'potencial_combinado', 'nivel1_completitud', 'nivel2_visibilidad', 'nivel3_madurez', 'segmento']]
    outputs['top10_potencial'] = top10
    
    # 2. MATRIZ DE CORRELACIONES CLAVE
    key_vars = ['nivel1_completitud', 'nivel2_visibilidad', 'nivel3_madurez', 'h_index', 'apc_usd', 'total_dois']
    existing_key_vars = [var for var in key_vars if var in df.columns]
    corr_key = df[existing_key_vars].corr()
    outputs['matriz_correlaciones'] = corr_key
    
    # 3. SEGMENTACIÓN ESTRATÉGICA
    segmentacion = df.groupby('segmento').agg({
        'nombre_revista': 'count',
        'potencial_combinado': 'mean',
        'h_index': 'mean',
        'apc_usd': 'mean',
        'total_dois': 'mean'
    }).round(2)
    segmentacion.columns = ['Cantidad', 'Potencial_Promedio', 'H_Index_Promedio', 'APC_Promedio', 'DOIs_Promedio']
    outputs['segmentacion'] = segmentacion
    
    # 4-6. DATOS PARA GRÁFICAS
    # Scatter APC vs H-index
    scatter_data = df[['nombre_revista', 'apc_usd', 'h_index', 'nivel1_completitud', 'segmento']].dropna()
    outputs['scatter_apc_hindex'] = scatter_data
    
    # Heatmap coherencia
    coherencia_vars = ['coherencia_resumenes', 'nivel1_coherencia', 'nivel2_visibilidad', 'nivel3_madurez']
    existing_coherencia = [var for var in coherencia_vars if var in df.columns]
    outputs['heatmap_coherencia'] = df[existing_coherencia].corr()
    
    # Radar perfiles
    radar_data = df.groupby('segmento')[['nivel1_completitud', 'nivel2_visibilidad', 'nivel3_madurez']].mean()
    outputs['radar_perfiles'] = radar_data
    
    # 7. BRECHAS DE OPORTUNIDAD PRIORITARIAS
    brechas = df[df['oportunidad_mejora'] > df['oportunidad_mejora'].quantile(0.8)][['nombre_revista', 'oportunidad_mejora', 'brecha_visibilidad', 'nivel1_completitud', 'is_in_doaj', 'apc_usd']].sort_values('oportunidad_mejora', ascending=False).head(10)
    outputs['brechas_oportunidad'] = brechas
    
    # 8. RECOMENDACIONES POR SEGMENTO
    recomendaciones = {
        'Estrella': 'Mantener liderazgo, explorar indexación premium',
        'Oportunidad': 'Aumentar visibilidad, considerar estrategias de marketing académico',
        'Problema': 'Mejorar calidad editorial, revisar procesos internos',
        'Veterana': 'Modernizar infraestructura, adoptar nuevos estándares',
        'Básico': 'Desarrollo integral en los tres niveles'
    }
    
    recom_df = pd.DataFrame([
        {'Segmento': k, 'Recomendacion': v, 'Cantidad': len(df[df['segmento'] == k])}
        for k, v in recomendaciones.items()
    ])
    outputs['recomendaciones'] = recom_df
    
    return outputs

def create_visualizations(outputs, df_unified):
    """Crea las 4 visualizaciones principales"""
    
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Análisis Comparativo Cruzado - Chile OJS', fontsize=16, fontweight='bold')
    
    # Colores por segmento
    colors = {'Estrella': 'gold', 'Oportunidad': 'lightgreen', 
              'Problema': 'salmon', 'Veterana': 'lightblue', 'Básico': 'lightgray'}
    
    # 1. Distribución por Segmento (Pie Chart)
    if 'segmentacion' in outputs:
        seg_data = outputs['segmentacion']
        wedges, texts, autotexts = axes[0,0].pie(
            seg_data['Cantidad'].values, 
            labels=seg_data.index,
            autopct='%1.1f%%', 
            startangle=90,
            colors=[colors.get(seg, 'gray') for seg in seg_data.index]
        )
        axes[0,0].set_title('Distribución de Revistas por Segmento')
    
    # 2. Matriz de Correlaciones
    if 'matriz_correlaciones' in outputs:
        sns.heatmap(outputs['matriz_correlaciones'], annot=True, cmap='RdBu_r', 
                   center=0, ax=axes[0,1], cbar_kws={'shrink': 0.8})
        axes[0,1].set_title('Matriz de Correlaciones Clave')
    
    # 3. Matriz de Posicionamiento Estratégico
    pos_data = df_unified[(df_unified['nivel1_completitud'].notna()) & 
                         (df_unified['nivel2_visibilidad'].notna())].copy()
    
    scatter = axes[1,0].scatter(
        pos_data['nivel1_completitud'], 
        pos_data['nivel2_visibilidad'],
        s=60, 
        c=[colors.get(seg, 'gray') for seg in pos_data['segmento']], 
        alpha=0.7, 
        edgecolors='black', 
        linewidth=0.5
    )
    
    # Líneas de referencia
    axes[1,0].axhline(y=pos_data['nivel2_visibilidad'].median(), color='red', linestyle='--', alpha=0.5)
    axes[1,0].axvline(x=pos_data['nivel1_completitud'].median(), color='red', linestyle='--', alpha=0.5)
    
    axes[1,0].set_xlabel('Calidad Editorial (Nivel 1)')
    axes[1,0].set_ylabel('Visibilidad Académica (Nivel 2)')
    axes[1,0].set_title('Matriz de Posicionamiento Estratégico')
    axes[1,0].grid(True, alpha=0.3)
    
    # Etiquetas de cuadrantes
    axes[1,0].text(0.95, 0.95, 'ESTRELLA', transform=axes[1,0].transAxes, ha='right', va='top', 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='gold', alpha=0.7))
    axes[1,0].text(0.05, 0.95, 'OPORTUNIDAD', transform=axes[1,0].transAxes, ha='left', va='top',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
    axes[1,0].text(0.05, 0.05, 'BÁSICO', transform=axes[1,0].transAxes, ha='left', va='bottom',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.7))
    axes[1,0].text(0.95, 0.05, 'PROBLEMA', transform=axes[1,0].transAxes, ha='right', va='bottom',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='salmon', alpha=0.7))
    
    # 4. Barras Segmentación por Cantidad
    if 'segmentacion' in outputs:
        seg_data = outputs['segmentacion']
        bars = axes[1,1].bar(
            range(len(seg_data)), 
            seg_data['Cantidad'].values,
            color=[colors.get(seg, 'gray') for seg in seg_data.index]
        )
        axes[1,1].set_xticks(range(len(seg_data)))
        axes[1,1].set_xticklabels(seg_data.index, rotation=45)
        axes[1,1].set_title('Cantidad por Segmento')
        axes[1,1].set_ylabel('Número de Revistas')
        axes[1,1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('visualizations/15_analisis_comparativo_cruzado.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Visualizaciones guardadas en: visualizations/15_analisis_comparativo_cruzado.png")

def main():
    """Función principal"""
    print("🔄 Iniciando análisis comparativo cruzado...")
    
    # Cargar datos
    df_dialnet, df_openalex, df_crossref = load_and_prepare_data()
    
    if df_crossref.empty:
        print("❌ No se pueden cargar los datos base de Crossref")
        return
    
    # Crear dataset unificado
    df_unified = create_unified_dataset(df_dialnet, df_openalex, df_crossref)
    print(f"📊 Dataset unificado: {len(df_unified)} revistas")
    
    # Calcular variables novedosas
    df_unified = calculate_novel_variables(df_unified)
    
    # Calcular tres niveles de análisis
    df_unified = calculate_three_levels(df_unified)
    
    # Crear segmentación estratégica
    df_unified = create_strategic_segments(df_unified)
    
    # Generar outputs
    outputs = generate_outputs(df_unified)
    
    # Crear visualizaciones
    create_visualizations(outputs, df_unified)
    
    # Guardar dataset final
    df_unified.to_csv(OUTPUT_FILE, index=False)
    print(f"💾 Dataset guardado: {OUTPUT_FILE}")
    
    # Mostrar resumen de outputs
    print("\n📋 RESUMEN DE OUTPUTS GENERADOS:")
    print("="*50)
    
    # 1. Top 10
    if 'top10_potencial' in outputs:
        print("\n1️⃣ TOP 10 REVISTAS POR POTENCIAL COMBINADO:")
        print(outputs['top10_potencial'][['nombre_revista', 'potencial_combinado', 'segmento']].to_string(index=False))
    
    # 2. Correlaciones
    if 'matriz_correlaciones' in outputs:
        print("\n2️⃣ CORRELACIONES MÁS FUERTES:")
        corr_matrix = outputs['matriz_correlaciones']
        # Encontrar correlaciones más altas
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if not pd.isna(corr_val) and abs(corr_val) > 0.5:
                    corr_pairs.append({
                        'Variable1': corr_matrix.columns[i],
                        'Variable2': corr_matrix.columns[j],
                        'Correlacion': round(corr_val, 3)
                    })
        if corr_pairs:
            corr_df = pd.DataFrame(corr_pairs).sort_values('Correlacion', key=abs, ascending=False)
            print(corr_df.to_string(index=False))
    
    # 3. Segmentación
    if 'segmentacion' in outputs:
        print("\n3️⃣ SEGMENTACIÓN ESTRATÉGICA:")
        print(outputs['segmentacion'].to_string())
    
    # 7. Brechas de oportunidad
    if 'brechas_oportunidad' in outputs:
        print("\n7️⃣ PRINCIPALES BRECHAS DE OPORTUNIDAD:")
        print(outputs['brechas_oportunidad'][['nombre_revista', 'oportunidad_mejora']].head().to_string(index=False))
    
    # 8. Recomendaciones
    if 'recomendaciones' in outputs:
        print("\n8️⃣ RECOMENDACIONES POR SEGMENTO:")
        print(outputs['recomendaciones'].to_string(index=False))
    
    print("\n✅ Análisis comparativo cruzado completado exitosamente")
    print(f"📁 Archivos generados:")
    print(f"   - {OUTPUT_FILE}")
    print(f"   - visualizations/15_analisis_comparativo_cruzado.png")

if __name__ == "__main__":
    main()