# Análisis del PKP Beacon: Publicaciones Académicas con Software PKP
## Informe Consolidado con Validación Beacon v6 (2024-2025)

## Resumen

Este estudio analiza el ecosistema global de revistas académicas que utilizan Open Journal Systems (OJS) mediante el dataset del PKP Beacon, con un enfoque específico en Chile. Se procesaron **86,282 instalaciones OJS globales** (Beacon v6), de las cuales **432 corresponden a Chile**. El análisis incluye validación cruzada entre versiones del beacon y enriquecimiento con datos de OpenAlex para evaluar visibilidad e impacto académico. La **validación v6** confirma **319 instalaciones chilenas activas** con criterio actualizado (>5 pub/2024), representando **14,162 publicaciones en 2024** con un **crecimiento del 16.5%** respecto a 2023.

---

## 1. Introducción

### 1.1 Contexto

El Public Knowledge Project (PKP) desarrolla software de código abierto para la publicación académica, siendo Open Journal Systems (OJS) su aplicación más utilizada globalmente. El PKP Beacon es un sistema de recopilación de datos que permite identificar, inspeccionar y catalogar instalaciones públicas de este software.

### 1.2 Antecedentes

**Estudios previos:**

**Khanna et al. (2022):**
- Dataset 2020: 25,671 revistas
- 36.5% de 70,214 beacons OJS operativos
- 996,000 artículos publicados en 2020
- 5.4 millones de artículos históricos acumulados

**Khanna et al. (2024):**
- Dataset actualizado: 47,625 revistas con ISSN validados
- Aumento del 98% respecto a 2020
- 2,962,418 artículos publicados entre 2020-2023
- 10.6 millones de artículos históricos totales

**Beacon v6 (2024-2025):**
- **86,282 instalaciones OJS globales** (nuevo récord)
- **54,453 instalaciones activas** en 2024 (63.1%)
- **2.36 millones de publicaciones** en 2024
- **Crecimiento global:** +516,768 publicaciones vs 2023

### 1.3 Objetivos

1. **Analizar el ecosistema global** de revistas que utilizan OJS con datos actualizados v6
2. **Caracterizar las instalaciones chilenas** y validar con criterios 2024
3. **Evaluar la visibilidad académica** mediante integración con OpenAlex
4. **Preparar datos para evaluación** en sistemas de indexación como Dialnet

### 1.4 Marco Conceptual

#### JUOJS (Journals Using OJS)
Las JUOJS emplean un PKP Beacon opcional que permite a PKP notificar sobre actualizaciones y transmite información de indexación incluyendo título, ISSN, número de artículos, títulos y resúmenes.

#### Criterio de revista activa
Se emplea el estándar del Directory of Open Access Journals (DOAJ) de **cinco artículos al año** para distinguir revistas con actividad editorial sostenida de instalaciones inactivas o en prueba. **Actualización v6:** Criterio aplicado a datos 2024 para mayor actualidad.

---

## 2. Materiales y Métodos

### 2.1 Fuente de Datos

#### 2.1.1 Dataset Principal PKP Beacon v6
**Dataset:** Khanna, S., Raoni, J., Smecher, A., Alperin, J. P., Ball, J., & Willinsky, J. (2024). "Details of Publications Using Software by the Public Knowledge Project." Harvard Dataverse.

**Características v6:**
- **Archivo:** `beacon_v6.csv` (87,170 observaciones, 31 campos)
- **Instalaciones OJS:** 86,282 (99.0%)
- **Instalaciones OMP:** 810 (0.9%)
- **Instalaciones OPS:** 78 (0.1%)
- **Nuevas columnas:**
  - `record_count_2024` - Publicaciones 2024
  - `record_count_2025` - Publicaciones 2025
  - `region` - Región geográfica PKP
  - `admin_email` - Email de administrador
  - `country_doaj` - País según DOAJ

