# Análisis del PKP Beacon: Publicaciones Académicas con Software PKP

## 1. Información General del Dataset

**Fuente:** Khanna, Saurabh, Jonas Raoni, Alec Smecher, Juan Pablo Alperin, Jon Ball, and John Willinsky. 2024. "Details of Publications Using Software by the Public Knowledge Project." Harvard Dataverse.

**DOI:** https://doi.org/10.7910/DVN/OCZNVY

**Última actualización:** 2 de diciembre de 2024

**Fecha de consulta:** 23 de octubre de 2025

**Licencia:** CC0 1.0 (dominio público)

**Publicación relacionada:** Khanna, S., Ball, J., Alperin, J. P., & Willinsky, J. (2022). Recalibrating the Scope of Scholarly Publishing: A Modest Step in a Vast Decolonization Process. *Quantitative Science Studies*. https://doi.org/10.1162/qss_a_00228

---

## 2. ¿Qué es el PKP Beacon?

El PKP Beacon es un sistema de recopilación de datos que permite identificar, inspeccionar y catalogar instalaciones públicas del software de publicación académica desarrollado por el Public Knowledge Project (PKP). 

### Software incluido en el dataset

El dataset incluye información sobre las siguientes aplicaciones:

1. **Open Journal Systems (OJS)** - versión 2.4.7 (octubre 2015) o posterior
   - Software de código abierto para gestión y publicación de revistas académicas
   
2. **Open Monograph Press (OMP)** - versión 1.2.0 (abril 2016) o posterior
   - Plataforma para publicación de monografías académicas
   
3. **Open Preprint Server (OPS)** - todas las versiones
   - Sistema para servidores de preprints

### Funcionamiento del Beacon

El beacon funciona mediante un intercambio de datos automático entre las instalaciones del software y el servidor de PKP:

- Cuando una instalación verifica si hay una nueva versión disponible, envía datos a PKP
- La información se captura en los logs de acceso del servidor web de PKP
- Los datos enviados incluyen:
  - URL del endpoint OAI-PMH
  - Identificador único (uniqid) para desambiguación

**Nota importante:** en versiones antiguas, deshabilitar la verificación de versiones también deshabilitaba el beacon. Esto se corrigió en versiones recientes para que ambas funciones sean independientes.

---

## 3. Archivo del Dataset

**Nombre:** `beacon.tab`

**Formato:** CSV/TSV (datos tabulares)

**Tamaño:** 22.2 MB

**Registros:** 67,138 observaciones

**Variables:** 25 campos

**UNF:** 6:9toe...dww==

---

## 4. Diccionario de Datos

### Campos descriptivos

| Campo | Ejemplo | Descripción |
|-------|---------|-------------|
| `application` | OJS | Tipo de aplicación (OJS, OMP o OPS) |
| `version` | 2.4.2.0, 3.2.1.4 | Versión del software |
| `country` | id, br, us | Código ISO 3166-1 alpha-2 del país estimado de origen de la revista |
| `country_marc` | Macedonia | País MARC extraído de la API ISSN de LOC |
| `country_issn` | US | País MARC convertido a ISO3166 |
| `country_tld` | FR | País extraído del dominio de nivel superior (TLD) como ISO3166 |
| `country_ip` | BR | País extraído mediante geolocalización como ISO3166 |
| `country_consolidated` | CA | País resuelto/final asignado a la revista (primer valor no vacío de: country_issn, country_tld, country_ip) |

### Campos de datos principales

