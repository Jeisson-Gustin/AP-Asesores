"""Pruebas del motor de costeo y cotización.

Ejecutar:  python3 modelo/test_cotizador.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cotizador import FASES_CRITERIO, Cotizador, Costeo, Modelo  # noqa: E402

fallos: list[str] = []


def check(condicion: bool, descripcion: str) -> None:
    if condicion:
        print(f"  ok   {descripcion}")
    else:
        print(f"  FALLA {descripcion}")
        fallos.append(descripcion)


def main() -> None:
    m = Modelo()
    cot = Cotizador(m)

    print("\nIntegridad del catálogo")
    for clave, recurso in m.recursos.items():
        for campo in ("nombre", "categoria", "descripcion", "entregable", "fases", "criterios_calidad"):
            check(campo in recurso, f"{clave} tiene '{campo}'")
        for fase in recurso["fases"]:
            check(fase["fase"] in m.p["fases"], f"{clave}: fase '{fase['fase']}' está definida")
            check(fase["rol"] in m.roles, f"{clave}: rol '{fase['rol']}' está definido")
            check(fase["horas"] > 0, f"{clave}: fase '{fase['fase']}' tiene horas positivas")

    print("\nCoherencia aritmética del costeo")
    for clave in m.recursos:
        c = m.costear_recurso(clave)
        suma_fases = sum(f["horas"] for f in m.recursos[clave]["fases"])
        check(abs(c.horas_totales - suma_fases) < 1e-9, f"{clave}: las horas suman")
        check(
            abs(c.horas_criterio + c.horas_asistidas - c.horas_totales) < 1e-9,
            f"{clave}: criterio + asistidas = total",
        )
        check(
            abs(sum(c.costo_por_rol.values()) - c.costo_directo) < 1e-6,
            f"{clave}: el costo por rol suma el costo directo",
        )
        check(m.costo_total(c) > c.costo_directo, f"{clave}: el overhead incrementa el costo")
        check(m.precio_lista(c) > m.precio_piso(c), f"{clave}: el precio de lista supera el piso")

    print("\nRelación entre precio, piso y margen")
    for clave in m.recursos:
        c = m.costear_recurso(clave)
        margen_piso = m.margen(m.precio_piso(c), c)
        check(
            abs(margen_piso - m.p["piso_rentabilidad_pct"]) < 1e-9,
            f"{clave}: vender al piso deja exactamente el margen mínimo",
        )

    print("\nÁlgebra de Costeo")
    a = m.costear_recurso("guia_html")
    doble = a.escalar(2)
    check(abs(doble.horas_totales - a.horas_totales * 2) < 1e-9, "escalar duplica las horas")
    check(abs(doble.costo_directo - a.costo_directo * 2) < 1e-6, "escalar duplica el costo")
    suma = a + a
    check(abs(suma.horas_totales - doble.horas_totales) < 1e-9, "a + a equivale a escalar por 2")
    check(abs(suma.pct_criterio - a.pct_criterio) < 1e-9, "sumar no altera la proporción de criterio")
    check(Costeo().pct_criterio == 0.0, "un costeo vacío no divide por cero")

    print("\nFactor de adecuación")
    comp_nueva = m.costear_composicion({"guia_html": 10})
    comp_adec = m.costear_composicion({}, {"guia_html": 10})
    check(
        abs(comp_adec.horas_totales - comp_nueva.horas_totales * m.p["factor_adecuacion"]) < 1e-9,
        "adecuar 10 guías cuesta el 40 % de producirlas",
    )

    print("\nPlantillas de curso")
    for clave, plantilla in m.plantillas.items():
        c = m.costear_plantilla(clave)
        check(c.horas_totales > 0, f"{clave}: tiene horas")
        check(
            all(r in m.recursos for r in plantilla["composicion"]),
            f"{clave}: todos sus componentes existen en el catálogo",
        )
        check(0.5 < c.pct_criterio < 0.85, f"{clave}: el criterio humano domina sin ser todo")

    horas_13 = m.costear_plantilla("curso_nuevo_13").horas_totales
    horas_16 = m.costear_plantilla("curso_nuevo_16").horas_totales
    horas_piloto = m.costear_plantilla("piloto_parcial").horas_totales
    check(horas_piloto < horas_13 < horas_16, "las plantillas escalan con el número de semanas")

    print("\nCotizaciones")
    for clave in cot.propuestas:
        c = cot.cotizar(clave)
        check(c["subtotal"] > 0, f"{clave}: subtotal positivo")
        check(
            abs(c["total"] - (c["subtotal"] - c["descuento"])) < 1e-6,
            f"{clave}: total = subtotal - descuento",
        )
        check(c["sobre_piso"], f"{clave}: el precio final respeta el piso de rentabilidad")
        check(
            c["margen"] >= m.p["piso_rentabilidad_pct"],
            f"{clave}: margen ({c['margen'] * 100:.1f} %) no baja del mínimo",
        )
        check(
            c["valor_si_todo_nuevo"] >= c["subtotal"],
            f"{clave}: producir todo desde cero nunca cuesta menos",
        )
        aplicado = c["plan"]["descuento"]
        check(
            aplicado <= cot.descuento_maximo(clave) + 1e-9,
            f"{clave}: el descuento aplicado no supera el máximo admisible",
        )

    print("\nPropuesta combinada")
    paquete = cot.cotizar("usc_paquete_ciencias_basicas")
    rc = cot.cotizar("usc_razonamiento_cuantitativo")
    qg = cot.cotizar("usc_quimica_general")
    check(
        paquete["subtotal"] < rc["subtotal"] + qg["subtotal"],
        "el paquete no duplica el trabajo compartido",
    )
    check(
        paquete["total"] < rc["total"] + qg["total"],
        "contratar los dos cursos juntos cuesta menos que por separado",
    )

    print("\nCoherencia con la propuesta ya presentada a la USC")
    comprometido = 25_730_000  # propuesta del 17 de septiembre de 2026, sin IVA
    desvio = abs(rc["total"] - comprometido) / comprometido
    check(desvio < 0.01, f"Razonamiento Cuantitativo respeta el precio comprometido (desvío {desvio * 100:.2f} %)")

    print("\nFases de criterio")
    check(
        FASES_CRITERIO <= set(m.p["fases"]),
        "las fases de criterio existen en los parámetros",
    )
    for nombre in FASES_CRITERIO:
        check(
            not m.p["fases"][nombre]["automatizable"],
            f"la fase '{nombre}' está marcada como no automatizable",
        )

    print(f"\n{'FALLARON ' + str(len(fallos)) if fallos else 'Todas las pruebas pasaron'}")
    if fallos:
        for f in fallos:
            print(f"  - {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
