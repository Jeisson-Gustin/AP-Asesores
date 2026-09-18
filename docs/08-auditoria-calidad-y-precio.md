# Auditoría de calidad y posición de precio

*Evaluación independiente de los recursos producidos frente al mercado · 18 de septiembre de 2026*

---

## 1. Alcance real de esta auditoría

**Recursos examinados directamente**, descargados del Drive y abiertos uno por uno:

| Recurso | Tipo | Fecha | Qué se revisó |
| --- | --- | --- | --- |
| `Lectura_Aplicaciones de las secciones cónicas.html` | Guía | sep 2026 | Código y render completo |
| `Guia_Interactiva_Igualdad_Identidad_Algebraica.html` | Guía | ago 2026 | Código y render completo |
| `Taller 1_Teoria_Conjuntos.html` | Taller | dic 2025 | Los 20 ejercicios, uno por uno |
| `Parcial 3.gift` | Cuestionario | dic 2025 | Los 20 ítems, uno por uno |
| `Igualdad_Completa_Ejercicios.h5p` | H5P | ago 2026 | Descomprimido: manifiesto, librerías y los 14 ítems |

**Dos advertencias que cambian cómo leer lo que sigue:**

1. **No pude entrar al aula de Moodle.** `98.81.179.151` no está en la lista de
   hosts permitidos del entorno donde trabajo. No es que el servidor esté caído:
   es una restricción de mi lado. Para auditar el aula necesito una exportación
   del curso (backup `.mbz`), o los archivos en una carpeta de Drive.
2. **Ninguno de los cinco recursos pertenece al curso de la USC.** El GIFT dice
   textualmente «EVALUACIÓN PARCIAL 2 — PROBABILIDAD Y ESTADÍSTICA I · Nivel:
   Segundo de Preparatoria», y el taller lleva el mismo encabezado. Son del PEAC.
   La carpeta que encontré con «Teoría de Conjuntos» coincide en tema con la
   semana 1 de Razonamiento Cuantitativo, pero no es el mismo material.

Las conclusiones valen para el estándar de producción de Desarrollos AP. Para
afirmar algo sobre el curso que le está cotizando a la USC, necesito ese material.

---

## 2. Qué encontré, recurso por recurso

### 2.1 Guía de secciones cónicas — buena

Lo que hace bien es mérito real: 24 ejercicios con verificación inmediata y
contador de aciertos, navegación en cuatro pestañas, SVG propio dibujando las
cuatro cónicas con su plano de corte, ocho tablas, problemas contextualizados de
verdad (estufa solar parabólica, galería de susurros), el error de clasificación
más común señalado, responsive, cero errores de consola.

No es un documento maquetado: es un objeto de aprendizaje interactivo.

**Falta:** objetivo de aprendizaje, competencias, referencias bibliográficas,
MathJax, atributos ARIA. Y las respuestas de los 24 ejercicios **no salen del
navegador**: el estudiante trabaja y el docente nunca se entera.

### 2.2 Guía de igualdad e identidad algebraica — simple

Del mismo periodo, sin interactividad alguna: cero botones, cero campos. Es
contenido expositivo con tablas. Se cobra igual que la anterior y no es lo mismo.

### 2.3 Taller de teoría de conjuntos — buen contenido, producto incompleto

Los 20 ejercicios están bien construidos y bien graduados: notación → cardinalidad
→ operaciones → aplicaciones con inclusión-exclusión → demostración de propiedades
→ integradores de tres conjuntos. Los contextos son actuales y pertinentes (redes
sociales, deportes, hábitos de lectura, cine). El ejercicio 19 es ingenioso: pide
el conjunto potencia de A∩B donde la intersección es vacía.

**Pero el catálogo lo vende como «taller de alta demanda con rúbrica y
solucionario», y el archivo no tiene ninguna de las dos.** Tampoco objetivo,
competencias, tiempo estimado ni producto entregable definido. La única
instrucción es «resuelve en tu libreta mostrando el procedimiento».

