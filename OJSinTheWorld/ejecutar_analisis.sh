#!/bin/bash

# Script para ejecutar todos los análisis OJS
echo "=========================================="
echo "EJECUTANDO ANÁLISIS COMPLETO OJS"
echo "=========================================="

# Crear directorio de visualizaciones si no existe
mkdir -p visualizations

# 1. Filtrar beacon para obtener solo OJS
echo ""
echo "1. Filtrando beacon para obtener solo aplicaciones OJS..."
python3 split_beacon.py

# 2. Análisis básico mundial
echo ""
echo "2. Ejecutando análisis básico mundial..."
Rscript analisis_basico.R

# 3. Análisis mundial detallado
echo ""
echo "3. Ejecutando análisis mundial detallado..."
Rscript analisis_ojs_mundial.R

# 4. Análisis específico de Chile
echo ""
echo "4. Ejecutando análisis específico de Chile..."
Rscript analisis_chile.R

# 5. Gráficos por continentes
echo ""
echo "5. Generando gráficos por continentes..."
Rscript grafico_continentes.R

# 6. Tablas como imágenes
echo ""
echo "6. Generando tablas como imágenes..."
Rscript generar_tabla_imagen.R
Rscript generar_tabla_simple.R
Rscript tablas_chile_png.R

echo ""
echo "=========================================="
echo "✓ ANÁLISIS COMPLETADO"
echo "=========================================="
echo ""
echo "Archivos generados en visualizations/:"
ls -la visualizations/

echo ""
echo "Para ver los resultados, revisa:"
echo "- ojsInTheWorld.md (documentación)"
echo "- visualizations/ (gráficos y tablas)"