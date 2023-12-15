Guía de código para el informe

``` r
# Instalar y cargar las librerías necesarias
install.packages("tidyverse")
install.packages("plotly")
install.packages("htmlwidgets")
library(tidyverse)
library(plotly)
library(htmlwidgets)

# Ruta al archivo CSV
ruta_csv <- "C:\\Users\\Patricio\\Desktop\\Incites Researchers.csv"

# Cargar el CSV en un dataframe
datos <- read.csv(ruta_csv)

# Seleccionar los 10 autores más citados
top_10_autores <- datos %>%
  dplyr::arrange(desc(`Times Cited`)) %>%
  head(10)

# Definir colores
colores <- c("#7DC22B", "#D0F092", "#537D1F", "#9FCF78", "#255714", "#B2DBA1", "#A2C441", "#4D6F21", "#C3E58D", "#83A03E")

# Crear el gráfico circular interactivo por país con plotly
plot_ly_object <- plot_ly(top_10_autores, labels = ~`Country.or.Region`, type = "pie", marker = list(colors = colores)) %>%
  layout(title = "Países de los 10 Autores Más Citados") %>%
  colorbar(title = "País") %>%
  layout(hoverlabel = list(bgcolor = "white", bordercolor = "black", font = list(color = "black")))

# Guardar el gráfico interactivo como un archivo HTML
htmlwidgets::saveWidget(plot_ly_object, file = "grafico_interactivo.html")
```
