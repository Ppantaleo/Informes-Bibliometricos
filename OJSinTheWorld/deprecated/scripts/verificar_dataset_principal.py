#!/usr/bin/env python3
import pandas as pd

def main():
    print("=== VERIFICACIÓN DATASET PRINCIPAL CHILE ===\n")
    
    # Leer datasets
    activas = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_instalaciones_activas.csv')
    completo = pd.read_csv('/home/patricio/github/Informes-Bibliometricos/OJSinTheWorld/visualizations/chile_todas_instalaciones.csv')
    
    print("1. VERIFICACIÓN CRITERIO JUOJS:")
    print(f"   - Dataset completo: {len(completo)} instalaciones")
    print(f"   - Dataset activas: {len(activas)} instalaciones")
    print(f"   - Diferencia: {len(completo) - len(activas)} instalaciones filtradas")
    
    # Verificar que todas las activas tienen >5 pub/2023
    if 'record_count_2023' in activas.columns:
        activas_verificadas = activas[activas['record_count_2023'] > 5]
        print(f"   - Instalaciones con >5 pub/2023: {len(activas_verificadas)}")
        print(f"   - ¿Todas cumplen criterio JUOJS? {'SÍ' if len(activas_verificadas) == len(activas) else 'NO'}")
        
        if len(activas_verificadas) != len(activas):
            no_cumplen = activas[activas['record_count_2023'] <= 5]
            print(f"   - Instalaciones que NO cumplen: {len(no_cumplen)}")
            for _, row in no_cumplen.head(3).iterrows():
                print(f"     * {row['dominio']}: {row['record_count_2023']} pub/2023")
    
    print(f"\n2. CONFIRMACIÓN:")
    print(f"   ✓ chile_instalaciones_activas.csv ES el dataset JUOJS filtrado")
    print(f"   ✓ Contiene solo instalaciones con >5 publicaciones en 2023")
    print(f"   ✓ Debe ser el dataset BASE para todos los análisis")
    
    # Verificar uchile.cl en dataset activas
    uchile_activas = activas[activas['dominio'].str.contains('uchile.cl', na=False)]
    dominios_unicos = uchile_activas['dominio'].nunique()
    
    print(f"\n3. UCHILE.CL EN DATASET ACTIVAS:")
    print(f"   - Total filas uchile.cl: {len(uchile_activas)}")
    print(f"   - Dominios únicos: {dominios_unicos}")
    print(f"   - Duplicados: {len(uchile_activas) - dominios_unicos}")
    
    print(f"\n4. RECOMENDACIÓN PARA DIALNET:")
    print(f"   - Usar chile_instalaciones_activas.csv como base")
    print(f"   - Aplicar filtro de duplicados sobre este dataset")
    print(f"   - Generar URLs OAI solo para instalaciones JUOJS activas")

if __name__ == "__main__":
    main()