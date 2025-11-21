# Informe OJS in the World - Beacon v6 (2024-2025)

## 1. Resumen Ejecutivo

Este informe presenta el análisis actualizado del ecosistema global de Open Journal Systems (OJS) basado en el **Beacon v6** de PKP, que incluye datos hasta 2024-2025. El análisis se centra en Chile como caso de estudio, utilizando metodología JUOJS (Journals Using OJS) con criterio actualizado de >5 publicaciones en 2024.

### Principales Hallazgos
- **Dataset global:** 86,282 instalaciones OJS activas
- **Chile:** 319 instalaciones activas JUOJS (>5 pub/2024)
- **URLs únicas:** 225 URLs OAI generadas para evaluación
- **Productividad 2024:** 14,162 publicaciones totales en Chile
- **Crecimiento:** +2,006 publicaciones vs 2023 (+16.5%)
- **Cobertura institucional:** Universidad de Chile lidera con 67 instalaciones

---

## 2. Metodología

### 2.1 Fuente de Datos

**Beacon v6 PKP (2024-2025)**
- **Archivo fuente:** `beacon_v6_ojs.csv` (86,282 registros OJS)
- **Período:** Datos hasta 2024-2025
- **Nuevas columnas:**
  - `admin_email` - Email de administrador
  - `country_doaj` - País según DOAJ
  - `best_doaj_url` - URL DOAJ verificada
  - `record_count_2024` - Publicaciones 2024
  - `record_count_2025` - Publicaciones 2025
  - `region` - Región geográfica

### 2.2 Criterio JUOJS Actualizado

**Definición JUOJS v6:**
- Instalaciones OJS con **>5 publicaciones en 2024** (criterio actualizado)
- Filtrado por país usando múltiples campos: `country_consolidated`, `country_issn`, `country_doaj`
- Eliminación de instalaciones de prueba y duplicados

### 2.3 Flujo Metodológico v6

#### 2.3.1 Preparación de Datos
```bash
# 3. Filtrar beacon por país (Chile)
Rscript scripts_v6/3_analisis_chile_v6.R
# Genera: visualizations_v6/chile_todas_instalaciones_v6.csv

# 4. Aplicar criterio JUOJS (>5 pub/2024)
Rscript scripts_v6/4_chile_juojs_filtrado_v6.R
# Genera: visualizations_v6/chile_juojs_activas_v6.csv (DATASET PRINCIPAL)
```

#### 2.3.2 Evaluación Dialnet
```bash
# 5. Generar URLs OAI desde dataset JUOJS v6
python3 scripts_v6/5_generar_urls_dialnet_v6.py
# Genera: visualizations_v6/chile_oai_urls_v6.csv
```

### 2.4 Archivos Principales v6

**Datasets Base:**
- `beacon_v6_ojs.csv` - Dataset OJS global v6
- `beacon_v6.tab` - Fuente original confiable

**Datasets Chile v6:**
- `visualizations_v6/chile_todas_instalaciones_v6.csv` - Todas las instalaciones
- **`visualizations_v6/chile_juojs_activas_v6.csv`** - **DATASET PRINCIPAL v6**

**Evaluación Dialnet v6:**
- `visualizations_v6/chile_oai_urls_v6.csv` - URLs para evaluación
- `dialnet_v6/*.html` - Informes de calidad v6

---

## 3. Resultados Chile v6

### 3.1 Estadísticas Generales
- **Total instalaciones identificadas:** 432
- **Instalaciones JUOJS activas (>5 pub/2024):** 319 (73.8%)
- **Instalaciones filtradas:** 113 (≤5 pub/2024)
- **URLs únicas generadas:** 225 (eliminados 94 duplicados)

### 3.2 Productividad 2024
- **Total publicaciones 2024:** 14,162
- **Total publicaciones 2023:** 12,156
- **Crecimiento neto:** +2,006 publicaciones (+16.5%)
- **Promedio por instalación:** 44.4 pub/instalación
- **Total histórico acumulado:** 144,529 publicaciones

### 3.3 Top 10 Instalaciones Más Productivas 2024

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

### 3.4 Análisis de Crecimiento 2023-2024
- **Instalaciones que crecieron:** 163 (51.1%)
- **Instalaciones que decrecieron:** 135 (42.3%)
- **Instalaciones estables:** 21 (6.6%)
- **Crecimiento promedio:** +6.3 pub/instalación

