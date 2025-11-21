# Análisis JUOJS (Journals Using OJS) para Chile - Beacon v6
# Filtrado específico de instalaciones activas (>5 pub/2024)
# Criterio actualizado para datos 2024-2025

library(dplyr)
library(readr)
library(knitr)

cat("=== ANÁLISIS JUOJS CHILE BEACON V6 ===\n")
cat("Filtrado de instalaciones activas (>5 publicaciones en 2024)\n\n")

# Cargar dataset completo de Chile v6
chile_completo <- read_csv("../visualizations_v6/chile_todas_instalaciones_v6.csv")

cat("Dataset completo v6 cargado:", nrow(chile_completo), "instalaciones\n")

# Aplicar criterio JUOJS v6: >5 publicaciones en 2024
chile_juojs_v6 <- chile_completo %>%
  filter(record_count_2024 > 5) %>%
  arrange(desc(record_count_2024))

cat("Después de filtro JUOJS v6:", nrow(chile_juojs_v6), "instalaciones activas\n")
cat("Instalaciones filtradas:", nrow(chile_completo) - nrow(chile_juojs_v6), "\n\n")

# Estadísticas JUOJS v6
cat("=== ESTADÍSTICAS JUOJS CHILE V6 ===\n")
cat("Total instalaciones activas 2024:", nrow(chile_juojs_v6), "\n")
cat("Porcentaje de actividad:", round(nrow(chile_juojs_v6)/nrow(chile_completo)*100, 1), "%\n")
cat("Total publicaciones 2024:", sum(chile_juojs_v6$record_count_2024, na.rm = TRUE), "\n")
cat("Total publicaciones 2023:", sum(chile_juojs_v6$record_count_2023, na.rm = TRUE), "\n")
cat("Crecimiento total 2023->2024:", sum(chile_juojs_v6$crecimiento_2023_2024, na.rm = TRUE), "\n")
cat("Promedio pub/instalación 2024:", round(mean(chile_juojs_v6$record_count_2024, na.rm = TRUE), 1), "\n")
cat("Total histórico acumulado:", sum(chile_juojs_v6$total_historico, na.rm = TRUE), "\n\n")

# Top 10 más productivas 2024
cat("=== TOP 10 INSTALACIONES MÁS PRODUCTIVAS 2024 ===\n")
top10_v6 <- chile_juojs_v6 %>%
  head(10) %>%
  select(context_name, dominio, issn, record_count_2024, crecimiento_2023_2024)

print(kable(top10_v6, 
      col.names = c("Revista/Contexto", "Dominio", "ISSN", "Pub. 2024", "Crecimiento"),
      format = "markdown"))

# Análisis de crecimiento
cat("\n\n=== ANÁLISIS DE CRECIMIENTO 2023-2024 ===\n")
crecimiento_stats <- chile_juojs_v6 %>%
  summarise(
    instalaciones_crecieron = sum(crecimiento_2023_2024 > 0, na.rm = TRUE),
    instalaciones_decrecieron = sum(crecimiento_2023_2024 < 0, na.rm = TRUE),
    instalaciones_estables = sum(crecimiento_2023_2024 == 0, na.rm = TRUE),
    crecimiento_promedio = round(mean(crecimiento_2023_2024, na.rm = TRUE), 1)
  )

cat("Instalaciones que crecieron:", crecimiento_stats$instalaciones_crecieron, "\n")
cat("Instalaciones que decrecieron:", crecimiento_stats$instalaciones_decrecieron, "\n")
cat("Instalaciones estables:", crecimiento_stats$instalaciones_estables, "\n")
cat("Crecimiento promedio:", crecimiento_stats$crecimiento_promedio, "pub/instalación\n")

# Análisis por región PKP
cat("\n\n=== DISTRIBUCIÓN JUOJS POR REGIÓN PKP ===\n")
regiones_juojs <- chile_juojs_v6 %>%
  count(region_pkp, sort = TRUE)
print(kable(regiones_juojs, col.names = c("Región PKP", "Instalaciones JUOJS"), format = "markdown"))

# Análisis institucional
cat("\n\n=== DISTRIBUCIÓN INSTITUCIONAL ===\n")
instituciones <- chile_juojs_v6 %>%
  mutate(
    institucion = case_when(
      grepl("uchile\\.cl", dominio) ~ "Universidad de Chile",
      grepl("uc\\.cl", dominio) ~ "Pontificia Universidad Católica",
      grepl("udec\\.cl", dominio) ~ "Universidad de Concepción",
      grepl("uach\\.cl", dominio) ~ "Universidad Austral de Chile",
      grepl("usach\\.cl", dominio) ~ "Universidad de Santiago",
      grepl("uv\\.cl", dominio) ~ "Universidad de Valparaíso",
      grepl("ufro\\.cl", dominio) ~ "Universidad de La Frontera",
      TRUE ~ "Otras instituciones"
    )
  ) %>%
  count(institucion, sort = TRUE)

print(kable(instituciones, 
      col.names = c("Institución", "Instalaciones"),
      format = "markdown"))

# Exportar dataset JUOJS v6
write.csv(chile_juojs_v6, "../visualizations_v6/chile_juojs_activas_v6.csv", row.names = FALSE)

cat("\n\nDataset JUOJS v6 exportado: visualizations_v6/chile_juojs_activas_v6.csv\n")
cat("Este es el DATASET PRINCIPAL V6 para todos los análisis posteriores\n")