Es una hoja de ejercicios, buena, pero no el producto descrito.

### 2.4 Cuestionario GIFT — tres problemas concretos

Estructura correcta: 20 ítems en cuatro tipos (10 selección múltiple, 5
verdadero/falso, 3 emparejar, 2 completar). Sintaxis válida, UTF-8, títulos
únicos. Los distractores son en general plausibles.

**Problema 1 — cero retroalimentación.** No hay un solo `#` de opción ni un
`####` general en todo el archivo. La skill `generacion-quizzes` la declara
obligatoria en cada pregunta y en cada opción incorrecta, y el modelo de costos
cobra media hora por quiz para redactarla.

**Problema 2 — cero preguntas numéricas.** La distribución de la propia skill
pide 25 % de ítems numéricos con tolerancia. En un curso de razonamiento
cuantitativo, no tener ítems de cálculo es una ausencia de fondo, no de forma.

**Problema 3 — un error científico.** El ítem `COMP1` pregunta qué símbolo indica
pertenencia y acepta como correctas `∈`, `pertenece` y **`epsilon`**. El símbolo
de pertenencia no es epsilon; confundirlos es precisamente el error frecuente que
la guía debería corregir, y aquí el cuestionario lo valida como acierto.

**Problema 4 — nomenclatura.** El archivo se llama `Parcial 3.gift` y su
contenido dice «PARCIAL 2».

### 2.5 Paquete H5P — técnicamente correcto, pedagógicamente plano

**Lo técnico está bien:** `h5p.json` en raíz, `content/content.json` presente,
siete librerías declaradas con versión exacta (`H5P.Blanks-1.14`,
`H5P.Question-1.5`, etc.), 114 archivos. Importa en Moodle sin problema.

**Verifiqué los 14 ítems uno por uno y los 14 son matemáticamente correctos.**
Propiedades de la igualdad, despejes, productos notables, sustitución. Aquí la
revisión científica sí se hizo.

**Lo pedagógico se queda corto:**

- **Un solo formato.** La skill pide variedad (selección múltiple, V/F, completar,
  arrastrar). Esto es solo «completar espacios».
- **Sin umbral de aprobación.** `passPercentage` no está configurado; la skill fija
  70 %. Moodle marcará «completado» con cualquier resultado.
- **Retroalimentación genérica.** Único mensaje: «Obtuviste :num de :total
  puntos». No hay retroalimentación por ítem ni por error.
- **Sin pistas.** H5P.Blanks permite `*respuesta:pista*` y no se usó en ninguno.
- **Licencia sin declarar** (`license: "U"`).
- **Demanda cognitiva baja.** Despejes de una operación. Correcto como refuerzo,
  que es su función, pero no más que eso.

### 2.6 Un hallazgo de proceso: el versionado está descontrolado

Encontré más de veinte archivos `.h5p` que son versiones del mismo recurso:
`Medicion_SI_Video_Interactivo` aparece como `_up`, `_v2`, `_x`, `_py`, `_r2`,
`_fresh`, `_final`, `_final2`, `_final3`, `_final4`, `upload_`, `upload2_`… Varios
pesan 6 MB cada uno.

Es exactamente el problema que su propia skill `curaduria-recursos` está diseñada
para resolver, sin aplicar al material propio. En una entrega a un cliente, esto
es el origen típico de publicar la versión equivocada.

---

## 3. El patrón, y cuánto vale

Los cinco recursos dicen lo mismo:

> **El contenido disciplinar es sólido. Lo que falta, de forma sistemática, es la
> capa pedagógica formal: objetivos, competencias, referencias, rúbricas,
> solucionarios, retroalimentación específica y umbrales.**

Y esa capa es justamente la que el modelo de precios cobra como «criterio
humano». Cuantificado sobre el catálogo:

