# Plan de negocio operativo

*Desarrollos AP · Cursos universitarios virtuales · 18 de septiembre de 2026*

---

## 1. Qué vendemos exactamente

No vendemos contenido. Vendemos **cursos que funcionan en el LMS de la
universidad y que se pueden auditar**.

La diferencia es operativa y se nota en la entrega. Un proveedor de contenido
entrega archivos. Nosotros entregamos un aula montada, con el libro de
calificaciones cuadrado, los paquetes H5P y SCORM reportando nota, las rúbricas
visibles antes de la entrega, el docente capacitado y un reporte de auditoría de
cinco niveles que la universidad puede archivar como evidencia de calidad ante
sus procesos de acreditación.

Ese último punto es el que cierra ventas. Una universidad acreditada necesita
poder demostrar cómo garantiza la calidad de su oferta virtual. Nuestro reporte
de auditoría es exactamente ese documento.

## 2. El modelo de producción y por qué es defendible

La producción combina generación asistida por IA con revisión profesional
humana, en proporción fija y declarada:

- La IA produce el borrador de contenido, el código HTML base, la estructura de
  los bancos de ítems y el esqueleto de los paquetes SCORM.
- Un profesional revisa, corrige, resuelve y valida **todo** lo que la IA
  produjo, antes de que llegue a un estudiante.

Sobre el catálogo completo, **el 66 % de las horas son criterio humano**: diseño
pedagógico, revisión científica, revisión didáctica y QA técnico. Esa proporción
no es un accidente; es la política de producción, está documentada recurso por
recurso en `docs/01-modelo-costos.md` y es auditable por el cliente.

**El argumento frente a la universidad:** la IA no nos permite cobrar menos por
hacer lo mismo. Nos permite dedicar dos de cada tres horas a lo que realmente
determina si un estudiante aprende, en lugar de gastarlas maquetando HTML y
escribiendo enunciados desde una hoja en blanco.

## 3. Estructura del equipo y capacidad real

| Rol | Vinculación | Costo/hora | Cuello de botella |
| --- | --- | ---: | --- |
| Dirección pedagógica y revisión científica | Socio fundador | $ 90.000 | **Sí** |
| Diseño instruccional | Por obra | $ 55.000 | No |
| Producción técnica y montaje LMS | Por obra | $ 45.000 | No |
| Diseño gráfico y multimedia | Por obra | $ 50.000 | No |

**El límite del negocio son las horas del socio, no el dinero ni la demanda.**
Todo lo demás se contrata por obra y escala con los proyectos.

| Tipo de proyecto | Horas totales | Horas de socio | Meses de socio |
| --- | ---: | ---: | ---: |
| Curso nuevo 16 semanas | 429 | 236 | 2,0 |
| Curso nuevo 13 semanas | 368 | 202 | 1,7 |
| Curso sobre material existente (tipo USC-RC) | 227 | 126 | 1,0 |
| Piloto de un parcial | 132 | 73 | 0,6 |

Con 120 horas facturables de socio al mes (1.440 al año), la capacidad máxima es
de **6 cursos nuevos o 11 cursos de adecuación al año**, y en la práctica una
mezcla de ambos.

## 4. Estructura de costos

Costos fijos mensuales: **$ 1.150.000** ($ 13.800.000 al año).

| Concepto | Mensual | Detalle |
| --- | ---: | --- |
| Herramientas de IA y software | $ 650.000 | Suscripciones de IA, Lumi/H5P, edición, diseño, Moodle de pruebas |
| Administración y legal | $ 500.000 | Contabilidad, facturación electrónica, cámara de comercio, contratos |

Todo lo demás es variable y se activa solo cuando hay proyecto. Esta es la
fortaleza estructural del modelo: **un semestre sin contratos cuesta $ 6.900.000,
no una nómina.**

### Punto de equilibrio

