#!/usr/bin/env python3
"""
Script para consultar políticas de acceso abierto de revistas chilenas
usando la API de Sherpa Romeo (Open Policy Finder)

Extrae información sobre:
- Políticas de archivo de datos de acceso abierto
- Políticas de autoarchivo
- Condiciones de copyright
- Embargos y restricciones
"""

import pandas as pd
import requests
import time
import json
import os
from urllib.parse import quote

# Configuración
INPUT_FILE = 'visualizations/chile_juojs_activas.csv'
OUTPUT_FILE = 'visualizations/chile_sherpa_policies.csv'
RATE_LIMIT_DELAY = 1.0  # 1 segundo entre requests para ser respetuosos
BASE_URL = "https://v2.sherpa.ac.uk/cgi/retrieve"
# Solicitar API key al usuario
print("=== CONSULTA DE POLÍTICAS SHERPA ROMEO ===")
print("\nPara usar este script necesitas:")
print("1. Activar tu contraseña en Sherpa Romeo")
print("2. Iniciar sesión en https://v2.sherpa.ac.uk")
print("3. Obtener tu API key desde tu panel de usuario")

API_KEY = input("\nIngresa tu API key de Sherpa Romeo: ").strip()
if not API_KEY or API_KEY == "TU_API_KEY_AQUI":
    print("❌ Error: Necesitas proporcionar una API key válida")
    exit(1)

USERNAME = "ppantaleo"  # Tu username de Sherpa