| Recurso | Fase declarada ausente en lo examinado | % del recurso | Valor |
| --- | --- | ---: | ---: |
| Taller práctico | Solucionario y rúbrica | 39,5 % | $ 274.638 |
| Actividad H5P | Variedad de formatos y umbral | 19,2 % | $ 83.537 |
| Guía HTML | Objetivo, competencias, progresión | 17,5 % | $ 187.444 |
| Quiz Moodle | Retroalimentación por opción | 12,5 % | $ 88.481 |

Aplicado a la cotización de 12 sesiones (AP-2026-004, $ 34.877.040 de lista):

> **$ 7.609.198 — el 21,8 % del alcance cotizado — corresponde a trabajo que el
> catálogo describe y que no aparece en los entregables que pude examinar.**

Esa es la cifra que importa. No es que el precio sea alto: es que una quinta
parte de lo que se promete no está en la muestra.

---

## 4. Qué significa para el precio

Esto **no cambia** la conclusión de que el precio está muy por debajo del
mercado internacional (sección 5). Cambia otra cosa: **ahora mismo hay un riesgo
real de incumplimiento de alcance**, y ese riesgo es más caro que cualquier
descuento.

Hay dos salidas, y solo una es buena:

**Salida buena — completar el producto y mantener el precio.** Las cuatro
carencias suman cerca de 2,5 horas por semana de curso. Sobre las 130-193 horas
de un proyecto, es un 8-12 % más de esfuerzo que ya está cobrado. Se hace y el
producto pasa a valer lo que dice el catálogo.

**Salida mala — bajar el precio un 21,8 %.** Ajusta el precio a lo que
efectivamente se entrega hoy, pero deja el producto por debajo del estándar que
usted mismo definió, y con eso pierde el argumento de venta entero.

**Recomendación: la primera.** Y hacerla antes de firmar con el cliente nuevo, no
después.

---

## 5. Posición de precio frente al mercado

### Benchmark de esfuerzo: Chapman Alliance

El estudio de referencia de la industria (250 organizaciones, ~4.000
profesionales) establece cuántas horas de desarrollo cuesta producir **una hora
de e-learning terminada**:

| Nivel | Descripción | Horas de desarrollo |
| --- | --- | ---: |
| Nivel 1 | Texto, imágenes, preguntas básicas | 49 – 79 |
| Nivel 2 | Interactividad, ejercicios, animación | 184 |
| Nivel 3 | Simulaciones, ramificación, gamificación | 490 – 716 |

La guía de cónicas es claramente **Nivel 2**: interactividad real, verificación,
gráficos propios.

**El ratio de Desarrollos AP, según nuestro modelo:**

| Recurso | Horas de desarrollo | Horas de e-learning | Ratio |
| --- | ---: | ---: | ---: |
| Guía de aprendizaje HTML | 5,7 | 1,0 | 5,7 : 1 |
| Guía de parcial | 13,3 | 3,0 | 4,4 : 1 |
| Actividad H5P | 2,6 | 0,4 | 6,5 : 1 |
| Quiz Moodle | 4,0 | 0,5 | 8,0 : 1 |
| Video interactivo H5P | 5,0 | 0,25 | 20,0 : 1 |
| **Promedio ponderado** | | | **3,9 : 1** |

Frente a un benchmark de 184:1 para ese nivel de interactividad, el modelo
declara ser **47 veces más eficiente**.

**Dos lecturas posibles, y solo una se puede verificar midiendo:**

- **(a) La ganancia es real.** El estudio es de 2010, anterior a la IA
  generativa. Producir el código base de una guía interactiva con 24 ejercicios
  verificados hoy toma una fracción de lo que tomaba entonces. Plausible.
- **(b) Las horas están subestimadas.** Yo construí esas horas leyendo sus
  skills, no cronometrando su trabajo. Si la guía de cónicas tomó 14 horas y no
  5,7, el margen del 54 % es en realidad cero.

**No se puede saber cuál es cierta sin medir. Ese es el punto ciego más grande
del negocio hoy.**

### Benchmark de precio

