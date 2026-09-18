# Protocolo de producción asistida por IA con revisión profesional

*Documento auditable por el cliente · Desarrollos AP · 2026*

---

## Propósito

Este documento declara cómo Desarrollos AP usa inteligencia artificial en la
producción de recursos educativos y qué garantías de revisión humana acompañan a
cada entregable.

Se entrega al cliente como anexo de toda propuesta. Su función es doble: responde
por anticipado a la pregunta sobre el uso de IA y convierte esa pregunta en el
argumento central de la propuesta.

---

## Principio rector

> **Ningún contenido generado por IA llega a un estudiante sin que un profesional
> lo haya verificado.**

La IA es una herramienta de producción, no una fuente de autoridad. Produce
borradores; no produce decisiones pedagógicas ni certeza disciplinar.

---

## Qué hace la IA y qué no

| La IA sí hace | La IA no hace |
| --- | --- |
| Borrador del desarrollo conceptual de una guía | Decidir qué conceptos van en qué semana |
| Código HTML y CSS base de un recurso | Decidir la progresión cognitiva del curso |
| Estructura de un banco de preguntas en GIFT | Certificar que un ítem tiene una única respuesta correcta |
| Esqueleto de un paquete SCORM | Definir el mapa de prerrequisitos que el diagnóstico evalúa |
| Redacción de enunciados y retroalimentación | Verificar que un taller es resoluble en el tiempo estimado |
| Variantes de ítems para ampliar un banco | Validar que los distractores son plausibles |
| Consolidación de informes y documentación | Firmar la auditoría de calidad |

La segunda columna es el servicio. La primera es cómo llegamos a poder prestarlo
en un plazo razonable.

---

## Las cuatro barreras de revisión

Todo recurso atraviesa cuatro filtros antes de publicarse. Ninguno es opcional y
ninguno lo ejecuta una máquina.

### Barrera 1 · Decisión pedagógica (antes de la IA)

Ocurre **antes** de cualquier generación. Un profesional define el objetivo de
aprendizaje con verbo observable, las competencias que se trabajan, las evidencias
verificables, la posición del recurso en la progresión y el contexto de
aplicación.

La IA recibe esa especificación. Nunca decide sobre ella.

**Evidencia:** documento de diseño curricular aprobado por la institución antes de
iniciar producción.

### Barrera 2 · Revisión científica

Verificación disciplinar de todo lo generado:

- Cada definición se contrasta con la bibliografía del programa.
- La notación se verifica símbolo por símbolo.
- **Cada ejemplo de cada guía se resuelve completo, a mano.**
- **Cada ítem de cada quiz se responde**, verificando que tenga exactamente una
  respuesta correcta.
- Cada distractor se evalúa: si es descartable por simple lógica, se reemplaza.
- Cada tolerancia numérica se recalcula.
- Cada taller se resuelve entero para confirmar que es resoluble, que los datos
  son consistentes y que el tiempo estimado es real.

**Evidencia:** solucionario de cada taller y de cada guía, entregado al docente.

**Esta es la barrera que la IA no puede cruzar y la razón por la que este servicio
tiene el precio que tiene.**

### Barrera 3 · Revisión didáctica

Verificación pedagógica de lo ya validado científicamente:

- La progresión va de lo concreto a lo abstracto.
- No hay saltos de complejidad entre semanas consecutivas.
- Los contextos son pertinentes para el perfil profesional del programa.
- La retroalimentación nombra el error específico, no dice «incorrecto».
- La actividad de refuerzo no duplica el quiz: es práctica, no evaluación.
- La rúbrica tiene descriptores observables y es comprensible para el estudiante.

**Evidencia:** checklist de los niveles 2 y 3 de la auditoría de calidad.

### Barrera 4 · Validación técnica

Prueba real en Moodle, no revisión de escritorio:

- Los archivos GIFT importan sin error de sintaxis.
- Los paquetes H5P tienen `h5p.json` en raíz y sus librerías existen en el Moodle
  destino.
- Los paquetes SCORM tienen `imsmanifest.xml` válido y reportan
  `lesson_status`, `score.raw` y `suspend_data`.
- El HTML valida en W3C, carga sin errores de consola y responde en móvil.
- **Cada recurso se recorre completo con usuario de prueba y se verifica que la
  calificación llegue al libro de calificaciones.**

