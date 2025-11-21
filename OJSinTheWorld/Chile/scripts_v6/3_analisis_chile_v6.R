# Análisis detallado de instalaciones OJS en Chile - Beacon v6
# Usa beacon_v6_ojs.csv (solo aplicaciones OJS con datos 2024-2025)
library(dplyr)
library(readr)
library(knitr)

cat("=== ANÁLISIS CHILE BEACON V6 ===\n")
cat("Procesando datos 2024-2025...\n\n")

# Cargar datos beacon v6
datos <- read_csv("../../beacon_v6_ojs.csv")

cat("Dataset beacon v6 cargado:", nrow(datos), "instalaciones OJS\n")

# Filtrar datos de Chile con criterios mejorados v6
chile_todos <- datos %>%
  filter(
    toupper(country_consolidated) == "CL" | 
    grepl("CL", toupper(country_issn)) | 
    grepl("CL", toupper(country_doaj)) |
    toupper(country_tld) == "CL" | 
    toupper(country_ip) == "CL"
  ) %>%
  mutate(
    # Convertir a numérico y manejar NAs
    record_count_2023 = as.numeric(record_count_2023),
    record_count_2024 = as.numeric(record_count_2024),
    record_count_2025 = as.numeric(record_count_2025),
    # Criterio JUOJS actualizado: >5 pub/2024
    activa_2024 = !is.na(record_count_2024) & record_count_2024 > 5,
    activa_2023 = !is.na(record_count_2023) & record_count_2023 > 5,
    dominio = gsub("https?://([^/]+).*", "\\1", oai_url),
    total_historico = total_record_count,
    # Nuevas métricas v6
    crecimiento_2023_2024 = ifelse(is.na(record_count_2024) | is.na(record_count_2023), 0, 
                                   record_count_2024 - record_count_2023),
    region_pkp = ifelse(is.na(region), "Sin región", region)
  ) %>%
  arrange(desc(record_count_2024))

cat("Instalaciones Chile identificadas:", nrow(chile_todos), "\n")

# Crear tabla completa con nuevas columnas v6
tabla_completa <- chile_todos %>%
  select(
    context_name, 
    dominio,
    issn,
    record_count_2023,
    record_count_2024,
    record_count_2025,
    crecimiento_2023_2024,
    total_historico,
    activa_2024,
    region_pkp
  ) %>%
  mutate(
    context_name = ifelse(is.na(context_name) | context_name == "", "Sin nombre", context_name),
    issn = ifelse(is.na(issn) | issn == "", "Sin ISSN", issn),
    record_count_2023 = ifelse(is.na(record_count_2023), 0, record_count_2023),
    record_count_2024 = ifelse(is.na(record_count_2024), 0, record_count_2024),
    record_count_2025 = ifelse(is.na(record_count_2025), 0, record_count_2025),
    crecimiento_2023_2024 = ifelse(is.na(crecimiento_2023_2024), 0, crecimiento_2023_2024),
    total_historico = ifelse(is.na(total_historico), 0, total_historico)
  )

print(kable(tabla_completa, 
      col.names = c("Revista/Contexto", "Dominio", "ISSN", "2023", "2024", "2025", "Crecimiento", "Total", "Activa 2024", "Región"),
      format = "markdown"))

# Estadísticas v6
chile_activas_2024 <- chile_todos %>% filter(activa_2024 == TRUE) %>% nrow()
chile_activas_2023 <- chile_todos %>% filter(activa_2023 == TRUE) %>% nrow()

cat("\n\n=== ESTADÍSTICAS CHILE BEACON V6 ===\n")
cat("Total instalaciones OJS:", nrow(chile_todos), "\n")
cat("Instalaciones activas 2024 (>5 pub):", chile_activas_2024, "\n")
cat("Instalaciones activas 2023 (>5 pub):", chile_activas_2023, "\n")
cat("Cambio 2023->2024:", chile_activas_2024 - chile_activas_2023, "\n")
cat("Porcentaje activas 2024:", round(chile_activas_2024/nrow(chile_todos)*100, 1), "%\n")
cat("Total publicaciones 2024:", sum(chile_todos$record_count_2024, na.rm = TRUE), "\n")
cat("Total publicaciones 2023:", sum(chile_todos$record_count_2023, na.rm = TRUE), "\n")
cat("Total histórico acumulado:", sum(chile_todos$total_historico, na.rm = TRUE), "\n")

# Análisis por región v6
cat("\n=== DISTRIBUCIÓN POR REGIÓN PKP ===\n")
regiones <- chile_todos %>%
  count(region_pkp, sort = TRUE)
print(kable(regiones, col.names = c("Región PKP", "Instalaciones"), format = "markdown"))

# Exportar tabla v6
write.csv(tabla_completa, "../visualizations_v6/chile_todas_instalaciones_v6.csv", row.names = FALSE)

cat("\n\nTabla exportada: visualizations_v6/chile_todas_instalaciones_v6.csv\n")
cat("NOTA: Para dataset JUOJS v6, usar script 2_chile_juojs_filtrado_v6.R\n")