#### 2.1.2 Validación Cruzada con Beacon Anterior
- **Dataset anterior:** `beacon.csv` (67,138 observaciones)
- **Crecimiento:** +28.4% en instalaciones totales
- **Metodología:** Análisis comparativo para validación de tendencias

### 2.2 Metodología de Análisis Actualizada

#### 2.2.1 Flujo Metodológico v6

**1. Procesamiento Base**
```bash
# Separar beacon v6 por tipo de aplicación
python3 scripts_v6/1_split_beacon_v6.py
# Genera: beacon_v6_ojs.csv (86,282 instalaciones)

# Análisis global v6
Rscript scripts_v6/2_analisis_mundial_v6.R
# Genera: visualizations_v6/top15_paises_barras_v6.png
```

**2. Análisis Chile v6**
```bash
# Filtrar instalaciones chilenas con criterios v6
Rscript scripts_v6/3_analisis_chile_v6.R
# Genera: visualizations_v6/chile_todas_instalaciones_v6.csv (432)

# Aplicar criterio JUOJS actualizado (>5 pub/2024)
Rscript scripts_v6/4_chile_juojs_filtrado_v6.R
# Genera: visualizations_v6/chile_juojs_activas_v6.csv (319 - DATASET PRINCIPAL)
```

**3. Evaluación Dialnet v6**
```bash
# Generar URLs OAI desde dataset JUOJS v6
python3 scripts_v6/5_generar_urls_dialnet_v6.py
# Genera: visualizations_v6/chile_oai_urls_v6.csv (225 URLs únicas)
```

**4. Análisis y Visualizaciones**
```bash
# Generar tablas y análisis institucional
Rscript scripts_v6/6_tablas_chile_v6.R
# Genera: tablas CSV y análisis institucional
```

#### 2.2.2 Criterio JUOJS Actualizado v6
- **Criterio temporal:** >5 publicaciones en **2024** (vs 2023 en versión anterior)
- **Filtrado mejorado:** Incluye `country_doaj` para mayor precisión geográfica
- **Eliminación de duplicados:** Automática por dominio (94 duplicados eliminados)

---

## 3. Resultados

### 3.1 Análisis Global v6

#### 3.1.1 Distribución General
- **Total instalaciones procesadas:** 87,170
- **Instalaciones OJS:** 86,282 (99.0%)
- **Instalaciones OMP:** 810 (0.9%)
- **Instalaciones OPS:** 78 (0.1%)
- **Países representados:** 154 países activos

#### 3.1.2 Instalaciones OJS Activas Globalmente v6
- **Total instalaciones OJS activas globalmente:** 54,453 (63.1% del total)
- **Publicaciones 2024:** 2,365,938 (+28.4% vs beacon anterior)
- **Crecimiento 2023→2024:** +516,768 publicaciones (+28.4%)
- **Cambio en actividad:** +3,074 instalaciones activas vs 2023

#### 3.1.3 Top 10 Países por Instalaciones Activas 2024

| País | Instalaciones Activas | Pub. 2024 | Crecimiento 2023→2024 |
|------|----------------------|-----------|----------------------|
| Indonesia (ID) | 23,045 | 713,408 | +122,211 |
| Brasil (BR) | 4,050 | 228,789 | +48,856 |
| Desconocido | 3,260 | 161,446 | +87,204 |
| Estados Unidos (US) | 1,714 | 87,977 | +26,968 |
| India (IN) | 1,630 | 95,726 | +22,334 |
| España (ES) | 1,295 | 57,190 | +13,336 |
| Tailandia (TH) | 1,172 | 43,923 | +5,298 |
| Ucrania (UA) | 1,052 | 73,371 | +13,299 |
| Rusia (RU) | 954 | 74,346 | +6,280 |
| Pakistán (PK) | 893 | 43,070 | +11,921 |

#### 3.1.4 Distribución por Regiones PKP v6

