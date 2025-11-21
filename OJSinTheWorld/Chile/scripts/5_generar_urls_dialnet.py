#!/usr/bin/env python3
"""
Generación de URLs OAI para evaluación en Dialnet
Basado en dataset JUOJS (chile_juojs_activas.csv)
Parte del flujo metodológico principal
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
    print("=== GENERACIÓN URLs DIALNET DESDE DATASET JUOJS ===\n")
    
    # Cargar dataset JUOJS
    try:
        juojs = pd.read_csv('../visualizations/chile_juojs_activas.csv')
        print(f"Dataset JUOJS cargado: {len(juojs)} instalaciones activas")
    except FileNotFoundError:
        print("ERROR: Ejecutar primero scripts/chile_juojs_filtrado.R")
        return
    
    # Eliminar duplicados por dominio
    duplicados_antes = len(juojs)
    juojs_unicos = juojs.drop_duplicates(subset=['dominio'], keep='first')
    duplicados_eliminados = duplicados_antes - len(juojs_unicos)
    
    print(f"Duplicados eliminados: {duplicados_eliminados}")
    print(f"URLs únicas: {len(juojs_unicos)}")
    
    # Generar URLs OAI
    juojs_unicos['oai_url'] = juojs_unicos['dominio'].apply(generar_url_oai)
    
    # Crear DataFrame para Dialnet
    dialnet_df = pd.DataFrame({
        'oai_url': juojs_unicos['oai_url'],
        'mensaje_error': ''  # Se llenará durante evaluación
    })
    
    # Estadísticas
    print(f"\nEstadísticas:")
    print(f"- Total URLs generadas: {len(dialnet_df)}")
    
    # Verificar uchile.cl
    uchile_count = dialnet_df['oai_url'].str.contains('uchile.cl').sum()
    print(f"- URLs uchile.cl: {uchile_count}")
    
    # Guardar archivo
    output_path = '../visualizations/chile_oai_urls_nuevo.csv'
    dialnet_df.to_csv(output_path, index=False)
    
    print(f"\nArchivo generado: {output_path}")
    print("Listo para evaluación manual en Dialnet Nexus")
    
    # Mostrar ejemplos
    print(f"\nEjemplos de URLs generadas:")
    for i, url in enumerate(dialnet_df['oai_url'].head(5), 1):
        print(f"{i}. {url}")

if __name__ == "__main__":
    main()