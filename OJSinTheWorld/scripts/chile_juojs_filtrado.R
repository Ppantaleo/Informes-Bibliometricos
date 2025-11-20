# Análisis JUOJS (Journals Using OJS) para Chile
# Filtrado específico de instalaciones activas (>5 pub/2023)
# Parte del flujo metodológico principal

library(dplyr)
library(readr)
library(knitr)

cat("=== ANÁLISIS JUOJS CHILE ===\n")
cat("Filtrado de instalaciones activas (>5 publicaciones en 2023)\n\n")

# Cargar dataset completo de Chile
chile_completo <- read_csv("visualizations/chile_todas_instalaciones.csv")

cat("Dataset completo cargado:", nrow(chile_completo), "instalaciones\n")

# Aplicar criterio JUOJS: >5 publicaciones en 2023
chile_juojs <- chile_completo %>%
  filter(record_count_2023 > 5) %>%
  arrange(desc(record_count_2023))

cat("Después de filtro JUOJS:", nrow(chile_juojs), "instalaciones activas\n")
cat("Instalaciones filtradas:", nrow(chile_completo) - nrow(chile_juojs), "\n\n")

# Estadísticas JUOJS
cat("=== ESTADÍSTICAS JUOJS CHILE ===\n")
cat("Total instalaciones activas:", nrow(chile_juojs), "\n")
cat("Porcentaje de actividad:", round(nrow(chile_juojs)/nrow(chile_completo)*100, 1), "%\n")
cat("Total publicaciones 2023:", sum(chile_juojs$record_count_2023, na.rm = TRUE), "\n")
cat("Promedio pub/instalación:", round(mean(chile_juojs$record_count_2023, na.rm = TRUE), 1), "\n")
cat("Total histórico acumulado:", sum(chile_juojs$total_historico, na.rm = TRUE), "\n\n")

# Top 10 más productivas
cat("=== TOP 10 INSTALACIONES MÁS PRODUCTIVAS 2023 ===\n")
top10 <- chile_juojs %>%
  head(10) %>%
  select(context_name, dominio, issn, record_count_2023)

print(kable(top10, 
      col.names = c("Revista/Contexto", "Dominio", "ISSN", "Pub. 2023"),
      format = "markdown"))

# Análisis por institución (dominio)
cat("\n\n=== DISTRIBUCIÓN INSTITUCIONAL ===\n")
instituciones <- chile_juojs %>%
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

# Exportar dataset JUOJS
write.csv(chile_juojs, "visualizations/chile_juojs_activas.csv", row.names = FALSE)

cat("\n\nDataset JUOJS exportado: visualizations/chile_juojs_activas.csv\n")
cat("Este es el DATASET PRINCIPAL para todos los análisis posteriores\n")