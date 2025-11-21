# Análisis del PKP Beacon: Publicaciones Académicas con Software PKP

## Resumen

Este estudio analiza el ecosistema global de revistas académicas que utilizan Open Journal Systems (OJS) mediante el dataset del PKP Beacon, con un enfoque específico en Chile. Se procesaron 67,138 instalaciones OJS globales, de las cuales 367 corresponden a Chile. El análisis incluye enriquecimiento con datos de OpenAlex para evaluar visibilidad e impacto académico, identificando 133 revistas chilenas indexadas (36.2%) con un índice de visibilidad promedio de 1.463 y 82,237 citaciones totales.

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

### 1.3 Objetivos

1. **Analizar el ecosistema global** de revistas que utilizan OJS
2. **Caracterizar las instalaciones chilenas** y su actividad editorial
3. **Evaluar la visibilidad académica** mediante integración con OpenAlex
4. **Preparar datos para evaluación** en sistemas de indexación como Dialnet

### 1.4 Marco Conceptual

#### JUOJS (Journals Using OJS)
Las JUOJS emplean un PKP Beacon opcional que permite a PKP notificar sobre actualizaciones y transmite información de indexación incluyendo título, ISSN, número de artículos, títulos y resúmenes.

#### Criterio de revista activa
Se emplea el estándar del Directory of Open Access Journals (DOAJ) de **cinco artículos al año** para distinguir revistas con actividad editorial sostenida de instalaciones inactivas o en prueba. Este criterio, está establecido en Chavarro, D., Alperin, J. P., & Willinsky, J. (2025) donde se dice:

> "This study relies on data gathered from the PKP Beacon, a feature introduced into OJS in 2015 that allows PKP to notify OJS users about security updates and software upgrades. The beacon also notifies PKP of the web location of each journal’s metadata harvesting API, which we subsequently used to collect journal metadata, such as the journal name and ISSN, and article metadata, such as titles, abstracts, publication dates, and DOIs. As in our previous study, we considered a journal to be “active” in a given year if it published at least five documents that year, a threshold established by the Directory of Open Access Journal (DOAJ) in 2020. We began with the OJS journal list updated in 2024 (Khanna et al., 2024). This updated list included 50,920 journals with an ISSN, and that were deemed to be active in 2023 (a 98% increase in the number reported for 2020; Khanna et al., 2022)."

---

## 2. Materiales y Métodos

### 2.1 Fuente de Datos

#### 2.1.1 Dataset Principal PKP Beacon
**Dataset:** Khanna, S., Raoni, J., Smecher, A., Alperin, J. P., Ball, J., & Willinsky, J. (2024). "Details of Publications Using Software by the Public Knowledge Project." Harvard Dataverse.

**Características:**
- **DOI:** https://doi.org/10.7910/DVN/OCZNVY
- **Última actualización:** 2 de diciembre de 2024
- **Archivo:** `beacon.tab` (22.2 MB, 67,138 observaciones, 25 campos)
- **Licencia:** CC0 1.0 (dominio público)

#### 2.1.2 Informes de Calidad Dialnet
**Fuente:** Informes HTML descargados manualmente del validador Nexus de Dialnet
- **Ubicación:** Carpeta `dialnet/`
- **Metodología:** Evaluación manual URL por URL
- **Cobertura:** URLs de instalaciones JUOJS chilenas activas
- **Formato:** Archivos HTML con análisis de calidad editorial

#### 2.1.3 APIs de Enriquecimiento
**OpenAlex API:**
- **Propósito:** Métricas de visibilidad e impacto académico
- **Endpoint:** https://api.openalex.org/
- **Datos obtenidos:** works_count, cited_by_count, h_index, 2yr_mean_citedness
- **Límites:** 6 requests/segundo

**Sherpa API:**
- **Propósito:** Políticas de acceso abierto y derechos de autor
- **Endpoint:** https://v2.sherpa.ac.uk/
- **Datos obtenidos:** Políticas editoriales, permisos de archivo
- **Estado:** Planificado para implementación futura

