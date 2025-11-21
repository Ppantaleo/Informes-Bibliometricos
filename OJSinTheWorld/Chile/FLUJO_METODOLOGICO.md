# Flujo Metodológico - Análisis PKP Beacon Chile

## Orden de Ejecución

### 1. Procesamiento Base (Nivel Superior)
```bash
# Separar beacon por tipo de aplicación
cd Chile/
python3 scripts/split_beacon.py

# Análisis global OJS
Rscript scripts/analisis_ojs_mundial.R
```

### 2. Análisis Chile - Completo
```bash
cd Chile/
# Generar dataset completo de Chile (todos los criterios de país)
Rscript scripts/analisis_chile.R
# Genera: visualizations/chile_todas_instalaciones.csv
```

### 3. Análisis Chile - JUOJS (Dataset Principal)
```bash
cd Chile/
# Filtrar solo instalaciones activas (>5 pub/2023)
Rscript scripts/chile_juojs_filtrado.R
# Genera: visualizations/chile_juojs_activas.csv (DATASET PRINCIPAL)
```

### 4. Evaluación Dialnet
```bash
cd Chile/
# Generar URLs OAI desde dataset JUOJS
python3 scripts/generar_urls_dialnet.py
# Genera: visualizations/chile_oai_urls_limpio.csv

# Evaluación manual en Dialnet Nexus (proceso externo)
# Descarga de informes HTML en carpeta dialnet/

# Verificar completitud
python3 scripts/find_missing_reports.py
```

### 5. Enriquecimiento con APIs (Futuro)
```bash
cd Chile/
# OpenAlex (sobre dataset JUOJS)
python3 scripts/openalex_juojs.py

# Otras APIs (sobre dataset JUOJS)
# ...
```

## Archivos Principales

### Datasets Base
- `../../beacon.csv` - Dataset original PKP Beacon
- `../../beacon_ojs.csv` - Solo aplicaciones OJS

### Datasets Chile
- `visualizations/chile_todas_instalaciones.csv` - Todas las instalaciones (399)
- **`visualizations/chile_juojs_activas.csv`** - **DATASET PRINCIPAL** (JUOJS activas)

### Evaluación Dialnet
- `visualizations/chile_oai_urls_limpio.csv` - URLs para evaluación
- `dialnet/*.html` - Informes de calidad descargados

### Archivos Deprecated
- `deprecated/scripts/` - Scripts experimentales
- `deprecated/visualizations/` - Archivos de prueba

## Principios Metodológicos

1. **Dataset Principal**: `chile_juojs_activas.csv` (instalaciones con >5 pub/2023)
2. **Consistencia**: Todos los análisis parten del mismo dataset JUOJS
3. **Trazabilidad**: Cada paso genera archivos intermedios verificables
4. **Reproducibilidad**: Scripts documentados y ordenados secuencialmente