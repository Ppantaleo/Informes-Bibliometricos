# Análisis de distribución mundial de instalaciones OJS activas
# Criterio: Activas = más de 5 publicaciones en 2023
# Usa beacon_ojs.csv (solo aplicaciones OJS)

library(dplyr)
library(ggplot2)
library(readr)
library(knitr)
library(kableExtra)

# Cargar datos
datos <- read_csv("beacon_ojs.csv")

# 1. PREPARACIÓN DE DATOS
# Identificar instalaciones activas (>5 publicaciones en 2023)
datos_activos <- datos %>%
  mutate(
    activa = record_count_2023 > 5,
    pais = case_when(
      !is.na(country_consolidated) ~ toupper(country_consolidated),
      !is.na(country_issn) ~ country_issn,
      !is.na(country_tld) ~ toupper(country_tld),
      TRUE ~ "DESCONOCIDO"
    )
  ) %>%
  filter(activa == TRUE)

# 2. TABLA RESUMEN POR PAÍSES
tabla_paises <- datos_activos %>%
  group_by(pais) %>%
  summarise(
    instalaciones_activas = n(),
    total_publicaciones_2023 = sum(record_count_2023, na.rm = TRUE),
    promedio_pub_por_instalacion = round(mean(record_count_2023, na.rm = TRUE), 1),
    .groups = 'drop'
  ) %>%
  arrange(desc(instalaciones_activas))

# Mostrar tabla
print("DISTRIBUCIÓN DE INSTALACIONES OJS ACTIVAS POR PAÍS (>5 pub/año)")
kable(tabla_paises, 
      col.names = c("País", "Instalaciones Activas", "Total Pub. 2023", "Promedio por Instalación"),
      format = "markdown")

# 3. GRÁFICO DE BARRAS - TOP 15 PAÍSES
top15_paises <- tabla_paises %>% head(15)

p1 <- ggplot(top15_paises, aes(x = reorder(pais, instalaciones_activas), y = instalaciones_activas)) +
  geom_col(fill = "steelblue", alpha = 0.8) +
  coord_flip() +
  labs(
    title = "Top 15 Países con Instalaciones OJS Activas",
    subtitle = "Criterio: >5 publicaciones en 2023",
    x = "País",
    y = "Número de Instalaciones Activas"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"))

ggsave("visualizations/top15_paises_barras.png", p1, width = 12, height = 8, dpi = 300)
print(p1)

# 4. GRÁFICO CIRCULAR - TOP 10
top10_paises <- tabla_paises %>% 
  head(10) %>%
  mutate(porcentaje = round(instalaciones_activas / sum(instalaciones_activas) * 100, 1))

p2 <- ggplot(top10_paises, aes(x = "", y = instalaciones_activas, fill = pais)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  labs(
    title = "Distribución de Instalaciones OJS Activas",
    subtitle = "Top 10 países (>5 pub/año en 2023)"
  ) +
  theme_void() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
    legend.position = "right"
  )

ggsave("visualizations/top10_paises_circular.png", p2, width = 10, height = 8, dpi = 300)
print(p2)

# 5. ESTADÍSTICAS GENERALES
cat("\n=== ESTADÍSTICAS GENERALES ===\n")
cat("Total instalaciones en dataset:", nrow(datos), "\n")
cat("Instalaciones activas (>5 pub/2023):", nrow(datos_activos), "\n")
cat("Porcentaje de instalaciones activas:", round(nrow(datos_activos)/nrow(datos)*100, 1), "%\n")
cat("Países con instalaciones activas:", nrow(tabla_paises), "\n")
cat("Total publicaciones 2023 (instalaciones activas):", sum(tabla_paises$total_publicaciones_2023), "\n")