# Generar tabla como imagen para los top 20 países
# Usa beacon_ojs.csv (solo aplicaciones OJS)
library(dplyr)
library(readr)
library(gridExtra)
library(grid)

# Cargar datos
tabla_paises <- read_csv("visualizations/tabla_paises_ojs_activos.csv")

# Seleccionar top 20 y formatear
top20 <- tabla_paises %>%
  head(20) %>%
  mutate(
    rank = 1:20,
    instalaciones_activas = format(instalaciones_activas, big.mark = ","),
    total_publicaciones_2023 = format(total_publicaciones_2023, big.mark = ",")
  ) %>%
  select(
    Rank = rank,
    País = pais,
    `Instalaciones Activas` = instalaciones_activas,
    `Publicaciones 2023` = total_publicaciones_2023,
    `Promedio por Instalación` = promedio_pub_por_instalacion
  )

# Crear tabla como grob
tabla_grob <- tableGrob(top20, 
                        rows = NULL,
                        theme = ttheme_default(
                          core = list(fg_params = list(cex = 0.8)),
                          colhead = list(fg_params = list(cex = 0.9, fontface = "bold")),
                          rowhead = list(fg_params = list(cex = 0.8))
                        ))

# Agregar título
titulo <- textGrob("Top 20 Países con Instalaciones OJS Activas (>5 pub/año en 2023)", 
                   gp = gpar(fontsize = 14, fontface = "bold"))

# Combinar título y tabla
tabla_final <- arrangeGrob(titulo, tabla_grob, 
                          heights = c(0.1, 0.9),
                          ncol = 1)

# Guardar como PNG
png("visualizations/tabla_top20_paises.png", width = 12, height = 10, units = "in", res = 300)
grid.draw(tabla_final)
dev.off()

cat("Tabla top 20 guardada como: visualizations/tabla_top20_paises.png\n")