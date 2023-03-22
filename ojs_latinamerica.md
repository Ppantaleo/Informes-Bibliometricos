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
read_csv(here::here("data/beacon.csv")) %>% 
  filter(country_tld == "AR") %>%
  filter(application == "ojs") %>%
  select(context_name, record_count_2010:record_count_2021) %>% 
  pivot_longer(cols = starts_with("record_count")) %>% 
  mutate(
    name = parse_number(name)
  ) %>% 
  filter(value >= 5) %>% 
  count(name) %>%
  mutate(name = as.integer(name)) %>% 
  ggplot(aes(x = name, y = n)) +
  geom_col(fill = "#3366cc") +
  geom_text(aes(label = n), vjust = -0.5) +
  scale_x_continuous(breaks = seq(2010, 2021, 1)) +
  scale_y_continuous(breaks = seq(0, 1000, 100)) +
  labs(
    x = "Year",
    y = "Journals",
  ) +
  expand_limits(x = c(2010, 2022)) + 
  theme_classic() +
  theme(
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 10),
    axis.ticks = element_blank(),
    plot.title = element_text(hjust = 0.5)
  )



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