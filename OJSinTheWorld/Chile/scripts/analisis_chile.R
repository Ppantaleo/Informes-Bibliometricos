# Análisis detallado de instalaciones OJS en Chile
# Usa beacon_ojs.csv (solo aplicaciones OJS)
library(dplyr)
library(readr)
library(knitr)

# Cargar datos
datos <- read_csv("beacon_ojs.csv")

# Filtrar datos de Chile
chile_todos <- datos %>%
  filter(
    country_consolidated == "CL" | 
    country_issn == "CL" | 
    country_tld == "CL" | 
    country_ip == "CL"
  ) %>%
  mutate(
    activa = record_count_2023 > 5,
    dominio = gsub("https?://([^/]+).*", "\\1", oai_url),
    total_historico = total_record_count
  ) %>%
  arrange(desc(record_count_2023))

# 1. TABLA COMPLETA - TODAS LAS INSTALACIONES
cat("=== TODAS LAS INSTALACIONES OJS EN CHILE ===\n")
cat("Total instalaciones:", nrow(chile_todos), "\n\n")

tabla_completa <- chile_todos %>%
  select(
    context_name, 
    dominio,
    issn,
    record_count_2023,
    record_count_2022,
    record_count_2021,
    record_count_2020,
    total_historico,
    activa
  ) %>%
  mutate(
    context_name = ifelse(is.na(context_name) | context_name == "", "Sin nombre", context_name),
    issn = ifelse(is.na(issn) | issn == "", "Sin ISSN", issn),
    record_count_2023 = ifelse(is.na(record_count_2023), 0, record_count_2023),
    record_count_2022 = ifelse(is.na(record_count_2022), 0, record_count_2022),
    record_count_2021 = ifelse(is.na(record_count_2021), 0, record_count_2021),
    record_count_2020 = ifelse(is.na(record_count_2020), 0, record_count_2020),
    total_historico = ifelse(is.na(total_historico), 0, total_historico)
  )

print(kable(tabla_completa, 
      col.names = c("Revista/Contexto", "Dominio", "ISSN", "2023", "2022", "2021", "2020", "Total", "Activa"),
      format = "markdown"))

# 2. TABLA SOLO ACTIVAS (>5 pub en 2023)
chile_activas <- chile_todos %>%
  filter(activa == TRUE) %>%
  select(
    context_name, 
    dominio,
    issn,
    record_count_2023,
    record_count_2022,
    record_count_2021,
    record_count_2020,
    total_historico
  ) %>%
  mutate(
    context_name = ifelse(is.na(context_name) | context_name == "", "Sin nombre", context_name),
    issn = ifelse(is.na(issn) | issn == "", "Sin ISSN", issn),
    record_count_2023 = ifelse(is.na(record_count_2023), 0, record_count_2023),
    record_count_2022 = ifelse(is.na(record_count_2022), 0, record_count_2022),
    record_count_2021 = ifelse(is.na(record_count_2021), 0, record_count_2021),
    record_count_2020 = ifelse(is.na(record_count_2020), 0, record_count_2020),
    total_historico = ifelse(is.na(total_historico), 0, total_historico)
  )

cat("\n\n=== INSTALACIONES OJS ACTIVAS EN CHILE (>5 pub/año en 2023) ===\n")
cat("Instalaciones activas:", nrow(chile_activas), "\n\n")

print(kable(chile_activas, 
      col.names = c("Revista/Contexto", "Dominio", "ISSN", "2023", "2022", "2021", "2020", "Total"),
      format = "markdown"))

# 3. ESTADÍSTICAS RESUMEN
cat("\n\n=== ESTADÍSTICAS CHILE ===\n")
cat("Total instalaciones OJS:", nrow(chile_todos), "\n")
cat("Instalaciones activas (>5 pub/2023):", nrow(chile_activas), "\n")
cat("Porcentaje activas:", round(nrow(chile_activas)/nrow(chile_todos)*100, 1), "%\n")
cat("Total publicaciones 2023:", sum(chile_todos$record_count_2023, na.rm = TRUE), "\n")
cat("Total publicaciones 2023 (solo activas):", sum(chile_activas$record_count_2023, na.rm = TRUE), "\n")
cat("Promedio pub/instalación (activas):", round(mean(chile_activas$record_count_2023, na.rm = TRUE), 1), "\n")
cat("Total histórico acumulado:", sum(chile_todos$total_historico, na.rm = TRUE), "\n")

# 4. EXPORTAR TABLAS
write.csv(tabla_completa, "visualizations/chile_todas_instalaciones.csv", row.names = FALSE)
write.csv(chile_activas, "visualizations/chile_instalaciones_activas.csv", row.names = FALSE)

cat("\nTablas exportadas:\n")
cat("- visualizations/chile_todas_instalaciones.csv\n")
cat("- visualizations/chile_instalaciones_activas.csv\n")