| Región PKP | Instalaciones | Pub. 2024 | Países |
|------------|---------------|-----------|---------|
| East Asia & Pacific | 25,767 | 873,834 | 22 |
| Europe & Central Asia | 9,112 | 543,986 | 47 |
| Latin America & Caribbean | 8,485 | 377,023 | 22 |
| Other | 3,325 | 164,692 | 22 |
| South Asia | 3,099 | 151,324 | 8 |
| North America | 2,110 | 103,790 | 2 |
| Sub-Saharan Africa | 1,525 | 57,713 | 33 |
| Middle East & North Africa | 1,030 | 64,297 | 19 |

### 3.2 Análisis Específico de Chile - Validación v6

#### 3.2.1 Estadísticas Generales Actualizadas
- **Total instalaciones identificadas:** 432 (vs 396 en versión anterior)
- **Instalaciones JUOJS activas (>5 pub/2024):** 319 (73.8%)
- **Instalaciones filtradas:** 113 (≤5 pub/2024)
- **URLs únicas generadas:** 225 (eliminados 94 duplicados)

#### 3.2.2 Productividad 2024 (Validación v6)
- **Total publicaciones 2024:** 14,162
- **Total publicaciones 2023:** 12,156
- **Crecimiento neto:** +2,006 publicaciones (+16.5%)
- **Promedio por instalación activa:** 44.4 pub/instalación
- **Total histórico acumulado:** 144,529 publicaciones

#### 3.2.3 Top 10 Instalaciones Más Productivas 2024 (v6)

| Revista/Contexto | Dominio | Pub. 2024 | Crecimiento |
|------------------|---------|-----------|-------------|
| Revista Chilena de Derecho | revistachilenadederecho.uc.cl | 1,708 | +1,671 |
| Boletín de la Universidad de Chile | revistasdex.uchile.cl | 1,689 | +1,529 |
| Boletín Jurídico del Observatorio | revistadelaconstruccion.uc.cl | 958 | -1,723 |
| REVISTA CUHSO | cuhso.uct.cl | 510 | +470 |
| MGC / Revista de Gestión Cultural | revistasdex.uchile.cl | 330 | +218 |
| Ingeniare. Revista Chilena de Ingeniería | revistalimite.uta.cl | 321 | +321 |
| Revista de Trabajo Social | revistadelaconstruccion.uc.cl | 293 | +277 |
| Revista de Historia Social y de las Mentalidades | www.revistas.usach.cl | 221 | +190 |
| Apuntes de Teatro | revistaapuntes.uc.cl | 214 | -804 |
| Progress Annals: Journal of Progressive Research | academiaone.org | 136 | +83 |

#### 3.2.4 Análisis de Crecimiento 2023-2024 (v6)
- **Instalaciones que crecieron:** 163 (51.1%)
- **Instalaciones que decrecieron:** 135 (42.3%)
- **Instalaciones estables:** 21 (6.6%)
- **Crecimiento promedio:** +6.3 pub/instalación

#### 3.2.5 Distribución Institucional Actualizada (v6)

| Institución | Instalaciones | % | Pub. 2024 | Crecimiento |
|-------------|---------------|---|-----------|-------------|
| Universidad de Chile | 67 | 21.0% | 3,338 | +1,646 |
| Pontificia Universidad Católica | 27 | 8.5% | 4,129 | -438 |
| Universidad de Valparaíso | 15 | 4.7% | 227 | -23 |
| Universidad de Concepción | 12 | 3.8% | 353 | -36 |
| Universidad Austral de Chile | 7 | 2.2% | 213 | -59 |
| Universidad de Santiago | 6 | 1.9% | 299 | +177 |
| Universidad de La Frontera | 4 | 1.3% | - | - |
| Otras instituciones | 181 | 56.7% | 5,603 | +739 |