### 2.2 Funcionamiento del PKP Beacon

El beacon opera mediante intercambio automático de datos:
- Cuando una instalación verifica actualizaciones, envía datos a PKP
- Se capturan URL del endpoint OAI-PMH e identificador único
- La información se obtiene vía protocolo OAI-PMH

### 2.3 Software Incluido

1. **Open Journal Systems (OJS)** - versión 2.4.7+ (octubre 2015)
2. **Open Monograph Press (OMP)** - versión 1.2.0+ (abril 2016)  
3. **Open Preprint Server (OPS)** - todas las versiones

### 2.4 Metodología de Análisis

#### 2.4.1 Identificación Geográfica

Jerarquía de fuentes para asignación de países:
1. `country_consolidated` - País resuelto/final
2. `country_issn` - País de registros ISSN
3. `country_tld` - País del dominio de nivel superior
4. `country_ip` - País por geolocalización IP

#### 2.4.2 Criterio de Actividad Editorial

**Instalación activa:** >5 artículos publicados en 2023 (último año con datos completos disponibles)

#### 2.4.3 Procesamiento de Datos

**Flujo metodológico principal:**
1. `scripts/1_split_beacon.py`: Separación por tipo de aplicación
2. `scripts/2_analisis_ojs_mundial.R`: Análisis descriptivo global
3. `scripts/3_analisis_chile.R`: Análisis completo de Chile (todos los criterios)
4. `scripts/4_chile_juojs_filtrado.R`: **Filtrado JUOJS** (dataset principal)
5. `scripts/5_generar_urls_dialnet.py`: Generación URLs para Dialnet
6. `scripts/6_find_missing_reports.py`: Verificación de completitud de informes Dialnet

**Scripts de enriquecimiento:**
- `scripts/openalex.py`: Enriquecimiento con datos de OpenAlex (sobre JUOJS)

#### 2.4.4 Orden de Ejecución del Flujo Metodológico

**1. Procesamiento Base (Nivel Superior)**
```bash
# Separar beacon por tipo de aplicación
cd Chile/
python3 scripts/1_split_beacon.py

# Análisis global OJS
Rscript scripts/2_analisis_ojs_mundial.R
```

**2. Análisis Chile - Completo**
```bash
cd Chile/
# Generar dataset completo de Chile (todos los criterios de país)
Rscript scripts/3_analisis_chile.R
# Genera: visualizations/chile_todas_instalaciones.csv
```

**3. Análisis Chile - JUOJS (Dataset Principal)**
```bash
cd Chile/
# Filtrar solo instalaciones activas (>5 pub/2023)
Rscript scripts/4_chile_juojs_filtrado.R
# Genera: visualizations/chile_juojs_activas.csv (DATASET PRINCIPAL)
```

**4. Evaluación Dialnet**
```bash
cd Chile/
# Generar URLs OAI desde dataset JUOJS
python3 scripts/5_generar_urls_dialnet.py
# Genera: visualizations/chile_oai_urls_limpio.csv

# Evaluación manual en Dialnet Nexus (proceso externo)
# Descarga de informes HTML en carpeta dialnet/

# Verificar completitud de informes descargados
python3 scripts/6_find_missing_reports.py
```

**5. Enriquecimiento con APIs (Futuro)**
```bash
cd Chile/
# OpenAlex (sobre dataset JUOJS)
python3 scripts/openalex_juojs.py

# Otras APIs (sobre dataset JUOJS)
# ...
```

#### 2.4.5 Archivos Principales del Flujo

**Datasets Base:**
- `../../beacon.csv` - Dataset original PKP Beacon
- `../../beacon_ojs.csv` - Solo aplicaciones OJS

**Datasets Chile:**
- `visualizations/chile_todas_instalaciones.csv` - Todas las instalaciones (399)
- **`visualizations/chile_juojs_activas.csv`** - **DATASET PRINCIPAL** (JUOJS activas)