| Escenario | Cursos/año para cubrir los fijos |
| --- | ---: |
| Solo cursos de adecuación (tipo USC-RC) | **1,44** |
| Solo cursos nuevos completos | **0,40** |

Un solo contrato como el de la Universidad Santiago de Cali cubre el 69 % de los
costos fijos de todo el año. El negocio es rentable desde el segundo contrato.

## 5. Escenarios de operación

Ingresos y utilidad anual según la mezcla de proyectos. La utilidad es después de
costos directos y de los fijos anuales.

| Escenario | Adecuación | Nuevos | Ocupación del socio | Ingresos | Utilidad | Margen |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Conservador | 2 | 1 | 30 % | $ 109.690.250 | $ 39.564.950 | 36 % |
| Base | 3 | 2 | 52 % | $ 193.661.164 | $ 83.337.764 | 43 % |
| Expansión | 4 | 3 | 74 % | $ 277.632.078 | $ 127.110.578 | 46 % |
| Óptimo en mezcla | 2 | 4 | 69 % | $ 284.444.984 | $ 142.106.984 | 50 % |

**Lectura estratégica.** Comparar las dos últimas filas: con menos ocupación del
socio (69 % contra 74 %) el escenario de mezcla óptima genera más utilidad. Los
cursos nuevos rinden mucho más por hora de socio que los de adecuación, porque el
descuento de adecuación se aplica sobre el precio pero el esfuerzo de revisión
científica no baja en la misma proporción.

**Regla de decisión:** priorizar cursos nuevos completos. Usar los proyectos de
adecuación como puerta de entrada a una institución, no como el negocio principal.

## 6. Escalera comercial

El recorrido de una institución, diseñado para que cada peldaño financie el
siguiente:

1. **Diagnóstico de aula (gratuito, 4 horas).** Se audita el curso que ya tienen
   y se entrega un informe con hallazgos concretos. Es la herramienta de venta
   más efectiva: el informe demuestra competencia antes de pedir dinero.
2. **Piloto de un parcial.** Cuatro semanas completas y funcionales que la
   universidad evalúa con estudiantes reales. Riesgo bajo para ellos.
3. **Curso completo.** El contrato base.
4. **Paquete de programa.** Ciencias básicas completas, 6 a 10 cursos.
5. **Partner estratégico.** Contrato plurianual con renovación y mantenimiento.

El diagnóstico gratuito cuesta cuatro horas de socio y es la inversión comercial
con mejor retorno del modelo.

## 7. Ingreso recurrente

La venta de un curso es un evento; el mantenimiento es un flujo. Tres líneas
recurrentes que no compiten por las horas de criterio del socio:

| Línea | Precio de lista | Frecuencia |
| --- | ---: | --- |
| Soporte técnico-pedagógico | $ 381.150 / mes | Mensual |
| Reporte analítico de desempeño | $ 810.700 | Semestral |
| Actualización de contenidos | 15 % del valor del curso | Anual |

Diez cursos en mantenimiento generan $ 45.738.000 al año solo por soporte, más
$ 16.214.000 si además contratan el reporte semestral: **$ 61.952.000 anuales**
con consumo marginal de horas de socio. Esta es la línea que convierte el negocio
de proyectos en un negocio con base estable.

## 8. Riesgos y cómo se mitigan

| Riesgo | Impacto | Mitigación |
| --- | --- | --- |
| **Dependencia del socio** | Alto | Documentar el criterio de revisión en las skills. Formar un segundo revisor científico antes de superar el 70 % de ocupación. |
| **Presión de precio por "eso lo hace la IA"** | Alto | Argumentario de la sección 9. Nunca justificar el precio por las horas: justificarlo por el riesgo que la universidad evita. |
| **Ciclo de compra público largo** | Medio | Piloto de parcial como contrato menor, más rápido de aprobar. Mantener un embudo con al menos tres instituciones simultáneas. |
| **Cliente concentrado en la USC** | Alto | Que ninguna institución supere el 50 % de los ingresos anuales a partir del segundo año. |
| **Reproceso por parcelación mal entregada** | Medio | El diseño curricular se factura y se aprueba como hito independiente antes de producir. Sin parcelación aprobada no arranca la producción. |
| **Cambio de versión de Moodle o de librerías H5P** | Bajo | Validación contra el Moodle destino en cada entrega. Contrato de actualización anual. |

