#!/usr/bin/env python3
"""
Script para analizar tipos de errores más comunes por gravedad desde informes Dialnet

Extrae:
- Top 5 errores de alta gravedad más frecuentes
- Top 5 errores de media gravedad más frecuentes
- Estadísticas adicionales de calidad editorial
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter, defaultdict

def procesar_errores_por_gravedad(carpeta_dialnet):
    """
    Procesa todos los HTMLs y extrae errores clasificados por gravedad
    """
    errores_alta = Counter()
    errores_media = Counter()
    
    carpeta = Path(carpeta_dialnet)
    archivos_html = sorted(carpeta.glob('*.html'))
    
    print(f"Analizando tipos de errores en {len(archivos_html)} informes...")
    
    for archivo in archivos_html:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            soup = BeautifulSoup(contenido, 'html.parser')
            
            # Buscar tabla de errores detallados (segunda tabla)
            tablas = soup.find_all('table', class_='tablaIndice')
            if len(tablas) > 1:
                segunda_tabla = tablas[1]
                filas = segunda_tabla.find_all('tr')
                
                for fila in filas:
                    celdas = fila.find_all('td')
                    if len(celdas) == 3:
                        # El primer td contiene un enlace con el texto del error
                        enlace = celdas[0].find('a')
                        if enlace:
                            tipo_error = enlace.get_text().strip()
                        else:
                            tipo_error = celdas[0].get_text().strip()
                        
                        gravedad = celdas[1].get_text().strip()
                        ocurrencias = celdas[2].get_text().strip()
                        
                        try:
                            ocurrencias_num = int(ocurrencias)
                            if gravedad.lower() == 'alta':
                                errores_alta[tipo_error] += ocurrencias_num
                            elif gravedad.lower() == 'media':
                                errores_media[tipo_error] += ocurrencias_num
                        except ValueError:
                            pass
                            
        except Exception as e:
            print(f"  Error procesando {archivo.name}: {e}")
    
    return errores_alta, errores_media

def analizar_distribucion_errores(carpeta_dialnet):
    """
    Analiza la distribución de errores por revista
    """
    distribucion = []
    
    carpeta = Path(carpeta_dialnet)
    archivos_html = sorted(carpeta.glob('*.html'))
    
    for archivo in archivos_html:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            soup = BeautifulSoup(contenido, 'html.parser')
            dominio = archivo.stem
            
            # Extraer totales por gravedad
            errores_alta = 0
            errores_media = 0
            
            tablas = soup.find_all('table', class_='tablaIndice')
            if tablas:
                primera_tabla = tablas[0]
                filas = primera_tabla.find_all('tr')
                for fila in filas:
                    # Verificar si la fila tiene clase 'alta' o 'media'
                    clase_fila = fila.get('class', [])
                    celdas = fila.find_all('td')
                    if len(celdas) == 2:
                        gravedad = celdas[0].get_text().strip()
                        cantidad = celdas[1].get_text().strip()
                        try:
                            cantidad_num = int(cantidad)
                            if gravedad.lower() == 'alta' or 'alta' in clase_fila:
                                errores_alta = cantidad_num
                            elif gravedad.lower() == 'media' or 'media' in clase_fila:
                                errores_media = cantidad_num
                        except ValueError:
                            pass
            
            distribucion.append({
                'dominio': dominio,
                'errores_alta': errores_alta,
                'errores_media': errores_media,
                'errores_total': errores_alta + errores_media
            })
            
        except Exception as e:
            print(f"  Error procesando {archivo.name}: {e}")
    
    return distribucion

def main():
    """Función principal"""
    print("=== ANÁLISIS DE TIPOS DE ERRORES DIALNET ===")
    
    carpeta_dialnet = "../dialnet"
    if not os.path.exists(carpeta_dialnet):
        print(f"❌ Error: No se encuentra la carpeta {carpeta_dialnet}")
        return
    
    # Analizar errores por gravedad
    errores_alta, errores_media = procesar_errores_por_gravedad(carpeta_dialnet)
    
    print(f"\n=== TOP 5 ERRORES DE ALTA GRAVEDAD ===")
    for i, (tipo_error, ocurrencias) in enumerate(errores_alta.most_common(5), 1):
        print(f"{i}. {tipo_error}: {ocurrencias:,} ocurrencias")
    
    print(f"\n=== TOP 5 ERRORES DE MEDIA GRAVEDAD ===")
    for i, (tipo_error, ocurrencias) in enumerate(errores_media.most_common(5), 1):
        print(f"{i}. {tipo_error}: {ocurrencias:,} ocurrencias")
    
    # Análisis de distribución
    distribucion = analizar_distribucion_errores(carpeta_dialnet)
    distribucion_ordenada = sorted(distribucion, key=lambda x: x['errores_total'], reverse=True)
    
    print(f"\n=== ESTADÍSTICAS ADICIONALES ===")
    
    # Revistas por rangos de errores
    rangos = {
        'Muy Alto (>2000)': len([r for r in distribucion if r['errores_total'] > 2000]),
        'Alto (1000-2000)': len([r for r in distribucion if 1000 <= r['errores_total'] <= 2000]),
        'Medio (500-999)': len([r for r in distribucion if 500 <= r['errores_total'] <= 999]),
        'Bajo (100-499)': len([r for r in distribucion if 100 <= r['errores_total'] <= 499]),
        'Muy Bajo (<100)': len([r for r in distribucion if r['errores_total'] < 100])
    }
    
    print("Distribución por rangos de errores:")
    for rango, cantidad in rangos.items():
        porcentaje = (cantidad / len(distribucion)) * 100
        print(f"  {rango}: {cantidad} revistas ({porcentaje:.1f}%)")
    
    # Proporción alta vs media gravedad
    total_alta = sum(errores_alta.values())
    total_media = sum(errores_media.values())
    total_errores = total_alta + total_media
    
    print(f"\nProporción de errores por gravedad:")
    if total_errores > 0:
        print(f"  Alta gravedad: {total_alta:,} ({total_alta/total_errores*100:.1f}%)")
        print(f"  Media gravedad: {total_media:,} ({total_media/total_errores*100:.1f}%)")
    else:
        print(f"  No se encontraron errores en los informes procesados")
        print(f"  Verificar estructura HTML de los archivos")
    
    # Revistas con mayor proporción de errores graves
    print(f"\n=== TOP 5 REVISTAS CON MAYOR PROPORCIÓN DE ERRORES GRAVES ===")
    revistas_proporcion = []
    for r in distribucion:
        if r['errores_total'] > 0:
            proporcion_alta = r['errores_alta'] / r['errores_total']
            revistas_proporcion.append({
                'dominio': r['dominio'],
                'proporcion_alta': proporcion_alta,
                'errores_alta': r['errores_alta'],
                'errores_total': r['errores_total']
            })
    
    revistas_proporcion_ordenadas = sorted(revistas_proporcion, key=lambda x: x['proporcion_alta'], reverse=True)
    for i, r in enumerate(revistas_proporcion_ordenadas[:5], 1):
        print(f"{i}. {r['dominio']}: {r['proporcion_alta']*100:.1f}% alta gravedad ({r['errores_alta']}/{r['errores_total']})")
    
    # Tipos de errores únicos
    tipos_unicos_alta = len(errores_alta)
    tipos_unicos_media = len(errores_media)
    tipos_unicos_total = len(set(list(errores_alta.keys()) + list(errores_media.keys())))
    
    print(f"\nDiversidad de tipos de errores:")
    print(f"  Tipos únicos alta gravedad: {tipos_unicos_alta}")
    print(f"  Tipos únicos media gravedad: {tipos_unicos_media}")
    print(f"  Tipos únicos total: {tipos_unicos_total}")
    
    print(f"\n✅ Análisis completado")

if __name__ == "__main__":
    main()