**Evidencia:** checklist de los niveles 1, 4 y 5 de la auditoría de calidad.

---

## La proporción declarada

Sobre el catálogo completo de recursos, la distribución de horas es:

| Tipo de trabajo | Proporción | Automatizable |
| --- | ---: | --- |
| Decisión pedagógica | 18,3 % | No |
| Revisión científica | 26,6 % | No |
| Revisión didáctica | 11,6 % | No |
| Validación y QA | 9,6 % | No |
| **Total criterio humano** | **66,1 %** | **No** |
| Generación asistida por IA | 9,6 % | Sí |
| Producción técnica | 24,3 % | Parcialmente |

*Distribución sobre un curso nuevo de 16 semanas (429 horas). La proporción de
criterio humano se mantiene en 66 % en todas las plantillas de curso.*

Estas proporciones están desglosadas recurso por recurso en
`docs/01-modelo-costos.md` y son verificables por el cliente.

Ejemplos concretos:

| Recurso | Horas | Criterio humano |
| --- | ---: | ---: |
| Diseño curricular y arquitectura del curso | 10,0 | 90 % |
| Sesión de capacitación docente | 3,5 | 86 % |
| Auditoría de calidad final | 6,0 | 83 % |
| Guía de aprendizaje en HTML | 5,7 | 77 % |
| Quiz evaluativo Moodle | 4,0 | 75 % |
| Taller de alta demanda con rúbrica | 3,8 | 74 % |

---

## Trazabilidad y propiedad

- **Propiedad intelectual.** Todo el material producido es propiedad de la
  institución contratante, sin restricción de uso, modificación o reproducción.
- **Fuentes.** Las guías citan la bibliografía obligatoria del programa. No se
  publican afirmaciones disciplinares sin respaldo en fuente verificable.
- **Material de terceros.** No se incorpora contenido con licencia restrictiva.
  Los videos de terceros enlazados se sustituyen por producción propia, porque
  dependen de canales que pueden desaparecer y no registran calificación.
- **Datos de estudiantes.** No se procesan datos personales de estudiantes durante
  la producción. Los reportes analíticos se elaboran sobre datos agregados y
  anonimizados que entrega la institución.
- **Confidencialidad.** El material de la institución no se usa para entrenar
  modelos ni se comparte con terceros.

---

## Errores conocidos del contenido generado con IA

Declaramos los fallos que buscamos de forma sistemática, porque conocerlos es
parte de la competencia profesional que se contrata:

| Error frecuente | Cómo se detecta |
| --- | --- |
| Ítems con dos respuestas correctas | Se responde cada ítem verificando la unicidad de la clave |
| Distractores descartables por lógica elemental | Revisión de plausibilidad de cada opción |
| Tolerancias numéricas mal calculadas | Recálculo de cada ítem numérico |
| Ejemplos con datos internamente inconsistentes | Resolución completa de cada ejemplo |
| Retroalimentación genérica que no orienta | Reescritura nombrando el error específico |
| Referencias bibliográficas inexistentes | Verificación de cada fuente citada |
| Notación mezclada entre convenciones | Revisión símbolo por símbolo |
| Progresión con saltos de complejidad | Checklist de coherencia entre semanas |
| H5P mal empaquetado que no importa | Validación de estructura y prueba de importación |
| SCORM que no reporta al libro de calificaciones | Recorrido con usuario de prueba |

---

## Compromiso de corrección

Si durante los meses de soporte contratados se detecta un error de contenido en
cualquier recurso entregado, se corrige **sin costo y sin discusión de alcance**,
dentro de los cinco días hábiles siguientes al reporte.

Este compromiso es posible precisamente por las cuatro barreras: son las que
mantienen la tasa de error lo bastante baja como para que la garantía no sea un
riesgo económico.

---

## Cómo auditar este protocolo

La institución puede verificar lo declarado, en cualquier momento del proyecto:

1. Pedir el solucionario de cualquier taller entregado.
2. Pedir el registro de resolución de cualquier banco de ítems.
3. Pedir el checklist de auditoría de cualquier recurso.
4. Solicitar una sesión de revisión conjunta de un recurso a elección.
5. Revisar el documento de diseño curricular aprobado antes de la producción.

Ninguna de estas peticiones tiene costo ni requiere aviso previo.
