#!/usr/bin/env python3
"""
Comparación precisa entre URLs v5 y v6
Compara chile_oai_urls_limpio.csv (v5) vs chile_oai_urls_limpio_v6.csv (v6)
Considera URLs con mismo dominio como coincidencias
"""

import pandas as pd
import sys
from urllib.parse import urlparse

def extraer_dominio(url):
    """Extrae el dominio de una URL, removiendo www y normalizando"""
    parsed = urlparse(url.strip())
    dominio = parsed.netloc.lower()
    # Remover www. si existe
    if dominio.startswith('www.'):
        dominio = dominio[4:]
    return dominio

def main():
    print("=== COMPARACIÓN PRECISA URLs v5 vs v6 (POR DOMINIO) ===\n")
    
    # Cargar archivos
    try:
        v5_df = pd.read_csv("../visualizations/chile_oai_urls_limpio.csv")
        v6_df = pd.read_csv("../visualizations_v6/chile_oai_urls_limpio_v6.csv")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return
    
    # Extraer URLs y dominios
    v5_urls = set(v5_df['oai_url'].str.strip())
    v6_urls = set(v6_df['oai_url'].str.strip())
    
    # Crear mapas de dominio -> URLs
    v5_dominios = {}
    v6_dominios = {}
    
    for url in v5_urls:
        dominio = extraer_dominio(url)
        if dominio not in v5_dominios:
            v5_dominios[dominio] = []
        v5_dominios[dominio].append(url)
    
    for url in v6_urls:
        dominio = extraer_dominio(url)
        if dominio not in v6_dominios:
            v6_dominios[dominio] = []
        v6_dominios[dominio].append(url)
    
    # Conjuntos de dominios
    dominios_v5 = set(v5_dominios.keys())
    dominios_v6 = set(v6_dominios.keys())
    
    print(f"URLs v5: {len(v5_urls)}")
    print(f"URLs v6: {len(v6_urls)}")
    print(f"Dominios v5: {len(dominios_v5)}")
    print(f"Dominios v6: {len(dominios_v6)}")
    print(f"Diferencia neta URLs: {len(v6_urls) - len(v5_urls):+d}")
    print(f"Diferencia neta dominios: {len(dominios_v6) - len(dominios_v5):+d}")
    print()
    
    # Dominios comunes
    dominios_comunes = dominios_v5 & dominios_v6
    print(f"Dominios comunes: {len(dominios_comunes)} ({len(dominios_comunes)/len(dominios_v5)*100:.1f}% de v5)")
    print()
    
    # Dominios nuevos en v6
    dominios_nuevos = dominios_v6 - dominios_v5
    print(f"=== DOMINIOS NUEVOS EN v6 ({len(dominios_nuevos)}) ===")
    for dominio in sorted(dominios_nuevos):
        urls_dominio = v6_dominios[dominio]
        print(f"+ {dominio}")
        for url in urls_dominio:
            print(f"  {url}")
    print()
    
    # Dominios removidos en v6
    dominios_removidos = dominios_v5 - dominios_v6
    print(f"=== DOMINIOS REMOVIDOS EN v6 ({len(dominios_removidos)}) ===")
    for dominio in sorted(dominios_removidos):
        urls_dominio = v5_dominios[dominio]
        print(f"- {dominio}")
        for url in urls_dominio:
            print(f"  {url}")
    print()
    
    # URLs que cambiaron en el mismo dominio (solo cambios sustanciales)
    cambios_url_sustanciales = []
    cambios_url_menores = []
    
    for dominio in dominios_comunes:
        if set(v5_dominios[dominio]) != set(v6_dominios[dominio]):
            # Verificar si es solo cambio menor (www, path, protocolo)
            url_v5 = v5_dominios[dominio][0]
            url_v6 = v6_dominios[dominio][0]
            
            # Normalizar para comparación
            parsed_v5 = urlparse(url_v5.strip())
            parsed_v6 = urlparse(url_v6.strip())
            
            # Extraer dominios normalizados (sin www)
            dom_v5 = parsed_v5.netloc.lower().replace('www.', '')
            dom_v6 = parsed_v6.netloc.lower().replace('www.', '')
            
            # Si el dominio base es el mismo, es cambio menor
            if dom_v5 == dom_v6:
                cambios_url_menores.append(dominio)
            else:
                cambios_url_sustanciales.append(dominio)
    
    print(f"=== DOMINIOS CON CAMBIOS MENORES DE URL ({len(cambios_url_menores)}) ===")
    print("(Cambios de www, protocolo o path - se consideran coincidencias)")
    for dominio in sorted(cambios_url_menores):
        urls_v5_dominio = set(v5_dominios[dominio])
        urls_v6_dominio = set(v6_dominios[dominio])
        print(f"≈ {dominio}")
        print(f"  v5: {', '.join(urls_v5_dominio)}")
        print(f"  v6: {', '.join(urls_v6_dominio)}")
    print()
    
    if cambios_url_sustanciales:
        print(f"=== DOMINIOS CON CAMBIOS SUSTANCIALES DE URL ({len(cambios_url_sustanciales)}) ===")
        for dominio in sorted(cambios_url_sustanciales):
            urls_v5_dominio = set(v5_dominios[dominio])
            urls_v6_dominio = set(v6_dominios[dominio])
            print(f"~ {dominio}")
            print(f"  v5: {', '.join(urls_v5_dominio)}")
            print(f"  v6: {', '.join(urls_v6_dominio)}")
        print()
    
    # Verificación de dominios específicos
    print("=== VERIFICACIÓN DOMINIOS ESPECÍFICOS ===")
    joralres_v5 = 'joralres.com' in dominios_v5
    joralres_v6 = 'joralres.com' in dominios_v6
    biotaxa_v5 = 'biotaxa.org' in dominios_v5
    biotaxa_v6 = 'biotaxa.org' in dominios_v6
    
    print(f"joralres.com - v5: {joralres_v5}, v6: {joralres_v6}")
    print(f"biotaxa.org - v5: {biotaxa_v5}, v6: {biotaxa_v6}")
    
    if joralres_v5 and joralres_v6:
        print(f"  joralres v5: {v5_dominios['joralres.com']}")
        print(f"  joralres v6: {v6_dominios['joralres.com']}")
    
    if biotaxa_v5 and biotaxa_v6:
        print(f"  biotaxa v5: {v5_dominios['biotaxa.org']}")
        print(f"  biotaxa v6: {v6_dominios['biotaxa.org']}")
    
    # Calcular dominios realmente sin cambios
    dominios_sin_cambios = len([d for d in dominios_comunes if set(v5_dominios[d]) == set(v6_dominios[d])])
    dominios_efectivamente_iguales = dominios_sin_cambios + len(cambios_url_menores)
    
    print(f"\n✓ Comparación por dominios completada")
    print(f"\nRESUMEN AJUSTADO:")
    print(f"- Dominios realmente nuevos: {len(dominios_nuevos)}")
    print(f"- Dominios realmente removidos: {len(dominios_removidos)}")
    print(f"- Dominios con cambios sustanciales: {len(cambios_url_sustanciales)}")
    print(f"- Dominios con cambios menores (≈ iguales): {len(cambios_url_menores)}")
    print(f"- Dominios sin cambios: {dominios_sin_cambios}")
    print(f"\nDOMINIOS EFECTIVAMENTE IGUALES: {dominios_efectivamente_iguales} ({dominios_efectivamente_iguales/len(dominios_v5)*100:.1f}% de v5)")
    print(f"CRECIMIENTO NETO REAL: +{len(dominios_nuevos) - len(dominios_removidos)} dominios")

if __name__ == "__main__":
    main()