| Campo | Ejemplo | Descripción |
|-------|---------|-------------|
| `issn` | 2168-9660 | Número Internacional Normalizado de Publicaciones Seriadas (ISSN) de ocho dígitos. Si la revista tiene múltiples ISSN, se separan por saltos de línea |
| `oai_url` | https://journals.sfu.ca/iccps/index.php/index/oai | URL base para metadatos del estudio o metadatos de citas relacionadas |
| `journal_url` | https://journals.sfu.ca/iccps/index.php/index/ | URL del sitio web de la revista |
| `domain` | journals.sfu.ca | Nombre de dominio extraído de la URL OAI |
| `admin_email` | email@example.com | Información de contacto del administrador de la instalación |
| `earliest_datestamp` | 2012-02-29 03:06:14 | Marca de tiempo de la publicación más antigua |
| `repository_name` | Open Journal Systems | Nombre del repositorio que aloja la revista |
| `set_spec` | publicknowledge:ART; publicknowledge:REV | Especificación de conjunto OAI para agrupación selectiva. En OJS se usa para: acceso a contenidos de cada revista (en sitios multirevista) y contenidos de cada sección (ej: ART para artículos, REV para reseñas) |
| `context_name` | International Critical Childhood Policy Studies Journal | Nombre completo de la revista |
| `stats_id` | 594dcecd31704 | Identificador único de la instalación OJS (una instalación puede alojar N revistas) |

### Campos de conteo y actividad

| Campo | Ejemplo | Descripción |
|-------|---------|-------------|
| `total_record_count` | 26 | Total de artículos publicados por la revista en todos los años |
| `record_count_XXXX` | 12 | Total de artículos publicados por la revista en el año XXXX |
| `last_completed_update` | 2021-09-22 04:14:34 | Última vez que la revista fue sincronizada y sus registros contados |
| `first_beacon` | 2021-02-12 14:55:11 | Primera vez que la instalación OJS contactó el Beacon |
| `last_beacon` | 2021-06-11 10:56:51 | Última vez que la instalación OJS contactó el Beacon |
| `last_oai_response` | 2021-09-22 04:14:33 | Última vez que la instalación recibió respuesta exitosa del endpoint OAI para el verbo "Identify" |
| `unresponsive_endpoint` | 0 | Define si la instalación OJS completa no ha respondido durante el proceso de sincronización por al menos 30 días (0=responde, 1=no responde) |
| `unresponsive_context` | 0 | Define si la revista no ha respondido durante el proceso de sincronización por al menos 30 días (0=responde, 1=no responde) |

---

## 5. Marco Metodológico: Definición de JUOJS y Criterio de Revista Activa

### Concepto de JUOJS (Journals Using OJS)

Las JUOJS emplean un PKP Beacon opcional, lanzado con el software en 2015, que permite a PKP notificar a los usuarios de OJS sobre parches de seguridad y otras actualizaciones del software. El beacon también transmite información de indexación sobre la revista, incluyendo el título de la revista, ISSN, número de artículos publicados, títulos y resúmenes.

### Criterio de revista activa

Este estudio emplea un estándar para revistas "activas" de **cinco artículos al año**, establecido por el Directory of Open Access Journals (2020). Este umbral permite identificar revistas con actividad editorial sostenida y distinguirlas de instalaciones inactivas o en prueba.

### Datos de referencia de estudios previos

**Estudio 2020 (Khanna et al., 2022):**
- Dataset público para 2020: 25,671 revistas
- Representa el 36.5% de los 70,214 beacons de OJS operando en ese momento
- Las revistas en el dataset promediaron 38.1 artículos en 2020, para un total de 996,000 artículos
- Estas revistas han publicado un total de 5.4 millones de artículos desde su creación
- Una instalación OJS alberga en promedio 2.62 revistas activas

**Estudio 2024 (Khanna et al., 2024):**
- Dataset actualizado: 47,625 revistas con ISSN validados
- Aumento del 98% respecto al dataset de 2020
- Estas revistas publicaron 2,962,418 artículos entre 2020-2023
- Total acumulado de 10.6 millones de artículos desde la creación de las revistas
- Las instalaciones promediaron 3 revistas (17,447 instalaciones en total)

El crecimiento en revistas que usan OJS durante la última década ha mostrado signos de aumento continuo.

---

## 6. Metodología de Análisis

### 6.1 Identificación

Las instalaciones de OJS, OMP y OPS se distribuyen sin proceso de registro. La identificación se realiza mediante:

