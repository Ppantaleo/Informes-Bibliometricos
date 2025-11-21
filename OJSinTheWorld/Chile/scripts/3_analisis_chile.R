# Análisis detallado de instalaciones OJS en Chile
# Usa beacon_ojs.csv (solo aplicaciones OJS)
library(dplyr)
library(readr)
library(knitr)

# Cargar datos
datos <- read_csv("../../beacon_ojs.csv")

# Filtrar datos de Chile
chile_todos <- datos %>%
  filter(
    toupper(country_consolidated) == "CL" | 
    grepl("CL", toupper(country_issn)) | 
    toupper(country_tld) == "CL" | 
    toupper(country_ip) == "CL"
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

# Contar instalaciones activas para estadísticas
chile_activas_count <- chile_todos %>%
  filter(activa == TRUE) %>%
  nrow()

cat("\n\n=== INSTALACIONES OJS ACTIVAS EN CHILE (>5 pub/año en 2023) ===\n")
cat("Instalaciones activas:", chile_activas_count, "\n")

# 3. ESTADÍSTICAS RESUMEN
cat("\n\n=== ESTADÍSTICAS CHILE ===\n")
cat("Total instalaciones OJS:", nrow(chile_todos), "\n")
cat("Instalaciones activas (>5 pub/2023):", chile_activas_count, "\n")
cat("Porcentaje activas:", round(chile_activas_count/nrow(chile_todos)*100, 1), "%\n")
cat("Total publicaciones 2023:", sum(chile_todos$record_count_2023, na.rm = TRUE), "\n")
cat("Total histórico acumulado:", sum(chile_todos$total_historico, na.rm = TRUE), "\n")

# 4. EXPORTAR TABLA
write.csv(tabla_completa, "../visualizations/chile_todas_instalaciones.csv", row.names = FALSE)

cat("\nTabla exportada:\n")
cat("- visualizations/chile_todas_instalaciones.csv\n")
cat("\nNOTA: Para dataset de instalaciones activas, usar script 4_chile_juojs_filtrado.R\n")