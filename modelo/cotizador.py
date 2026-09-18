"""Motor de costeo y cotización de Desarrollos AP.

Separa dos modelos que no deben confundirse:

  - Modelo de costo interno: lo que cuesta producir. Define el piso por debajo
    del cual una venta destruye valor.
  - Modelo de precio de venta: lo que se cobra. Se sostiene en el valor que el
    curso genera a la institución, no en las horas trabajadas.

Uso:
    python3 cotizador.py                 # resumen del catálogo y de las plantillas
    python3 cotizador.py --recurso guia_html
    python3 cotizador.py --curso curso_nuevo_13
    python3 cotizador.py --csv salidas/
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

BASE = Path(__file__).parent

# Fases cuyo trabajo no puede delegarse a la IA: son criterio profesional.
FASES_CRITERIO = {"diseno", "revision_cientifica", "revision_didactica", "qa"}


def cargar(nombre: str) -> dict:
    return json.loads((BASE / nombre).read_text(encoding="utf-8"))


@dataclass
class Costeo:
    """Resultado del costeo de un recurso o de un conjunto de recursos."""

    horas_totales: float = 0.0
    horas_criterio: float = 0.0
    horas_asistidas: float = 0.0
    costo_directo: float = 0.0
    horas_por_rol: dict[str, float] = field(default_factory=dict)
    costo_por_rol: dict[str, float] = field(default_factory=dict)
    horas_por_fase: dict[str, float] = field(default_factory=dict)

    def __add__(self, otro: "Costeo") -> "Costeo":
        nuevo = Costeo(
            horas_totales=self.horas_totales + otro.horas_totales,
            horas_criterio=self.horas_criterio + otro.horas_criterio,
            horas_asistidas=self.horas_asistidas + otro.horas_asistidas,
            costo_directo=self.costo_directo + otro.costo_directo,
        )
        for attr in ("horas_por_rol", "costo_por_rol", "horas_por_fase"):
            acumulado = dict(getattr(self, attr))
            for clave, valor in getattr(otro, attr).items():
                acumulado[clave] = acumulado.get(clave, 0.0) + valor
            setattr(nuevo, attr, acumulado)
        return nuevo

    def escalar(self, factor: float) -> "Costeo":
        return Costeo(
            horas_totales=self.horas_totales * factor,
            horas_criterio=self.horas_criterio * factor,
            horas_asistidas=self.horas_asistidas * factor,
            costo_directo=self.costo_directo * factor,
            horas_por_rol={k: v * factor for k, v in self.horas_por_rol.items()},
            costo_por_rol={k: v * factor for k, v in self.costo_por_rol.items()},
            horas_por_fase={k: v * factor for k, v in self.horas_por_fase.items()},
        )

    @property
    def pct_criterio(self) -> float:
        """Proporción de horas que son criterio humano y no producción asistida."""
        return self.horas_criterio / self.horas_totales if self.horas_totales else 0.0


class Modelo:
    def __init__(self) -> None:
        self.p = cargar("parametros.json")
        self.c = cargar("catalogo_recursos.json")
        self.recursos = self.c["recursos"]
        self.plantillas = self.c["plantillas_curso"]
        self.roles = self.p["roles"]

    # ---------- Modelo de costo interno ----------

    def costear_recurso(self, clave: str) -> Costeo:
        recurso = self.recursos[clave]
        r = Costeo()
        for fase in recurso["fases"]:
            horas, rol, nombre_fase = fase["horas"], fase["rol"], fase["fase"]
            costo = horas * self.roles[rol]["tarifa_costo_hora"]
            r.horas_totales += horas
            r.costo_directo += costo
            if nombre_fase in FASES_CRITERIO:
                r.horas_criterio += horas
            else:
                r.horas_asistidas += horas
            r.horas_por_rol[rol] = r.horas_por_rol.get(rol, 0.0) + horas
            r.costo_por_rol[rol] = r.costo_por_rol.get(rol, 0.0) + costo
            r.horas_por_fase[nombre_fase] = r.horas_por_fase.get(nombre_fase, 0.0) + horas
        return r

    def costo_total(self, costeo: Costeo) -> float:
        """Costo directo más overhead operativo."""
        return costeo.costo_directo * (1 + self.p["overhead_pct"])

    # ---------- Modelo de precio de venta ----------

    def precio_lista(self, costeo: Costeo) -> float:
        return self.costo_total(costeo) * self.p["multiplicador_precio_lista"]

    def precio_piso(self, costeo: Costeo) -> float:
        """Precio mínimo que todavía deja el margen de rentabilidad exigido.

        margen = (precio - costo) / precio  =>  precio = costo / (1 - margen)
        """
        return self.costo_total(costeo) / (1 - self.p["piso_rentabilidad_pct"])

    def margen(self, precio: float, costeo: Costeo) -> float:
        return (precio - self.costo_total(costeo)) / precio if precio else 0.0

    # ---------- Composición de cursos ----------

    def costear_composicion(
        self, composicion: dict[str, float], adecuacion: dict[str, float] | None = None
    ) -> Costeo:
        """Costea un conjunto de recursos.

        `composicion` son unidades de producción nueva. `adecuacion` son unidades
        de recursos preexistentes, que se cobran al factor de adecuación.
        """
        total = Costeo()
        for clave, cantidad in composicion.items():
            if cantidad:
                total = total + self.costear_recurso(clave).escalar(cantidad)
        for clave, cantidad in (adecuacion or {}).items():
            if cantidad:
                factor = cantidad * self.p["factor_adecuacion"]
                total = total + self.costear_recurso(clave).escalar(factor)
        return total

    def costear_plantilla(self, clave: str) -> Costeo:
        return self.costear_composicion(self.plantillas[clave]["composicion"])


@dataclass
class LineaCotizacion:
    nombre: str
    cantidad_nueva: float
    cantidad_adecuacion: float
    precio_unitario: float
    precio_adecuacion: float

    @property
    def subtotal(self) -> float:
        return (
            self.cantidad_nueva * self.precio_unitario
            + self.cantidad_adecuacion * self.precio_adecuacion
        )


class Cotizador:
    """Construye cotizaciones a partir de propuestas.json, validando el piso."""

    def __init__(self, modelo: Modelo | None = None) -> None:
        self.m = modelo or Modelo()
        datos = cargar("propuestas.json")
        self.planes = datos["planes_comerciales"]
        self.propuestas = datos["propuestas"]

    def _resolver(self, clave: str) -> tuple[dict[str, float], dict[str, float]]:
        """Devuelve (nuevos, adecuacion) resolviendo propuestas combinadas."""
        p = self.propuestas[clave]
        if "combina" not in p:
            return dict(p.get("nuevos", {})), dict(p.get("adecuacion", {}))

        nuevos: dict[str, float] = {}
        adecuacion: dict[str, float] = {}
        for sub in p["combina"]:
            sub_nuevos, sub_adec = self._resolver(sub)
            for origen, destino in ((sub_nuevos, nuevos), (sub_adec, adecuacion)):
                for k, v in origen.items():
                    destino[k] = destino.get(k, 0.0) + v
        # El trabajo que no se duplica al contratar juntos se descuenta una vez.
        for k, v in p.get("ahorro_compartido", {}).items():
            if k in nuevos:
                nuevos[k] = max(0.0, nuevos[k] - v)
        return nuevos, adecuacion

    def cotizar(self, clave: str) -> dict:
        p = self.propuestas[clave]
        nuevos, adecuacion = self._resolver(clave)
        factor = self.m.p["factor_adecuacion"]

        lineas: list[LineaCotizacion] = []
        for rec in self.m.recursos:
            cn, ca = nuevos.get(rec, 0.0), adecuacion.get(rec, 0.0)
            if not cn and not ca:
                continue
            unitario = self.m.precio_lista(self.m.costear_recurso(rec))
            lineas.append(
                LineaCotizacion(
                    nombre=self.m.recursos[rec]["nombre"],
                    cantidad_nueva=cn,
                    cantidad_adecuacion=ca,
                    precio_unitario=unitario,
                    precio_adecuacion=unitario * factor,
                )
            )

        costeo = self.m.costear_composicion(nuevos, adecuacion)
        subtotal = sum(l.subtotal for l in lineas)
        plan = self.planes[p["plan"]]
        descuento = subtotal * plan["descuento"]
        total = subtotal - descuento
        piso = self.m.precio_piso(costeo)

        return {
            "propuesta": p,
            "plan": plan,
            "lineas": lineas,
            "costeo": costeo,
            "subtotal": subtotal,
            "descuento": descuento,
            "total": total,
            "costo_total": self.m.costo_total(costeo),
            "piso": piso,
            "margen": self.m.margen(total, costeo),
            "sobre_piso": total >= piso,
            "valor_si_todo_nuevo": sum(
                (l.cantidad_nueva + l.cantidad_adecuacion) * l.precio_unitario for l in lineas
            ),
        }

    def descuento_maximo(self, clave: str) -> float:
        """Mayor descuento que todavía respeta el piso de rentabilidad."""
        c = self.cotizar(clave)
        return max(0.0, 1 - c["piso"] / c["subtotal"]) if c["subtotal"] else 0.0


# ---------- Presentación ----------


def money(v: float) -> str:
    """Formato colombiano: $ 1.234.567"""
    return "$ " + f"{round(v):,}".replace(",", ".")


def tabla_md(encabezados: list[str], filas: list[list[str]], alinear_der: set[int] | None = None) -> str:
    alinear_der = alinear_der or set()
    sep = ["---:" if i in alinear_der else "---" for i in range(len(encabezados))]
    out = ["| " + " | ".join(encabezados) + " |", "| " + " | ".join(sep) + " |"]
    out += ["| " + " | ".join(f) + " |" for f in filas]
    return "\n".join(out)


def tabla_catalogo(m: Modelo) -> str:
    filas = []
    for clave, recurso in m.recursos.items():
        c = m.costear_recurso(clave)
        filas.append([
            recurso["nombre"],
            f"{c.horas_totales:.1f}",
            f"{c.pct_criterio * 100:.0f} %",
            money(m.costo_total(c)),
            money(m.precio_piso(c)),
            money(m.precio_lista(c)),
        ])
    return tabla_md(
        ["Recurso", "Horas", "Criterio humano", "Costo total", "Precio piso", "Precio lista"],
        filas,
        alinear_der={1, 2, 3, 4, 5},
    )


def detalle_recurso(m: Modelo, clave: str) -> str:
    recurso = m.recursos[clave]
    c = m.costear_recurso(clave)
    fases_meta = m.p["fases"]
    filas = []
    for fase in recurso["fases"]:
        marca = "—" if fases_meta[fase["fase"]]["automatizable"] else "sí"
        filas.append([
            fases_meta[fase["fase"]]["nombre"],
            m.roles[fase["rol"]]["nombre"],
            f"{fase['horas']:.1f}",
            marca,
            money(fase["horas"] * m.roles[fase["rol"]]["tarifa_costo_hora"]),
        ])
    out = [
        f"### {recurso['nombre']}",
        "",
        recurso["descripcion"],
        "",
        f"**Entregable.** {recurso['entregable']}",
        "",
        tabla_md(
            ["Fase", "Rol", "Horas", "¿Criterio humano?", "Costo"],
            filas,
            alinear_der={2, 4},
        ),
        "",
        f"**Total: {c.horas_totales:.1f} horas**, de las cuales "
        f"{c.horas_criterio:.1f} ({c.pct_criterio * 100:.0f} %) son criterio humano no automatizable.",
        "",
        f"- Costo directo: {money(c.costo_directo)}",
        f"- Costo total con overhead ({m.p['overhead_pct'] * 100:.0f} %): {money(m.costo_total(c))}",
        f"- Precio piso (margen {m.p['piso_rentabilidad_pct'] * 100:.0f} %): {money(m.precio_piso(c))}",
        f"- **Precio de lista: {money(m.precio_lista(c))}**",
        f"- Adecuación de un recurso existente ({m.p['factor_adecuacion'] * 100:.0f} %): "
        f"{money(m.precio_lista(c) * m.p['factor_adecuacion'])}",
        "",
        "**Criterios de calidad verificados antes de entregar:**",
        "",
    ]
    out += [f"- {crit}" for crit in recurso["criterios_calidad"]]
    if recurso.get("nota"):
        out += ["", f"> {recurso['nota']}"]
    return "\n".join(out)


def detalle_curso(m: Modelo, clave: str) -> str:
    plantilla = m.plantillas[clave]
    filas = []
    for rec_clave, cantidad in plantilla["composicion"].items():
        c = m.costear_recurso(rec_clave)
        filas.append([
            m.recursos[rec_clave]["nombre"],
            str(cantidad),
            f"{c.horas_totales:.1f}",
            f"{c.horas_totales * cantidad:.1f}",
            money(m.precio_lista(c)),
            money(m.precio_lista(c) * cantidad),
        ])
    total = m.costear_plantilla(clave)
    filas.append([
        "**Total**",
        f"**{sum(plantilla['composicion'].values())}**",
        "",
        f"**{total.horas_totales:.1f}**",
        "",
        f"**{money(m.precio_lista(total))}**",
    ])
    return "\n".join([
        f"### {plantilla['nombre']}",
        "",
        plantilla["descripcion"],
        "",
        tabla_md(
            ["Componente", "Cant.", "Horas c/u", "Horas", "Precio unit.", "Subtotal"],
            filas,
            alinear_der={1, 2, 3, 4, 5},
        ),
        "",
        f"- Horas totales: **{total.horas_totales:.1f}** "
        f"({total.horas_criterio:.1f} h de criterio humano, {total.pct_criterio * 100:.0f} %)",
        f"- Costo total de producción: {money(m.costo_total(total))}",
        f"- Precio piso (no descender de aquí): **{money(m.precio_piso(total))}**",
        f"- Precio de lista: **{money(m.precio_lista(total))}**",
    ])


def detalle_cotizacion(cot: Cotizador, clave: str) -> str:
    c = cot.cotizar(clave)
    p, costeo = c["propuesta"], c["costeo"]
    iva_pct = cot.m.p["iva_pct"]

    filas = []
    for l in c["lineas"]:
        cantidad = []
        if l.cantidad_nueva:
            cantidad.append(f"{l.cantidad_nueva:g} nuevo")
        if l.cantidad_adecuacion:
            cantidad.append(f"{l.cantidad_adecuacion:g} adec.")
        filas.append([
            l.nombre,
            " + ".join(cantidad),
            money(l.precio_unitario),
            money(l.precio_adecuacion),
            money(l.subtotal),
        ])

    estado = "dentro del piso" if c["sobre_piso"] else "POR DEBAJO DEL PISO — no firmar"
    ahorro = c["valor_si_todo_nuevo"] - c["subtotal"]

    out = [
        f"### {p['institucion']} — {p['curso']}",
        "",
        p["contexto"],
        "",
        tabla_md(
            ["Componente", "Cantidad", "Precio nuevo", "Precio adecuación", "Subtotal"],
            filas,
            alinear_der={2, 3, 4},
        ),
        "",
        tabla_md(
            ["Concepto", "Valor"],
            [
                ["Subtotal", money(c["subtotal"])],
                [f"Descuento · {c['plan']['nombre']} ({c['plan']['descuento'] * 100:.0f} %)",
                 f"({money(c['descuento'])})"],
                ["**Total sin IVA**", f"**{money(c['total'])}**"],
                [f"IVA ({iva_pct * 100:.0f} %, sujeto a régimen)", money(c["total"] * iva_pct)],
                ["**Total con IVA**", f"**{money(c['total'] * (1 + iva_pct))}**"],
            ],
            alinear_der={1},
        ),
        "",
        "**Control interno (no se muestra al cliente):**",
        "",
        f"- Horas de producción: {costeo.horas_totales:.1f} "
        f"({costeo.horas_criterio:.1f} h de criterio humano, {costeo.pct_criterio * 100:.0f} %)",
        f"- Costo total: {money(c['costo_total'])}",
        f"- Precio piso: {money(c['piso'])} → **{estado}**",
        f"- Margen efectivo: **{c['margen'] * 100:.1f} %**",
        f"- Descuento máximo admisible: **{cot.descuento_maximo(clave) * 100:.1f} %**",
        "",
        f"**Argumento de venta.** Producir estos recursos íntegramente desde cero costaría "
        f"{money(c['valor_si_todo_nuevo'])}. Aprovechar lo que la institución ya tiene "
        f"le ahorra {money(ahorro)}.",
    ]
    if p.get("nota"):
        out += ["", f"> {p['nota']}"]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Costeo y cotización de Desarrollos AP")
    ap.add_argument("--recurso", help="clave del recurso a detallar")
    ap.add_argument("--curso", help="clave de la plantilla de curso a detallar")
    ap.add_argument("--cotizacion", help="clave de la propuesta a cotizar")
    ap.add_argument("--csv", help="directorio donde exportar el catálogo en CSV")
    args = ap.parse_args()

    m = Modelo()

    if args.recurso:
        print(detalle_recurso(m, args.recurso))
        return
    if args.curso:
        print(detalle_curso(m, args.curso))
        return
    if args.cotizacion:
        print(detalle_cotizacion(Cotizador(m), args.cotizacion))
        return
    if args.csv:
        destino = Path(args.csv)
        destino.mkdir(parents=True, exist_ok=True)
        lineas = ["recurso;horas;horas_criterio;pct_criterio;costo_total;precio_piso;precio_lista"]
        for clave, recurso in m.recursos.items():
            c = m.costear_recurso(clave)
            lineas.append(
                f"{recurso['nombre']};{c.horas_totales:.1f};{c.horas_criterio:.1f};"
                f"{c.pct_criterio:.3f};{round(m.costo_total(c))};"
                f"{round(m.precio_piso(c))};{round(m.precio_lista(c))}"
            )
        (destino / "catalogo_costos.csv").write_text("\n".join(lineas), encoding="utf-8")
        print(f"Exportado a {destino / 'catalogo_costos.csv'}")
        return

    print("CATÁLOGO DE RECURSOS\n")
    print(tabla_catalogo(m))
    print("\n\nPLANTILLAS DE CURSO\n")
    filas = []
    for clave, plantilla in m.plantillas.items():
        c = m.costear_plantilla(clave)
        filas.append([
            plantilla["nombre"],
            f"{c.horas_totales:.0f}",
            f"{c.pct_criterio * 100:.0f} %",
            money(m.costo_total(c)),
            money(m.precio_piso(c)),
            money(m.precio_lista(c)),
        ])
    print(tabla_md(
        ["Plantilla", "Horas", "Criterio", "Costo total", "Precio piso", "Precio lista"],
        filas,
        alinear_der={1, 2, 3, 4, 5},
    ))


if __name__ == "__main__":
    main()
