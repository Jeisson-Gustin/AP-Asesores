# Desarrollos AP · Modelo de negocio de cursos universitarios virtuales

Elementos operativos del plan de negocio: modelo de costos por recurso, política
de precios, portafolio de servicios, argumentario de ventas y motor de
cotizaciones.

---

## Respuesta corta a «¿cuánto cuesta crear un curso?»

| Producto | Horas | Costo de producción | Precio de lista |
| --- | ---: | ---: | ---: |
| Curso nuevo completo, 16 semanas | 429 | $ 33.461.450 | $ 73.615.190 |
| Curso nuevo completo, 13 semanas | 368 | $ 28.701.200 | $ 63.142.640 |
| Curso sobre material existente (tipo USC) | 227 | $ 17.739.920 | $ 39.027.824 |
| Piloto de un parcial, 4 semanas | 132 | $ 10.326.250 | $ 22.717.750 |

Y por recurso individual:

| Recurso | Horas | Criterio humano | Costo | Precio de lista |
| --- | ---: | ---: | ---: | ---: |
| Guía de aprendizaje en HTML | 5,7 | 77 % | $ 485.650 | $ 1.068.430 |
| Video interactivo H5P | 5,0 | 50 % | $ 339.900 | $ 747.780 |
| Actividad H5P de refuerzo | 2,6 | 62 % | $ 197.450 | $ 434.390 |
| Quiz evaluativo Moodle (GIFT) | 4,0 | 75 % | $ 321.750 | $ 707.850 |
| Taller de alta demanda con rúbrica | 3,8 | 74 % | $ 316.250 | $ 695.750 |
| Paquete SCORM diagnóstico | 5,5 | 67 % | $ 396.000 | $ 871.200 |
| Examen parcial con banco ampliado | 5,0 | 66 % | $ 417.450 | $ 918.390 |
| Diseño curricular del curso | 10,0 | 90 % | $ 951.500 | $ 2.093.300 |

El catálogo completo, con el desglose de horas fase por fase, está en
[`docs/01-modelo-costos.md`](docs/01-modelo-costos.md).

---

## Documentos

| Documento | Para qué sirve | Destinatario |
| --- | --- | --- |
| [01 · Modelo de costos](docs/01-modelo-costos.md) | Cuánto cuesta cada recurso y en qué se van las horas | Interno |
| [02 · Plan de negocio](docs/02-plan-negocio.md) | Capacidad, punto de equilibrio, escenarios, riesgos | Interno |
| [03 · Portafolio de servicios](docs/03-portafolio-servicios.md) | Qué se vende y a qué precio | **Cliente** |
| [04 · Argumentario de ventas](docs/04-argumentario-ventas.md) | Cómo sostener el precio y responder objeciones | Interno |
| [05 · Cotizaciones](docs/05-cotizaciones.md) | Cotizaciones vigentes con control de margen | Mixto |
| [06 · Protocolo de revisión con IA](docs/06-protocolo-revision-ia.md) | Cómo se usa la IA y qué revisa un humano | **Cliente** |
| [07 · Propuesta USC](docs/07-propuesta-usc.md) | Propuesta ejecutiva para la Universidad Santiago de Cali | **Cliente** |
| [08 · Auditoría de calidad y precio](docs/08-auditoria-calidad-y-precio.md) | Evaluación de los recursos reales frente al mercado; posición de precio | Interno |

Los documentos 01 y 05 **se generan** desde el modelo. No editarlos a mano.

---

## El modelo

```
modelo/
├── parametros.json          Tarifas, overhead, margen, factor de adecuación
├── catalogo_recursos.json   Cada recurso descompuesto en fases, roles y horas
├── propuestas.json          Planes comerciales y propuestas por institución
├── cotizador.py             Motor de costeo y cotización
├── roi.py                   Modelo de retorno para la institución cliente
├── generar_documentos.py    Regenera docs/01 y docs/05
└── test_cotizador.py        Pruebas de coherencia del modelo
```

### Uso

```bash
# Catálogo completo y plantillas de curso
python3 modelo/cotizador.py

# Desglose de un recurso: en qué se van sus horas
python3 modelo/cotizador.py --recurso guia_html

# Composición y precio de una plantilla de curso
python3 modelo/cotizador.py --curso curso_nuevo_16

# Cotización completa con control interno de margen
python3 modelo/cotizador.py --cotizacion usc_razonamiento_cuantitativo

# Retorno para la institución, con análisis de sensibilidad
python3 modelo/roi.py --estudiantes 400 --matricula 4500000

# Regenerar los documentos derivados
python3 modelo/generar_documentos.py

# Verificar la coherencia del modelo
python3 modelo/test_cotizador.py
```

### Cómo recalibrar

Todo el modelo se recalibra editando `modelo/parametros.json`:

- ¿Cambian las tarifas? `roles[*].tarifa_costo_hora`
- ¿Cambia el margen objetivo? `multiplicador_precio_lista`
- ¿Hasta dónde se puede negociar? `piso_rentabilidad_pct`
- ¿Cuánto vale adecuar material existente? `factor_adecuacion`

Después, ejecutar `generar_documentos.py` y `test_cotizador.py`.

---

## Los tres números que gobiernan cada decisión

| Número | Qué es | Regla |
| --- | --- | --- |
| **Costo total** | Lo que sale del bolsillo, con overhead | Nunca se muestra al cliente |
| **Precio piso** | El mínimo que deja 25 % de margen | **No se cruza nunca** |
| **Precio de lista** | El precio publicado | El ancla de toda negociación |

Ante presión de precio: **se reduce alcance, no precio.**

---

## De dónde salen las horas

Las horas no son estimaciones de intuición. Cada recurso está descompuesto en las
fases del procedimiento documentado en las siete skills del modelo instruccional
(`diseno-curricular`, `generacion-guias`, `produccion-h5p-scorm`,
`generacion-quizzes`, `creacion-actividades-moodle`, `control-calidad`,
`curaduria-recursos`), con un responsable y un criterio de calidad verificable
por fase.

**El 66 % de las horas es criterio humano** —decisión pedagógica, revisión
científica, revisión didáctica y QA técnico— y ese es el argumento comercial
central: la IA acelera el borrador y el código base, lo que libera horas para más
revisión profesional, no para cobrar menos.

---

## Nota sobre el modelo anterior

El archivo `Estrategia_Precio_Curso_DesarrollosAP_2026.xlsx` (abril de 2026)
contenía un «Plan Básico» de $ 4.800.000 con margen efectivo de **−54 %**. El
problema era de nomenclatura: ese plan describía 3 guías y 70 horas, es decir un
piloto de un parcial, no un curso. Llamarlo «curso» instaló un ancla de precio 13
veces inferior a la realidad.

En este modelo ese producto es el **Piloto de un parcial**, con precio de lista de
$ 22.717.750. Ver `docs/02-plan-negocio.md`, sección 10.
