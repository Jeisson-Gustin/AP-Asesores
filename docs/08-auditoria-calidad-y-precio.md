# Auditoría de calidad y posición de precio

*Evaluación independiente de los recursos producidos frente al mercado · 18 de septiembre de 2026*

---

## 0. Qué pude verificar y qué no

Antes de cualquier juicio, el alcance de esta auditoría, porque determina cuánto
vale lo que sigue.

**Examiné directamente:**

- `Guia_Interactiva_Igualdad_Identidad_Algebraica.html` (agosto de 2026, 69 KB)
- `Lectura_Aplicaciones de las secciones cónicas.html` (septiembre de 2026, 75 KB)

De ambas revisé el código fuente completo, su estructura semántica, su
comportamiento en navegador y su render en escritorio y en móvil.

**No examiné, y por tanto no puedo juzgar:**

- Ningún paquete H5P real (los archivos del Drive pesan 6 MB y no pude abrirlos
  por esta vía).
- Ningún banco de preguntas GIFT.
- Ningún paquete SCORM.
- Ningún taller con su rúbrica y solucionario.
- El aula de la Universidad Santiago de Cali (`98.81.179.151`), que no es
  accesible desde aquí.

**Consecuencia honesta:** juzgué 2 de los 22 tipos de recurso del catálogo, y
ninguno de los dos pertenece al curso que se le está cotizando a la USC. Las
conclusiones sobre guías HTML son sólidas; todo lo demás es extrapolación y está
marcado como tal.

---

## 1. Calidad real de lo examinado

### La guía de secciones cónicas: buena, con carencias concretas

Es el recurso más reciente y el más representativo de lo que produce hoy.

**Lo que está bien hecho, y es mérito real:**

| Aspecto | Observación |
| --- | --- |
| Interactividad | 24 ejercicios con verificación inmediata, contador de aciertos en vivo, 73 controles, 16 campos de entrada |
| Estructura | Navegación por pestañas en 4 bloques temáticos, 8 tablas, 12 subsecciones |
| Gráficos | SVG propio que ilustra las cuatro cónicas y su plano de corte — no es una imagen tomada de internet |
| Contextualización | Problemas reales: estufa solar parabólica, galería de susurros, órbitas |
| Errores frecuentes | Señalados explícitamente («el error de clasificación más común») |
| Redacción | Precisa, sin relleno, con anclaje histórico (Apolonio) que da sentido al tema |
| Técnica | Responsive, cero errores de consola, CSS embebido, no rompe el estilo del LMS |
| Identificación | Captura nombre, grupo y matrícula del estudiante |

Esto **no es** un documento de texto maquetado. Es un objeto de aprendizaje
interactivo con autoevaluación. Está por encima del PDF o el Word que muchas
universidades siguen llamando «material virtual».

**Lo que falta, y es verificable:**

| Carencia | Impacto |
| --- | --- |
| **Sin objetivo de aprendizaje explícito** | Su propia skill lo exige como sección obligatoria |
| **Sin competencias declaradas** | Ídem. Es lo primero que revisa un par académico en acreditación |
| **Sin referencias bibliográficas** | Ídem. En contexto universitario es una ausencia grave |
| **Sin MathJax ni KaTeX** | La notación usa Unicode; funciona para `x² + y² = 36`, pero no para integrales, matrices, sumatorias o fracciones complejas |
| **Sin atributos ARIA** | No cumple WCAG. Un estudiante con lector de pantalla no puede usar los ejercicios |
| **Las respuestas no salen del navegador** | El estudiante resuelve 24 ejercicios y el docente nunca se entera: no hay reporte al libro de calificaciones |

### La guía de jerarquía de operaciones: notablemente más simple

Del mismo mes, pero sin interactividad alguna (cero botones, cero campos). Es
contenido expositivo con tablas. Las mismas carencias documentales.

**Lectura:** hay dispersión de calidad entre recursos del mismo periodo. El
catálogo de precios cobra lo mismo por ambos, y no son lo mismo.

---

## 2. El riesgo más serio: la brecha entre lo declarado y lo entregado

La skill `generacion-guias` define ocho secciones obligatorias:

> encabezado · **objetivo de aprendizaje** · **competencias trabajadas** ·
> contenidos clave · desarrollo conceptual · síntesis · conexión con la semana
> siguiente · **referencias bibliográficas**

Las guías reales tienen entre cuatro y cinco de esas ocho. **Faltan
sistemáticamente las tres resaltadas.**

Esto importa por tres razones, en orden de gravedad:

1. **El modelo de costos que construimos supone que se cumplen las ocho.** Las
   5,7 horas de la guía semanal incluyen 1,0 h de revisión didáctica que cubre
   objetivo, competencias y progresión. Si eso no se está haciendo, el precio
   cobra trabajo que no se entrega.
2. **El argumento de venta es la auditabilidad.** Todo el material comercial dice
   que el cliente puede auditar el proceso. Si audita y encuentra esta brecha, se
   cae la credibilidad de todo lo demás, incluido el 66 % de criterio humano.
3. **Es exactamente lo que revisa un par académico.** En un proceso de
   acreditación, objetivo y competencias no son adorno: son el primer punto de la
   lista.

**La buena noticia:** es la carencia más barata de cerrar de todas las
detectadas. Añadir objetivo, competencias y referencias a una guía ya escrita son
30-45 minutos. No cambia el precio y elimina el riesgo.

---

## 3. Posición de precio frente al mercado

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

## 4. Respuestas directas

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

## 5. Lo que haría antes de la próxima propuesta

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