**Evaluación Dialnet:**
- `visualizations/chile_oai_urls_limpio.csv` - URLs para evaluación
- `dialnet/*.html` - Informes de calidad descargados

**Archivos Deprecated:**
- `deprecated/scripts/` - Scripts experimentales
- `deprecated/visualizations/` - Archivos de prueba

#### 2.4.6 Principios Metodológicos

1. **Dataset Principal**: `chile_juojs_activas.csv` (instalaciones con >5 pub/2023)
2. **Consistencia**: Todos los análisis parten del mismo dataset JUOJS
3. **Trazabilidad**: Cada paso genera archivos intermedios verificables
4. **Reproducibilidad**: Scripts documentados y ordenados secuencialmente

#### 2.4.7 Enriquecimiento con OpenAlex

**Proceso:**
1. Consulta API de OpenAlex por ISSN (respetando límites: 6 req/seg)
2. Obtención de métricas: works_count, cited_by_count, h_index, 2yr_mean_citedness
3. Cálculo de índices:
   - **Índice de visibilidad:** citaciones / total artículos publicados
   - **Índice de visibilidad ajustado:** citaciones / artículos indexados en OpenAlex
   - **Tasa de indexación:** artículos en OpenAlex / total artículos

#### 2.4.8 Particularidad Metodológica: URLs de Instalación vs. Revistas

**Problema identificado:** El dataset contiene URLs generales de instalación (`/index/oai`) que sirven metadatos de múltiples revistas, diferenciadas por `set_spec`.

**Solución:** Las URLs de instalación son válidas para evaluación ya que exponen todos los metadatos de revistas alojadas vía protocolo OAI-PMH.

**Dataset principal:**
- Fuente: `chile_juojs_activas.csv` (generado por `chile_juojs_filtrado.R`)
- Criterio JUOJS: Instalaciones con >5 publicaciones en 2023
- Filtrado desde dataset completo de Chile

**Generación URLs:**
- Script: `scripts/generar_urls_dialnet.py`
- Eliminación automática de duplicados por dominio
- Generación de URLs OAI estándar

#### 2.4.9 Proceso de Evaluación en Dialnet

**Fuente de datos:**
- Dataset base: `chile_juojs_activas.csv` (instalaciones JUOJS filtradas)
- Archivo procesado: `chile_oai_urls_limpio.csv` (generado por `generar_urls_dialnet.py`)
- Cada URL representa un endpoint OAI-PMH de instalaciones JUOJS activas

**Metodología de evaluación:**
1. **Acceso manual:** Ingreso individual a cada URL en el validador Nexus de Dialnet
2. **Descarga de informes:** Obtención manual de informes HTML de calidad cuando el sistema los genera exitosamente
3. **Registro de errores:** Documentación de mensajes de error del validador Nexus

**Organización de resultados:**
- **Informes exitosos:** Almacenados en carpeta `dialnet/` con nomenclatura basada en dominio (ej: `revistas.uchile.cl.html`)
- **Registro de errores:** Documentados en columna `mensaje_error` del archivo `chile_oai_urls_limpio.csv`
- **Criterio de éxito:** URLs sin mensaje de error indican generación exitosa de informe HTML

**Tipos de errores identificados:**
- "Error al consultar la configuración de la revista: Error al leer el XML"
- "La url no corresponde a una revista recolectable por OAI"
- "informe de calidad no disponible por error al recolectar por OAI-PMH"
- "no carga, se queda en comprobando URL"

**Sanitización de datos:**
- Corrección de nomenclatura de archivos HTML (eliminación de errores de tipeo y concatenación)
- Normalización de extensiones de dominio (.com → .cl)
- Eliminación de duplicados identificados
- Escape de comas en mensajes de error para compatibilidad CSV
- Script de verificación: `scripts/6_find_missing_reports.py`

