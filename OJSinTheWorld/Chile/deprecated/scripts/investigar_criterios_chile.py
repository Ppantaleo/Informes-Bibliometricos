#!/usr/bin/env python3
import pandas as pd

def main():
    print("=== INVESTIGANDO CRITERIOS DE CLASIFICACIÓN CHILE ===\n")
    
    # Leer dataset JUOJS activas
    juojs = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_instalaciones_activas.csv')
    
    # URLs sospechosas identificadas
    urls_sospechosas = ['spdiojs.org', 'revistas.unam.mx']
    
    print("1. ANÁLISIS DE URLs SOSPECHOSAS:")
    
    for url_sospechosa in urls_sospechosas:
        # Buscar en el dataset
        registros = juojs[juojs['dominio'].str.contains(url_sospechosa, na=False)]
        
        if len(registros) > 0:
            print(f"\n   URL: {url_sospechosa}")
            print(f"   Registros encontrados: {len(registros)}")
            
            for _, row in registros.iterrows():
                print(f"   - Dominio: {row['dominio']}")
                print(f"   - Nombre: {row['context_name']}")
                print(f"   - ISSN: {row['issn']}")
                print(f"   - Pub 2023: {row['record_count_2023']}")
                print(f"   - Total histórico: {row['total_historico']}")
        else:
            print(f"\n   URL {url_sospechosa}: NO encontrada en dataset")
    
    # Buscar otros dominios no .cl
    print(f"\n2. ANÁLISIS DE DOMINIOS NO .CL:")
    
    dominios_no_cl = juojs[~juojs['dominio'].str.endswith('.cl', na=False)]
    
    print(f"   Total dominios no .cl: {len(dominios_no_cl)}")
    
    if len(dominios_no_cl) > 0:
        print(f"\n   Dominios no .cl encontrados:")
        for _, row in dominios_no_cl.iterrows():
            print(f"   - {row['dominio']} | {row['context_name']} | ISSN: {row['issn']}")
    
    # Verificar si hay columnas de país en el dataset original
    print(f"\n3. VERIFICACIÓN DE CRITERIOS DE PAÍS:")
    
    # Intentar leer el dataset completo para ver criterios
    try:
        completo = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_todas_instalaciones.csv')
        
        print(f"   Columnas en dataset completo: {list(completo.columns)}")
        
        # Buscar las URLs sospechosas en el dataset completo
        for url_sospechosa in urls_sospechosas:
            registros_completo = completo[completo['dominio'].str.contains(url_sospechosa, na=False)]
            
            if len(registros_completo) > 0:
                print(f"\n   {url_sospechosa} en dataset completo:")
                for _, row in registros_completo.iterrows():
                    print(f"   - Dominio: {row['dominio']}")
                    print(f"   - Nombre: {row['context_name']}")
                    # Mostrar todas las columnas para entender criterios
                    for col in row.index:
                        if 'country' in col.lower() or 'pais' in col.lower():
                            print(f"   - {col}: {row[col]}")
    
    except FileNotFoundError:
        print("   Dataset completo no encontrado")
    
    # Verificar si hay archivo beacon original
    print(f"\n4. RECOMENDACIÓN:")
    print(f"   - Revisar archivo beacon.tab original para ver criterios de país")
    print(f"   - Verificar columnas: country_consolidated, country_issn, country_tld, country_ip")
    print(f"   - Posibles razones para clasificación como Chile:")
    print(f"     * ISSN registrado en Chile")
    print(f"     * IP geolocalizada en Chile")
    print(f"     * Configuración del servidor")
    print(f"     * Afiliación institucional chilena")

if __name__ == "__main__":
    main()