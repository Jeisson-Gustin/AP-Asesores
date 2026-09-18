/* Genera el PDF imprimible del formulario a partir del HTML.
 *
 *   node herramientas/generar_pdf_formulario.mjs
 *
 * Requiere Playwright con Chromium. El PDF sale de las reglas @media print
 * del propio formulario, así que HTML y PDF nunca se desincronizan.
 */
import { chromium } from 'playwright';

const ENTRADA = 'herramientas/formulario_necesidades.html';
const SALIDA  = 'salidas/Formulario_Levantamiento_Necesidades_AP.pdf';

const navegador = await chromium.launch();
const pagina = await navegador.newPage();
await pagina.goto('file://' + process.cwd() + '/' + ENTRADA);
await pagina.waitForTimeout(1500);                    // esperar las fuentes
await pagina.evaluate(() => { try { localStorage.removeItem('ap-formulario'); } catch (e) {} });
await pagina.reload();
await pagina.waitForTimeout(1500);
await pagina.pdf({
  path: SALIDA,
  format: 'Letter',
  printBackground: true,
  margin: { top: '14mm', bottom: '16mm', left: '13mm', right: '13mm' },
});
console.log('PDF escrito en ' + SALIDA);
await navegador.close();
