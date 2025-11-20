#!/usr/bin/env python3
import pandas as pd
import re

def generar_url_oai(dominio):
    """Genera URL OAI a partir del dominio"""
    # Asegurar que tenga protocolo
    if not dominio.startswith(('http://', 'https://')):
        # Usar https por defecto, excepto para algunos casos conocidos
        protocolo = 'https://'
        if any(x in dominio for x in ['www.reto.ubo.cl', 'revistapyr.ucm.cl', 'rhv.uv.cl']):
            protocolo = 'http://'
        dominio = protocolo + dominio
    
    # Agregar endpoint OAI estándar
    if not dominio.endswith('/'):
        dominio += '/'
    
    return dominio + 'index.php/index/oai'

def main():
    print("=== REGENERANDO chile_oai_urls_limpio.csv DESDE DATASET JUOJS ===\n")
    
    # Leer dataset JUOJS activas
    juojs = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_instalaciones_activas.csv')
    
    print(f"1. DATASET JUOJS CARGADO:")
    print(f"   - Total instalaciones: {len(juojs)}")
    print(f"   - Columnas: {list(juojs.columns)}")
    
    # Verificar duplicados
    duplicados = juojs['dominio'].duplicated().sum()
    print(f"   - Duplicados encontrados: {duplicados}")
    
    # Eliminar duplicados manteniendo el primer registro
    juojs_unicos = juojs.drop_duplicates(subset=['dominio'], keep='first')
    print(f"   - Después de eliminar duplicados: {len(juojs_unicos)}")
    
    # Generar URLs OAI
    juojs_unicos['oai_url'] = juojs_unicos['dominio'].apply(generar_url_oai)
    
    # Crear DataFrame para Dialnet con columna de mensaje_error vacía
    dialnet_df = pd.DataFrame({
        'oai_url': juojs_unicos['oai_url'],
        'mensaje_error': ''
    })
    
    print(f"\n2. URLs OAI GENERADAS:")
    print(f"   - Total URLs únicas: {len(dialnet_df)}")
    
    # Mostrar algunos ejemplos
    print(f"\n   Ejemplos de URLs generadas:")
    for i, url in enumerate(dialnet_df['oai_url'].head(5), 1):
        print(f"   {i}. {url}")
    
    # Verificar uchile.cl específicamente
    uchile_urls = dialnet_df[dialnet_df['oai_url'].str.contains('uchile.cl')]
    print(f"\n3. VERIFICACIÓN UCHILE.CL:")
    print(f"   - URLs uchile.cl generadas: {len(uchile_urls)}")
    
    # Guardar archivo
    output_path = '/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_oai_urls_limpio_juojs.csv'
    dialnet_df.to_csv(output_path, index=False)
    
    print(f"\n4. ARCHIVO GENERADO:")
    print(f"   - Ruta: {output_path}")
    print(f"   - Registros: {len(dialnet_df)}")
    print(f"   - Columnas: {list(dialnet_df.columns)}")
    
    # Comparar con archivo anterior
    try:
        anterior = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_oai_urls_limpio.csv')
        print(f"\n5. COMPARACIÓN CON ARCHIVO ANTERIOR:")
        print(f"   - Archivo anterior: {len(anterior)} URLs")
        print(f"   - Archivo nuevo: {len(dialnet_df)} URLs")
        print(f"   - Diferencia: {len(dialnet_df) - len(anterior)} URLs")
        
        # URLs que están en el nuevo pero no en el anterior
        urls_anteriores = set(anterior['oai_url'])
        urls_nuevas = set(dialnet_df['oai_url'])
        
        solo_en_nuevo = urls_nuevas - urls_anteriores
        solo_en_anterior = urls_anteriores - urls_nuevas
        
        print(f"   - Solo en nuevo: {len(solo_en_nuevo)}")
        print(f"   - Solo en anterior: {len(solo_en_anterior)}")
        
        if len(solo_en_nuevo) > 0:
            print(f"\n   Ejemplos de URLs solo en nuevo:")
            for i, url in enumerate(list(solo_en_nuevo)[:3], 1):
                print(f"   {i}. {url}")
        
        if len(solo_en_anterior) > 0:
            print(f"\n   Ejemplos de URLs solo en anterior:")
            for i, url in enumerate(list(solo_en_anterior)[:3], 1):
                print(f"   {i}. {url}")
                
    except FileNotFoundError:
        print(f"\n5. ARCHIVO ANTERIOR NO ENCONTRADO")
    
    print(f"\n6. PRÓXIMOS PASOS:")
    print(f"   - Revisar el archivo generado: {output_path}")
    print(f"   - Si está correcto, reemplazar chile_oai_urls_limpio.csv")
    print(f"   - Actualizar documentación con nuevos números")

if __name__ == "__main__":
    main()