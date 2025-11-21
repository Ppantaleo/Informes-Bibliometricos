# Generar tabla simple como imagen usando ggplot
library(dplyr)
library(ggplot2)
library(readr)

# Cargar datos
tabla_paises <- read_csv("visualizations/tabla_paises_ojs_activos.csv")

# Preparar top 20
top20 <- tabla_paises %>%
  head(20) %>%
  mutate(
    rank = 1:20,
    instalaciones_f = format(instalaciones_activas, big.mark = ","),
    publicaciones_f = format(total_publicaciones_2023, big.mark = ","),
    promedio_f = format(promedio_pub_por_instalacion, nsmall = 1)
  ) %>%
  select(rank, pais, instalaciones_f, publicaciones_f, promedio_f)

# Crear tabla visual con ggplot
p_tabla <- ggplot(top20, aes(x = 1, y = rank)) +
  geom_text(aes(x = 0.5, label = rank), size = 3, hjust = 0.5) +
  geom_text(aes(x = 2, label = pais), size = 3, hjust = 0) +
  geom_text(aes(x = 4, label = instalaciones_f), size = 3, hjust = 1) +
  geom_text(aes(x = 5.5, label = publicaciones_f), size = 3, hjust = 1) +
  geom_text(aes(x = 6.5, label = promedio_f), size = 3, hjust = 1) +
  # Encabezados
  geom_text(aes(x = 0.5, y = 0), label = "Rank", size = 4, fontface = "bold", hjust = 0.5) +
  geom_text(aes(x = 2, y = 0), label = "País", size = 4, fontface = "bold", hjust = 0) +
  geom_text(aes(x = 4, y = 0), label = "Instalaciones", size = 4, fontface = "bold", hjust = 1) +
  geom_text(aes(x = 5.5, y = 0), label = "Pub. 2023", size = 4, fontface = "bold", hjust = 1) +
  geom_text(aes(x = 6.5, y = 0), label = "Promedio", size = 4, fontface = "bold", hjust = 1) +
  scale_y_reverse(limits = c(21, -1)) +
  xlim(0, 7) +
  labs(title = "Top 20 Países con Instalaciones OJS Activas",
       subtitle = "Criterio: >5 publicaciones por año en 2023") +
  theme_void() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold", margin = margin(b = 10)),
    plot.subtitle = element_text(hjust = 0.5, size = 12, margin = margin(b = 20)),
    plot.margin = margin(20, 20, 20, 20)
  )

# Guardar
ggsave("visualizations/tabla_top20_paises.png", p_tabla, 
       width = 12, height = 14, dpi = 300, bg = "white")

print(p_tabla)
cat("Tabla top 20 guardada como: visualizations/tabla_top20_paises.png\n")