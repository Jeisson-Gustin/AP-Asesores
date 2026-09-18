# Argumentario de ventas

*Cómo sostener el precio y responder a las objeciones · Desarrollos AP · 2026*

---

## Regla de oro

**Nunca justificar el precio enumerando horas.**

Quien justifica con horas invita a que le regateen las horas. El precio se
justifica con dos cosas: el resultado que produce y el riesgo que evita.

Las horas existen, están documentadas en `docs/01-modelo-costos.md` y se muestran
si un comité de compras las exige para un proceso formal. Pero no son el
argumento de apertura. Son el respaldo.

---

## 1. El argumento principal: el costo de no hacerlo

Un curso de ciencias básicas de primer semestre con alta reprobación no es un
problema académico aislado. Es una fuga de matrícula.

El razonamiento que se presenta a un decano o a un vicerrector:

> Cada estudiante que reprueba tiene una probabilidad alta de retirarse. Cada
> retiro es matrícula que la universidad deja de recibir en los semestres
> siguientes. La pregunta no es cuánto cuesta rediseñar el curso: es cuánto
> cuesta no rediseñarlo.

### Cómo usar el modelo de retorno

El modelo está en `modelo/roi.py` y se ejecuta con los parámetros de cada
institución:

```
python3 modelo/roi.py --estudiantes 400 --matricula 4500000 --inversion 25719336
```

**Advertencia operativa.** El modelo con supuestos intermedios arroja retornos de
15 veces la inversión. **No presentar ese número.** Un retorno de 15x suena a
folleto y destruye credibilidad en la primera pregunta escéptica.

**Presentar siempre el escenario de piso:**

> Con los supuestos más conservadores —2 puntos de reducción en la reprobación y
> asumiendo que solo 1 de cada 5 estudiantes que reprueba termina retirándose— el
> curso genera $ 34.000.000 anuales en matrícula preservada y se paga en nueve
> meses.

Ese número es defendible, resiste el escrutinio y sigue siendo contundente.

### El número que cierra

> **La inversión se recupera reteniendo 3 estudiantes** de una cohorte de 400.
> Menos del 1 % del curso.

Es el dato más poderoso del argumentario porque convierte una cifra grande y
abstracta en algo que el interlocutor puede verificar con su propia intuición.

### Antes de presentar cualquier cifra

Pedir a la institución sus datos reales: matriculados por periodo, histórico de
notas de los últimos cuatro semestres, tarifa de matrícula vigente y cruce de
reprobación con retiro efectivo. Presentar un modelo de retorno con cifras
inventadas es la forma más rápida de perder un contrato.

La petición de datos, además, es en sí misma una técnica de venta: convierte la
conversación en un ejercicio conjunto y compromete al interlocutor con el
resultado.

---

## 2. El argumento de la trazabilidad

Para una universidad en proceso de acreditación o renovación de registro
calificado, la pregunta incómoda es: *¿cómo demuestran ustedes la calidad de su
oferta virtual?*

Entregamos un **reporte de auditoría de cinco niveles**: estructural, pedagógico,
de coherencia interna, técnico y de comunicación. Con checklist punto por punto,
hallazgos críticos, hallazgos menores y recomendaciones priorizadas.

Ese documento tiene valor propio, independiente del curso. Es evidencia
archivable para el proceso de acreditación.

**Cómo se presenta:**

> Además del curso, ustedes reciben el documento que demuestra ante pares
> académicos cómo se garantizó su calidad. Eso no lo entrega un proveedor de
> contenidos.

---

## 3. El argumento del uso de IA

Se declara abiertamente, siempre, antes de que lo pregunten. Declararlo primero
convierte una objeción potencial en una ventaja.

**El guion:**