| Referencia | USD por hora de e-learning | Equivalente COP* |
| --- | ---: | ---: |
| Nivel 1, plantillas | 10.000 | $ 40.000.000 |
| Nivel 2, a medida | 15.000 | $ 60.000.000 |
| Nivel 2, Chapman ajustado a 2026 | 26.400 | $ 105.600.000 |
| **Desarrollos AP (cotizaciones actuales)** | **69 – 141** | **$ 277.000 – 563.000** |

*Tasa supuesta de $4.000 por dólar, no verificada. Ajustar si es materialmente distinta.

**Desarrollos AP cobra entre el 0,4 % y el 1,6 % del benchmark internacional.**

Ese benchmark es de mercado corporativo estadounidense, con locución
profesional, video de estudio y equipos de ocho personas. No es comparable
directamente. Pero una brecha de dos órdenes de magnitud no se explica solo por
el mercado: indica que **el precio está muy lejos del techo, no del piso.**

### Tarifas frente al mercado laboral colombiano

| Concepto | Valor |
| --- | ---: |
| Diseñador instruccional, salario promedio Colombia | $ 2.697.226 / mes = $ 16.858 / h |
| Con prestaciones (×1,5) | $ 25.286 / h |
| Freelance de diseño instruccional en Latinoamérica | USD 10–30 / h |
| **Modelo AP: costo hora DI** | **$ 55.000 / h** |
| **Modelo AP: hora DI facturada al cliente** | **$ 133.100 / h** |
| **Modelo AP: hora del socio facturada** | **$ 217.800 / h** |

Aquí sí hay una observación crítica: **la tarifa de costo del diseñador
instruccional, $55.000/h, está muy por encima del costo laboral real de ese
perfil en Colombia ($25.286/h con prestaciones).**

Eso infla el costo modelado y, con él, el precio piso. No es un problema
comercial —el precio de venta sigue siendo bajo frente al mercado— pero sí
significa que **el margen real es mayor que el 31 % que reportan las
cotizaciones**, si esas horas se pagan a tarifa de mercado.

La tarifa del socio ($217.800/h facturada) sí está en rango: un consultor senior
con posgrado en Colombia factura entre $150.000 y $250.000 la hora.

---

## 6. Respuestas directas

### ¿Los recursos valen lo que se está cobrando?

**Sí, y con holgura.** Una guía interactiva con 24 ejercicios autoevaluables,
gráficos propios y contextualización real, a $1.068.430, es un precio razonable
incluso para el mercado colombiano y muy bajo para cualquier referencia
internacional.

La cotización de $10.006.736 por 25 horas de e-learning equivale a USD 100 por
hora terminada. Proveedores internacionales cobran entre USD 10.000 y 26.400 por
esa misma unidad.

### ¿Estamos al mismo nivel que otras empresas?

Depende de la dimensión:

| Dimensión | Posición |
| --- | --- |
| Diseño visual e interactividad | **Al nivel o por encima** del proveedor regional típico |
| Contextualización disciplinar | **Por encima.** Los problemas son reales y pertinentes, no genéricos |
| Rigor documental (objetivos, competencias, referencias) | **Por debajo**, incluso de su propio estándar declarado |
| Accesibilidad (WCAG, ARIA) | **Por debajo** del estándar internacional |
| Integración con el LMS | **Por debajo**: las guías HTML no reportan nota al libro de calificaciones |
| Producción audiovisual | **Por debajo** de proveedores con estudio propio |
| Precio | **Muy por debajo** del mercado |

### ¿Falta mucho por mejorar?

No mucho, y lo que falta es barato. En orden de retorno sobre esfuerzo:

1. **Objetivo, competencias y referencias en cada guía.** 30-45 min por guía.
   Cierra el riesgo más serio.
2. **MathJax.** Una línea de CDN. Habilita notación matemática seria.
3. **Reporte al LMS.** Que las guías interactivas registren el resultado, vía
   H5P o envolviendo el HTML en un SCORM. Es la diferencia entre «material de
   consulta» y «actividad evaluable».