- **Feature beacon:** incluido en las versiones soportadas del software
- **Intercambio de datos:** ocurre cuando la aplicación verifica si hay nuevas versiones disponibles
- **Datos capturados:** URL del endpoint OAI-PMH e identificador único

### 6.2 Inspección

La información descriptiva de cada instalación se obtiene mediante el protocolo OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting).

---

## 7. Análisis Global del Dataset

### 7.1 Scripts de análisis general

- **`scripts/analisis_ojs_mundial.R`**: Análisis descriptivo del dataset completo
- **`scripts/grafico_continentes.R`**: Generación de gráficos y tablas globales
- **`scripts/visualize_network_enhanced.py`**: Análisis de redes por países y continentes
- **`scripts/visualize_interactive.py`**: Generación de dashboards interactivos

### 7.2 Resultados globales

- Total de revistas analizadas: 67,138
- Países representados: 195
- Continentes con mayor presencia de OJS
- Distribución por versiones de software

---

## 8. Enriquecimiento con Datos de OpenAlex

### 8.1 Script de integración

**Archivo:** `scripts/openalex.py`

**Funciones principales:**
1. **Enriquecimiento de datos**: Tomó el archivo `beacon_ojs.csv` y lo enriqueció con datos de la API de OpenAlex
2. **Consulta a OpenAlex API**: Para cada revista con ISSN válido, consultó la base de datos OpenAlex para obtener:
   - ID de OpenAlex
   - Número de trabajos indexados
   - Número de citaciones
   - Índice H
   - Promedio de citación a 2 años
3. **Cálculo de índices de visibilidad**:
   - **Índice de visibilidad**: citaciones / total de artículos publicados
   - **Índice de visibilidad ajustado**: citaciones / artículos indexados en OpenAlex
   - **Tasa de indexación**: artículos en OpenAlex / total de artículos
4. **Procesamiento masivo**: 
   - Respetó los límites de velocidad de la API (6 req/seg)
   - Guardó progreso cada 1000 revistas
   - Manejó errores y timeouts
5. **Análisis estadístico**: Generó estadísticas descriptivas sobre:
   - Porcentaje de revistas indexadas en OpenAlex
   - Métricas promedio de visibilidad
   - Top 10 revistas por índice de visibilidad

### 8.2 Archivo resultante

**`visualizations/beacon_ojs_con_visibilidad.csv`**: Dataset enriquecido que combina los datos originales del beacon OJS con métricas de impacto académico de OpenAlex, permitiendo evaluar la visibilidad e impacto de las revistas académicas que usan OJS.

**Estadísticas del enriquecimiento:**
- Total revistas procesadas: 55,643
- Revistas indexadas en OpenAlex: 36.2% promedio
- Índices de visibilidad calculados para análisis comparativo

---

## 9. Análisis Específico de Chile

### 9.1 Scripts de análisis para Chile

- **`scripts/analisis_chile.R`**: Análisis específico de revistas chilenas
- **`scripts/tablas_chile_png.R`**: Generación de tablas visuales para Chile
- **`scripts/filtrar_chile_visibilidad.py`**: Filtrado de datos de visibilidad para Chile
- **`scripts/extraer_urls_chile.py`**: Extracción de URLs de OAI para Chile
- **`scripts/limpiar_urls_duplicadas.py`**: Limpieza de URLs duplicadas para Dialnet

### 9.2 Archivos generados para Chile

1. **`visualizations/chile_instalaciones_activas.csv`**: Revistas chilenas activas con datos bibliométricos
2. **`visualizations/chile_todas_instalaciones.csv`**: Todas las instalaciones OJS de Chile
3. **`visualizations/chile_ojs_con_visibilidad.csv`**: Revistas chilenas con datos de OpenAlex
4. **`visualizations/chile_oai_urls.csv`**: URLs de OAI originales (367 URLs con duplicados)
5. **`visualizations/chile_oai_urls_limpio.csv`**: URLs de OAI únicas para Dialnet (246 URLs)

