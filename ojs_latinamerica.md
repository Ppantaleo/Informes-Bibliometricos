PKP Analytics in Latinamerica 2010 - 2021
================
Updated: March 22, 2023 [In construction]

-   <a href="#argentina-in-2010-21"
    id="toc-argentina-in-2010-21">Argentina in 2010 - 2021</a>
-   <a href="#juojs-global-presence-in-2020"
    id="toc-argentina-in-2010-2021">Argentina in 2010 - 2021</a>
-   <a href="#juojs-growth-2010-20" id="toc-juojs-growth-2010-20">JUOJS
    Growth (2010-20)</a>
-   <a href="#assessing-overlaps" id="toc-assessing-overlaps">Assessing
    overlaps</a>
    -   <a href="#web-of-science" id="toc-web-of-science">Web of Science</a>
    -   <a href="#scopus" id="toc-scopus">Scopus</a>
    -   <a href="#dimensions" id="toc-dimensions">Dimensions</a>
    -   <a href="#ebsco-host" id="toc-ebsco-host">EBSCO Host</a>
    -   <a href="#google-scholar" id="toc-google-scholar">Google Scholar</a>
    -   <a href="#latindex" id="toc-latindex">Latindex</a>
-   <a href="#top-100-cited-journal-domains"
    id="toc-top-100-cited-journal-domains">Top 100 cited journal domains</a>

------------------------------------------------------------------------

## Argentina in 2010-21

``` r
# global df
df_world <-
  df %>%
  drop_na(country) %>%
  count(country, name = "total")

labels <- function(x) {
  if_else(x < 500, as.character(x), "500+")
}

shapefile %>% 
  clean_names() %>%
  rename(country = name) %>%
  mutate(
    country = if_else(country == "Libyan Arab Jamahiriya", "Libya", country),
    country = if_else(country == "United Republic of Tanzania", "Tanzania", country),
    country = if_else(country == "Cote d'Ivoire", "Côte d'Ivoire", country),
    country = if_else(country == "Congo", "Republic of the Congo", country),
    country = if_else(country == "Viet Nam", "Vietnam", country),
    country = if_else(str_detect(country, "Iran"), "Iran", country),
    country = if_else(str_detect(country, "Korea, Republic of"), "South Korea", country),
    country = if_else(str_detect(country, "Korea, Democratic People's Republic of"), "North Korea", country),
    country = if_else(str_detect(country, "Surinam"), "Surinam", country)
  ) %>%
  left_join(df_world, by = "country") %>% #arrange(area) %>% select(country, total, area)
  filter(total > 0 | area > 1000) %>% 
  filter(country != "Antarctica") %>% 
  mutate(
    total = replace_na(total, 0),
    total = pmin(total, 500)
  ) %>%
  ggplot() +
  geom_sf(aes(fill = total), size = 0.1, color = "gray", show.legend = T) +
  scale_fill_gradientn(
    breaks = seq(0, 500, 100),
    labels = labels,
    colors = RColorBrewer::brewer.pal(n = 9, name = "Blues")
  ) +
  guides(
    fill =
      guide_colorbar(
        barheight = 0.5,
        barwidth = 15,
        title = "Journals",
        title.vjust = 1,
      )
  ) +
  theme_void() +
  theme(legend.position = "bottom")
```

<img src="ojs_global_paper_files/figure-gfm/unnamed-chunk-8-1.png" width="100%" />

------------------------------------------------------------------------

<br/><br/>

## JUOJS Growth (2010-20)

``` r
 read_csv(here::here("data/beacon-public.csv")) %>% 
  select(context_name, record_count_2010:record_count_2020) %>% 
  pivot_longer(cols = starts_with("record_count")) %>% 
  mutate(
    name = parse_number(name)
  ) %>% 
  filter(value >= 5) %>% 
  count(name) %>%
  mutate(name = as.integer(name)) %>% 
  ggplot(aes(name, n)) +
  geom_line() +
  geom_point(size = 2) +
  theme_classic() +
  scale_x_continuous(breaks = seq(2010, 2020, 1)) +
  scale_y_continuous(breaks = seq(0, 25000, 5000)) +
  theme(
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 10),
    axis.ticks = element_blank(),
    plot.title = element_text(hjust = 0.5)
  ) +
  labs(
    x = "Year",
    y = "Journals",
  )
```

<img src="ojs_global_paper_files/figure-gfm/unnamed-chunk-9-1.png" width="100%" />

------------------------------------------------------------------------