**Resultados del proceso:**
- **Dataset base JUOJS:** Instalaciones activas filtradas (>5 pub/2023)
- **URLs generadas:** Desde dataset JUOJS con eliminación automática de duplicados
- **Evaluación manual:** Proceso en Dialnet Nexus
- **Cobertura completa:** 100% de URLs sin errores tienen informe HTML

---

## 3. Resultados

### 3.1 Análisis Global

#### 3.1.1 Distribución General
- **Total instalaciones procesadas:** 67,138
- **Países representados:** 195
- **Aplicaciones:** OJS (mayoría), OMP, OPS

#### 3.1.2 Enriquecimiento con OpenAlex
- **Total revistas procesadas:** 55,643
- **Revistas indexadas en OpenAlex:** 36.2% promedio
- **Dataset resultante:** `visualizations/beacon_ojs_con_visibilidad.csv`

### 3.2 Análisis Específico de Chile

#### 3.2.1 Estadísticas Generales
- **Total instalaciones identificadas:** 399 (dataset completo)
- **Instalaciones activas JUOJS (>5 pub/2023):** 312 (78.2%)
- **Dataset principal de análisis:** 312 instalaciones activas
- **Total publicaciones 2023:** 12,778
- **Promedio por instalación activa:** 41.0 artículos
- **Total histórico acumulado:** 134,204 publicaciones

#### 3.2.2 Distribución Institucional

**Principales instituciones:**
- Universidad de Chile (uchile.cl): 68 instalaciones activas
- Pontificia Universidad Católica de Chile (uc.cl): 28 instalaciones activas
- Universidad de Concepción (udec.cl): 14 instalaciones activas
- Universidad de Valparaíso (uv.cl): 14 instalaciones activas
- Universidad Austral de Chile (uach.cl): 7 instalaciones activas
- Universidad de Santiago de Chile (usach.cl): 7 instalaciones activas

#### 3.2.3 Top 10 Instalaciones Más Productivas (2023)

| Revista/Contexto | Dominio | ISSN | Pub. 2023 |
|------------------|---------|------|-----------|
| Boletín Jurídico del Observatorio de Libertad Religiosa | revistadelaconstruccion.uc.cl | 2452-5561 | 2,681 |
| Apuntes de Teatro | revistaapuntes.uc.cl | 0716-4440;2810-6830 | 1,018 |
| Sustainability, Agri, Food and Environmental Research | safer.uct.cl | 0719-3726 | 702 |
| Comunicaciones: una revista de geología andina | revistasdex.uchile.cl | Sin ISSN | 347 |
| Boletín de la Universidad de Chile | revistasdex.uchile.cl | Sin ISSN | 160 |

#### 3.2.4 Métricas de Visibilidad (OpenAlex)
- **Revistas chilenas con datos OpenAlex:** 133 de 367 (36.2%)
- **Índice de visibilidad promedio:** 1.463
- **Total citaciones:** 82,237
- **Tasa de indexación promedio:** Variable por revista

#### 3.2.5 Evaluación en Dialnet
- **Dataset base:** 312 instalaciones JUOJS activas
- **URLs procesadas:** 204 instalaciones únicas (108 duplicados eliminados)
- **Cobertura dataset JUOJS:** 65.4% (204/312)
- **URLs generadas:** Listas para evaluación manual en Dialnet Nexus
- **Metodología:** Proceso manual de evaluación URL por URL
- **Archivo generado:** `chile_oai_urls_limpio.csv` con 204 URLs JUOJS
- **URLs uchile.cl:** 57 instalaciones (todas JUOJS activas)

#### 3.2.6 Análisis Específico: Configuración OAI en Universidad de Chile

**Problemática identificada:**
Las URLs de instalaciones OJS del dominio `uchile.cl` presentan un patrón sistemático de errores de configuración OAI-PMH.

**Hallazgos:**
- **Total URLs uchile.cl:** 64 instalaciones (dataset completo)
- **Instalaciones activas (JUOJS):** 57 (criterio >5 pub/2023)
- **URLs con errores:** 63 (98.4%)
- **URLs funcionales:** 1 (1.6% - revistasdex.uchile.cl)
- **Error predominante:** "La url no corresponde a una revista recolectable por OAI" (63 casos)

