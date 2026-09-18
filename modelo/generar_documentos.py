"""Genera los documentos cuyas cifras salen del modelo.

Estos archivos NO se editan a mano: se regeneran con

    python3 modelo/generar_documentos.py

Así el catálogo de costos y las cotizaciones nunca se desincronizan de
parametros.json, catalogo_recursos.json y propuestas.json.
"""

from pathlib import Path

from cotizador import (
    Cotizador,
    Modelo,
    detalle_cotizacion,
    detalle_curso,
    detalle_recurso,
    money,
    tabla_catalogo,
    tabla_md,
)

RAIZ = Path(__file__).parent.parent
DOCS = RAIZ / "docs"
FECHA = "18 de septiembre de 2026"

AVISO = (
    "<!-- Generado por modelo/generar_documentos.py. No editar a mano: "
    "los cambios se pierden en la siguiente regeneración. "
    "Para cambiar cifras, editar modelo/parametros.json o modelo/catalogo_recursos.json. -->"
)


def encabezado(titulo: str, subtitulo: str) -> str:
    return f"{AVISO}\n\n# {titulo}\n\n*{subtitulo} · Desarrollos AP · {FECHA}*\n"


def doc_costos(m: Modelo) -> str:
    partes = [
        encabezado(
            "Modelo de costos por recurso",
            "Cuánto cuesta producir cada recurso educativo digital",
        ),
        """
## Para qué sirve este documento

Responde a una sola pregunta: **cuánto cuesta producir cada cosa que vendemos.**
De ahí salen tres números que gobiernan toda decisión comercial.

| Número | Qué significa | Para qué se usa |
| --- | --- | --- |
| **Costo total** | Lo que sale del bolsillo, con overhead | Nunca se muestra al cliente |
| **Precio piso** | El mínimo que deja el margen exigido | La línea que ningún descuento cruza |
| **Precio de lista** | El precio publicado | El ancla de toda negociación |

Las horas no son estimaciones de intuición: salen del procedimiento documentado en
las siete skills del modelo instruccional. Cada fase de cada recurso corresponde a
un paso real del proceso, con un responsable y un criterio de calidad verificable.
""",
        "## Parámetros del modelo\n",
        tabla_md(
            ["Rol", "Tarifa/hora", "Qué hace"],
            [
                [r["nombre"], money(r["tarifa_costo_hora"]), r["descripcion"]]
                for r in m.roles.values()
            ],
            alinear_der={1},
        ),
        f"""
- **Overhead operativo:** {m.p['overhead_pct'] * 100:.0f} %. {m.p['_nota_overhead']}
- **Multiplicador de precio de lista:** {m.p['multiplicador_precio_lista']}. {m.p['_nota_multiplicador']}
- **Piso de rentabilidad:** {m.p['piso_rentabilidad_pct'] * 100:.0f} % de margen. {m.p['_nota_piso']}
- **Factor de adecuación:** {m.p['factor_adecuacion'] * 100:.0f} %. {m.p['_nota_adecuacion']}

## La columna que sostiene el precio

La columna **criterio humano** es el argumento comercial central. Mide qué proporción
de las horas corresponde a trabajo que la IA no puede hacer: decidir la progresión
pedagógica, resolver cada ejemplo para verificar que está bien, validar que un
distractor es plausible, probar que el SCORM reporta la nota al libro de calificaciones.

En el catálogo completo, **dos de cada tres horas son criterio humano**. La IA acelera
el borrador y el código base; no reemplaza el juicio. Eso es exactamente lo que se
vende, y es la razón por la que el precio no se compara con el de un proveedor que
genera contenido sin revisarlo.

## Catálogo de costos y precios
""",
        tabla_catalogo(m),
        """
## Desglose recurso por recurso

Cada recurso muestra en qué se van las horas, quién las ejecuta y qué se verifica
antes de entregarlo. Esta es la evidencia que sostiene la cotización frente a una
oficina de compras que pregunte por qué cuesta lo que cuesta.
""",
    ]
    partes += [detalle_recurso(m, clave) + "\n" for clave in m.recursos]
    partes.append("## Plantillas de curso\n")
    partes += [detalle_curso(m, clave) + "\n" for clave in m.plantillas]
    return "\n".join(partes)


def doc_cotizaciones(cot: Cotizador) -> str:
    partes = [
        encabezado(
            "Cotizaciones vigentes",
            "Universidad Santiago de Cali y plantillas de cotización",
        ),
        """
## Cómo leer estas cotizaciones

Cada cotización trae dos bloques. El primero es lo que ve el cliente: componentes,
cantidades, precios y total. El segundo, marcado como **control interno**, es lo que
no se muestra: el costo real, el piso de rentabilidad y hasta dónde se puede negociar
sin destruir margen.

Regla operativa: **el descuento máximo admisible no se cruza nunca.** Si un cliente
exige más, la respuesta no es bajar el precio sino reducir el alcance.

## Planes comerciales
""",
        tabla_md(
            ["Plan", "Cursos", "Descuento", "Por qué existe"],
            [
                [p["nombre"], p["cursos"], f"{p['descuento'] * 100:.0f} %", p["razon"]]
                for p in cot.planes.values()
            ],
            alinear_der={2},
        ),
        "",
    ]
    partes += [detalle_cotizacion(cot, clave) + "\n" for clave in cot.propuestas]
    return "\n".join(partes)


def main() -> None:
    m = Modelo()
    cot = Cotizador(m)
    DOCS.mkdir(parents=True, exist_ok=True)

    salidas = {
        "01-modelo-costos.md": doc_costos(m),
        "05-cotizaciones.md": doc_cotizaciones(cot),
    }
    for nombre, contenido in salidas.items():
        (DOCS / nombre).write_text(contenido, encoding="utf-8")
        print(f"escrito docs/{nombre}")

    salidas_dir = RAIZ / "salidas"
    salidas_dir.mkdir(exist_ok=True)
    lineas = ["recurso;horas;horas_criterio;pct_criterio;costo_total;precio_piso;precio_lista"]
    for clave, recurso in m.recursos.items():
        c = m.costear_recurso(clave)
        lineas.append(
            f"{recurso['nombre']};{c.horas_totales:.1f};{c.horas_criterio:.1f};"
            f"{c.pct_criterio:.3f};{round(m.costo_total(c))};"
            f"{round(m.precio_piso(c))};{round(m.precio_lista(c))}"
        )
    (salidas_dir / "catalogo_costos.csv").write_text("\n".join(lineas), encoding="utf-8")
    print("escrito salidas/catalogo_costos.csv")


if __name__ == "__main__":
    main()