### 3.5 Distribución Institucional

| Institución | Instalaciones | % |
|-------------|---------------|---|
| Universidad de Chile | 67 | 21.0% |
| Pontificia Universidad Católica | 27 | 8.5% |
| Universidad de Valparaíso | 15 | 4.7% |
| Universidad de Concepción | 12 | 3.8% |
| Universidad Austral de Chile | 7 | 2.2% |
| Universidad de Santiago | 6 | 1.9% |
| Universidad de La Frontera | 4 | 1.3% |
| Otras instituciones | 181 | 56.7% |

### 3.6 Distribución Geográfica PKP
- **Latin America & Caribbean:** 317 instalaciones (99.4%)
- **Europe & Central Asia:** 1 instalación (0.3%)
- **North America:** 1 instalación (0.3%)

### 3.7 URLs OAI Generadas para Dialnet
- **Total URLs únicas:** 225
- **URLs Universidad de Chile:** 58 (25.8%)
- **Publicaciones 2024 representadas:** 11,540 (81.5% del total)
- **Crecimiento neto representado:** +1,843 publicaciones

#### Ejemplos URLs Top 5:
1. `https://revistachilenadederecho.uc.cl/index.php/index/oai` (1,708 pub/2024)
2. `https://revistasdex.uchile.cl/index.php/index/oai` (1,689 pub/2024)
3. `https://revistadelaconstruccion.uc.cl/index.php/index/oai` (958 pub/2024)
4. `https://cuhso.uct.cl/index.php/index/oai` (510 pub/2024)
5. `https://revistalimite.uta.cl/index.php/index/oai` (321 pub/2024)

---

## 4. Scripts Actualizados v6

Los siguientes scripts han sido adaptados para el nuevo beacon v6:

3. **`scripts_v6/3_analisis_chile_v6.R`** - Filtrado por país con nuevos campos
4. **`scripts_v6/4_chile_juojs_filtrado_v6.R`** - Criterio JUOJS 2024
5. **`scripts_v6/5_generar_urls_dialnet_v6.py`** - Generación URLs v6

### 4.1 Cambios Principales
- **Criterio temporal:** >5 pub/2024 (vs >5 pub/2023)
- **Filtrado mejorado:** Incluye `country_doaj` para mejor precisión
- **Nuevas métricas:** Análisis de tendencias 2023-2024-2025
- **Regiones:** Análisis geográfico por regiones PKP

---

## 5. Archivos Generados v6

### 5.1 Datasets Principales
- **`visualizations_v6/chile_todas_instalaciones_v6.csv`** - 432 instalaciones completas
- **`visualizations_v6/chile_juojs_activas_v6.csv`** - 319 instalaciones activas (DATASET PRINCIPAL)
- **`visualizations_v6/chile_oai_urls_v6.csv`** - 225 URLs para evaluación Dialnet

### 5.2 Próximos Pasos

1. **✅ Scripts v6 ejecutados** - Datasets actualizados generados
2. **Evaluación Dialnet** con 225 URLs OAI
3. **Análisis comparativo** v5 vs v6
4. **Enriquecimiento OpenAlex** con datos 2024
5. **Visualizaciones interactivas** con nuevas métricas
6. **Análisis de tendencias** proyección 2025

## 6. Conclusiones Preliminares

### 6.1 Crecimiento Sostenido
- Chile mantiene un **ecosistema OJS robusto** con 319 instalaciones activas
- **Crecimiento del 16.5%** en publicaciones 2024 vs 2023
- **Universidad de Chile domina** el panorama con 21% de las instalaciones

### 6.2 Concentración Institucional
- **Top 6 universidades** concentran 40.3% de las instalaciones
- **Diversidad institucional** con 56.7% en "otras instituciones"
- **Región PKP** predominantemente Latin America & Caribbean (99.4%)

### 6.3 Productividad Destacada
- **Revista Chilena de Derecho** lidera con crecimiento excepcional (+1,671 pub)
- **Boletín Universidad de Chile** mantiene alta productividad (1,689 pub)
- **51.1% de instalaciones** muestran crecimiento positivo

### 6.4 Calidad del Dataset v6
- **73.8% de instalaciones** cumplen criterio JUOJS (>5 pub/2024)
- **225 URLs únicas** listas para evaluación de calidad
- **Eliminación efectiva** de 94 duplicados por dominio

---

*Informe generado con Beacon v6 PKP - Datos 2024-2025*