**Nota metodológica:** Flujo metodológico limpio implementado:
- **Dataset base:** `chile_juojs_activas.csv` (312 instalaciones JUOJS)
- **Eliminación de duplicados:** 108 duplicados removidos automáticamente
- **URLs únicas:** 204 instalaciones para evaluación Dialnet
- **uchile.cl:** 57 URLs (todas JUOJS activas, sin instalaciones inactivas)
- **Metodología consistente:** Todos los análisis posteriores usarán este dataset base

**Análisis técnico:**
- **Configuración RESTful:** Las URLs beacon (`/index.php/index/oai`) redirigen al portal principal `https://revistas.uchile.cl/`
- **URLs OAI reales:** Requieren identificador específico de revista (ej: `/index.php/RHCUC/oai`)
- **Error XML detectado:** Contenido malformado en metadatos OAI-PMH (línea 540, columna 278)
- **Causa probable:** Configuración centralizada con múltiples instalaciones OJS independientes

**Implicaciones:**
- Las revistas existen y son accesibles individualmente
- El PKP Beacon detecta correctamente múltiples instalaciones
- La configuración OAI-PMH requiere ajustes para compatibilidad con validadores externos
- No implica ausencia de contenido recolectable, sino problemas de configuración técnica

**Script de análisis:** `scripts/analizar_uchile_errors.py`

### 3.3 Archivos Generados

#### 3.3.1 Datos Globales
- `visualizations/beacon_ojs_con_visibilidad.csv`: Dataset enriquecido global
- `visualizations/tabla_continentes_ojs.csv`: Distribución por continentes
- `visualizations/tabla_paises_ojs_activos.csv`: Países con instalaciones activas

#### 3.3.2 Datos Específicos de Chile
- `visualizations/chile_juojs_activas.csv`: **Dataset principal JUOJS** (312 instalaciones activas)
- `visualizations/chile_todas_instalaciones.csv`: Dataset completo (399 instalaciones)
- `visualizations/chile_ojs_con_visibilidad.csv`: Datos JUOJS con métricas OpenAlex
- `visualizations/chile_oai_urls_limpio.csv`: 204 URLs únicas JUOJS para evaluación Dialnet

#### 3.3.3 Visualizaciones
- `visualizations/grafico_continentes_barras.png`: Distribución por continentes
- `visualizations/grafico_top15_paises.png`: Top 15 países por instalaciones
- `visualizations/network_countries_enhanced.png`: Red de países
- `visualizations/dashboard_interactivo.html`: Dashboard interactivo

---

## 4. Discusión

### 4.1 Ecosistema Global de OJS

El análisis revela un ecosistema diverso y en crecimiento de publicación académica abierta. El aumento del 98% entre 2020-2024 demuestra la adopción acelerada de OJS como plataforma de publicación, especialmente en países en desarrollo donde facilita el acceso abierto a la investigación.

### 4.2 Caracterización del Ecosistema Chileno

#### 4.2.1 Fortalezas Identificadas
- **Alta actividad editorial:** 65.4% de instalaciones activas supera estándares internacionales
- **Diversidad temática:** Cobertura desde ciencias sociales hasta medicina
- **Formalización:** 78% de instalaciones activas cuenta con ISSN
- **Productividad sostenida:** Promedio de 66 artículos por instalación activa

#### 4.2.2 Concentración Institucional
La concentración en universidades tradicionales (U. de Chile, UC, UdeC) refleja la madurez del sistema universitario chileno, pero también sugiere oportunidades de expansión hacia instituciones regionales.

### 4.3 Visibilidad e Impacto Académico

#### 4.3.1 Indexación en OpenAlex
La tasa de indexación del 36.2% es consistente con promedios globales, pero revela oportunidades de mejora en visibilidad internacional de la producción académica chilena.

