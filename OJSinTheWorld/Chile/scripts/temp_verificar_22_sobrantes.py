#!/usr/bin/env python3
import pandas as pd

def verificar_sobrantes():
    # Lista de archivos HTML sobrantes (sin extensión .html)
    archivos_sobrantes = [
        "www.j-miner.cl", "www.salud.uda.cl", "www.revistas.uda.cl", "www.mpc.ms-editions.cl",
        "www.rae-ear.org", "www.debatesjuridicosysociales.cl", "www.rioc.ufro.cl", 
        "www.espacioysociedad.cl", "www.gestionytendencias.cl", "www.revistapensamientoacademico.cl",
        "www.capicreview.com", "www.praxis.uahurtado.cl", "www.ducere.cl", 
        "www.revistaestudioshemisfericosypolares.cl", "www.rehabilitacionintegral.cl",
        "www.macrohistoria.com", "www.revistamahpat.com", "www.nuevasdimensiones.uahurtado.cl",
        "revistachilenadeneurocirugia.com", "www.jcchems.com", "www.joralres.com", "www.europadelesteunida.com"
    ]
    
    # Leer beacon completo
    df_beacon = pd.read_csv('../beacon_ojs.csv')
    df_todas = pd.read_csv('visualizations/chile_todas_instalaciones.csv')
    
    print("=== VERIFICACIÓN COMPLETA DE 22 ARCHIVOS SOBRANTES ===\n")
    
    for archivo in archivos_sobrantes:
        dominio_base = archivo.replace('www.', '')
        print(f"📁 {archivo}.html")
        
        # Buscar en beacon con múltiples variantes
        variantes = [
            archivo,
            dominio_base,
            f"https://{archivo}",
            f"http://{archivo}",
            f"https://{dominio_base}",
            f"http://{dominio_base}"
        ]
        
        encontrado_beacon = False
        for variante in variantes:
            beacon_match = df_beacon[df_beacon['oai_url'].str.contains(variante, case=False, na=False)]
            if len(beacon_match) > 0:
                print(f"   ✅ ENCONTRADO en beacon: {variante}")
                print(f"      Revista: {beacon_match.iloc[0]['context_name']}")
                print(f"      Pub 2023: {beacon_match.iloc[0]['record_count_2023']}")
                print(f"      URL beacon: {beacon_match.iloc[0]['oai_url']}")
                encontrado_beacon = True
                break
        
        if not encontrado_beacon:
            print(f"   ❌ NO encontrado en beacon")
        
        # Buscar en dataset completo de Chile con criterio amplio
        todas_matches = df_todas[df_todas['dominio'].str.contains(dominio_base, case=False, na=False)]
        
        if len(todas_matches) > 0:
            for _, match in todas_matches.iterrows():
                print(f"   📊 Dataset Chile: {match['context_name']}")
                print(f"      Dominio: {match['dominio']}")
                print(f"      Pub 2023: {match['record_count_2023']}")
                print(f"      Activa: {match['activa']}")
                if match['record_count_2023'] <= 5:
                    print(f"      ❌ ELIMINADA por criterio JUOJS (≤5 pub/2023)")
                else:
                    print(f"      ⚠️  DEBERÍA estar en JUOJS (>5 pub/2023)")
        
        print()

if __name__ == "__main__":
    verificar_sobrantes()