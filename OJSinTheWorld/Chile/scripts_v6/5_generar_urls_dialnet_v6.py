#!/usr/bin/env python3
"""
Generación de URLs OAI para evaluación en Dialnet - Beacon v6
Basado en dataset JUOJS v6 (chile_juojs_activas_v6.csv)
Criterio actualizado: >5 publicaciones en 2024
"""

import pandas as pd
import re

def generar_url_oai(dominio):
    """Genera URL OAI estándar a partir del dominio"""
    # Asegurar protocolo
    if not dominio.startswith(('http://', 'https://')):
        # Usar https por defecto, http para casos específicos
        protocolo = 'http://' if any(x in dominio for x in [
            'reto.ubo.cl', 'revistapyr.ucm.cl', 'rhv.uv.cl', 
            'intushistoria.uai.cl', 'www.autoctonia.cl'
        ]) else 'https://'
        dominio = protocolo + dominio
    
    # Agregar endpoint OAI estándar
    if not dominio.endswith('/'):
        dominio += '/'
    
    return dominio + 'index.php/index/oai'

def main():
    print("=== GENERACIÓN URLs DIALNET DESDE DATASET JUOJS V6 ===\n")
    
    # Cargar dataset JUOJS v6
    try:
        juojs_v6 = pd.read_csv('../visualizations_v6/chile_juojs_activas_v6.csv')
        print(f"Dataset JUOJS v6 cargado: {len(juojs_v6)} instalaciones activas (>5 pub/2024)")
    except FileNotFoundError:
        print("ERROR: Ejecutar primero scripts_v6/2_chile_juojs_filtrado_v6.R")
        return
    
    # Eliminar duplicados por dominio
    duplicados_antes = len(juojs_v6)
    juojs_unicos = juojs_v6.drop_duplicates(subset=['dominio'], keep='first')
    duplicados_eliminados = duplicados_antes - len(juojs_unicos)
    
    print(f"Duplicados eliminados: {duplicados_eliminados}")
    print(f"URLs únicas: {len(juojs_unicos)}")
    
    # Generar URLs OAI
    juojs_unicos['oai_url'] = juojs_unicos['dominio'].apply(generar_url_oai)
    
    # Crear DataFrame para Dialnet v6
    dialnet_v6_df = pd.DataFrame({
        'oai_url': juojs_unicos['oai_url'],
        'mensaje_error': '',  # Se llenará durante evaluación
        'pub_2024': juojs_unicos['record_count_2024'],
        'pub_2023': juojs_unicos['record_count_2023'],
        'crecimiento': juojs_unicos['crecimiento_2023_2024'],
        'region_pkp': juojs_unicos['region_pkp']
    })
    
    # Estadísticas v6
    print(f"\n=== ESTADÍSTICAS URLS V6 ===")
    print(f"Total URLs generadas: {len(dialnet_v6_df)}")
    print(f"Publicaciones 2024 total: {dialnet_v6_df['pub_2024'].sum()}")
    print(f"Crecimiento 2023->2024: {dialnet_v6_df['crecimiento'].sum()}")
    
    # Verificar uchile.cl
    uchile_count = dialnet_v6_df['oai_url'].str.contains('uchile.cl').sum()
    print(f"URLs uchile.cl: {uchile_count}")
    
    # Análisis por región
    print(f"\n=== DISTRIBUCIÓN POR REGIÓN PKP ===")
    regiones = dialnet_v6_df['region_pkp'].value_counts()
    for region, count in regiones.items():
        print(f"- {region}: {count} URLs")
    
    # Guardar archivo v6
    output_path = '../visualizations_v6/chile_oai_urls_v6.csv'
    dialnet_v6_df.to_csv(output_path, index=False)
    
    print(f"\nArchivo generado: {output_path}")
    print("Listo para evaluación manual en Dialnet Nexus")
    
    # Mostrar ejemplos
    print(f"\n=== EJEMPLOS URLs GENERADAS V6 ===")
    for i, (url, pub2024) in enumerate(zip(dialnet_v6_df['oai_url'].head(5), 
                                          dialnet_v6_df['pub_2024'].head(5)), 1):
        print(f"{i}. {url} ({pub2024} pub/2024)")
    
    # Top 5 más productivas 2024
    print(f"\n=== TOP 5 MÁS PRODUCTIVAS 2024 ===")
    top5 = dialnet_v6_df.nlargest(5, 'pub_2024')
    for i, (url, pub2024, crecimiento) in enumerate(zip(top5['oai_url'], 
                                                       top5['pub_2024'], 
                                                       top5['crecimiento']), 1):
        print(f"{i}. {url}")
        print(f"   {pub2024} pub/2024 (crecimiento: {crecimiento:+d})")

if __name__ == "__main__":
    main()