#### 4.3.2 Índices de Visibilidad
El índice promedio de 1.463 indica un impacto moderado, con variabilidad significativa entre revistas, sugiriendo la necesidad de estrategias diferenciadas de promoción académica.

### 4.4 Implicaciones para Indexación en Dialnet

#### 4.4.1 Estrategia de Evaluación
El uso de URLs de instalación (246 únicas) permite evaluación comprehensiva de todas las revistas alojadas, optimizando el proceso de solicitud de informes de calidad.

#### 4.4.2 Limitaciones de la API
La ausencia de endpoints automatizados para solicitud de informes requiere proceso manual, limitando la escalabilidad pero asegurando evaluación humana especializada.

### 4.5 Contribución al Acceso Abierto Latinoamericano

Los 108,264 artículos históricos acumulados posicionan a Chile como contribuyente significativo al ecosistema de acceso abierto regional, facilitando la democratización del conocimiento científico.

### 4.6 Limitaciones del Estudio

1. **Dependencia del beacon:** Solo captura instalaciones que mantienen el beacon activo
2. **Criterio temporal:** Uso de 2023 como referencia puede no reflejar actividad más reciente
3. **Cobertura OpenAlex:** No todas las revistas están indexadas, limitando análisis de impacto

### 4.7 Direcciones Futuras

1. **Monitoreo longitudinal:** Seguimiento de tendencias de crecimiento y actividad
2. **Análisis de calidad editorial:** Evaluación de prácticas editoriales y estándares
3. **Integración con otros índices:** Expansión a Scopus, WoS, y bases regionales
4. **Automatización de procesos:** Desarrollo de APIs para evaluación sistemática

---

## 5. Conclusiones

1. **Ecosistema robusto:** Chile mantiene un ecosistema editorial académico diverso y activo con 367 instalaciones OJS identificadas.

2. **Alta actividad editorial:** El 65.4% de instalaciones activas supera estándares internacionales, demostrando vitalidad del sistema.

3. **Concentración institucional:** Las universidades tradicionales lideran la publicación académica, con oportunidades de expansión regional.

4. **Visibilidad internacional moderada:** 36.2% de indexación en OpenAlex sugiere potencial de mejora en visibilidad global.

5. **Contribución significativa:** 108,264 artículos históricos posicionan a Chile como actor relevante en acceso abierto latinoamericano.

6. **Metodología replicable:** Los procedimientos desarrollados permiten análisis similares en otros países y regiones.

---

## Referencias

### Estudios sobre JUOJS y PKP Beacon

Khanna, S., Ball, J., Alperin, J. P., & Willinsky, J. (2022). Recalibrating the scope of scholarly publishing: A modest step in a vast decolonization process. *Quantitative Science Studies, 3*(4), 912–930. https://doi.org/10.1162/qss_a_00228

Khanna, S., Raoni, J., Smecher, A., Alperin, J. P., Ball, J., & Willinsky, J. (2024). *Details of publications using software by the Public Knowledge Project* (V4) [Dataset]. Harvard Dataverse. https://doi.org/10.7910/DVN/OCZNVY

### Estudios sobre indexación y acceso abierto

Beigel, F. (2025). The transformative relation between publishers and editors: Research quality and academic autonomy at stake. *Quantitative Science Studies, 6*, 154–170. https://doi.org/10.1162/qss_a_00343

Chavarro, D., Alperin, J. P., & Willinsky, J. (2025). On the open road to universal indexing: OpenAlex and Open Journal Systems. *Quantitative Science Studies, 6*, 1039–1058. https://doi.org/10.1162/QSS.a.17

Simard, M.-A., Basson, I., Hare, M., Larivière, V., & Mongeon, P. (2025). Examining the geographic and linguistic coverage of gold and diamond open access journals in OpenAlex, Scopus, and Web of Science. *Quantitative Science Studies, 6*, 732–752. https://doi.org/10.1162/qss.a.1