> Usamos inteligencia artificial para producir el borrador de las guías, el
> código HTML base y la estructura de los bancos de preguntas. Lo decimos de
> entrada porque es nuestra ventaja, no nuestro atajo.
>
> Lo que la IA produce no llega nunca a un estudiante sin revisión. Cada ejemplo
> de cada guía se resuelve a mano. Cada ítem de cada quiz se responde y se
> verifica que tenga una única respuesta correcta y distractores plausibles. Cada
> paquete H5P y SCORM se prueba en Moodle comprobando que registre la nota.
>
> El 66 % de nuestras horas son revisión humana, y esa proporción está
> documentada recurso por recurso. Ustedes pueden auditarla.
>
> La IA no nos hace más baratos. Nos permite dedicar dos de cada tres horas a lo
> que determina si un estudiante aprende, en lugar de gastarlas maquetando HTML
> y escribiendo enunciados desde una hoja en blanco.

**Por qué funciona:** el interlocutor ya sabe que existe la IA y probablemente ya
recibió propuestas de proveedores que la usan sin decirlo. Declararlo con la
proporción exacta de revisión humana nos separa de dos competidores a la vez: del
proveedor tradicional caro y lento, y del proveedor que genera contenido sin
control de calidad.

---

## 4. Manejo de objeciones

### «Es muy costoso»

Primero, diagnosticar contra qué lo comparan. La respuesta cambia por completo.

**Si lo comparan con un proveedor de contenidos:**

> No estamos vendiendo lo mismo. Ellos entregan archivos; nosotros entregamos el
> aula funcionando, auditada y con el docente capacitado. Si al final del proceso
> alguien de su equipo tiene que montar los recursos en Moodle, cuadrar el libro
> de calificaciones y verificar que los H5P reporten nota, ese costo no
> desapareció: se trasladó a su nómina.

**Si lo comparan con hacerlo internamente:**

> Un curso de 16 semanas exige 429 horas de producción. Esas horas existen se las
> paguen a nosotros o se las paguen a sus docentes en descarga académica. La
> diferencia es que nosotros las entregamos estandarizadas, probadas en Moodle y
> con auditoría independiente. Y sus docentes siguen dando clase.

**Si es una objeción de presupuesto genuina:**

> Entiendo la restricción. En lugar de bajar el precio, ajustemos el alcance:
> podemos empezar con un parcial completo, que ustedes evalúan con estudiantes
> reales, y decidir sobre el resto con evidencia en la mano.

**Lo que nunca se hace:** bajar el precio sin quitar alcance. Enseña al cliente
que el precio inicial estaba inflado y compromete todas las negociaciones
futuras.

### «Nosotros ya tenemos el material»

Esta objeción es en realidad una oportunidad: significa que hay un aula que
podemos diagnosticar gratis.

> Perfecto, eso abarata el proyecto de manera sustancial. Adecuar un recurso que
> ustedes ya tienen cuesta el 40 % de producirlo desde cero. Déjenme hacer el
> diagnóstico del aula sin costo y les digo exactamente qué se conserva, qué se
> estandariza y qué falta.

En el caso de la Universidad Santiago de Cali, el inventario mostró 99 recursos
aprovechables de 107, lo que significó un ahorro de $ 38.442.426 frente a
producir el curso desde cero. **Ese dato vende solo.**

### «¿Por qué no lo hace nuestro propio equipo con IA?»

La objeción más frecuente y la más fácil de responder bien.

> Pueden hacerlo, y varias universidades lo están intentando. El problema no es
> generar el contenido: eso hoy lo hace cualquiera en una tarde. El problema es
> el filtro.
>
> Un banco de 60 preguntas generado con IA trae, típicamente, ítems con dos
> respuestas correctas, distractores descartables por simple lógica y tolerancias
> numéricas mal puestas. Detectar eso exige resolver los 60 ítems uno por uno,
> con criterio disciplinar. Ese es el trabajo, y es el que no se puede saltar.
>
> Pregúntenle a su equipo quién va a resolver los 60 ítems, quién va a verificar
> que el SCORM reporte la nota al libro de calificaciones y quién va a firmar la
> auditoría de calidad. Si tienen esa persona y le pueden liberar 429 horas, no
> nos necesitan.

### «Necesitamos verlo antes de comprometernos»

