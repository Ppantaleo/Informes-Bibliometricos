# Consultas SPARQL de Ejemplo - PredVoc

Este documento contiene consultas SPARQL de ejemplo para explorar y utilizar el vocabulario PredVoc.

## ⚠️ Nota Importante

**Este vocabulario NO tiene SPARQL endpoint público.**

Para ejecutar estas consultas, tienes dos opciones:

### Opción A: Apache Jena Fuseki (Local)
```bash
# 1. Descargar Apache Jena Fuseki
wget https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.10.0.tar.gz
tar -xzf apache-jena-fuseki-4.10.0.tar.gz
cd apache-jena-fuseki-4.10.0

# 2. Iniciar servidor
./fuseki-server --mem /predvoc

# 3. Abrir interfaz web
# http://localhost:3030

# 4. Upload dataset
# Cargar predvoc-skos.ttl en el dataset /predvoc

# 5. Ejecutar consultas en:
# http://localhost:3030/predvoc/sparql
```

### Opción B: Python + rdflib
```python
from rdflib import Graph

# Cargar vocabulario
g = Graph()
g.parse("predvoc-skos.ttl", format="turtle")

# Ejecutar consulta
query = """
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?faceta ?labelES
WHERE {
  ?faceta skos:topConceptOf predvoc: ;
          skos:prefLabel ?labelES .
  FILTER(lang(?labelES) = "es")
}
"""

for row in g.query(query):
    print(row)
```

---

## Prefijos Comunes
```sparql
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX predrev: <http://purl.org/predrev/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
```

---

## Consultas sobre el Vocabulario (SKOS)

### Q1: Listar todas las facetas (Top Concepts)
```sparql
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?faceta ?labelES ?labelEN
WHERE {
  ?faceta skos:topConceptOf predvoc: ;
          skos:prefLabel ?labelES , ?labelEN .
  FILTER(lang(?labelES) = "es")
  FILTER(lang(?labelEN) = "en")
}
ORDER BY ?labelES
```

### Q2: Contar conceptos por faceta
```sparql
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?faceta ?labelES (COUNT(?concepto) AS ?total)
WHERE {
  ?faceta skos:topConceptOf predvoc: ;
          skos:prefLabel ?labelES .
  ?concepto skos:broader ?faceta .
  FILTER(lang(?labelES) = "es")
}
GROUP BY ?faceta ?labelES
ORDER BY DESC(?total)
```

### Q3: Buscar indicadores por palabra clave (español)
```sparql
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concepto ?label ?definicion
WHERE {
  ?concepto a skos:Concept ;
            skos:prefLabel ?label ;
            skos:definition ?definicion .
  FILTER(lang(?label) = "es")
  FILTER(lang(?definicion) = "es")
  FILTER(CONTAINS(LCASE(?label), "issn") || CONTAINS(LCASE(?definicion), "issn"))
}
```

### Q4: Obtener jerarquía completa de un concepto
```sparql
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concepto ?label ?padre ?labelPadre
WHERE {
  predvoc:issn-falso skos:prefLabel ?label ;
                     skos:broader* ?padre .
  ?padre skos:prefLabel ?labelPadre .
  FILTER(lang(?label) = "es")
  FILTER(lang(?labelPadre) = "es")
}
```

### Q5: Listar conceptos relacionados
```sparql
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concepto ?label ?relacionado ?labelRelacionado
WHERE {
  predvoc:revista-secuestrada skos:prefLabel ?label ;
                              skos:related ?relacionado .
  ?relacionado skos:prefLabel ?labelRelacionado .
  FILTER(lang(?label) = "es")
  FILTER(lang(?labelRelacionado) = "es")
}
```

### Q6: Sinónimos (altLabel) de un concepto
```sparql
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concepto ?prefLabel ?altLabel
WHERE {
  predvoc:apc-ocultos skos:prefLabel ?prefLabel ;
                      skos:altLabel ?altLabel .
  FILTER(lang(?prefLabel) = "es")
  FILTER(lang(?altLabel) = "es")
}
```

---

## Consultas sobre Revistas (Instancias)

### Q7: Listar todas las revistas evaluadas
```sparql
PREFIX predrev: <http://purl.org/predrev/>

SELECT ?revista ?titulo ?issn ?nivelRiesgo
WHERE {
  ?revista a predrev:Revista ;
           predrev:titulo ?titulo ;
           predrev:issn ?issn ;
           predrev:nivel-riesgo ?nivelRiesgo .
}
ORDER BY ?nivelRiesgo ?titulo
```

### Q8: Revistas depredadoras con indicadores específicos
```sparql
PREFIX predrev: <http://purl.org/predrev/>
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?revista ?titulo ?indicador ?labelIndicador
WHERE {
  ?revista a predrev:Revista ;
           predrev:titulo ?titulo ;
           predrev:nivel-riesgo "Depredadora" ;
           predrev:indicadores-depredadores ?indicador .
  ?indicador skos:prefLabel ?labelIndicador .
  FILTER(lang(?labelIndicador) = "es")
}
```

