# Consultas SPARQL de Ejemplo

## Configuración
Carga `predvoc-skos.ttl` en Apache Jena Fuseki o similar.

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

### 3. Buscar conceptos sobre "falso"
```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concepto ?label
WHERE {
  ?concepto skos:prefLabel ?label .
  FILTER(CONTAINS(LCASE(?label), "falso"))
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

- Estas consultas asumen que has cargado `predvoc-skos.ttl`
- El ejemplo Python requiere además `predvoc-instances.ttl` para consultas sobre revistas
- Las propiedades OWL (severity, detectionMethod) solo están disponibles si cargas también `predvoc-owl.owl`
- Para consultas complejas que combinen múltiples archivos, cárgalos todos en el mismo dataset

---

**Licencia:** CC-BY 4.0  
**Última actualización:** 2025-01-08  
**Repositorio:** https://github.com/Ppantaleo/Informes-Bibliometricos/tree/main/UC3M/predvoc