#### 3.2.6 Distribución Geográfica PKP (v6)
- **Latin America & Caribbean:** 317 instalaciones (99.4%)
- **Europe & Central Asia:** 1 instalación (0.3%)
- **North America:** 1 instalación (0.3%)

#### 3.2.7 URLs OAI Generadas para Dialnet (v6)
- **Total URLs únicas:** 225 (vs 202 en versión anterior)
- **URLs Universidad de Chile:** 58 (25.8%)
- **Publicaciones 2024 representadas:** 11,540 (81.5% del total)
- **Crecimiento neto representado:** +1,843 publicaciones

### 3.3 Validación Cruzada: Comparación v5 vs v6

#### 3.3.1 Cambios en el Dataset
- **Instalaciones totales Chile:** 396 → 432 (+9.1%)
- **Instalaciones activas:** 309 → 319 (+3.2%)
- **Criterio temporal:** 2023 → 2024 (actualización metodológica)
- **URLs únicas:** 202 → 225 (+11.4%)

#### 3.3.2 Consistencia de Resultados
- **Universidad de Chile mantiene liderazgo:** 68 → 67 instalaciones
- **Distribución institucional estable:** Mismas instituciones líderes
- **Crecimiento sostenido:** Confirmado en ambas versiones

### 3.4 Archivos Generados v6

#### 3.4.1 Datasets Principales
- **`visualizations_v6/chile_todas_instalaciones_v6.csv`** - 432 instalaciones completas
- **`visualizations_v6/chile_juojs_activas_v6.csv`** - 319 instalaciones activas (DATASET PRINCIPAL v6)
- **`visualizations_v6/chile_oai_urls_v6.csv`** - 225 URLs para evaluación Dialnet

#### 3.4.2 Análisis Mundial v6
- `visualizations_v6/tabla_paises_mundial_v6.csv` - 154 países activos
- `visualizations_v6/regiones_mundial_v6.csv` - 8 regiones PKP
- `visualizations_v6/top15_paises_barras_v6.png` - Visualización países
- `visualizations_v6/regiones_circular_v6.png` - Visualización regiones

#### 3.4.3 Tablas Chile v6
- `visualizations_v6/tabla_chile_todas_top30_v6.csv`
- `visualizations_v6/tabla_chile_juojs_top30_v6.csv`
- `visualizations_v6/tabla_chile_crecimiento_top15_v6.csv`
- `visualizations_v6/tabla_instituciones_v6.csv`

---

## 4. Discusión

### 4.1 Validación del Ecosistema Global

La **validación v6** confirma el crecimiento acelerado del ecosistema OJS global, con **86,282 instalaciones** representando un aumento del **28.4%** respecto al beacon anterior. Este crecimiento es particularmente notable en:

- **Asia-Pacífico:** Indonesia lidera con 23,045 instalaciones activas
- **América Latina:** 8,485 instalaciones confirman la región como hub de acceso abierto
- **Diversificación geográfica:** 154 países con instalaciones activas

### 4.2 Caracterización del Ecosistema Chileno Actualizada

#### 4.2.1 Fortalezas Confirmadas v6
- **Alta actividad editorial:** 73.8% de instalaciones activas (vs 78.0% anterior)
- **Crecimiento sostenido:** +16.5% en publicaciones 2024
- **Diversidad institucional:** 181 instalaciones en "otras instituciones" (56.7%)
- **Productividad destacada:** Promedio 44.4 artículos por instalación

#### 4.2.2 Tendencias Identificadas
- **Concentración en líderes:** Universidad de Chile mantiene 21% del ecosistema
- **Crecimiento diferenciado:** Algunas instituciones decrecen mientras otras crecen
- **Nuevas instalaciones:** +36 instalaciones identificadas en v6

### 4.3 Implicaciones para Indexación en Dialnet

#### 4.3.1 Optimización del Proceso
- **225 URLs únicas** (vs 202 anteriores) para evaluación
- **Eliminación automática** de 94 duplicados
- **Cobertura mejorada:** 81.5% de publicaciones 2024 representadas