def consultar_sherpa_romeo(issn):
    """
    Consulta la API de Sherpa Romeo para obtener políticas de una revista por ISSN
    """
    results = {
        'issn_consultado': issn,
        'sherpa_id': None,
        'titulo_sherpa': None,
        'editorial': None,
        'open_access_policy': None,
        'self_archiving_policy': None,
        'copyright_policy': None,
        'embargo_months': None,
        'preprint_archiving': None,
        'postprint_archiving': None,
        'publisher_version_archiving': None,
        'found_in_sherpa': False,
        'error': None
    }
    
    # Limpiar ISSN
    issn_clean = str(issn).strip()
    if issn_clean == 'Sin ISSN' or not issn_clean:
        results['error'] = 'Sin ISSN válido'
        return results
    
    # Si hay múltiples ISSNs, tomar el primero
    issn_list = issn_clean.replace('\n', ';').split(';')
    
    for issn_single in issn_list[:2]:  # Máximo 2 intentos
        issn_single = issn_single.strip()
        if len(issn_single) < 8:
            continue
            
        try:
            # Construir URL de consulta con autenticación
            params = {
                'item-type': 'publication',
                'format': 'Json',
                'filter': f'issn={issn_single}',
                'api-key': API_KEY
            }
            
            headers = {
                'User-Agent': f'Chile-OJS-Analysis/{USERNAME}'
            }
            
            response = requests.get(BASE_URL, params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verificar si se encontraron resultados
                if 'items' in data and len(data['items']) > 0:
                    item = data['items'][0]
                    
                    results['sherpa_id'] = item.get('id')
                    results['titulo_sherpa'] = item.get('title', [''])[0] if item.get('title') else None
                    results['found_in_sherpa'] = True
                    
                    # Extraer información del publisher
                    publishers = item.get('publishers', [])
                    if publishers:
                        publisher = publishers[0]
                        results['editorial'] = publisher.get('publisher', {}).get('name', [''])[0] if publisher.get('publisher', {}).get('name') else None
                        
                        # Extraer políticas
                        policies = publisher.get('publication_count', [])
                        if policies:
                            policy = policies[0]
                            
                            # Política de acceso abierto
                            oa_policy = policy.get('open_access_policy')
                            if oa_policy:
                                results['open_access_policy'] = oa_policy.get('policy_type')
                            
                            # Políticas de autoarchivo
                            archiving_policies = policy.get('self_archiving_policy', {})
                            if archiving_policies:
                                results['preprint_archiving'] = archiving_policies.get('preprint', {}).get('policy')
                                results['postprint_archiving'] = archiving_policies.get('postprint', {}).get('policy')
                                results['publisher_version_archiving'] = archiving_policies.get('publisher_version', {}).get('policy')
                                
                                # Embargo
                                postprint_info = archiving_policies.get('postprint', {})
                                if postprint_info and 'embargo' in postprint_info:
                                    embargo_info = postprint_info['embargo']
                                    if 'amount' in embargo_info:
                                        results['embargo_months'] = embargo_info['amount']
                            
                            # Política de copyright
                            copyright_info = policy.get('copyright_policy')
                            if copyright_info:
                                results['copyright_policy'] = copyright_info.get('policy_type')
                    
                    # Si encontramos datos, salir del loop
                    break
                    
            elif response.status_code == 429:
                results['error'] = 'Rate limit exceeded'
                time.sleep(5)  # Esperar más si hay rate limit
                
        except requests.exceptions.Timeout:
            results['error'] = 'Timeout'
        except requests.exceptions.RequestException as e:
            results['error'] = f'Request error: {str(e)}'
        except json.JSONDecodeError:
            results['error'] = 'Invalid JSON response'
        except Exception as e:
            results['error'] = f'Unexpected error: {str(e)}'
    
    return results

# Cargar datos de revistas chilenas activas
print(f"\nCargando {INPUT_FILE}...")
try:
    chile_activas = pd.read_csv(INPUT_FILE)
    print(f"Total revistas chilenas activas: {len(chile_activas)}")
except FileNotFoundError:
    print(f"❌ Error: No se encuentra el archivo {INPUT_FILE}")
    exit(1)

# Filtrar revistas con ISSN válido
revistas_con_issn = chile_activas[
    (chile_activas['issn'].notna()) & 
    (chile_activas['issn'] != 'Sin ISSN')
].copy()

print(f"Revistas con ISSN válido: {len(revistas_con_issn)}")

# Consultar Sherpa Romeo para cada revista
print(f"\nConsultando Sherpa Romeo API...")
print("Esto puede tomar varios minutos...")

sherpa_results = []

for idx, row in revistas_con_issn.iterrows():
    revista = row['context_name']
    issn = row['issn']
    
    print(f"  Consultando: {revista[:50]}... (ISSN: {issn})")
    
    # Consultar Sherpa Romeo
    sherpa_data = consultar_sherpa_romeo(issn)
    
    # Agregar información de la revista
    sherpa_data['context_name'] = revista
    sherpa_data['dominio'] = row.get('dominio', '')
    sherpa_data['total_record_count'] = row.get('total_historico', 0)
    
    sherpa_results.append(sherpa_data)
    
    # Respetar rate limits
    time.sleep(RATE_LIMIT_DELAY)
    
    # Guardar progreso cada 50 revistas
    if len(sherpa_results) % 50 == 0:
        temp_df = pd.DataFrame(sherpa_results)
        temp_df.to_csv('sherpa_progress.csv', index=False)
        print(f"    Progreso guardado: {len(sherpa_results)} revistas procesadas")

# Crear DataFrame con resultados
print(f"\nProcesando resultados...")
sherpa_df = pd.DataFrame(sherpa_results)

# Estadísticas
total_consultadas = len(sherpa_df)
encontradas = sherpa_df['found_in_sherpa'].sum()
con_politicas_oa = sherpa_df['open_access_policy'].notna().sum()
con_autoarchivo = sherpa_df['self_archiving_policy'].notna().sum()

print(f"\n=== ESTADÍSTICAS SHERPA ROMEO ===")
print(f"Total revistas consultadas: {total_consultadas}")
print(f"Encontradas en Sherpa Romeo: {encontradas} ({encontradas/total_consultadas*100:.1f}%)")
print(f"Con políticas de acceso abierto: {con_politicas_oa}")
print(f"Con políticas de autoarchivo: {con_autoarchivo}")

if encontradas > 0:
    encontradas_df = sherpa_df[sherpa_df['found_in_sherpa']]
    
    print(f"\n=== ANÁLISIS DE POLÍTICAS ===")
    
    # Políticas de acceso abierto
    if con_politicas_oa > 0:
        oa_policies = encontradas_df['open_access_policy'].value_counts()
        print(f"\nPolíticas de acceso abierto:")
        for policy, count in oa_policies.items():
            print(f"  {policy}: {count}")
    
    # Políticas de autoarchivo
    archiving_summary = {
        'Preprint permitido': encontradas_df['preprint_archiving'].notna().sum(),
        'Postprint permitido': encontradas_df['postprint_archiving'].notna().sum(),
        'Versión editorial permitida': encontradas_df['publisher_version_archiving'].notna().sum()
    }
    
    print(f"\nPolíticas de autoarchivo:")
    for policy, count in archiving_summary.items():
        print(f"  {policy}: {count}")
    
    # Embargos
    con_embargo = encontradas_df['embargo_months'].notna().sum()
    if con_embargo > 0:
        embargo_promedio = encontradas_df['embargo_months'].mean()
        print(f"\nEmbargos:")
        print(f"  Revistas con embargo: {con_embargo}")
        print(f"  Embargo promedio: {embargo_promedio:.1f} meses")

# Top revistas con mejores políticas de acceso abierto
print(f"\n=== TOP REVISTAS CON POLÍTICAS FAVORABLES ===")
if encontradas > 0:
    encontradas_df = sherpa_df[sherpa_df['found_in_sherpa']]
    favorables = encontradas_df[
        (encontradas_df['open_access_policy'].notna()) |
        (encontradas_df['postprint_archiving'].notna())
    ].copy()

    if len(favorables) > 0:
        top_favorables = favorables[[
            'context_name', 'issn_consultado', 'editorial', 
            'open_access_policy', 'postprint_archiving', 'embargo_months'
        ]].head(10)
        
        print(top_favorables.to_string(index=False))
    else:
        print("No se encontraron revistas con políticas favorables documentadas")
else:
    print("No se encontraron revistas chilenas en Sherpa Romeo")
    print("\nPosibles causas:")
    print("- Cobertura limitada de revistas latinoamericanas en Sherpa Romeo")
    print("- ISSNs chilenos no indexados en la base de datos")
    print("- Cambios en la estructura de la API")

# Guardar resultados
sherpa_df.to_csv(OUTPUT_FILE, index=False)

print(f"\n✅ Consulta completada")
print(f"Archivo generado: {OUTPUT_FILE}")
print(f"Total columnas: {len(sherpa_df.columns)}")

# Resumen de errores
errores = sherpa_df[sherpa_df['error'].notna()]
if len(errores) > 0:
    print(f"\n⚠ Advertencia: {len(errores)} revistas tuvieron errores en la consulta")
    error_types = errores['error'].value_counts()
    print("Tipos de errores:")
    for error, count in error_types.items():
        print(f"  {error}: {count}")

# Limpiar archivo temporal
if os.path.exists('sherpa_progress.csv'):
    os.remove('sherpa_progress.csv')