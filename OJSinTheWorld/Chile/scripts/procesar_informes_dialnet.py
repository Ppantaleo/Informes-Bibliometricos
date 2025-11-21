#!/usr/bin/env python3
"""
Script para procesar informes HTML de Dialnet y extraer información de calidad

Extrae:
- URL fuente y fecha de consulta
- Totales de errores por gravedad
- Tipos de errores más comunes
- Porcentajes de metadatos completos
"""

import os
import re
import csv
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extraer_porcentaje(texto):
    """Extrae el valor numérico de un porcentaje (ej: '55%' -> 55)"""
    match = re.search(r'(\d+(?:\.\d+)?)\s*%', texto)
    if match:
        return float(match.group(1))
    return None

def procesar_html_dialnet(ruta_html):
    """
    Procesa un archivo HTML de informe de Dialnet y extrae información estructurada

    Args:
        ruta_html: Path al archivo HTML

    Returns:
        dict con los datos extraídos
    """
    with open(ruta_html, 'r', encoding='utf-8') as f:
        contenido = f.read()

    soup = BeautifulSoup(contenido, 'html.parser')

    # Extraer nombre del archivo (dominio)
    dominio = Path(ruta_html).stem

    # Extraer URL fuente y fecha
    url_fuente = None
    fecha_consulta = None

    parrafos = soup.find_all('p')
    for p in parrafos:
        texto = p.get_text()
        if 'URL fuente:' in texto:
            link = p.find('a')
            if link:
                url_fuente = link.get('href', '')
        elif 'Fecha consulta:' in texto:
            match = re.search(r'Fecha consulta:\s*(.+)', texto)
            if match:
                fecha_consulta = match.group(1).strip()

    # Extraer totales de errores por gravedad
    errores_alta = 0
    errores_media = 0

    tablas = soup.find_all('table', class_='tablaIndice')
    if tablas:
        # Primera tabla contiene el resumen de gravedad
        primera_tabla = tablas[0]
        filas = primera_tabla.find_all('tr')
        for fila in filas:
            celdas = fila.find_all('td')
            if len(celdas) == 2:
                gravedad = celdas[0].get_text().strip()
                cantidad = celdas[1].get_text().strip()
                try:
                    cantidad_num = int(cantidad)
                    if 'Alta' in gravedad:
                        errores_alta = cantidad_num
                    elif 'Media' in gravedad:
                        errores_media = cantidad_num
                except ValueError:
                    pass

    # Extraer tipos de errores más comunes
    errores_detallados = []
    if len(tablas) > 1:
        segunda_tabla = tablas[1]
        filas = segunda_tabla.find_all('tr')
        for fila in filas:
            celdas = fila.find_all('td')
            if len(celdas) == 3:
                tipo_error = celdas[0].get_text().strip()
                gravedad = celdas[1].get_text().strip()
                ocurrencias = celdas[2].get_text().strip()
                try:
                    ocurrencias_num = int(ocurrencias)
                    errores_detallados.append({
                        'tipo': tipo_error,
                        'gravedad': gravedad,
                        'ocurrencias': ocurrencias_num
                    })
                except ValueError:
                    pass

    # Extraer metadatos completos a nivel de revista
    metadatos_revista = {}

    # Buscar el div con el título "Metadatos completos a nivel de Revista"
    h2_revista = soup.find('h2', string=re.compile(r'Metadatos completos a nivel de Revista'))
    if h2_revista:
        # Buscar el grid horizontal que contiene las barras
        contenedor = h2_revista.find_parent('div')
        if contenedor:
            grid = contenedor.find('div', class_='grid horizontal')
            if grid:
                barras = grid.find_all('div', class_='bar')
                for barra in barras:
                    nombre = barra.get('data-name', '')
                    titulo = barra.get('title', '')
                    porcentaje = extraer_porcentaje(titulo)
                    if nombre and porcentaje is not None:
                        metadatos_revista[nombre] = porcentaje

    # Extraer información de últimos ejemplares
    ejemplares = []

    # Buscar todos los ejemplares
    h2_ejemplares = soup.find_all('h2', class_='title', string=re.compile(r'EJEMPLAR'))
    for h2_ej in h2_ejemplares:
        titulo_ejemplar = h2_ej.get_text().strip()
        # Extraer año, vol, num
        match = re.search(r'(\d{4})\s+Vol\.\s*(\d+)\s+Nº\.\s*(\d+)', titulo_ejemplar)
        if match:
            anio, vol, num = match.groups()

            # Buscar metadatos del ejemplar
            contenedor_ej = h2_ej.find_parent('div', class_='chart-wrap ejemplar')
            if contenedor_ej:
                grid_ej = contenedor_ej.find('div', class_='grid horizontal')
                if grid_ej:
                    barras_ej = grid_ej.find_all('div', class_='bar')
                    metadatos_ej = {}
                    for barra in barras_ej:
                        nombre = barra.get('data-name', '')
                        titulo = barra.get('title', '')
                        porcentaje = extraer_porcentaje(titulo)
                        if nombre and porcentaje is not None:
                            metadatos_ej[nombre] = porcentaje

                    ejemplares.append({
                        'anio': anio,
                        'volumen': vol,
                        'numero': num,
                        'metadatos': metadatos_ej
                    })

    # Top 5 tipos de errores más frecuentes
    errores_detallados_sorted = sorted(errores_detallados, key=lambda x: x['ocurrencias'], reverse=True)
    top_errores = errores_detallados_sorted[:5]

    resultado = {
        'dominio': dominio,
        'url_fuente': url_fuente,
        'fecha_consulta': fecha_consulta,
        'errores_alta': errores_alta,
        'errores_media': errores_media,
        'errores_total': errores_alta + errores_media,
        'metadatos_revista': metadatos_revista,
        'top_errores': top_errores,
        'ejemplares': ejemplares[:5]  # Solo últimos 5 ejemplares
    }

    return resultado

