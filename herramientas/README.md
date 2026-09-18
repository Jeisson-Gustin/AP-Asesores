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

## Regenerar los datos

`datos.json` se exporta desde el modelo. Tras cambiar `modelo/parametros.json` o
`modelo/catalogo_recursos.json`, hay que regenerarlo y volver a inyectarlo en el
bloque `<script id="datos">` de `cotizador.html`.