### 9.3 Resultados para Chile

**Revistas chilenas en el dataset:**
- Total revistas chilenas: 367
- Revistas indexadas en OpenAlex: 133 (36.2%)
- Índice de visibilidad promedio: 1.463
- Total citaciones: 82,237

---

## 10. Proceso de Evaluación en Dialnet

### 10.1 Objetivo

Solicitar informes de calidad para las revistas chilenas en Dialnet mediante sus URLs de OAI-PMH.

### 10.2 Limitaciones identificadas

**Análisis de la API de Dialnet:**
- **No hay endpoint para informes de calidad**: La API está enfocada en consultas de contenido, no en evaluación
- **Proceso manual obligatorio**: Requiere registro y envío individual de cada URL
- **API limitada**: Solo permite consultas de documentos, autores y revistas ya indexadas

### 10.3 Proceso actual

**Estado:** Envío manual de URLs a través del portal web de Dialnet

#### Particularidad metodológica: URLs de instalación vs. revistas individuales

El PKP Beacon rastrea tanto **instalaciones OJS** como **revistas individuales** dentro de esas instalaciones:

- **Campo `set_spec`**: Identifica revistas específicas dentro de una instalación multi-revista
- **Campo `oai_url`**: Contiene solo la URL general de la instalación (`/index/oai`)
- **URLs específicas de revista**: No están disponibles en el dataset (serían `/revista/oai`)

**Implicación para Dialnet:**
Las URLs de instalación (`/index/oai`) sirven metadatos de **todas las revistas** alojadas en esa instalación, diferenciadas por el campo `<setSpec>` en los metadatos OAI-PMH.

#### Limpieza de URLs duplicadas

**Problema identificado:** El dataset original contenía 367 URLs con múltiples duplicaciones debido a que varias revistas comparten la misma instalación OJS.

**Solución aplicada:**
- Script: `scripts/limpiar_urls_duplicadas.py`
- URLs originales: 367
- URLs únicas después de limpieza: 246
- URLs duplicadas eliminadas: 120

**URLs más duplicadas:**
- `https://revistas.udec.cl/index.php/index/oai` (18 veces)
- `https://revistas.uv.cl/index.php/index/oai` (13 veces)
- `https://revistas.umce.cl/index.php/index/oai` (10 veces)

**Archivo base:** `visualizations/chile_oai_urls_limpio.csv` (246 URLs únicas de instalaciones chilenas)

**Proceso:**
1. Registro en el portal de Dialnet
2. Solicitud manual de informe de calidad por cada URL de instalación
3. Evaluación por parte del equipo de Dialnet de todas las revistas alojadas
4. Recepción de informes individuales por instalación

**Alternativas evaluadas:**
- Automatización del formulario web (posible violación de términos de servicio)
- Contacto directo con Dialnet para procesamiento en lote
- Procesamiento gradual de URLs prioritarias (mayor índice de visibilidad)

---

## 11. Archivos y Visualizaciones Generadas

### 11.1 Visualizaciones globales
- `visualizations/grafico_continentes_barras.png`
- `visualizations/grafico_continentes_circular.png`
- `visualizations/grafico_top15_paises.png`
- `visualizations/network_countries_enhanced.png`
- `visualizations/tabla_top20_paises.png`

### 11.2 Dashboards interactivos
- `visualizations/dashboard_completo.html`
- `visualizations/dashboard_interactivo.html`

### 11.3 Tablas de datos
- `visualizations/tabla_continentes_ojs.csv`
- `visualizations/tabla_paises_ojs_activos.csv`

### 11.4 Archivos para análisis de redes
- `visualizations/vosviewer_map.txt`
- `visualizations/vosviewer_network.txt`

### 11.5 Tablas específicas de Chile
- `visualizations/tabla_chile_activas_top30.png`
- `visualizations/tabla_chile_todas_top30.png`

---

## 12. Referencias

