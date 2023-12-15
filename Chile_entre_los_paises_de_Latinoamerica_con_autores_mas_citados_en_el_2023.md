Guía de código para el informe

Figura 1 

``` r
# Cargar las librerías necesarias
library(tidyverse)
library(plotly)
library(htmlwidgets)

# Ruta al archivo CSV
ruta_csv <- "C:\\...\\Incites Researchers.csv"

# Cargar el CSV en un dataframe
datos <- read.csv(ruta_csv)

# Seleccionar los 10 autores más citados
top_10_autores <- datos %>%
  dplyr::arrange(desc(`Times.Cited`)) %>%
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

Tabla 1

``` r
# Cargar las librerías necesarias
library(knitr)
library(kableExtra)
library(dplyr)  # Agregamos la carga de la librería dplyr

# Seleccionar los primeros diez autores
top_10_autores <- datos %>%
    dplyr::arrange(desc(`Times.Cited`)) %>%
    head(10)

# Seleccionar columnas específicas
tabla_autores <- top_10_autores %>%
    select(`Name`, `Affiliation`, `Times.Cited`, `Country.or.Region`, `X..All.Open.Access.Documents`)

# Imprimir la tabla con estilo
kable(tabla_autores, "html") %>%
    kable_styling(full_width = FALSE, position = "center", bootstrap_options = "striped", font_size = 14) %>%
    add_header_above(c(" " = 1, "Información del Autor" = 4), bold = TRUE, color = "white", background = "#7DC22B")

```

Figura 2

``` r
# Cargar las librerías necesarias
library(plotly)

# Crear un gráfico de barras interactivo con plotly y etiquetas al hacer hover
plot_ly(x = instituciones_mas_citadas$Affiliation, 
        y = instituciones_mas_citadas$TotalCitas, 
        type = 'bar',
        text = instituciones_mas_citadas$TotalCitas,
        hoverinfo = "text",  # Mostrar solo el texto en hover
        marker = list(color = colores_verdes)) %>%
  layout(title = "Top 10 Instituciones con Más Citas",
         xaxis = list(title = "Institución"),
         yaxis = list(title = "Total de Citas"),
         showlegend = FALSE)  # Ocultar la leyenda
```

Figura 3

``` r
# Crear un resumen por país y sumar las citas
resumen_por_pais <- datos %>%
  group_by(`Country.or.Region`) %>%
  summarize(TotalCitas = sum(`Times.Cited`)) %>%
  ungroup() %>%
  arrange(desc(TotalCitas)) %>%
  head(10)

# Reordenar el dataframe por la cantidad total de citas en orden descendente
resumen_por_pais$`Country.or.Region` <- factor(resumen_por_pais$`Country.or.Region`, levels = resumen_por_pais$`Country.or.Region`)

# Crear un gráfico de barras interactivo con plotly
plot_ly(
  x = resumen_por_pais$`Country.or.Region`,
  y = resumen_por_pais$TotalCitas,
  type = 'bar',
  text = paste(
    "País: ", resumen_por_pais$`Country.or.Region`,
    "<br>Total de Citas: ", resumen_por_pais$TotalCitas
  ),
  hoverinfo = "text",
  marker = list(color = colores_verdes)
) %>%
  layout(
    title = "Top 10 Países con Más Citas",
    xaxis = list(title = "País"),
    yaxis = list(title = "Total de Citas"),
    showlegend = FALSE  # Ocultar la leyenda
  )
``` 