> Tenemos dos formas. El diagnóstico de su aula actual, sin costo, que les
> entrega un informe con hallazgos concretos aunque no contraten. O el piloto de
> un parcial: cuatro semanas completas y funcionando, que ustedes evalúan con
> estudiantes reales antes de decidir sobre el curso entero.

### «El proceso de compra es largo»

> Lo sabemos y por eso el piloto de parcial está dimensionado para caber en
> contratación directa o mínima cuantía en la mayoría de instituciones. Empezamos
> por ahí mientras avanza el proceso mayor.

### «¿Qué pasa si el docente no quiere usarlo?»

La objeción que más contratos hunde en la fase de implementación.

> Es el riesgo real del proyecto y por eso la capacitación docente está incluida,
> no es un adicional. Además, el diseño curricular se construye con el docente
> titular, no contra él: él aprueba la arquitectura antes de que produzcamos nada.
> El curso termina siendo suyo, con nuestra producción detrás.

---

## 5. Secuencia de una reunión de venta

1. **Preguntar primero.** ¿Cuál es la tasa de reprobación del curso? ¿Cuántos
   estudiantes por cohorte? ¿Qué pasó la última vez que intentaron virtualizarlo?
   Escuchar más que hablar en los primeros veinte minutos.
2. **Mostrar el diagnóstico.** Si ya se hizo, es el momento. Los hallazgos
   concretos sobre su propia aula valen más que cualquier presentación.
3. **Nombrar el problema en sus términos.** Deserción, acreditación, carga
   docente: el que más le duela al interlocutor.
4. **Presentar el modelo de producción,** declarando el uso de IA y la proporción
   de revisión humana.
5. **Mostrar el retorno con el escenario conservador.**
6. **Presentar el precio con el ancla correcta:** primero el valor de producir
   todo desde cero, después el ahorro por aprovechar lo existente, después el
   precio final.
7. **Cerrar con una decisión pequeña:** autorizar el diagnóstico, agendar la
   reunión con el docente titular, pedir los datos de reprobación. Nunca pedir la
   firma del contrato como siguiente paso inmediato.

---

## 6. El orden de presentación del precio

El orden importa más que el número. Siempre el mismo:

1. **Ancla alta.** «Producir estos 107 recursos desde cero cuesta $ 77.470.250.»
2. **Ahorro.** «Aprovechando lo que ustedes ya tienen, el trabajo baja a
   $ 39.027.824.»
3. **Descuento nombrado.** «Como primera implementación con la universidad, se
   aplica un descuento de acceso del 34 %.»
4. **Precio final.** «La inversión es de $ 25.719.336.»
5. **Retorno inmediatamente después.** «Que se recupera reteniendo tres
   estudiantes de una cohorte de 400.»

Nunca decir el precio final aislado. Un número sin contexto solo puede parecer
caro.

---

## 7. Frases que no se usan

| No decir | Decir |
| --- | --- |
| «Le hago un descuento» | «Ajustamos el alcance a su presupuesto» |
| «La IA lo hace rápido» | «La IA nos libera horas para revisar más» |
| «Son 429 horas de trabajo» | «Es un curso de 16 semanas, auditado y funcionando» |
| «Es barato comparado con otros» | «Es lo que cuesta hacerlo bien» |
| «Podemos entregarlo en dos semanas» | «El diseño curricular se aprueba antes de producir» |
| «Confíen en nosotros» | «Les hago el diagnóstico sin costo y ustedes deciden» |

---

## 8. Señales de un cliente que no conviene

Reconocerlas temprano ahorra meses:

- Quiere el curso completo en menos de seis semanas.
- No tiene parcelación oficial ni quiere construirla.
- El docente titular no participa en ninguna reunión.
- Compara exclusivamente por precio y pide cotizaciones de tres proveedores sin
  diferenciar alcance.
- Pide bajar el precio más del descuento máximo admisible sin reducir alcance.
- No autoriza acceso al Moodle de pruebas.

Ante tres o más señales, ofrecer únicamente el piloto de parcial. Si insisten en
el curso completo bajo esas condiciones, declinar: el reproceso destruye el
margen y la relación termina mal de todos modos.