### Q9: Revistas con APC superior a 3000 USD
```sparql
PREFIX predrev: <http://purl.org/predrev/>

SELECT ?revista ?titulo ?apc ?nivelRiesgo
WHERE {
  ?revista a predrev:Revista ;
           predrev:titulo ?titulo ;
           predrev:apc-monto ?apc ;
           predrev:nivel-riesgo ?nivelRiesgo .
  FILTER(?apc > 3000)
}
ORDER BY DESC(?apc)
```

### Q10: Revistas con tiempo de revisión sospechosamente rápido
```sparql
PREFIX predrev: <http://purl.org/predrev/>

SELECT ?revista ?titulo ?tiempoRevision ?nivelRiesgo
WHERE {
  ?revista a predrev:Revista ;
           predrev:titulo ?titulo ;
           predrev:tiempo-revision ?tiempoRevision ;
           predrev:nivel-riesgo ?nivelRiesgo .
  FILTER(?tiempoRevision < 14)  # Menos de 2 semanas
}
ORDER BY ?tiempoRevision
```

---

## Consultas Analíticas

### Q11: Distribución de indicadores por nivel de gravedad
```sparql
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?severity (COUNT(?concepto) AS ?total)
WHERE {
  ?concepto a skos:Concept ;
            predvoc:severity ?severity .
}
GROUP BY ?severity
ORDER BY DESC(?total)
```

### Q12: Indicadores más frecuentes en revistas evaluadas
```sparql
PREFIX predrev: <http://purl.org/predrev/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?indicador ?label (COUNT(?revista) AS ?frecuencia)
WHERE {
  ?revista a predrev:Revista ;
           predrev:indicadores-depredadores ?indicador .
  ?indicador skos:prefLabel ?label .
  FILTER(lang(?label) = "es")
}
GROUP BY ?indicador ?label
ORDER BY DESC(?frecuencia)
```

### Q13: Revistas evaluadas por mes
```sparql
PREFIX predrev: <http://purl.org/predrev/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (SUBSTR(STR(?fecha), 1, 7) AS ?mes) (COUNT(?revista) AS ?total)
WHERE {
  ?revista a predrev:Revista ;
           predrev:fecha-evaluacion ?fecha .
}
GROUP BY (SUBSTR(STR(?fecha), 1, 7))
ORDER BY ?mes
```

---

## Consultas de Validación

### Q14: Conceptos sin definición en español
```sparql
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concepto ?label
WHERE {
  ?concepto a skos:Concept ;
            skos:inScheme predvoc: ;
            skos:prefLabel ?label .
  FILTER(lang(?label) = "es")
  FILTER NOT EXISTS {
    ?concepto skos:definition ?def .
    FILTER(lang(?def) = "es")
  }
}
```

### Q15: Conceptos huérfanos (sin broader)
```sparql
PREFIX predvoc: <http://purl.org/predvoc/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concepto ?label
WHERE {
  ?concepto a skos:Concept ;
            skos:inScheme predvoc: ;
            skos:prefLabel ?label .
  FILTER(lang(?label) = "es")
  FILTER NOT EXISTS { ?concepto skos:broader ?x }
  FILTER NOT EXISTS { ?concepto skos:topConceptOf predvoc: }
}
```

---

## Uso desde Línea de Comandos

### Con Apache Jena ARQ (local)
```bash
# Instalar Apache Jena
wget https://dlcdn.apache.org/jena/binaries/apache-jena-4.10.0.tar.gz
tar -xzf apache-jena-4.10.0.tar.gz

# Ejecutar consulta desde archivo
./apache-jena-4.10.0/bin/arq --data=predvoc-skos.ttl --query=query.rq
```

### Con Python rdflib
```python
from rdflib import Graph

g = Graph()
g.parse("predvoc-skos.ttl", format="turtle")
g.parse("predvoc-instances.ttl", format="turtle")

query = """
PREFIX predrev: <http://purl.org/predrev/>
SELECT ?titulo ?nivelRiesgo
WHERE {
  ?revista a predrev:Revista ;
           predrev:titulo ?titulo ;
           predrev:nivel-riesgo ?nivelRiesgo .
}
"""

for row in g.query(query):
    print(f"{row.titulo}: {row.nivelRiesgo}")
```

---

## Notas

- Estas consultas asumen que has cargado `predvoc-skos.ttl` y `predvoc-instances.ttl`
- Las consultas sobre revistas (Q7-Q13) requieren instancias de ejemplo
- Las propiedades OWL (severity, detectionMethod) solo están disponibles si cargas también `predvoc-owl.owl`
- Para consultas complejas que combinen múltiples archivos, cárgalos todos en el mismo dataset

---

**Licencia:** CC-BY 4.0  
**Última actualización:** 2025-01-08  
**Repositorio:** https://github.com/Ppantaleo/Informes-Bibliometricos/tree/main/UC3M/predvoc