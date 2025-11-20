#!/usr/bin/env python3
import pandas as pd
import os
from urllib.parse import urlparse

def extract_domain_from_url(url):
    """Extrae el dominio de una URL para comparar con nombres de archivos"""
    parsed = urlparse(url)
    domain = parsed.netloc
    # Remover www. si existe
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def main():
    # Leer el CSV
    df = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_oai_urls_limpio.csv')
    
    # Filtrar URLs sin mensaje de error (campo vacío o NaN)
    urls_sin_error = df[df['mensaje_error'].isna() | (df['mensaje_error'] == '')]['oai_url'].tolist()
    
    print(f"URLs sin mensaje de error: {len(urls_sin_error)}")
    
    # Obtener lista de archivos en dialnet/
    dialnet_dir = '/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/dialnet'
    archivos_dialnet = []
    
    if os.path.exists(dialnet_dir):
        archivos_dialnet = [f for f in os.listdir(dialnet_dir) if f.endswith('.html')]
    
    print(f"Archivos HTML en dialnet/: {len(archivos_dialnet)}")
    
    # Extraer dominios de archivos (remover .html)
    dominios_archivos = [f.replace('.html', '') for f in archivos_dialnet]
    
    # Encontrar URLs sin archivo correspondiente
    urls_sin_archivo = []
    
    for url in urls_sin_error:
        dominio_url = extract_domain_from_url(url)
        
        # Buscar si existe un archivo con este dominio (considerando variaciones con www.)
        archivo_encontrado = False
        for dominio_archivo in dominios_archivos:
            # Comparar dominios removiendo www. de ambos
            dominio_url_clean = dominio_url.replace('www.', '')
            dominio_archivo_clean = dominio_archivo.replace('www.', '')
            
            if dominio_url_clean == dominio_archivo_clean:
                archivo_encontrado = True
                break
        
        if not archivo_encontrado:
            urls_sin_archivo.append(url)
    
    print(f"\nURLs sin mensaje de error pero sin archivo HTML descargado: {len(urls_sin_archivo)}")
    print("\nListado de URLs faltantes:")
    for i, url in enumerate(urls_sin_archivo, 1):
        dominio = extract_domain_from_url(url)
        print(f"{i}. {url}")
        print(f"   Dominio esperado: {dominio}.html")
    
    # Verificar también si hay archivos sin URL correspondiente
    print(f"\n{'='*60}")
    print("VERIFICACIÓN INVERSA: Archivos sin URL correspondiente")
    
    archivos_sin_url = []
    for archivo in archivos_dialnet:
        dominio_archivo = archivo.replace('.html', '')
        
        # Buscar si existe una URL con este dominio (considerando variaciones con www.)
        url_encontrada = False
        for url in urls_sin_error:
            dominio_url = extract_domain_from_url(url)
            # Comparar dominios removiendo www. de ambos
            dominio_url_clean = dominio_url.replace('www.', '')
            dominio_archivo_clean = dominio_archivo.replace('www.', '')
            
            if dominio_url_clean == dominio_archivo_clean:
                url_encontrada = True
                break
        
        if not url_encontrada:
            archivos_sin_url.append(archivo)
    
    if archivos_sin_url:
        print(f"\nArchivos HTML sin URL correspondiente: {len(archivos_sin_url)}")
        for archivo in archivos_sin_url:
            print(f"- {archivo}")
    else:
        print("\nTodos los archivos HTML tienen su URL correspondiente.")

if __name__ == "__main__":
    main()