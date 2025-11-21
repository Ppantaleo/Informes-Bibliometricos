# Gráfico por continentes
# Usa beacon_ojs.csv (solo aplicaciones OJS)
library(dplyr)
library(ggplot2)
library(readr)

# Cargar datos
datos <- read_csv("../../beacon_ojs.csv")

# Preparar datos activos con continentes
datos_activos <- datos %>%
  mutate(
    activa = record_count_2023 > 5,
    pais_codigo = case_when(
      !is.na(country_consolidated) ~ toupper(country_consolidated),
      !is.na(country_issn) ~ country_issn,
      !is.na(country_tld) ~ toupper(country_tld),
      TRUE ~ "DESCONOCIDO"
    ),
    continente = case_when(
      # Asia
      pais_codigo %in% c("ID", "IN", "TH", "PK", "MY", "SG", "VN", "BD", "KZ", "PH", "CN", "KG", "MN", "LK", "KW", "SA", "AE", "QA", "OM", "BH", "AF", "KH", "MV", "BN", "TL", "MM", "KR", "JP", "TW", "HK", "MO") ~ "Asia",
      # Europa
      pais_codigo %in% c("ES", "UA", "RU", "PL", "IT", "DE", "GB", "PT", "HU", "RO", "RS", "FI", "DK", "NL", "CZ", "FR", "SE", "BE", "GR", "HR", "CH", "NO", "BG", "AT", "SK", "EE", "LV", "LT", "SI", "BY", "IE", "IS", "CY", "MT", "AL", "MK", "ME", "BA") ~ "Europa",
      # América del Norte
      pais_codigo %in% c("US", "CA", "MX", "GT", "CR", "PA", "NI", "SV", "HN", "DO", "PR", "TT", "BB") ~ "América del Norte",
      # América del Sur
      pais_codigo %in% c("BR", "CO", "AR", "PE", "EC", "CL", "VE", "PY", "BO", "UY", "GY") ~ "América del Sur",
      # África
      pais_codigo %in% c("NG", "ZA", "KE", "MA", "DZ", "ET", "GH", "TZ", "EG", "ZM", "CM", "TN", "ZW", "AO", "CD", "BT", "RW", "BW", "SN", "BJ", "MW", "SO", "SZ", "BF", "GM", "CI", "GN", "MG", "TG") ~ "África",
      # Oceanía
      pais_codigo %in% c("AU", "NZ", "VU", "PW", "MH", "NF", "CC") ~ "Oceanía",
      # Oriente Medio
      pais_codigo %in% c("IR", "IQ", "SY", "JO", "LB", "IL", "PS", "YE") ~ "Oriente Medio",
      # Asia Central
      pais_codigo %in% c("UZ", "AZ", "AM", "GE", "MD") ~ "Asia Central",
      # Norte de África
      pais_codigo %in% c("LY", "SD") ~ "Norte de África",
      TRUE ~ "Otros/Desconocido"
    )
  ) %>%
  filter(activa == TRUE)

# Resumen por continentes
resumen_continentes <- datos_activos %>%
  group_by(continente) %>%
  summarise(
    instalaciones_activas = n(),
    total_publicaciones_2023 = sum(record_count_2023, na.rm = TRUE),
    promedio_pub_por_instalacion = round(mean(record_count_2023, na.rm = TRUE), 1),
    .groups = 'drop'
  ) %>%
  arrange(desc(instalaciones_activas))

# Mostrar tabla
cat("=== INSTALACIONES OJS ACTIVAS POR CONTINENTE ===\n")
print(resumen_continentes)

# Gráfico de barras por continentes
p1 <- ggplot(resumen_continentes, aes(x = reorder(continente, instalaciones_activas), y = instalaciones_activas)) +
  geom_col(fill = "darkgreen", alpha = 0.8) +
  coord_flip() +
  labs(
    title = "Instalaciones OJS Activas por Continente",
    subtitle = "Criterio: >5 publicaciones en 2023",
    x = "Continente",
    y = "Número de Instalaciones Activas"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"))

ggsave("visualizations/grafico_continentes_barras.png", p1, width = 12, height = 8, dpi = 300)
print(p1)

# Gráfico circular
p2 <- ggplot(resumen_continentes, aes(x = "", y = instalaciones_activas, fill = continente)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  labs(
    title = "Distribución Mundial de Instalaciones OJS Activas",
    subtitle = "Por continente (>5 pub/año en 2023)"
  ) +
  theme_void() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
    legend.position = "right",
    legend.title = element_blank()
  ) +
  scale_fill_brewer(type = "qual", palette = "Set3")

ggsave("visualizations/grafico_continentes_circular.png", p2, width = 12, height = 8, dpi = 300)
print(p2)

# Guardar tabla
write.csv(resumen_continentes, "visualizations/tabla_continentes_ojs.csv", row.names = FALSE)

cat("\nArchivos generados:\n")
cat("- visualizations/grafico_continentes_barras.png\n")
cat("- visualizations/grafico_continentes_circular.png\n")
cat("- visualizations/tabla_continentes_ojs.csv\n")