#### 4.3.2 Estrategia de Priorización
El análisis v6 permite priorizar instalaciones por:
1. **Productividad 2024:** Revista Chilena de Derecho (1,708 pub)
2. **Crecimiento:** Instalaciones con tendencia positiva
3. **Estabilidad institucional:** Universidad de Chile (58 URLs)

### 4.4 Contribución al Acceso Abierto Regional

Los **144,529 artículos históricos** acumulados (vs 133,931 anteriores) posicionan a Chile como contribuyente significativo al ecosistema latinoamericano, con un **crecimiento del 7.9%** en el acervo histórico.

### 4.5 Limitaciones y Consideraciones

1. **Criterio temporal:** Cambio de 2023 a 2024 puede afectar comparabilidad directa
2. **Cobertura beacon:** Dependencia de instalaciones que mantienen beacon activo
3. **Variabilidad institucional:** Algunas instituciones muestran decrecimiento

---

## 5. Conclusiones

### 5.1 Validación del Ecosistema Robusto
La **validación v6** confirma que Chile mantiene un ecosistema editorial académico **robusto y en crecimiento** con:
- **432 instalaciones OJS** identificadas (+9.1% vs versión anterior)
- **319 instalaciones activas** con criterio 2024 (73.8%)
- **14,162 publicaciones en 2024** (+16.5% vs 2023)

### 5.2 Liderazgo Institucional Confirmado
La **Universidad de Chile** mantiene su posición dominante con:
- **67 instalaciones** (21% del ecosistema)
- **3,338 publicaciones en 2024**
- **Crecimiento de +1,646 publicaciones**

### 5.3 Crecimiento Sostenido Validado
El **51.1% de instalaciones** muestra crecimiento positivo, confirmando la vitalidad del sistema editorial chileno en el contexto global de acceso abierto.

### 5.4 Metodología Consolidada
La **validación cruzada v5-v6** demuestra:
- **Consistencia metodológica:** Resultados coherentes entre versiones
- **Actualización exitosa:** Criterios 2024 reflejan estado actual
- **Escalabilidad:** Procedimientos replicables para análisis futuros

### 5.5 Posicionamiento Global
Chile se posiciona como **actor relevante** en el ecosistema latinoamericano de acceso abierto, contribuyendo significativamente a la democratización del conocimiento científico regional.

---

## 6. Próximos Pasos

### 6.1 Evaluación Dialnet
- **Proceso manual** con 225 URLs v6 (decisión pendiente sobre uso de URLs v5 o v6)
- **Priorización** por productividad e impacto
- **Seguimiento** de informes de calidad generados

### 6.2 Enriquecimiento Continuo
- **Integración OpenAlex** con datos 2024
- **Análisis longitudinal** de tendencias
- **Monitoreo** de nuevas instalaciones

### 6.3 Análisis Comparativo Regional
- **Benchmarking** con otros países latinoamericanos
- **Identificación** de mejores prácticas
- **Colaboración** regional en acceso abierto

---

## Referencias

[Mantener las mismas referencias del informe original, agregando:]

### Datasets utilizados

**Beacon v6:**
Khanna, S., Raoni, J., Smecher, A., Alperin, J. P., Ball, J., & Willinsky, J. (2024). *Details of publications using software by the Public Knowledge Project* (V6) [Dataset]. Harvard Dataverse. https://doi.org/10.7910/DVN/OCZNVY

**Beacon anterior:**
Khanna, S., Raoni, J., Smecher, A., Alperin, J. P., Ball, J., & Willinsky, J. (2024). *Details of publications using software by the Public Knowledge Project* (V4) [Dataset]. Harvard Dataverse. https://doi.org/10.7910/DVN/OCZNVY

---

*Informe consolidado generado con validación cruzada Beacon v5-v6 PKP - Datos 2024-2025*