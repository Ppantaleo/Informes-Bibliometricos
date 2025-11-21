# Análisis básico OJS sin dependencias complejas
# Usa beacon_ojs.csv (solo aplicaciones OJS)
library(dplyr)
library(ggplot2)
library(readr)

# Cargar datos
datos <- read_csv("../../beacon_ojs.csv")

# Preparar datos activos (>5 pub en 2023)
datos_activos <- datos %>%
  mutate(
    activa = record_count_2023 > 5,
    pais_codigo = case_when(
      !is.na(country_consolidated) ~ toupper(country_consolidated),
      !is.na(country_issn) ~ country_issn,
      !is.na(country_tld) ~ toupper(country_tld),
      TRUE ~ "DESCONOCIDO"
    ),
    pais = case_when(
      pais_codigo == "ID" ~ "Indonesia",
      pais_codigo == "BR" ~ "Brasil",
      pais_codigo == "US" ~ "Estados Unidos",
      pais_codigo == "IN" ~ "India",
      pais_codigo == "ES" ~ "España",
      pais_codigo == "TH" ~ "Tailandia",
      pais_codigo == "UA" ~ "Ucrania",
      pais_codigo == "RU" ~ "Rusia",
      pais_codigo == "CO" ~ "Colombia",
      pais_codigo == "PK" ~ "Pakistán",
      pais_codigo == "AR" ~ "Argentina",
      pais_codigo == "MX" ~ "México",
      pais_codigo == "PL" ~ "Polonia",
      pais_codigo == "NG" ~ "Nigeria",
      pais_codigo == "IT" ~ "Italia",
      pais_codigo == "MY" ~ "Malasia",
      pais_codigo == "PE" ~ "Perú",
      pais_codigo == "DE" ~ "Alemania",
      pais_codigo == "CA" ~ "Canadá",
      TRUE ~ pais_codigo
    )
  ) %>%
  filter(activa == TRUE)

# Tabla resumen por países
tabla_paises <- datos_activos %>%
  group_by(pais, pais_codigo) %>%
  summarise(
    instalaciones_activas = n(),
    total_publicaciones_2023 = sum(record_count_2023, na.rm = TRUE),
    promedio_pub_por_instalacion = round(mean(record_count_2023, na.rm = TRUE), 1),
    .groups = 'drop'
  ) %>%
  arrange(desc(instalaciones_activas))

# Mostrar tabla
cat("=== INSTALACIONES OJS ACTIVAS POR PAÍS (>5 pub/año en 2023) ===\n")
print(tabla_paises)

# Gráfico de barras - Top 15
top15 <- tabla_paises %>% head(15)

p1 <- ggplot(top15, aes(x = reorder(pais, instalaciones_activas), y = instalaciones_activas)) +
  geom_col(fill = "steelblue", alpha = 0.8) +
  coord_flip() +
  labs(
    title = "Top 15 Países con Instalaciones OJS Activas",
    subtitle = "Criterio: >5 publicaciones en 2023",
    x = "País",
    y = "Número de Instalaciones Activas"
  ) +
  theme_minimal()

# Configurar dispositivo gráfico para evitar PDF automático
png("visualizations/grafico_top15_paises.png", width = 12, height = 8, units = "in", res = 300)
print(p1)
dev.off()

# También guardar con ggsave
ggsave("visualizations/grafico_top15_paises.png", p1, width = 12, height = 8, dpi = 300)

# Estadísticas generales
cat("\n=== ESTADÍSTICAS GENERALES ===\n")
cat("Total instalaciones en dataset:", nrow(datos), "\n")
cat("Instalaciones activas (>5 pub/2023):", nrow(datos_activos), "\n")
cat("Porcentaje de instalaciones activas:", round(nrow(datos_activos)/nrow(datos)*100, 1), "%\n")
cat("Países con instalaciones activas:", nrow(tabla_paises), "\n")
cat("Total publicaciones 2023 (instalaciones activas):", sum(tabla_paises$total_publicaciones_2023), "\n")

# Guardar tabla como CSV
write.csv(tabla_paises, "visualizations/tabla_paises_ojs_activos.csv", row.names = FALSE)
cat("Tabla guardada como: visualizations/tabla_paises_ojs_activos.csv\n")