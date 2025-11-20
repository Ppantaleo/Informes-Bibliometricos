#!/usr/bin/env python3
import pandas as pd
import re

def extract_domain(url):
    """Extrae el dominio de una URL"""
    match = re.search(r'https?://([^/]+)', url)
    return match.group(1) if match else url

def main():
    print("=== ACLARACIÓN NÚMEROS UCHILE.CL ===\n")
    
    # Leer datasets
    chile_completo = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_todas_instalaciones.csv')
    chile_activas = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_instalaciones_activas.csv')
    chile_dialnet = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_oai_urls_limpio.csv')
    
    # Filtrar uchile.cl
    uchile_completo = chile_completo[chile_completo['dominio'].str.contains('uchile.cl', na=False)]
    uchile_activas = chile_activas[chile_activas['dominio'].str.contains('uchile.cl', na=False)]
    uchile_dialnet = chile_dialnet[chile_dialnet['oai_url'].str.contains('uchile.cl', na=False)]
    
    print("1. NÚMEROS BÁSICOS:")
    print(f"   - Dataset completo uchile.cl: {len(uchile_completo)}")
    print(f"   - Dataset activas uchile.cl: {len(uchile_activas)}")
    print(f"   - URLs Dialnet uchile.cl: {len(uchile_dialnet)}")
    print(f"   - Diferencia (completo - activas): {len(uchile_completo) - len(uchile_activas)}")
    print(f"   - Diferencia (completo - dialnet): {len(uchile_completo) - len(uchile_dialnet)}")
    
    # Verificar si hay diferencias en los dominios
    dominios_completo = set(uchile_completo['dominio'])
    dominios_activas = set(uchile_activas['dominio'])
    dominios_dialnet = set(uchile_dialnet['oai_url'].apply(extract_domain))
    
    print(f"\n2. ANÁLISIS DE DOMINIOS:")
    print(f"   - Dominios únicos en completo: {len(dominios_completo)}")
    print(f"   - Dominios únicos en activas: {len(dominios_activas)}")
    print(f"   - Dominios únicos en dialnet: {len(dominios_dialnet)}")
    
    # Encontrar dominios que están en completo pero NO en activas
    solo_en_completo = dominios_completo - dominios_activas
    print(f"\n3. DOMINIOS SOLO EN COMPLETO (NO ACTIVAS): {len(solo_en_completo)}")
    for i, dominio in enumerate(sorted(solo_en_completo), 1):
        # Buscar publicaciones
        pub_info = uchile_completo[uchile_completo['dominio'] == dominio]['record_count_2023'].iloc[0]
        print(f"   {i:2d}. {dominio} ({pub_info} pub/2023)")
    
    # Encontrar dominios que están en completo pero NO en dialnet
    solo_en_completo_no_dialnet = dominios_completo - dominios_dialnet
    print(f"\n4. DOMINIOS SOLO EN COMPLETO (NO EN DIALNET): {len(solo_en_completo_no_dialnet)}")
    for i, dominio in enumerate(sorted(solo_en_completo_no_dialnet), 1):
        pub_info = uchile_completo[uchile_completo['dominio'] == dominio]['record_count_2023'].iloc[0]
        print(f"   {i:2d}. {dominio} ({pub_info} pub/2023)")
    
    # Verificar si hay duplicados en algún dataset
    print(f"\n5. VERIFICACIÓN DE DUPLICADOS:")
    duplicados_completo = uchile_completo['dominio'].duplicated().sum()
    duplicados_activas = uchile_activas['dominio'].duplicated().sum()
    duplicados_dialnet = uchile_dialnet['oai_url'].apply(extract_domain).duplicated().sum()
    
    print(f"   - Duplicados en completo: {duplicados_completo}")
    print(f"   - Duplicados en activas: {duplicados_activas}")
    print(f"   - Duplicados en dialnet: {duplicados_dialnet}")
    
    # Mostrar los números que deberían coincidir con la documentación
    print(f"\n6. NÚMEROS PARA DOCUMENTACIÓN:")
    print(f"   - Sección 3.2.2 (activas): {len(dominios_activas)} instalaciones")
    print(f"   - Sección 3.2.6 (dialnet): {len(dominios_dialnet)} instalaciones")
    print(f"   - Diferencia esperada: {len(dominios_dialnet) - len(dominios_activas)}")
    
    # Verificar si los 47 de la documentación coinciden
    if len(dominios_activas) != 47:
        print(f"\n   ⚠️  ADVERTENCIA: Documentación dice 47, pero encontramos {len(dominios_activas)}")
        print(f"   Posible causa: Filtros diferentes o datasets actualizados")

if __name__ == "__main__":
    main()