4. **Accesibilidad básica.** Etiquetas ARIA y navegación por teclado. Cada vez
   más universidades lo exigen en pliegos.
5. **Homogeneidad.** Que la guía más simple se parezca a la mejor.

### ¿Cuáles son los valores reales que se deben cobrar?

**Mantener los precios actuales.** No hay evidencia de estar cobrando de más;
hay evidencia de lo contrario.

Con dos condiciones:

- **Medir las horas reales del próximo proyecto.** Es lo único que convierte
  este modelo de estimación en dato. Si las horas reales superan las estimadas en
  más de un 30 %, hay que revisar precios hacia arriba, no hacia abajo.
- **Cerrar la brecha documental antes de facturar como «auditable».**

**Margen de subida disponible**, una vez cerradas las carencias de la sección 3:

| Escenario | Precio de la guía HTML | Justificación |
| --- | ---: | --- |
| Hoy | $ 1.068.430 | Precio actual |
| Con objetivo, competencias, referencias y MathJax | $ 1.250.000 | Cumple el estándar declarado |
| Con reporte al LMS (SCORM envolvente) | $ 1.450.000 | Pasa de material a actividad evaluable |
| Con accesibilidad WCAG AA | $ 1.600.000 | Habilita pliegos públicos que lo exigen |

Esa ruta sube el precio un 50 % sin aumentar las horas en la misma proporción:
las cuatro mejoras juntas añaden cerca de 2 horas por guía.

---

## 7. Lo que haría antes de la próxima propuesta

1. **Cronometrar.** Registrar horas reales por recurso en el siguiente proyecto,
   con las mismas fases del catálogo. Sin esto, todo el modelo es una hipótesis.
2. **Corregir la tarifa del DI** en `parametros.json`, de $55.000 a un valor
   defendible frente al mercado laboral ($30.000–35.000/h). Sube el margen
   reportado y hace el modelo más honesto.
3. **Añadir objetivo, competencias y referencias** a las guías existentes antes
   de usarlas como muestra comercial.
4. **Preparar una muestra.** La guía de cónicas, con esas tres secciones
   añadidas, es una excelente carta de presentación. Enviarla al cliente nuevo
   antes que cualquier cotización.
5. **No bajar el precio por inseguridad.** El análisis no encontró ningún
   indicio de sobreprecio. Encontró lo contrario.

---

## Fuentes consultadas

- [Chapman Alliance, *How Long Does it Take to Create Learning?*](https://www.slideserve.com/yves/how-long-does-it-take-to-create-learning-a-chapman-alliance-research-study-september-2010)
- [Time Estimates for E-Learning Development — Christy Tucker](https://christytuckerlearning.com/time-estimates-for-e-learning-development/)
- [Custom eLearning Development Cost 2026 — TrainingCost.com](https://trainingcost.com/elearning-development-cost)
- [E-Learning Development Costs 2026 — BlueCarrot](https://bluecarrot.io/blog/e-learning-content-development-cost-per-hour-explained/)
- [Salario de Diseñador Instruccional en Colombia — Computrabajo](https://co.computrabajo.com/salarios/disenador-instruccional)
- [¿Cuánto cuesta producir un curso de e-learning? — Diseño de la Instrucción](https://2-learn.net/director/cuanto-cuesta-producir-un-curso-de-e-learning/)
- [Cuánto cuesta un curso e-learning: tiempos, tarifas y presupuesto — DExpA](https://experienciadeaprendizaje.com/101/cuanto-cuesta-un-curso-elearning-tiempos-tarifas-presupuesto/)
- [Desarrollo de contenidos e-learning Colombia — Artismedia Learning](https://artismedialearning.com/desarrollo-de-contenidos-e-learning-para-bogota-medellin-y-colombia/)
- [¿Cuánto cuesta desarrollar un curso virtual? — Platunico](https://www.platunico.com/elearning/cuanto-cuesta-desarrollar-un-curso-virtual)
