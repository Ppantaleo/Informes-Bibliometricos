# Consultas SPARQL de Ejemplo

## Configuración
Las consultas pueden ejecutarse en:
- **Protégé**: Window → Tabs → SPARQL Query (dentro del archivo predvoc-skos.ttl abierto)
- **Apache Jena Fuseki**: Cargar `predvoc-skos.ttl` en un dataset
- **Herramientas online**: SPARQL playground con el archivo cargado

## Consultas Básicas

### 1. Listar todas las facetas
```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX predvoc: <http://purl.org/predvoc/>

SELECT ?faceta ?label
WHERE {
  ?faceta skos:topConceptOf predvoc: .
  ?faceta skos:prefLabel ?label .
  FILTER(LANG(?label) = "es")
}
```

### 2. Contar conceptos por faceta
```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?faceta (COUNT(?concepto) as ?total)
WHERE {
  ?concepto skos:broader ?faceta .
}
GROUP BY ?faceta
```

### 3. Buscar conceptos que contengan "falso"
```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concepto ?label
WHERE {
  ?concepto skos:prefLabel ?label .
  FILTER(REGEX(STR(?label), "falso", "i"))
}
```

### 4. Buscar conceptos relacionados con revisión
```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concepto ?label
WHERE {
  ?concepto skos:prefLabel ?label .
  FILTER(REGEX(STR(?label), "revis", "i"))
}
```

---

## Notas

- Todas las consultas funcionan directamente en Protégé (pestaña SPARQL Query)
- Para consultas más complejas que combinen schema y scheme, carga también `predrev-map.ttl`
- Las propiedades OWL personalizadas (`severity`, `detectionMethod`) requieren cargar `predvoc-owl.owl`