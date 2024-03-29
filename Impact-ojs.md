## Data Processing OJS in Latinamerica

### 1. Initial Data Upload

```r
library(readr)
datos <- read_csv("ruta/del/archivo/bacon.csv")
```
### 2. Filtered by Latin American Countries

```r
library(dplyr)
datos_latinoamerica <- datos %>%
  filter(country_consolidated %in% c("AR", "BO", "BR", "CL", "CO", "CR", "CU", "DO", "EC", "SV", "GT", "HN", "MX", "NI", "PA", "PY", "PE", "PR", "UY", "VE"))
```

### 3. Filtering by "OJS" Application

```r
datos_latinoamerica_OJS <- datos_latinoamerica %>%
  filter(application == "ojs")
```

### 4. Ordered Table Creation

```r
tabla_ordenada <- datos_latinoamerica_OJS %>%
  arrange(country_consolidated) %>%
  select(country_consolidated, oai_url, repository_name, context_name, issn)
```

### 5. Export to CSV

```r
write.csv(tabla_ordenada, "ruta/del/archivo/tabla_ordenada.csv", row.names = FALSE)
```

## Data Processing OJS in Latinamerica without ISSN

```r
# Filtrar las filas que tienen issn igual a cadena vacía o NA
filas_sin_issn <- filter(tabla_ordenada, issn == "" | is.na(issn) | issn == "NA")

# Obtener el número de filas sin ISSN
num_filas_sin_issn <- nrow(filas_sin_issn)

# Mostrar el resultado
cat("Número de filas sin ISSN:", num_filas_sin_issn, "\n")
```