## 9. Cómo se defiende el precio

Tres argumentos, en orden de efectividad:

**Primero: el costo de no hacerlo.** Un curso de ciencias básicas de primer
semestre con alta reprobación genera deserción, y cada estudiante que deserta es
matrícula que la universidad deja de recibir durante varios semestres. El cálculo
está en `docs/04-argumentario-ventas.md` con los parámetros que la propia
universidad debe validar. En casi cualquier escenario razonable, el curso se paga
con un puñado de estudiantes retenidos.

**Segundo: el costo de hacerlo internamente.** Producir un curso de 16 semanas
exige 429 horas. Asignarlas a docentes de planta significa descarga académica, sin
garantía de estandarización técnica ni de que los paquetes H5P y SCORM reporten
correctamente. Y sin auditoría independiente.

**Tercero: la trazabilidad.** Entregamos el reporte de auditoría de cinco niveles.
Para un programa en proceso de acreditación, ese documento tiene valor propio.

**Lo que nunca se hace:** justificar el precio enumerando horas. Invita a
regatearlas. El precio se justifica por el resultado y por el riesgo evitado.

## 10. Disciplina de precios

Reglas no negociables:

1. **El precio piso no se cruza nunca.** Está calculado para cada recurso y cada
   cotización en `docs/05-cotizaciones.md`. Por debajo del 25 % de margen, la
   operación no cubre el riesgo de reproceso.
2. **Ante presión de precio, se reduce alcance, no precio.** Menos semanas, menos
   recursos por semana, menos meses de soporte. El precio unitario se mantiene.
3. **Los descuentos son por volumen o por acceso, nunca por negociación.** Cada
   descuento de la tabla comercial tiene una razón económica escrita.
4. **El descuento de primera implementación es irrepetible.** Se concede una sola
   vez por institución y se declara como tal en la propuesta.

### El error que este modelo corrige

El archivo `Estrategia_Precio_Curso_DesarrollosAP_2026.xlsx` (abril de 2026)
contiene un "Plan Básico" de $ 4.800.000 con margen efectivo de **−54 %**: vendía
por debajo del costo. El problema era de nomenclatura antes que de precio: ese
plan describía 3 guías y 70 horas, es decir un **piloto de un parcial**, no un
curso. Llamarlo "curso" instaló un ancla de precio 13 veces inferior a la
realidad.

En este modelo ese producto se llama **Piloto de un parcial** y su precio de lista
es de $ 22.717.750. La corrección de nomenclatura es, por sí sola, la decisión
comercial más rentable de este plan.

## 11. Hitos de los próximos 12 meses

| Trimestre | Objetivo | Indicador |
| --- | --- | --- |
| Q4 2026 | Cerrar Razonamiento Cuantitativo con la USC | Contrato firmado |
| Q4 2026 | Presentar el paquete de ciencias básicas | Propuesta radicada |
| Q1 2027 | Entregar RC y obtener carta de satisfacción | Curso en producción con estudiantes |
| Q1 2027 | Diagnóstico gratuito en dos instituciones nuevas | Dos informes entregados |
| Q2 2027 | Cerrar la segunda institución | Contrato firmado |
| Q2 2027 | Formar un segundo revisor científico | Revisor validando con doble ciego |
| Q3 2027 | Convertir tres cursos a mantenimiento recurrente | $ 1,1 M/mes recurrente |

**Métrica única de salud del negocio:** horas de socio facturadas al mes. Por
debajo de 60 hay un problema comercial. Por encima de 100 hay un problema de
capacidad que se resuelve formando al segundo revisor, no rechazando contratos.
