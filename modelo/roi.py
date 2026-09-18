"""Modelo de retorno para la institución cliente.

Responde a la pregunta que cierra la venta: ¿qué gana la universidad con esto?

IMPORTANTE: los valores por defecto son SUPUESTOS DE TRABAJO, no datos de la
Universidad Santiago de Cali. Antes de presentarlos hay que pedirle a la
institución sus cifras reales de matrícula, tamaño de cohorte y tasa de
reprobación del curso. Un modelo de retorno con cifras inventadas se cae en la
primera pregunta del comité de compras y se lleva la credibilidad con él.

Uso:
    python3 roi.py
    python3 roi.py --estudiantes 500 --matricula 5200000 --reduccion 0.04
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


def money(v: float) -> str:
    return "$ " + f"{round(v):,}".replace(",", ".")


@dataclass
class Supuestos:
    """Parámetros que la institución debe validar antes de usar este modelo."""

    estudiantes_cohorte: int = 400
    reprobacion_actual: float = 0.35
    reduccion_reprobacion_pp: float = 0.05
    proporcion_reprobados_que_desertan: float = 0.35
    matricula_semestral: float = 4_500_000
    semestres_restantes: float = 2.0
    cohortes_por_ano: int = 2
    horas_docente_ahorradas_semestre: float = 40.0
    costo_hora_docente: float = 65_000
    vida_util_curso_anos: float = 3.0

    def descripcion(self) -> list[tuple[str, str, str]]:
        """(parámetro, valor, cómo se valida)"""
        return [
            ("Estudiantes por cohorte", f"{self.estudiantes_cohorte}",
             "Registro académico: matriculados en el curso por periodo"),
            ("Reprobación actual", f"{self.reprobacion_actual * 100:.0f} %",
             "Histórico de notas del curso, últimos 4 periodos"),
            ("Reducción esperada", f"{self.reduccion_reprobacion_pp * 100:.0f} pp",
             "Se mide comparando el periodo piloto con el histórico"),
            ("Reprobados que terminan desertando", f"{self.proporcion_reprobados_que_desertan * 100:.0f} %",
             "Cruce de reprobación con retiro efectivo (SPADIES institucional)"),
            ("Matrícula semestral", money(self.matricula_semestral),
             "Tarifa vigente del programa"),
            ("Semestres restantes contabilizados", f"{self.semestres_restantes:.0f}",
             "Criterio conservador: solo los dos siguientes, no la carrera completa"),
            ("Cohortes por año", f"{self.cohortes_por_ano}",
             "Calendario académico del programa"),
            ("Horas docente ahorradas por semestre", f"{self.horas_docente_ahorradas_semestre:.0f}",
             "Preparación de material, elaboración y calificación de evaluaciones"),
            ("Costo hora docente", money(self.costo_hora_docente),
             "Costo institucional con prestaciones"),
            ("Vida útil del curso", f"{self.vida_util_curso_anos:.0f} años",
             "Antes de requerir actualización mayor"),
        ]


def calcular(s: Supuestos, inversion: float) -> dict:
    # Retención: estudiantes que no desertan gracias a la mejora del curso.
    retenidos_cohorte = (
        s.estudiantes_cohorte
        * s.reduccion_reprobacion_pp
        * s.proporcion_reprobados_que_desertan
    )
    retenidos_ano = retenidos_cohorte * s.cohortes_por_ano
    matricula_preservada_ano = retenidos_ano * s.matricula_semestral * s.semestres_restantes

    # Liberación de tiempo docente.
    ahorro_docente_ano = (
        s.horas_docente_ahorradas_semestre * s.costo_hora_docente * s.cohortes_por_ano
    )

    beneficio_ano = matricula_preservada_ano + ahorro_docente_ano
    beneficio_vida = beneficio_ano * s.vida_util_curso_anos

    return {
        "retenidos_cohorte": retenidos_cohorte,
        "retenidos_ano": retenidos_ano,
        "matricula_preservada_ano": matricula_preservada_ano,
        "ahorro_docente_ano": ahorro_docente_ano,
        "beneficio_ano": beneficio_ano,
        "beneficio_vida": beneficio_vida,
        "inversion": inversion,
        "retorno_vida": beneficio_vida / inversion if inversion else 0,
        "meses_recuperacion": inversion / (beneficio_ano / 12) if beneficio_ano else 0,
        "punto_equilibrio_estudiantes": (
            inversion / (s.matricula_semestral * s.semestres_restantes)
            if s.matricula_semestral else 0
        ),
    }


def informe(s: Supuestos, inversion: float, etiqueta: str) -> str:
    r = calcular(s, inversion)
    filas = [
        f"| {p} | {v} | {c} |" for p, v, c in s.descripcion()
    ]
    return "\n".join([
        f"## Retorno estimado · {etiqueta}",
        "",
        "### Supuestos (a validar con la institución antes de presentar)",
        "",
        "| Parámetro | Valor supuesto | Cómo se valida |",
        "| --- | ---: | --- |",
        *filas,
        "",
        "### Resultado",
        "",
        "| Concepto | Valor |",
        "| --- | ---: |",
        f"| Inversión en el curso | {money(r['inversion'])} |",
        f"| Estudiantes retenidos por cohorte | {r['retenidos_cohorte']:.1f} |",
        f"| Estudiantes retenidos por año | {r['retenidos_ano']:.1f} |",
        f"| Matrícula preservada por año | {money(r['matricula_preservada_ano'])} |",
        f"| Tiempo docente liberado por año | {money(r['ahorro_docente_ano'])} |",
        f"| **Beneficio anual** | **{money(r['beneficio_ano'])}** |",
        f"| Beneficio en {s.vida_util_curso_anos:.0f} años de vida útil | {money(r['beneficio_vida'])} |",
        f"| **Retorno sobre la inversión** | **{r['retorno_vida']:.1f}x** |",
        f"| Meses para recuperar la inversión | {r['meses_recuperacion']:.1f} |",
        "",
        f"**El número que cierra la conversación:** la inversión se recupera reteniendo "
        f"**{r['punto_equilibrio_estudiantes']:.1f} estudiantes** que de otro modo habrían "
        f"desertado. Sobre una cohorte de {s.estudiantes_cohorte}, equivale al "
        f"{r['punto_equilibrio_estudiantes'] / s.estudiantes_cohorte * 100:.1f} % del curso.",
    ])


def sensibilidad(s: Supuestos, inversion: float) -> str:
    """Muestra qué pasa si los supuestos optimistas no se cumplen."""
    filas = []
    for reduccion in (0.02, 0.03, 0.05, 0.08):
        for desercion in (0.20, 0.35, 0.50):
            v = Supuestos(**{**s.__dict__, "reduccion_reprobacion_pp": reduccion,
                             "proporcion_reprobados_que_desertan": desercion})
            r = calcular(v, inversion)
            filas.append(
                f"| {reduccion * 100:.0f} pp | {desercion * 100:.0f} % | "
                f"{money(r['beneficio_ano'])} | {r['retorno_vida']:.1f}x | "
                f"{r['meses_recuperacion']:.0f} |"
            )
    return "\n".join([
        "### Análisis de sensibilidad",
        "",
        "Qué pasa si los supuestos resultan más pesimistas. La fila más conservadora "
        "(2 pp de reducción, 20 % de deserción) es el escenario de piso.",
        "",
        "| Reducción de reprobación | Reprobados que desertan | Beneficio anual | Retorno | Meses |",
        "| ---: | ---: | ---: | ---: | ---: |",
        *filas,
    ])


def main() -> None:
    ap = argparse.ArgumentParser(description="Modelo de retorno para la institución")
    ap.add_argument("--estudiantes", type=int, default=400)
    ap.add_argument("--matricula", type=float, default=4_500_000)
    ap.add_argument("--reduccion", type=float, default=0.05, help="reducción de reprobación en puntos (0.05 = 5 pp)")
    ap.add_argument("--desercion", type=float, default=0.35)
    ap.add_argument("--inversion", type=float, default=25_719_336)
    ap.add_argument("--etiqueta", default="Razonamiento Cuantitativo · USC")
    args = ap.parse_args()

    s = Supuestos(
        estudiantes_cohorte=args.estudiantes,
        matricula_semestral=args.matricula,
        reduccion_reprobacion_pp=args.reduccion,
        proporcion_reprobados_que_desertan=args.desercion,
    )
    print(informe(s, args.inversion, args.etiqueta))
    print()
    print(sensibilidad(s, args.inversion))


if __name__ == "__main__":
    main()