def procesar_todos_informes(carpeta_dialnet):
    """
    Procesa todos los archivos HTML en la carpeta de Dialnet

    Args:
        carpeta_dialnet: Path a la carpeta con los HTML

    Returns:
        lista de diccionarios con los datos de cada informe
    """
    resultados = []

    carpeta = Path(carpeta_dialnet)
    archivos_html = sorted(carpeta.glob('*.html'))

    print(f"Procesando {len(archivos_html)} archivos HTML...")

    for archivo in archivos_html:
        print(f"  Procesando: {archivo.name}")
        try:
            datos = procesar_html_dialnet(archivo)
            resultados.append(datos)
        except Exception as e:
            print(f"    ERROR procesando {archivo.name}: {e}")

    return resultados

def generar_csv_resumen(resultados, archivo_salida):
    """
    Genera un CSV con el resumen de todos los informes

    Args:
        resultados: lista de diccionarios con datos procesados
        archivo_salida: path del archivo CSV de salida
    """
    if not resultados:
        print("No hay resultados para generar CSV")
        return

    # Campos principales
    campos = [
        'dominio',
        'url_fuente',
        'fecha_consulta',
        'errores_alta',
        'errores_media',
        'errores_total',
        'palabras_clave_pct',
        'autores_pct',
        'enlaces_pct',
        'referencias_pct',
        'resumenes_pct',
        'titulos_pct',
        'afiliaciones_pct',
        'top_error_1',
        'top_error_1_ocurrencias',
        'top_error_2',
        'top_error_2_ocurrencias',
        'top_error_3',
        'top_error_3_ocurrencias'
    ]

    with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

        for resultado in resultados:
            metadatos = resultado['metadatos_revista']
            top_errores = resultado['top_errores']

            fila = {
                'dominio': resultado['dominio'],
                'url_fuente': resultado['url_fuente'],
                'fecha_consulta': resultado['fecha_consulta'],
                'errores_alta': resultado['errores_alta'],
                'errores_media': resultado['errores_media'],
                'errores_total': resultado['errores_total'],
                'palabras_clave_pct': metadatos.get('Palabras clave', ''),
                'autores_pct': metadatos.get('Autores', ''),
                'enlaces_pct': metadatos.get('Enlaces', ''),
                'referencias_pct': metadatos.get('Referencias', ''),
                'resumenes_pct': metadatos.get('Resúmenes', ''),
                'titulos_pct': metadatos.get('Títulos', ''),
                'afiliaciones_pct': metadatos.get('Afiliaciones', ''),
            }

            # Agregar top 3 errores
            for i in range(3):
                if i < len(top_errores):
                    fila[f'top_error_{i+1}'] = top_errores[i]['tipo']
                    fila[f'top_error_{i+1}_ocurrencias'] = top_errores[i]['ocurrencias']
                else:
                    fila[f'top_error_{i+1}'] = ''
                    fila[f'top_error_{i+1}_ocurrencias'] = ''

            writer.writerow(fila)

    print(f"\nCSV generado: {archivo_salida}")

