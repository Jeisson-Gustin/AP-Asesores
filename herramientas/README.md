# Cotizador interactivo

`cotizador.html` es una página autocontenida (sin dependencias ni servidor) que
lleva embebidos los datos del modelo. Se abre en cualquier navegador y sirve para
cotizar en vivo frente a un cliente.

**Publicado en:** https://claude.ai/artifact/KWbXe1nigBY6cidVAp2WbF

## Dos vistas

- **Interna:** muestra costo de producción, precio piso, margen, horas de socio y
  descuento máximo admisible. Para preparar la cotización.
- **Cliente:** oculta costos y márgenes. Deja solo el valor si todo fuera nuevo,
  el ahorro por aprovechar lo existente, el precio y el retorno. **Es la vista que
  se proyecta en la reunión.**

La vista elegida se recuerda en el navegador.

## Qué hace

- Parte de una propuesta existente o de una plantilla de curso y permite ajustar
  cantidades de producción nueva y de adecuación recurso por recurso.
- Al hacer clic en el nombre de un recurso, despliega en qué se van sus horas,
  marcando cada fase como criterio humano o asistida por IA, y qué se verifica
  antes de entregarlo. **Es el argumento de venta más fuerte de la herramienta.**
- Recalcula el margen en vivo y avisa cuando el descuento cruza el piso de
  rentabilidad.
- Calcula el retorno para la institución con parámetros editables.

## Cambiar tarifas y topes de precio

El bloque **Tarifas y márgenes** (solo en vista interna) permite cambiar en vivo:

- la tarifa por hora de cada uno de los cuatro roles,
- el overhead operativo,
- el multiplicador que define el **precio máximo** (precio de lista),
- el margen mínimo que define el **precio mínimo** (piso de rentabilidad).

Todo se recalcula desde las fases de cada recurso, así que el costo, el mínimo y
el máximo responden de inmediato. «Restaurar valores del modelo» vuelve a
`parametros.json`. Mientras los valores difieran del modelo publicado, la
herramienta lo advierte.

El panel lateral muestra el **rango cobrable** con botones para fijar el precio
en el mínimo o en el máximo, y una aguja que indica dónde cae el precio actual
dentro de ese rango. Este bloque es interno y se oculta en vista cliente.

## Descargar la cotización en PDF

El bloque **Generar la cotización** produce un PDF con los componentes
seleccionados: alcance, tabla de componentes con valores unitarios, totales con
descuento e IVA, argumento de ahorro, protocolo de producción con IA, garantías y
condiciones. **No incluye costos, márgenes ni tarifas internas.**

El PDF se genera con `pdf.js`, un escritor propio sin dependencias (PDF 1.4 con
las fuentes base Helvetica). No usa ningún CDN: funciona siempre, también sin
conexión.

En el artifact publicado la descarga usa la capacidad `downloads`, que pide
confirmación al visor. Abierto como archivo local, usa la descarga normal del
navegador.

## Regenerar los datos

`datos.json` se exporta desde el modelo. Tras cambiar `modelo/parametros.json` o
`modelo/catalogo_recursos.json`, hay que regenerarlo y volver a inyectarlo en el
bloque `<script id="datos">` de `cotizador.html`.

---

# Formulario de levantamiento de necesidades

Recoge, recurso por recurso, qué necesita el curso del cliente. Con el resumen
que exporta se arma la cotización en el cotizador.

**Publicado en:** https://claude.ai/artifact/7G3BRBiLpAM65dzAbRygbc

## Archivos

| Archivo | Para qué |
| --- | --- |
| `formulario_necesidades.html` | Versión autónoma: se abre en cualquier navegador y se imprime |
| `formulario_necesidades.artifact.html` | La misma página sin el envoltorio HTML, para publicar como Artifact |
| `generar_pdf_formulario.mjs` | Genera el PDF imprimible desde el HTML |
| `../salidas/Formulario_Levantamiento_Necesidades_AP.pdf` | PDF de 13 páginas para enviar o imprimir |

Los tres se generan desde `modelo/catalogo_oferta.json`:

```bash
python3 modelo/generar_formulario.py          # regenera ambos HTML
node herramientas/generar_pdf_formulario.mjs  # regenera el PDF
```

## Qué contiene

15 secciones (A–O) con **79 tipos de recurso** y **119 casillas de cantidad**:

- **A–C** — identificación, contexto del curso y punto de partida (qué material existe ya).
- **D** — las cinco guías HTML, de teórica simple a integral con prueba tipo Saber.
- **E** — 20 tipos de H5P con banco de preguntas, cada uno en 10, 15 y 20 preguntas.
- **F–G** — H5P de presentación y H5P compuestos (libro interactivo, escenario ramificado).
- **H** — videos interactivos de 3, 4 y 5 interacciones, con o sin producción del video base.
- **I** — cuatro tipos de paquete SCORM.
- **J** — cuestionarios de 10, 15 y 20 preguntas, examen parcial y simulacro Saber Pro.
- **K–L** — actividades y recursos nativos de Moodle.
- **M** — arquitectura, auditoría de calidad y acompañamiento.
- **N–O** — requerimientos especiales y observaciones.

## Cómo se usa

1. Se envía el PDF, o el enlace del formulario en pantalla.
2. El cliente marca cantidades. Lo diligenciado se guarda solo en su navegador.
3. **Copiar resumen** produce un texto ordenado por familia, con los códigos de cada recurso.
4. Ese resumen se traslada al cotizador para obtener el precio.

**El formulario no muestra precios.** Es deliberado: primero se define el alcance,
después se cotiza.
