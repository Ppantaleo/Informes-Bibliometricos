# PredVoc: Vocabulario Controlado de Indicadores de Publicación Depredadora

Vocabulario SKOS bilingüe (ES/EN) para identificación y clasificación de revistas científicas con prácticas editoriales depredadoras.

## 📁 Estructura del Repositorio
```
predvoc/
├── predrev-map.ttl           # Schema: Perfil de aplicación (10 elementos metadatos)
├── predvoc-skos.ttl          # Scheme: Vocabulario SKOS (50-80 conceptos, 6 facetas)
├── predvoc-skos.rdf          # Scheme: Vocabulario RDF/XML  
├── predvoc-owl.owl           # Extensión OWL (propiedades: severity, detectionMethod, etc.)
├── predvoc-instances.ttl     # 8 ejemplos revistas (legítimas/depredadoras/secuestradas)
├── predvoc-void.ttl          # Metadatos VoID del dataset
├── sparql-queries.md         # 15 consultas SPARQL de ejemplo
├── docs/                     # Documentación HTML para GitHub Pages
│   ├── index.html            # Landing page del proyecto
│   ├── predrev-map.html      # Documentación schema
│   └── predvoc-skos.html     # Documentación scheme
└── README.md                 # Este archivo
```

## 🎯 Componentes Principales

### PredRev-MAP (Schema)
**Archivo:** `predrev-map.ttl`  
Perfil de aplicación de metadatos con 10 elementos para describir revistas científicas:
- Datos básicos: título, ISSN, editorial, sitio web
- Datos evaluación: APC, tiempo revisión, indexación
- **Campo clave:** `predrev:indicadores-depredadores` → usa PredVoc-SKOS como valores

### PredVoc-SKOS (Scheme)
**Archivo:** `predvoc-skos.ttl`  
Vocabulario controlado con 50-80 indicadores organizados en 6 facetas:
1. **Integridad Editorial:** revista secuestrada, ISSN falso, comité ficticio
2. **Revisión por Pares:** revisión inexistente, aceptación inmediata, revisores falsos
3. **Prácticas Comerciales:** APC ocultos, facturación fraudulenta, spam
4. **Indexación y Métricas:** indexación falsa, factor impacto falso
5. **Sitio Web:** errores frecuentes, falta información contacto
6. **Afiliaciones:** dirección falsa, email gratuito, afiliación falsa

### PredVoc-OWL (Extensión)
**Archivo:** `predvoc-owl.owl`  
Propiedades personalizadas para conceptos SKOS:
- `predvoc:severity`: critical | high | moderate | low
- `predvoc:detectionMethod`: manual | automated | hybrid
- `predvoc:evidenceType`: visual | documentary | behavioral
- `predvoc:prevalenceRate`: decimal 0.0-1.0

### Instancias de Ejemplo
**Archivo:** `predvoc-instances.ttl`  
8 ejemplos demuestran integración schema+scheme:
- Revista depredadora típica
- Revista sospechosa
- Revista legítima (Nature Communications)
- Revista secuestrada (hijacked)
- Revista emergente regional
- Revista con problemas comerciales
- Revista OA legítima (BMC Biology)
- Revista con indexación fraudulenta

## 🔍 Consultas SPARQL

**Archivo:** `sparql-queries.md`  
15 consultas ejemplo organizadas en 4 categorías:
- Consultas sobre vocabulario (listar facetas, contar conceptos, buscar términos)
- Consultas sobre revistas (listar evaluadas, filtrar por indicadores)
- Consultas analíticas (distribución gravedad, indicadores frecuentes)
- Consultas validación (conceptos sin definición, huérfanos)

**Nota:** Ver `sparql-queries.md` para instrucciones de configuración local (Apache Jena Fuseki o Python rdflib).

## 🌐 Documentación

**Documentación completa:** https://ppantaleo.github.io/Informes-Bibliometricos/UC3M/predvoc/

Incluye:
- Landing page con descripción completa del proyecto
- Documentación técnica del schema (PredRev-MAP)
- Documentación técnica del scheme (PredVoc-SKOS)
- Ejemplos de uso integrado

## 📊 Metadatos

**Archivo:** `predvoc-void.ttl`  
Descripción VoID del dataset:
- Estadísticas: ~2500 tripletas, 58 entidades, 15 propiedades
- Vocabularios usados: SKOS, Dublin Core, OWL
- Formatos disponibles: Turtle (.ttl), RDF/XML (.rdf)

## 🔗 Namespaces

- **PredRev-MAP:** `http://purl.org/predrev/`
- **PredVoc-SKOS:** `http://purl.org/predvoc/`

## 🚀 Uso Rápido
```turtle
# Ejemplo: Describir revista con indicadores
@prefix predrev: <http://purl.org/predrev/> .
@prefix predvoc: <http://purl.org/predvoc/> .

<http://example.org/journal/xyz> a predrev:Revista ;
    predrev:titulo "Journal XYZ" ;
    predrev:issn "1234-5678" ;
    predrev:indicadores-depredadores 
        predvoc:issn-falso ,
        predvoc:apc-ocultos ;
    predrev:nivel-riesgo "Depredadora" .
```

## 📥 Descargas

Vocabulario disponible en múltiples formatos:

**PredVoc-SKOS (Vocabulario):**
- Turtle: [predvoc-skos.ttl](https://ppantaleo.github.io/Informes-Bibliometricos/UC3M/predvoc/predvoc-skos.ttl)
- RDF/XML: [predvoc-skos.rdf](https://ppantaleo.github.io/Informes-Bibliometricos/UC3M/predvoc/predvoc-skos.rdf)

**PredRev-MAP (Schema):**
- Turtle: [predrev-map.ttl](https://ppantaleo.github.io/Informes-Bibliometricos/UC3M/predvoc/predrev-map.ttl)

**Otros archivos:**
- [predvoc-instances.ttl](https://ppantaleo.github.io/Informes-Bibliometricos/UC3M/predvoc/predvoc-instances.ttl) - Ejemplos revistas
- [predvoc-void.ttl](https://ppantaleo.github.io/Informes-Bibliometricos/UC3M/predvoc/predvoc-void.ttl) - Metadatos VoID
- [predvoc-owl.owl](https://ppantaleo.github.io/Informes-Bibliometricos/UC3M/predvoc/predvoc-owl.owl) - Extensión OWL

## 📄 Licencia

CC-BY 4.0

## 🔗 Enlaces

- **Documentación:** https://ppantaleo.github.io/Informes-Bibliometricos/UC3M/predvoc/
- **Repositorio:** https://github.com/Ppantaleo/Informes-Bibliometricos/tree/main/UC3M/predvoc