# Análisis mundial OJS - Beacon v6
# Criterio actualizado: >5 publicaciones en 2024
# Usa beacon_v6_ojs.csv con datos 2024-2025

library(dplyr)
library(ggplot2)
library(readr)
library(knitr)

cat("=== ANÁLISIS MUNDIAL OJS BEACON V6 ===\n")
cat("Procesando datos globales 2024-2025...\n\n")

# Cargar datos v6
datos <- read_csv("../../beacon_v6_ojs.csv")

cat("Dataset beacon v6 OJS cargado:", nrow(datos), "instalaciones\n")

# Preparación de datos v6
datos_activos <- datos %>%
  mutate(
    # Criterio actualizado: >5 pub en 2024
    activa_2024 = !is.na(record_count_2024) & record_count_2024 > 5,
    activa_2023 = !is.na(record_count_2023) & record_count_2023 > 5,
    pais = case_when(
      !is.na(country_consolidated) ~ toupper(country_consolidated),
      !is.na(country_doaj) ~ toupper(country_doaj),
      !is.na(country_issn) ~ toupper(country_issn),
      !is.na(country_tld) ~ toupper(country_tld),
      TRUE ~ "DESCONOCIDO"
    )
  ) %>%
  filter(activa_2024 == TRUE)

cat("Instalaciones activas 2024 (>5 pub):", nrow(datos_activos), "\n\n")

# Tabla resumen por países v6
tabla_paises <- datos_activos %>%
  group_by(pais) %>%
  summarise(
    instalaciones_activas = n(),
    total_pub_2024 = sum(record_count_2024, na.rm = TRUE),
    total_pub_2023 = sum(record_count_2023, na.rm = TRUE),
    crecimiento = total_pub_2024 - total_pub_2023,
    promedio_2024 = round(mean(record_count_2024, na.rm = TRUE), 1),
    .groups = 'drop'
  ) %>%
  arrange(desc(instalaciones_activas))

cat("=== TOP 20 PAÍSES POR INSTALACIONES ACTIVAS 2024 ===\n")
print(kable(tabla_paises %>% head(20), 
      col.names = c("País", "Activas", "Pub 2024", "Pub 2023", "Crecimiento", "Promedio"),
      format = "markdown"))

# Análisis por regiones v6
if("region" %in% colnames(datos_activos)) {
  regiones_stats <- datos_activos %>%
    filter(!is.na(region)) %>%
    group_by(region) %>%
    summarise(
      instalaciones = n(),
      pub_2024 = sum(record_count_2024, na.rm = TRUE),
      paises = n_distinct(pais),
      .groups = 'drop'
    ) %>%
    arrange(desc(instalaciones))
  
  cat("\n\n=== DISTRIBUCIÓN POR REGIONES PKP ===\n")
  print(kable(regiones_stats, 
        col.names = c("Región PKP", "Instalaciones", "Pub 2024", "Países"),
        format = "markdown"))
}

# Gráfico top 15 países - barras
top15_paises <- tabla_paises %>% head(15)

p1 <- ggplot(top15_paises, aes(x = reorder(pais, instalaciones_activas), 
                               y = instalaciones_activas)) +
  geom_col(fill = "steelblue", alpha = 0.8) +
  coord_flip() +
  labs(
    title = "Top 15 Países - Instalaciones OJS Activas 2024",
    subtitle = "Criterio: >5 publicaciones en 2024 (Beacon v6)",
    x = "País",
    y = "Instalaciones Activas",
    caption = "Fuente: PKP Beacon v6"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
    plot.subtitle = element_text(hjust = 0.5, size = 10)
  )

ggsave("../visualizations_v6/top15_paises_barras_v6.png", p1, 
       width = 12, height = 8, dpi = 300)

# Gráfico regiones - circular (si existe)
if("region" %in% colnames(datos_activos) && nrow(regiones_stats) > 0) {
  p2 <- ggplot(regiones_stats, aes(x = "", y = instalaciones, fill = region)) +
    geom_bar(stat = "identity", width = 1) +
    coord_polar("y", start = 0) +
    labs(
      title = "Distribución Global por Regiones PKP",
      subtitle = "Instalaciones OJS Activas 2024 (Beacon v6)",
      fill = "Región PKP",
      caption = "Fuente: PKP Beacon v6"
    ) +
    theme_void() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
      plot.subtitle = element_text(hjust = 0.5, size = 10),
      legend.position = "right"
    )
  
  ggsave("../visualizations_v6/regiones_circular_v6.png", p2, 
         width = 10, height = 8, dpi = 300)
}

# Estadísticas generales v6
cat("\n\n=== ESTADÍSTICAS GLOBALES V6 ===\n")
cat("Total instalaciones en dataset:", nrow(datos), "\n")
cat("Instalaciones activas 2024 (>5 pub):", nrow(datos_activos), "\n")
cat("Porcentaje activas 2024:", round(nrow(datos_activos)/nrow(datos)*100, 1), "%\n")
cat("Países con instalaciones activas:", nrow(tabla_paises), "\n")
cat("Total publicaciones 2024:", sum(tabla_paises$total_pub_2024), "\n")
cat("Total publicaciones 2023:", sum(tabla_paises$total_pub_2023), "\n")
cat("Crecimiento global 2023->2024:", sum(tabla_paises$crecimiento), "\n")

# Comparación 2023 vs 2024
activas_2023 <- sum(!is.na(datos$record_count_2023) & datos$record_count_2023 > 5)
activas_2024 <- nrow(datos_activos)
cambio_actividad <- activas_2024 - activas_2023

cat("Instalaciones activas 2023:", activas_2023, "\n")
cat("Cambio en actividad 2023->2024:", cambio_actividad, "\n")

# Exportar datos
write.csv(tabla_paises, "../visualizations_v6/tabla_paises_mundial_v6.csv", row.names = FALSE)
if(exists("regiones_stats")) {
  write.csv(regiones_stats, "../visualizations_v6/regiones_mundial_v6.csv", row.names = FALSE)
}

cat("\n=== ARCHIVOS GENERADOS ===\n")
cat("- visualizations_v6/top15_paises_barras_v6.png\n")
if(exists("regiones_stats")) {
  cat("- visualizations_v6/regiones_circular_v6.png\n")
}
cat("- visualizations_v6/tabla_paises_mundial_v6.csv\n")
if(exists("regiones_stats")) {
  cat("- visualizations_v6/regiones_mundial_v6.csv\n")
}