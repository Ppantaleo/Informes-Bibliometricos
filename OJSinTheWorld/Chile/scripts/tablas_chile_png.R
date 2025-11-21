# Generar tablas de Chile como imágenes PNG
library(dplyr)
library(ggplot2)
library(readr)

# Cargar datos de Chile
chile_todas <- read_csv("visualizations/chile_todas_instalaciones.csv")
chile_activas <- read_csv("visualizations/chile_instalaciones_activas.csv")

# Función para crear tabla visual
crear_tabla_visual <- function(datos, titulo, archivo, mostrar_activa = FALSE) {
  
  # Preparar datos (top 30 para que sea legible)
  datos_tabla <- datos %>%
    head(30) %>%
    mutate(
      rank = 1:n(),
      context_name = ifelse(nchar(context_name) > 50, 
                           paste0(substr(context_name, 1, 47), "..."), 
                           context_name),
      dominio = ifelse(nchar(dominio) > 25, 
                      paste0(substr(dominio, 1, 22), "..."), 
                      dominio),
      issn = ifelse(nchar(issn) > 20, 
                   paste0(substr(issn, 1, 17), "..."), 
                   issn)
    )
  
  # Crear gráfico base
  p <- ggplot(datos_tabla, aes(x = 1, y = rank)) +
    # Datos
    geom_text(aes(x = 0.5, label = rank), size = 2.5, hjust = 0.5) +
    geom_text(aes(x = 1.5, label = context_name), size = 2.2, hjust = 0) +
    geom_text(aes(x = 4.5, label = dominio), size = 2, hjust = 0) +
    geom_text(aes(x = 6.5, label = record_count_2023), size = 2.5, hjust = 1) +
    geom_text(aes(x = 7.2, label = record_count_2022), size = 2.5, hjust = 1) +
    geom_text(aes(x = 7.9, label = total_historico), size = 2.5, hjust = 1) +
    # Encabezados
    annotate("text", x = 0.5, y = 0, label = "#", size = 3, fontface = "bold") +
    annotate("text", x = 1.5, y = 0, label = "Revista", size = 3, fontface = "bold", hjust = 0) +
    annotate("text", x = 4.5, y = 0, label = "Dominio", size = 3, fontface = "bold", hjust = 0) +
    annotate("text", x = 6.5, y = 0, label = "2023", size = 3, fontface = "bold") +
    annotate("text", x = 7.2, y = 0, label = "2022", size = 3, fontface = "bold") +
    annotate("text", x = 7.9, y = 0, label = "Total", size = 3, fontface = "bold") +
    scale_y_reverse(limits = c(31, -1)) +
    xlim(0, 8.5) +
    labs(title = titulo) +
    theme_void() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14, face = "bold", margin = margin(b = 15)),
      plot.margin = margin(15, 15, 15, 15)
    )
  
  # Agregar columna activa si es necesario
  if(mostrar_activa) {
    p <- p + 
      geom_text(aes(x = 8.3, label = ifelse(activa, "Sí", "No")), size = 2.5, hjust = 0.5) +
      annotate("text", x = 8.3, y = 0, label = "Activa", size = 3, fontface = "bold")
  }
  
  return(p)
}

# 1. Tabla de todas las instalaciones (top 30)
p1 <- crear_tabla_visual(chile_todas, 
                        "Top 30 Instalaciones OJS en Chile - Todas", 
                        "tabla_chile_todas.png", 
                        mostrar_activa = TRUE)

ggsave("visualizations/tabla_chile_todas_top30.png", p1, 
       width = 16, height = 20, dpi = 300, bg = "white")

# 2. Tabla solo instalaciones activas (top 30)
p2 <- crear_tabla_visual(chile_activas, 
                        "Top 30 Instalaciones OJS Activas en Chile (>5 pub/año 2023)", 
                        "tabla_chile_activas.png")

ggsave("visualizations/tabla_chile_activas_top30.png", p2, 
       width = 16, height = 20, dpi = 300, bg = "white")

print(p1)
print(p2)

cat("Tablas de Chile generadas:\n")
cat("- visualizations/tabla_chile_todas_top30.png\n")
cat("- visualizations/tabla_chile_activas_top30.png\n")