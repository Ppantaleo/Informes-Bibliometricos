#!/usr/bin/env python3
import pandas as pd
from collections import Counter

def main():
    # Leer el CSV
    df = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/Chile/visualizations/chile_oai_urls_limpio.csv')
    
    # Filtrar URLs de uchile.cl
    uchile_urls = df[df['oai_url'].str.contains('uchile.cl', na=False)]
    
    print(f"Total URLs de uchile.cl: {len(uchile_urls)}")
    print(f"URLs con mensaje de error: {len(uchile_urls[uchile_urls['mensaje_error'].notna() & (uchile_urls['mensaje_error'] != '')])}")
    print(f"URLs sin mensaje de error: {len(uchile_urls[uchile_urls['mensaje_error'].isna() | (uchile_urls['mensaje_error'] == '')])}")
    
    # Contar tipos de errores
    errores = uchile_urls[uchile_urls['mensaje_error'].notna() & (uchile_urls['mensaje_error'] != '')]['mensaje_error']
    contador_errores = Counter(errores)
    
    print("\nTipos de errores encontrados:")
    for error, count in contador_errores.items():
        print(f"- '{error}': {count} URLs")
    
    # Mostrar todas las URLs de uchile.cl
    print(f"\nListado completo de URLs de uchile.cl:")
    for i, (_, row) in enumerate(uchile_urls.iterrows(), 1):
        status = "SIN ERROR" if pd.isna(row['mensaje_error']) or row['mensaje_error'] == '' else row['mensaje_error']
        print(f"{i:2d}. {row['oai_url']}")
        print(f"    Status: {status}")
    
    # Análisis específico del error más común
    error_mas_comun = contador_errores.most_common(1)[0] if contador_errores else None
    if error_mas_comun:
        print(f"\nError más común: '{error_mas_comun[0]}' ({error_mas_comun[1]} URLs)")
        urls_con_error_comun = uchile_urls[uchile_urls['mensaje_error'] == error_mas_comun[0]]
        print("URLs afectadas:")
        for _, row in urls_con_error_comun.iterrows():
            print(f"- {row['oai_url']}")

if __name__ == "__main__":
    main()