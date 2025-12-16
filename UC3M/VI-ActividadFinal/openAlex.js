// ============================================================================
// DESCARGAR REGISTROS DE OPENALEX - Limite API 10,000
// ============================================================================

const API_BASE = 'https://api.openalex.org/works?filter=publication_year:2024,type:preprint,cited_by_count:>5&sort=cited_by_count:desc';
const PER_PAGE = 200;
const TOTAL_RECORDS = 10000; // Total de registros que queremos
const TOTAL_PAGES = Math.ceil(TOTAL_RECORDS / PER_PAGE); // ~163 páginas
const DELAY_MS = 150; // Delay entre requests para no saturar la API

console.log(`🚀 Iniciando descarga masiva de OpenAlex`);
console.log(`📊 Total a descargar: ${TOTAL_RECORDS} registros`);
console.log(`📄 Páginas necesarias: ${TOTAL_PAGES} páginas de ${PER_PAGE} registros`);
console.log(`⏱️  Tiempo estimado: ${Math.ceil(TOTAL_PAGES * DELAY_MS / 1000 / 60)} minutos`);
console.log(`\n⚠️  NO CIERRES ESTA VENTANA HASTA QUE TERMINE\n`);

// Función para descargar una página con reintentos
async function fetchPageWithRetry(pageNum, maxRetries = 3) {
    const url = `${API_BASE}&per-page=${PER_PAGE}&page=${pageNum}`;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            return data;
            
        } catch (error) {
            if (attempt === maxRetries) {
                console.error(`❌ Error en página ${pageNum} después de ${maxRetries} intentos:`, error);
                throw error;
            }
            console.warn(`⚠️  Reintentando página ${pageNum} (intento ${attempt + 1}/${maxRetries})...`);
            await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
        }
    }
}

// Función para descargar todas las páginas
async function downloadAllPages() {
    let allWorks = [];
    let successCount = 0;
    let errorCount = 0;
    
    for (let page = 1; page <= TOTAL_PAGES; page++) {
        try {
            const data = await fetchPageWithRetry(page);
            
            if (data.results && data.results.length > 0) {
                allWorks = allWorks.concat(data.results);
                successCount++;
                
                // Actualizar progreso cada 10 páginas
                if (page % 10 === 0 || page === TOTAL_PAGES) {
                    const progress = (page / TOTAL_PAGES * 100).toFixed(1);
                    console.log(`📥 Progreso: ${progress}% | Página ${page}/${TOTAL_PAGES} | Total: ${allWorks.length} registros`);
                }
            } else {
                console.warn(`⚠️  Página ${page} sin resultados, deteniendo descarga`);
                break;
            }
            
            // Delay entre requests
            if (page < TOTAL_PAGES) {
                await new Promise(resolve => setTimeout(resolve, DELAY_MS));
            }
            
        } catch (error) {
            errorCount++;
            console.error(`❌ Error en página ${page}:`, error);
            
            // Si hay demasiados errores consecutivos, detener
            if (errorCount > 5) {
                console.error('❌ Demasiados errores, deteniendo descarga');
                break;
            }
        }
    }
    
    console.log(`\n✅ Descarga completada`);
    console.log(`   - Páginas exitosas: ${successCount}/${TOTAL_PAGES}`);
    console.log(`   - Páginas con error: ${errorCount}`);
    console.log(`   - Total registros: ${allWorks.length}`);
    
    return allWorks;
}

// Función para convertir a CSV
function convertToCSV(works) {
    console.log('📝 Convirtiendo a CSV...');
    
    // Header
    let csv = 'ID,Title,Year,Citations,DOI,Type,Source,Authors,Countries,Institutions,Concepts\n';
    
    // Filas
    works.forEach(work => {
        // Extraer autores (solo nombres)
        const authors = (work.authorships || [])
            .map(a => a.author?.display_name || '')
            .filter(n => n)
            .join('; ');
        
        // Extraer países
        const countries = (work.authorships || [])
            .flatMap(a => a.countries || [])
            .filter((v, i, a) => a.indexOf(v) === i) // únicos
            .join('; ');
        
        // Extraer instituciones
        const institutions = (work.authorships || [])
            .flatMap(a => a.institutions || [])
            .map(i => i.display_name || '')
            .filter((v, i, a) => v && a.indexOf(v) === i) // únicos y no vacíos
            .join('; ');
        
        // Extraer conceptos principales
        const concepts = (work.concepts || [])
            .slice(0, 5) // Solo top 5
            .map(c => c.display_name)
            .join('; ');
        
        const row = [
            work.id || '',
            `"${(work.title || '').replace(/"/g, '""')}"`,
            work.publication_year || '',
            work.cited_by_count || 0,
            work.doi || '',
            work.type || '',
            `"${(work.primary_location?.source?.display_name || '').replace(/"/g, '""')}"`,
            `"${authors.replace(/"/g, '""')}"`,
            `"${countries.replace(/"/g, '""')}"`,
            `"${institutions.replace(/"/g, '""')}"`,
            `"${concepts.replace(/"/g, '""')}"`
        ];
        csv += row.join(',') + '\n';
    });
    
    console.log('✅ CSV generado');
    return csv;
}

// Función para descargar archivo
function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    console.log(`💾 Archivo descargado: ${filename}`);
}

// ============================================================================
// EJECUCIÓN PRINCIPAL
// ============================================================================

(async function() {
    const startTime = Date.now();
    
    try {
        // 1. Descargar todos los datos
        const works = await downloadAllPages();
        
        if (works.length === 0) {
            console.error('❌ No se descargaron datos');
            return;
        }
        
        // 2. Guardar JSON completo
        console.log('\n💾 Guardando archivos...');
        const jsonContent = JSON.stringify(works, null, 2);
        downloadFile(jsonContent, 'openAlex_preprints2024_COMPLETO.json', 'application/json');
        
        // 3. Guardar CSV
        const csvContent = convertToCSV(works);
        downloadFile(csvContent, 'openAlex_preprints2024_COMPLETO.csv', 'text/csv');
        
        // Estadísticas finales
        const duration = Math.ceil((Date.now() - startTime) / 1000 / 60);
        console.log('\n🎉 ¡DESCARGA COMPLETADA EXITOSAMENTE!');
        console.log('\n📊 Estadísticas finales:');
        console.log(`   - Total registros descargados: ${works.length}`);
        console.log(`   - Tiempo total: ${duration} minutos`);
        console.log(`   - Archivos generados:`);
        console.log(`     • openAlex_preprints2024_COMPLETO.json (datos completos)`);
        console.log(`     • openAlex_preprints2024_COMPLETO.csv (simplificado)`);
        console.log('\n✅ Revisa tus descargas del navegador\n');
        
    } catch (error) {
        console.error('❌ Error fatal en la ejecución:', error);
    }
})();