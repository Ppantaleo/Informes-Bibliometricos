#!/usr/bin/env python3
import pandas as pd

def main():
    # Leer los datasets necesarios
    print("Leyendo datasets...")
    
    # Dataset completo de Chile (todas las instalaciones)
    chile_completo = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_todas_instalaciones.csv')
    
    # Dataset de instalaciones activas (JUOJS)
    chile_activas = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_instalaciones_activas.csv')
    
    # Dataset de URLs para Dialnet
    chile_dialnet = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_oai_urls_limpio.csv')
    
    print("=== VERIFICACIÓN DE CRITERIOS JUOJS ===\n")
    
    # 1. Análisis general
    print("1. NÚMEROS GENERALES:")
    print(f"   - Total instalaciones Chile (dataset completo): {len(chile_completo)}")
    print(f"   - Instalaciones activas JUOJS (>5 pub/2023): {len(chile_activas)}")
    print(f"   - URLs evaluadas en Dialnet: {len(chile_dialnet)}")
    
    # 2. Análisis específico de uchile.cl
    print("\n2. ANÁLISIS UCHILE.CL:")
    
    # Filtrar uchile.cl en cada dataset
    uchile_completo = chile_completo[chile_completo['dominio'].str.contains('uchile.cl', na=False)]
    uchile_activas = chile_activas[chile_activas['dominio'].str.contains('uchile.cl', na=False)]
    uchile_dialnet = chile_dialnet[chile_dialnet['oai_url'].str.contains('uchile.cl', na=False)]
    
    print(f"   - Total uchile.cl (dataset completo): {len(uchile_completo)}")
    print(f"   - Activas uchile.cl (JUOJS): {len(uchile_activas)}")
    print(f"   - URLs uchile.cl en Dialnet: {len(uchile_dialnet)}")
    print(f"   - Diferencia (completo - activas): {len(uchile_completo) - len(uchile_activas)}")
    
    # 3. Verificar criterio de actividad
    print("\n3. VERIFICACIÓN CRITERIO ACTIVIDAD (>5 pub/2023):")
    
    if 'record_count_2023' in uchile_completo.columns:
        # Mostrar distribución de publicaciones 2023 para uchile.cl
        uchile_con_pub = uchile_completo[uchile_completo['record_count_2023'].notna()]
        activas_manual = uchile_con_pub[uchile_con_pub['record_count_2023'] > 5]
        inactivas_manual = uchile_con_pub[uchile_con_pub['record_count_2023'] <= 5]
        
        print(f"   - URLs uchile.cl con datos de publicaciones: {len(uchile_con_pub)}")
        print(f"   - URLs con >5 pub/2023: {len(activas_manual)}")
        print(f"   - URLs con ≤5 pub/2023: {len(inactivas_manual)}")
        
        # Mostrar algunas URLs inactivas
        print(f"\n   Ejemplos de URLs uchile.cl INACTIVAS (≤5 pub/2023):")
        for i, (_, row) in enumerate(inactivas_manual.head(5).iterrows(), 1):
            print(f"   {i}. {row['dominio']} ({row['record_count_2023']} pub)")
        
        # Mostrar algunas URLs activas
        print(f"\n   Ejemplos de URLs uchile.cl ACTIVAS (>5 pub/2023):")
        for i, (_, row) in enumerate(activas_manual.head(5).iterrows(), 1):
            print(f"   {i}. {row['dominio']} ({row['record_count_2023']} pub)")
    
    # 4. Verificar si Dialnet usa dataset completo
    print("\n4. VERIFICACIÓN FUENTE DIALNET:")
    
    # Comparar dominios de Dialnet con ambos datasets
    # Extraer dominios de las URLs de Dialnet
    import re
    def extract_domain(url):
        match = re.search(r'https?://([^/]+)', url)
        return match.group(1) if match else url
    
    dominios_dialnet = set(chile_dialnet['oai_url'].apply(extract_domain))
    dominios_completo = set(chile_completo['dominio'])
    dominios_activas = set(chile_activas['dominio'])
    
    # Dominios en Dialnet que NO están en activas pero SÍ en completo
    solo_en_completo = dominios_dialnet - dominios_activas
    solo_en_completo_y_en_dataset = solo_en_completo.intersection(dominios_completo)
    
    print(f"   - URLs en Dialnet que NO están en JUOJS activas: {len(solo_en_completo)}")
    print(f"   - De estas, cuántas SÍ están en dataset completo: {len(solo_en_completo_y_en_dataset)}")
    
    if len(solo_en_completo_y_en_dataset) > 0:
        print(f"\n   Ejemplos de dominios en Dialnet pero NO en JUOJS activas:")
        for i, dominio in enumerate(list(solo_en_completo_y_en_dataset)[:5], 1):
            # Buscar publicaciones 2023 si está disponible
            if 'record_count_2023' in chile_completo.columns:
                matching_rows = chile_completo[chile_completo['dominio'] == dominio]
                if len(matching_rows) > 0:
                    pub_info = matching_rows['record_count_2023'].iloc[0]
                    pub_text = f" ({pub_info} pub/2023)" if pd.notna(pub_info) else " (sin datos pub)"
                else:
                    pub_text = " (no encontrado)"
            else:
                pub_text = ""
            print(f"   {i}. {dominio}{pub_text}")
    
    # 5. Conclusión
    print(f"\n5. CONCLUSIÓN:")
    cobertura_completo = len(dominios_dialnet.intersection(dominios_completo)) / len(dominios_dialnet) * 100
    cobertura_activas = len(dominios_dialnet.intersection(dominios_activas)) / len(dominios_dialnet) * 100
    
    print(f"   - Dialnet cubre {cobertura_completo:.1f}% del dataset COMPLETO")
    print(f"   - Dialnet cubre {cobertura_activas:.1f}% del dataset ACTIVAS (JUOJS)")
    print(f"   - Confirmación: Dialnet usa el dataset {'COMPLETO' if cobertura_completo > cobertura_activas else 'ACTIVAS'}")

if __name__ == "__main__":
    main()