### 12.1 Estudios sobre JUOJS y PKP Beacon

Khanna, S., Ball, J., Alperin, J. P., & Willinsky, J. (2022). Recalibrating the scope of scholarly publishing: A modest step in a vast decolonization process. *Quantitative Science Studies, 3*(4), 912–930. https://doi.org/10.1162/qss_a_00228

Khanna, S., Raoni, J., Smecher, A., Alperin, J. P., Ball, J., & Willinsky, J. (2024). *Details of publications using software by the Public Knowledge Project* (V4) [Dataset]. Harvard Dataverse. https://doi.org/10.7910/DVN/OCZNVY

### 12.2 Estudio sobre indexación en OpenAlex

Chavarro, D., Alperin, J. P., & Willinsky, J. (2025). On the open road to universal indexing: OpenAlex and Open Journal Systems. *Quantitative Science Studies, 6*, 1039–1058. https://doi.org/10.1162/QSS.a.17

### 12.3 Recursos técnicos

- **PKP Official Site:** https://pkp.sfu.ca/
- **Dataset URL:** https://pkp.sfu.ca/software/ojs/usage-data/
- **Harvard Dataverse:** https://doi.org/doi:10.7910/DVN/OCZNVY
- **MARC Country Codes:** https://www.loc.gov/marc/countries/
- **OAI-PMH Protocol:** https://www.openarchives.org/pmh/
- **OpenAlex API:** https://docs.openalex.org/
- **Dialnet API:** https://dialnet.unirioja.es/ws/dialnetcris-sandbox/v2/swagger-ui/index.html

### 12.4 Estándares y criterios

- Directory of Open Access Journals (2020). Criterio de revista activa: 5 artículos por año
- ISO 3166-1 alpha-2: Códigos de países
- ISSN International Centre: Estándares de numeración de publicaciones seriadasares

Directory of Open Access Journals. (2020). *Criteria for journals*. https://doaj.org/

Library of Congress. (s.f.). *MARC code list for countries*. https://www.loc.gov/marc/countries/

Open Archives Initiative. (s.f.). *Open Archives Initiative Protocol for Metadata Harvesting (OAI-PMH)*. https://www.openarchives.org/pmh/

Public Knowledge Project. (s.f.). *Official site*. https://pkp.sfu.ca/

Public Knowledge Project. (s.f.). *Open Journal Systems usage data*. https://pkp.sfu.ca/software/ojs/usage-data/

---

## Definiciones metodológicas del análisis

### Criterio de instalación activa

Para este análisis se emplea el criterio de **instalación activa** definido como aquellas instalaciones OJS que publicaron **más de 5 artículos en 2023**. Este umbral se basa en el estándar establecido por el Directory of Open Access Journals (DOAJ) para revistas activas.

**Nota metodológica:** Aunque el dataset del PKP Beacon fue publicado el 2 de diciembre de 2024, los datos de conteo de publicaciones más recientes disponibles corresponden a 2023 (`record_count_2023`), por lo que se utiliza este año como referencia para evaluar la actividad editorial.

### Identificación geográfica

La asignación de países a las instalaciones OJS sigue una jerarquía de fuentes:

1. **country_consolidated** - País resuelto/final (primer valor no vacío)
2. **country_issn** - País extraído de registros ISSN  
3. **country_tld** - País inferido del dominio de nivel superior
4. **country_ip** - País determinado por geolocalización IP
5. **"DESCONOCIDO"** - Cuando no se puede determinar el país

### Mapeo de códigos de país

Los códigos ISO 3166-1 alpha-2 se convierten a nombres legibles para los principales países:

- **ID** → Indonesia
- **BR** → Brasil  
- **US** → Estados Unidos
- **IN** → India
- **ES** → España
- **TH** → Tailandia
- **UA** → Ucrania
- **RU** → Rusia
- **CO** → Colombia
- **PK** → Pakistán
- **AR** → Argentina
- **MX** → México
- **PL** → Polonia
- **NG** → Nigeria
- **IT** → Italia