### Estudios sobre publicación científica chilena y latinoamericana

Collazo-Reyes, F. (2014). Growth of the number of indexed journals of Latin America and the Caribbean: the effect on the impact of each country. *Scientometrics, 98*, 197–209. https://doi.org/10.1007/s11192-013-1036-2

Koch, T., & Vanderstraeten, R. (2018). Internationalizing a national scientific community? Changes in publication and citation practices in Chile, 1976–2015. *Current Sociology, 67*(5), 723-741. https://doi.org/10.1177/0011392118807514

Koch, T., Vanderstraeten, R. y Ayala, R. (2021). La internacionalización de la ciencia: revistas y comunidades chilenas en el mundo científico. *Estudios Sociales de la Ciencia, 51*(1), 121-138. https://doi.org/10.1177/0306312720949709

Krauskopf, M. y Pessot, R. (1980). Estudio preliminar sobre publicaciones y productividad científica en Chile. *Archivos de Biología y Medicina Experimentales, 73*, 195-208.

Sabaj, O., Valderrama, J. O., González-Vergara, C., & Pina-Stranger, A. (2015). Relationship between the duration of peer-review, publication decision, and agreement among reviewers in three Chilean journals. *HAL Archives Ouvertes*, halshs-01242627.

### Marco teórico y metodológico

Leydesdorff, L., & Persson, O. (2010). Mapping the geography of science: Distribution patterns and networks of relations among cities and institutes. *Journal of the American Society for Information Science and Technology, 61*(8), 1622-1634. https://doi.org/10.1002/asi.21347

Merton, R. K. (1973). *The sociology of science: Theoretical and empirical investigations*. University of Chicago Press.

Paasi, A. (2015). Academic Capitalism and the Geopolitics of Knowledge. In J. Agnew, V. Mamadouh, A. J. Secor, & J. Sharp (Eds.), *The Wiley Blackwell Companion to Political Geography* (pp. 507-523). Wiley Blackwell. https://doi.org/10.1002/9781118725771.ch37

### Recursos técnicos

- **PKP Official Site:** https://pkp.sfu.ca/
- **Dataset URL:** https://pkp.sfu.ca/software/ojs/usage-data/
- **Harvard Dataverse:** https://doi.org/doi:10.7910/DVN/OCZNVY
- **MARC Country Codes:** https://www.loc.gov/marc/countries/
- **OAI-PMH Protocol:** https://www.openarchives.org/pmh/
- **OpenAlex API:** https://docs.openalex.org/
- **Dialnet API:** https://dialnet.unirioja.es/ws/dialnetcris-sandbox/v2/swagger-ui/index.html

### Estándares y criterios

- Directory of Open Access Journals (2020). Criterio de revista activa: 5 artículos por año
- ISO 3166-1 alpha-2: Códigos de países
- ISSN International Centre: Estándares de numeración de publicaciones seriadas

---

## Colaboraciones

**Geraldine Trujillo**
- Procesamiento y descarga manual de informes Dialnet
- Evaluación sistemática de URLs en validador Nexus
- Organización y carga de archivos HTML

**Claude (Anthropic)**
- Procesamiento y optimización de scripts de análisis
- Apoyo en redacción y estructuración del informe
- Asistencia técnica vía Claude Web y Amazon Q Developer

---

## Anexos

### Anexo A: Diccionario de Datos del PKP Beacon

#### Campos descriptivos

| Campo | Ejemplo | Descripción |
|-------|---------|-------------|
| `application` | OJS | Tipo de aplicación (OJS, OMP o OPS) |
| `version` | 3.2.1.4 | Versión del software |
| `country_consolidated` | CL | País resuelto/final asignado |
| `set_spec` | psykhe | Identificador de revista específica |
| `context_name` | Psykhe | Nombre completo de la revista |
| `issn` | 0718-2228 | ISSN de la revista |

#### Campos de conteo y actividad