def generar_csv_detallado(resultados, archivo_salida):
    """
    Genera un CSV detallado con todos los tipos de errores por revista

    Args:
        resultados: lista de diccionarios con datos procesados
        archivo_salida: path del archivo CSV de salida
    """
    campos = [
        'dominio',
        'tipo_error',
        'gravedad',
        'ocurrencias'
    ]

    with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

        for resultado in resultados:
            for error in resultado['top_errores']:
                fila = {
                    'dominio': resultado['dominio'],
                    'tipo_error': error['tipo'],
                    'gravedad': error['gravedad'],
                    'ocurrencias': error['ocurrencias']
                }
                writer.writerow(fila)

    print(f"CSV detallado generado: {archivo_salida}")

def main():
    """Función principal"""
    # Definir rutas
    base_dir = Path(__file__).parent.parent
    carpeta_dialnet = base_dir / 'dialnet'
    carpeta_visualizations = base_dir / 'visualizations'

    # Crear carpeta de visualizations si no existe
    carpeta_visualizations.mkdir(exist_ok=True)

    # Procesar informes
    resultados = procesar_todos_informes(carpeta_dialnet)

    print(f"\nTotal de informes procesados: {len(resultados)}")

    if resultados:
        # Generar CSV resumen
        archivo_resumen = carpeta_visualizations / 'dialnet_informes_resumen.csv'
        generar_csv_resumen(resultados, archivo_resumen)

        # Generar CSV detallado de errores
        archivo_detallado = carpeta_visualizations / 'dialnet_errores_detallados.csv'
        generar_csv_detallado(resultados, archivo_detallado)

        # Mostrar estadísticas generales
        print("\n" + "="*60)
        print("ESTADÍSTICAS GENERALES")
        print("="*60)

        total_errores_alta = sum(r['errores_alta'] for r in resultados)
        total_errores_media = sum(r['errores_media'] for r in resultados)

        print(f"Total errores ALTA: {total_errores_alta:,}")
        print(f"Total errores MEDIA: {total_errores_media:,}")
        print(f"Total errores: {total_errores_alta + total_errores_media:,}")

        # Promedios de metadatos
        metadatos_tipos = ['Palabras clave', 'Autores', 'Enlaces', 'Referencias',
                          'Resúmenes', 'Títulos', 'Afiliaciones']

        print("\n" + "-"*60)
        print("PROMEDIOS DE COMPLETITUD DE METADATOS")
        print("-"*60)

        for tipo in metadatos_tipos:
            valores = [r['metadatos_revista'].get(tipo)
                      for r in resultados
                      if tipo in r['metadatos_revista']]
            if valores:
                promedio = sum(valores) / len(valores)
                print(f"{tipo:20s}: {promedio:6.1f}%")

if __name__ == '__main__':
    main()