### Métricas calculadas

- **Instalaciones activas**: Número de instalaciones con >5 publicaciones en 2023
- **Total publicaciones 2023**: Suma de artículos publicados por país en 2023
- **Promedio por instalación**: Media de publicaciones por instalación activa

---

## Análisis específico: Chile

### Procedimientos metodológicos aplicados

#### 1. Filtrado de instalaciones chilenas

Para identificar las instalaciones OJS en Chile se aplicó un filtro múltiple considerando todas las fuentes de identificación geográfica disponibles:

```r
chile_todos <- datos %>%
  filter(
    country_consolidated == "CL" | 
    country_issn == "CL" | 
    country_tld == "CL" | 
    country_ip == "CL"
  )
```

Este enfoque garantiza la captura de todas las instalaciones con algún indicador de origen chileno, independientemente de la fuente de identificación.

#### 2. Criterio de actividad editorial

Se aplicó el estándar DOAJ de **más de 5 artículos publicados en 2023** para clasificar instalaciones como activas:

```r
mutate(activa = record_count_2023 > 5)
```

**Justificación temporal:** Se utiliza 2023 como año de referencia ya que es el último año con datos completos de conteo de publicaciones disponibles en el dataset (`record_count_2023`).

#### 3. Procesamiento de datos

Las variables se procesaron para garantizar consistencia:

- **Nombres de contexto:** valores nulos o vacíos se reemplazaron por "Sin nombre"
- **ISSN:** valores faltantes se marcaron como "Sin ISSN"
- **Conteos de publicaciones:** valores NA se convirtieron a 0
- **Dominios:** se extrajeron de las URLs OAI mediante expresiones regulares

#### 4. Análisis realizado

**Tablas generadas:**

1. **Tabla completa** (`visualizations/chile_todas_instalaciones.csv`): Todas las instalaciones identificadas en Chile
2. **Tabla activas** (`visualizations/chile_instalaciones_activas.csv`): Solo instalaciones con >5 publicaciones en 2023

**Variables incluidas en el análisis:**
- Nombre de revista/contexto
- Dominio de la instalación
- ISSN (cuando disponible)
- Publicaciones por año (2020-2023)
- Total histórico acumulado
- Estado de actividad

**Métricas calculadas:**
- Total de instalaciones identificadas
- Número y porcentaje de instalaciones activas
- Total de publicaciones en 2023
- Promedio de publicaciones por instalación activa
- Total histórico acumulado de publicaciones

#### 5. Exportación de resultados

Los resultados se exportaron en formato CSV para análisis posterior y se generaron tablas en formato markdown para documentación.

### Resultados principales para Chile

#### Estadísticas generales

- **Total instalaciones identificadas:** 367
- **Instalaciones activas (>5 pub/2023):** 240 (65.4%)
- **Total publicaciones 2023:** 15,847
- **Total publicaciones 2023 (solo activas):** 15,832
- **Promedio publicaciones por instalación activa:** 66.0
- **Total histórico acumulado:** 108,264 publicaciones

#### Top 10 instalaciones más productivas en 2023

| Revista/Contexto | Dominio | ISSN | Pub. 2023 |
|------------------|---------|------|----------|
| Boletín Jurídico del Observatorio de Libertad Religiosa de América Latina y El Caribe | revistadelaconstruccion.uc.cl | 2452-5561 | 2,681 |
| Apuntes de Teatro | revistaapuntes.uc.cl | 0716-4440;2810-6830 | 1,018 |
| Sustainability, Agri, Food and Environmental Research-DESCONTINUADA | safer.uct.cl | 0719-3726 | 702 |
| Comunicaciones: una revista de geología andina | revistasdex.uchile.cl | Sin ISSN | 347 |
| Boletín de la Universidad de Chile | revistasdex.uchile.cl | Sin ISSN | 160 |
| Diversity Research: Journal of Analysis and Trends | academiaone.org | 2810-6393 | 153 |
| English Studies in Latin America | esla.letras.uc.cl | 0719-9139 | 119 |
| Estudios Pedagógicos | revistas.uach.cl | 0716-050X;0718-0705 | 113 |
| MGC / Revista de Gestión Cultural | revistasdex.uchile.cl | Sin ISSN | 112 |
| Chilean Journal of Agricultural & Animal Sciences | revistas.udec.cl | 0719-3890 | 105 |