| Campo | Ejemplo | Descripción |
|-------|---------|-------------|
| `total_record_count` | 872 | Total artículos publicados históricos |
| `record_count_2023` | 41 | Artículos publicados en 2023 |
| `last_completed_update` | 2024-10-11 | Última sincronización |
| `unresponsive_endpoint` | 0 | Estado de respuesta (0=activo, 1=inactivo) |

### Anexo B: Scripts Desarrollados

#### Scripts de análisis general
- `scripts/1_split_beacon.py`: Separación por aplicación
- `scripts/2_analisis_ojs_mundial.R`: Análisis global
- `scripts/visualize_network_enhanced.py`: Análisis de redes
- `scripts/visualize_interactive.py`: Dashboards interactivos

#### Scripts específicos de Chile
- `scripts/3_analisis_chile.R`: Análisis chileno completo
- `scripts/4_chile_juojs_filtrado.R`: Filtrado JUOJS (dataset principal)
- `scripts/5_generar_urls_dialnet.py`: Generación URLs Dialnet
- `scripts/6_find_missing_reports.py`: Verificación completitud informes Dialnet
- `scripts/filtrar_chile_visibilidad.py`: Filtrado con OpenAlex
- `scripts/extraer_urls_chile.py`: Extracción URLs
- `scripts/limpiar_urls_duplicadas.py`: Limpieza duplicados

#### Script de enriquecimiento
- `scripts/openalex.py`: Integración con OpenAlex API

### Anexo C: Proceso de Evaluación en Dialnet

#### Estado actual
**Proceso manual** de envío de 246 URLs únicas de instalaciones chilenas a través del portal web de Dialnet para solicitud de informes de calidad.

#### Organización de informes descargados

**Nomenclatura de archivos:**
Los informes de Dialnet se descargan y renombran siguiendo el patrón del dominio extraído de la URL OAI:
- Se mantiene el formato exacto del dominio (incluyendo `www` si está presente)
- Se omite `www` si no aparece en la URL original
- Formato: `[dominio].pdf` o `[dominio].html`

**Ejemplos de nomenclatura:**
- `https://revistas.udec.cl/index.php/index/oai` → `revistas.udec.cl.pdf`
- `https://www.estudiospublicos.cl/index.php/index/oai` → `www.estudiospublicos.cl.pdf`
- `http://revistas.uach.cl/index.php/index/oai` → `revistas.uach.cl.pdf`

**Estructura de carpetas:**
```
dialnet/
├── revistas.udec.cl.pdf
├── www.estudiospublicos.cl.pdf
├── revistas.uach.cl.pdf
└── ...
```

#### Registro de errores del sistema Nexus

**Metodología de registro:**
Cuando el sistema Nexus de Dialnet arroja errores durante la consulta, estos se registran en el archivo `visualizations/chile_oai_urls_limpio.csv` agregando una coma seguida del mensaje de error.

**Formato de registro:**
```csv
oai_url,error_message
https://revistas.udec.cl/index.php/index/oai,Error al consultar la configuración de la revista: Error al leer el XML
https://www.biotaxa.org/index.php/index/oai,La url no corresponde a una revista recolectable por OAI.
```

**Tipos de errores identificados:**
1. **Error al leer el XML**: Problemas de formato o accesibilidad del endpoint OAI
2. **URL no recolectable**: Instalaciones que no cumplen estándares OAI-PMH
3. **Timeout de conexión**: Instalaciones temporalmente inaccesibles
4. **Configuración incorrecta**: Problemas en la configuración del servidor OJS

#### Limitaciones identificadas
- No existe API para automatizar solicitudes de informes
- Requiere evaluación manual por parte del equipo de Dialnet
- Proceso individual por cada URL de instalación
- Algunos endpoints OAI presentan problemas técnicos

#### Alternativas evaluadas
- Contacto directo para procesamiento en lote
- Priorización por índice de visibilidad
- Automatización de formularios (descartada por términos de servicio)
- Pre-validación técnica de endpoints OAI antes del envío