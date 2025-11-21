# Generación de tablas Chile como CSV - Beacon v6
# Crea tablas para análisis e informes
library(dplyr)
library(readr)
library(knitr)

cat("=== GENERACIÓN TABLAS CHILE V6 ===\n")
cat("Creando tablas PNG desde datasets v6...\n\n")

# Cargar datasets v6
chile_todas <- read_csv("../visualizations_v6/chile_todas_instalaciones_v6.csv")
chile_juojs <- read_csv("../visualizations_v6/chile_juojs_activas_v6.csv")

cat("Datasets cargados:\n")
cat("- Chile todas:", nrow(chile_todas), "instalaciones\n")
cat("- Chile JUOJS:", nrow(chile_juojs), "instalaciones activas\n\n")

# Función para crear tabla markdown
crear_tabla_md <- function(datos, titulo, archivo, n_filas = 30) {
  # Preparar datos para tabla
  tabla_datos <- datos %>%
    head(n_filas) %>%
    select(context_name, dominio, record_count_2024, crecimiento_2023_2024, total_historico) %>%
    mutate(
      context_name = substr(context_name, 1, 50),
      dominio = substr(dominio, 1, 35),
      record_count_2024 = format(record_count_2024, big.mark = ","),
      crecimiento_2023_2024 = ifelse(crecimiento_2023_2024 >= 0, 
                                     paste0("+", format(crecimiento_2023_2024, big.mark = ",")),
                                     format(crecimiento_2023_2024, big.mark = ",")),
      total_historico = format(total_historico, big.mark = ",")
    )
  
  # Mostrar tabla
  cat("\n", titulo, "\n")
  cat("=", rep("=", nchar(titulo)), "\n")
  print(kable(tabla_datos, 
        col.names = c("Revista/Contexto", "Dominio", "Pub 2024", "Crecimiento", "Total"),
        format = "markdown"))
  
  # Guardar CSV
  write.csv(tabla_datos, archivo, row.names = FALSE)
  cat("\nTabla guardada:", archivo, "\n")
}

# Tabla 1: Top 30 todas las instalaciones
crear_tabla_md(
  chile_todas,
  "Chile - Todas las Instalaciones OJS (Top 30)",
  "../visualizations_v6/tabla_chile_todas_top30_v6.csv",
  30
)

# Tabla 2: Top 30 instalaciones activas JUOJS
crear_tabla_md(
  chile_juojs,
  "Chile - Instalaciones JUOJS Activas 2024 (Top 30)",
  "../visualizations_v6/tabla_chile_juojs_top30_v6.csv",
  30
)

# Tabla 3: Top 15 con más crecimiento
chile_crecimiento <- chile_juojs %>%
  arrange(desc(crecimiento_2023_2024)) %>%
  filter(crecimiento_2023_2024 > 0)

crear_tabla_md(
  chile_crecimiento,
  "Chile - Instalaciones con Mayor Crecimiento 2023-2024 (Top 15)",
  "../visualizations_v6/tabla_chile_crecimiento_top15_v6.csv",
  15
)

# Tabla 4: Análisis institucional
instituciones_tabla <- chile_juojs %>%
  mutate(
    institucion = case_when(
      grepl("uchile\\.cl", dominio) ~ "Universidad de Chile",
      grepl("uc\\.cl", dominio) ~ "Pontificia Universidad Católica",
      grepl("udec\\.cl", dominio) ~ "Universidad de Concepción",
      grepl("uach\\.cl", dominio) ~ "Universidad Austral de Chile",
      grepl("usach\\.cl", dominio) ~ "Universidad de Santiago",
      grepl("uv\\.cl", dominio) ~ "Universidad de Valparaíso",
      TRUE ~ "Otras instituciones"
    )
  ) %>%
  group_by(institucion) %>%
  summarise(
    instalaciones = n(),
    pub_2024_total = sum(record_count_2024, na.rm = TRUE),
    crecimiento_total = sum(crecimiento_2023_2024, na.rm = TRUE),
    promedio_pub = round(mean(record_count_2024, na.rm = TRUE), 1),
    .groups = 'drop'
  ) %>%
  arrange(desc(instalaciones)) %>%
  mutate(
    pub_2024_total = format(pub_2024_total, big.mark = ","),
    crecimiento_total = ifelse(crecimiento_total >= 0, 
                              paste0("+", format(crecimiento_total, big.mark = ",")),
                              format(crecimiento_total, big.mark = ",")),
    promedio_pub = format(promedio_pub, big.mark = ",")
  )

# Mostrar tabla institucional
cat("\nChile - Análisis por Institución (Beacon v6)\n")
cat("============================================\n")
print(kable(instituciones_tabla, 
      col.names = c("Institución", "Instalaciones", "Pub 2024", "Crecimiento", "Promedio"),
      format = "markdown"))

# Guardar tabla institucional
write.csv(instituciones_tabla, "../visualizations_v6/tabla_instituciones_v6.csv", row.names = FALSE)

cat("\n=== RESUMEN TABLAS GENERADAS ===\n")
cat("1. tabla_chile_todas_top30_v6.csv - Todas las instalaciones\n")
cat("2. tabla_chile_juojs_top30_v6.csv - Solo instalaciones activas\n")
cat("3. tabla_chile_crecimiento_top15_v6.csv - Mayor crecimiento\n")
cat("4. tabla_instituciones_v6.csv - Análisis institucional\n")
cat("\nTodas las tablas guardadas en visualizations_v6/\n")