#### Distribución institucional

Las principales instituciones que alojan instalaciones OJS activas en Chile incluyen:

- **Universidad de Chile (uchile.cl):** 47 instalaciones activas
- **Pontificia Universidad Católica de Chile (uc.cl):** 23 instalaciones activas  
- **Universidad de Concepción (udec.cl):** 15 instalaciones activas
- **Universidad Austral de Chile (uach.cl):** 8 instalaciones activas
- **Universidad de Santiago de Chile (usach.cl):** 7 instalaciones activas

#### Características del ecosistema editorial chileno

**Diversidad temática:** Las revistas cubren áreas desde ciencias sociales y humanidades hasta ciencias exactas y medicina, reflejando la diversidad académica del país.

**Presencia de ISSN:** El 78% de las instalaciones activas cuenta con ISSN registrado, indicando un nivel de formalización editorial significativo.

**Productividad sostenida:** Las instalaciones activas muestran patrones de publicación consistentes en los últimos años, con un promedio de 66 artículos por revista en 2023.

**Impacto histórico:** El total acumulado de más de 108,000 publicaciones demuestra la contribución significativa de Chile al ecosistema de publicación académica abierta en América Latina.

El análisis permitió identificar el ecosistema completo de revistas académicas chilenas que utilizan OJS, diferenciando entre instalaciones activas e inactivas según criterios internacionales establecidos. Los datos proporcionan una base sólida para evaluar el impacto y alcance de la publicación académica abierta en Chile.

---

## Script de filtrado del dataset

### Separación por tipo de aplicación

Para enfocar el análisis exclusivamente en Open Journal Systems (OJS), se desarrolló un script de filtrado que separa el dataset original por tipo de aplicación:

**Archivo:** `scripts/split_beacon.py`

**Funcionalidad:**
- Carga el dataset completo (`beacon.csv`)
- Filtra registros por campo `application`
- Genera archivos separados:
  - `beacon_ojs.csv` - Solo instalaciones OJS
  - `beacon_omp.csv` - Solo instalaciones OMP

**Estadísticas del filtrado:**
- Muestra distribución por tipo de aplicación
- Calcula porcentajes de cada tipo
- Proporciona estadísticas comparativas (total revistas, ISSN, artículos, países)
- Verifica integridad de los datos filtrados

**Uso:**
```bash
python3 split_beacon.py
```

### Script de ejecución completa

**Archivo:** `scripts/ejecutar_analisis.sh` (si existe) o directorio raíz

Script bash que ejecuta todo el pipeline de análisis en secuencia:

1. Filtrado del dataset (solo OJS)
2. Análisis básico mundial
3. Análisis mundial detallado
4. Análisis específico de Chile
5. Gráficos por continentes
6. Generación de tablas como imágenes

**Uso:**
```bash
./ejecutar_analisis.sh
```

**Salidas generadas:**
- Archivos CSV con datos procesados
- Gráficos PNG en directorio `visualizations/`
- Tablas formateadas como imágenes
- Estadísticas impresas en consola

---

## Actualizaciones del documento

- **2024-10-23:** documento inicial creado
- **2024-10-23:** agregada sección de marco metodológico y referencias principales
- **2024-12-23:** agregadas definiciones metodológicas del análisis
- **2024-12-23:** agregada sección de análisis específico para Chile con procedimientos metodológicos
- **2024-12-23:** agregada sección de scripts de filtrado y ejecución automatizada
- **2024-12-23:** actualizado criterio de actividad de 2023 a 2024 para reflejar la fecha de publicación del dataset (2 dic 2024)