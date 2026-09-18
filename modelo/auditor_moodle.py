"""Auditor de recursos educativos digitales.

Revisa recursos contra los criterios obligatorios de las skills del modelo
instruccional y reporta, uno por uno, qué cumple y qué falta.

Acepta:
  - un backup de Moodle (.mbz): inventaria el curso y audita su banco de
    preguntas, sus actividades y los archivos incrustados;
  - una carpeta suelta con .html, .gift y .h5p.

Uso:
    python3 modelo/auditor_moodle.py <ruta.mbz | carpeta> [--md salida.md]

No requiere dependencias externas.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import tarfile
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------- utilidades

def texto_visible(h: str) -> str:
    """Texto de un HTML, sin scripts ni estilos."""
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def cuenta(patron: str, texto: str) -> int:
    return len(re.findall(patron, texto, re.I))


@dataclass
class Hallazgo:
    criterio: str
    cumple: bool
    detalle: str = ""
    critico: bool = False


@dataclass
class Informe:
    nombre: str
    tipo: str
    hallazgos: list[Hallazgo] = field(default_factory=list)
    datos: dict = field(default_factory=dict)

    def ok(self, criterio, detalle=""):
        self.hallazgos.append(Hallazgo(criterio, True, detalle))

    def falla(self, criterio, detalle="", critico=False):
        self.hallazgos.append(Hallazgo(criterio, False, detalle, critico))

    @property
    def cumplidos(self) -> int:
        return sum(1 for h in self.hallazgos if h.cumple)

    @property
    def pct(self) -> float:
        return self.cumplidos / len(self.hallazgos) if self.hallazgos else 0.0

    @property
    def criticos(self) -> list[Hallazgo]:
        return [h for h in self.hallazgos if not h.cumple and h.critico]


# ------------------------------------------------------------ auditores

def auditar_guia(nombre: str, h: str) -> Informe:
    """Criterios de la skill generacion-guias."""
    inf = Informe(nombre, "Guía HTML")
    t = texto_visible(h)
    inf.datos = {"palabras": len(t.split()), "kb": len(h) // 1024}

    secciones = {
        "Objetivo de aprendizaje": r"objetivo\s+(de\s+)?(aprendizaje|la\s+sesi)",
        "Competencias trabajadas": r"competencia",
        "Referencias bibliográficas": r"referencia|bibliograf|fuentes\s+consultadas",
        "Síntesis o mapa conceptual": r"s[íi]ntesis|mapa\s+conceptual|resumen|cierre",
        "Conexión con la siguiente sesión": r"siguiente\s+(semana|sesi|tema)|pr[óo]xima\s+(semana|sesi)|conexi[óo]n\s+con",
    }
    for et, pat in secciones.items():
        crit = et in ("Objetivo de aprendizaje", "Competencias trabajadas",
                      "Referencias bibliográficas")
        (inf.ok if re.search(pat, t, re.I) else
         lambda c, d: inf.falla(c, d, critico=crit))(et, "sección obligatoria")

    n_ej = cuenta(r"ejemplo", t)
    (inf.ok if n_ej >= 2 else inf.falla)("Ejemplos pareados", f"{n_ej} menciones de «ejemplo»")

    n_err = cuenta(
        r"error(es)?\b[^.]{0,40}\b(frecuente|com[úu]n|t[íi]pico|habitual)"
        r"|\berror\b[^.]{0,30}\?"
        r"|no\s+confund|ojo\s+con|cuidado\s+con|nota\s+de\s+atenci[óo]n", t)
    (inf.ok if n_err >= 1 else inf.falla)("Errores frecuentes señalados", f"{n_err} avisos")

    tiene_math = bool(re.search(r"mathjax|katex", h, re.I))
    (inf.ok if tiene_math else inf.falla)(
        "Notación con MathJax/KaTeX",
        "presente" if tiene_math else "usa Unicode; limita fórmulas complejas")

    (inf.ok if "viewport" in h else inf.falla)("Responsive (viewport)")
    (inf.ok if cuenta(r"@media", h) else inf.falla)("Media queries")
    (inf.ok if re.search(r'<html[^>]+lang=', h) else inf.falla)("Idioma declarado")

    n_aria = cuenta(r"aria-[a-z]+=|role=", h)
    (inf.ok if n_aria else inf.falla)("Accesibilidad (ARIA)", f"{n_aria} atributos")

    imgs, alts = cuenta(r"<img", h), cuenta(r"<img[^>]+alt=", h)
    if imgs:
        (inf.ok if alts == imgs else inf.falla)("Texto alternativo en imágenes", f"{alts}/{imgs}")

    botones = cuenta(r"<button", h)
    inputs = cuenta(r"<input", h)
    inf.datos["interactivo"] = botones + inputs
    if botones + inputs:
        inf.ok("Interactividad", f"{botones} botones, {inputs} campos")
        reporta = bool(re.search(r"H5P|postMessage|fetch\(|XMLHttpRequest|SCORM|LMS", h, re.I))
        (inf.ok if reporta else lambda c, d: inf.falla(c, d, critico=True))(
            "Reporta resultado al LMS",
            "presente" if reporta else "el estudiante responde y el docente no se entera")
    else:
        inf.falla("Interactividad", "documento expositivo, sin ejercicios")

    return inf


def auditar_gift(nombre: str, texto: str) -> Informe:
    """Criterios de la skill generacion-quizzes."""
    inf = Informe(nombre, "Banco de preguntas GIFT")
    cuerpo = re.sub(r"^\s*//.*$", "", texto, flags=re.M)      # sin comentarios
    titulos = re.findall(r"::([^:]+)::", cuerpo)
    inf.datos = {"items": len(titulos)}

    (inf.ok if titulos else inf.falla)("Contiene ítems", f"{len(titulos)} ítems")
    (inf.ok if len(titulos) == len(set(titulos)) else inf.falla)(
        "Títulos únicos", f"{len(titulos) - len(set(titulos))} duplicados")

    tipos = {
        "Selección múltiple": bool(re.search(r"\{[^}]*~", cuerpo, re.S)),
        "Verdadero/Falso": bool(re.search(r"\{\s*(TRUE|FALSE|T|F)\s*[#}]", cuerpo)),
        "Numérica": bool(re.search(r"\{\s*#[^#}]", cuerpo)),
        "Emparejar": bool(re.search(r"=.*->", cuerpo)),
        "Completar (cloze)": bool(re.search(r"\{\d+:[A-Z]+:", cuerpo) or
                                  re.search(r"\{\s*=[^~}]+\s*=[^~}]+\}", cuerpo, re.S)),
    }
    presentes = [k for k, v in tipos.items() if v]
    inf.datos["tipos"] = presentes
    (inf.ok if len(presentes) >= 4 else inf.falla)(
        "Al menos 4 tipos de pregunta", ", ".join(presentes) or "ninguno detectado")
    (inf.ok if tipos["Numérica"] else lambda c, d: inf.falla(c, d, critico=True))(
        "Incluye ítems numéricos", "la skill pide ~25 % de cálculo con tolerancia")

    # Retroalimentación: '#' por opción, '####' general.
    retro_opcion = len(re.findall(r"[~=][^#\n}]*#(?!#)", cuerpo))
    retro_general = len(re.findall(r"####", cuerpo))
    inf.datos["retro"] = (retro_opcion, retro_general)
    (inf.ok if retro_opcion else lambda c, d: inf.falla(c, d, critico=True))(
        "Retroalimentación por opción", f"{retro_opcion} encontradas")
    (inf.ok if retro_general else lambda c, d: inf.falla(c, d, critico=True))(
        "Retroalimentación general", f"{retro_general} encontradas")

    (inf.ok if "﻿" not in texto else inf.falla)("UTF-8 sin BOM")

    # Distractores sospechosos
    malos = len(re.findall(r"~\s*(ninguna de las anteriores|todas las anteriores)", cuerpo, re.I))
    (inf.ok if not malos else inf.falla)("Sin distractores comodín", f"{malos} encontrados")
    return inf


def auditar_h5p(nombre: str, datos: bytes) -> Informe:
    """Criterios de la skill produccion-h5p-scorm."""
    inf = Informe(nombre, "Paquete H5P")
    try:
        z = zipfile.ZipFile(__import__("io").BytesIO(datos))
    except zipfile.BadZipFile:
        inf.falla("Archivo ZIP válido", "no se pudo abrir", critico=True)
        return inf

    nombres = z.namelist()
    (inf.ok if "h5p.json" in nombres else lambda c, d: inf.falla(c, d, critico=True))(
        "h5p.json en la raíz", "obligatorio para importar")
    (inf.ok if "content/content.json" in nombres else
     lambda c, d: inf.falla(c, d, critico=True))("content/content.json presente")

    if "h5p.json" not in nombres:
        return inf

    meta = json.loads(z.read("h5p.json"))
    deps = meta.get("preloadedDependencies", [])
    inf.datos = {"titulo": meta.get("title", ""), "libreria": meta.get("mainLibrary", ""),
                 "librerias": len(deps)}
    (inf.ok if deps else inf.falla)("Librerías declaradas", f"{len(deps)}")
    (inf.ok if all("majorVersion" in d for d in deps) else inf.falla)(
        "Versiones de librería fijadas")
    lic = meta.get("license", "U")
    (inf.ok if lic not in ("U", "", None) else inf.falla)(
        "Licencia declarada", f"license = «{lic}»")

    if "content/content.json" not in nombres:
        return inf
    c = json.loads(z.read("content/content.json"))
    txt = json.dumps(c, ensure_ascii=False)

    beh = c.get("behaviour", {}) or {}
    umbral = beh.get("passPercentage", c.get("passPercentage"))
    (inf.ok if umbral else lambda cr, d: inf.falla(cr, d, critico=True))(
        "Umbral de aprobación configurado",
        f"{umbral} %" if umbral else "sin umbral: Moodle marcará «completado» con cualquier nota")

    # Retroalimentación por rangos, más allá del marcador genérico
    ofb = c.get("overallFeedback", [])
    especifica = [f for f in ofb if not re.fullmatch(
        r"\s*(obtuviste\s+)?:num\s*(de|/)\s*:total.*", f.get("feedback", ""), re.I)]
    (inf.ok if len(ofb) > 1 or especifica else inf.falla)(
        "Retroalimentación por rangos",
        f"{len(ofb)} rango(s); genérica" if ofb and not especifica else f"{len(ofb)} rangos")

    tips = len(re.findall(r'"tip"\s*:\s*"[^"]+"', txt)) + len(re.findall(r"\*[^*]+:[^*]+\*", txt))
    (inf.ok if tips else inf.falla)("Pistas por ítem", f"{tips} pistas")

    n_q = len(c.get("questions", []) or c.get("questionSet", {}).get("questions", []))
    if n_q:
        inf.datos["items"] = n_q
        (inf.ok if n_q >= 10 else inf.falla)("Al menos 10 ítems", f"{n_q} ítems")

    libs_contenido = {d.get("machineName", "") for d in deps}
    tipos_pregunta = {l for l in libs_contenido if re.search(
        r"MultiChoice|TrueFalse|Blanks|DragText|DragQuestion|Summary|MarkTheWords", l)}
    (inf.ok if len(tipos_pregunta) >= 2 else inf.falla)(
        "Variedad de formatos", ", ".join(sorted(tipos_pregunta)) or "un solo formato")
    return inf


def auditar_taller(nombre: str, h: str) -> Informe:
    """Criterios de la skill creacion-actividades-moodle."""
    inf = Informe(nombre, "Taller / actividad")
    t = texto_visible(h)
    inf.datos = {"palabras": len(t.split())}
    n_ej = len(re.findall(r"(?:^|\s)(\d{1,2})[.)]\s", t))
    inf.datos["ejercicios"] = n_ej

    reqs = [
        ("Rúbrica de evaluación", r"r[úu]brica|criterios\s+de\s+evaluaci|niveles\s+de\s+logro", True),
        ("Solucionario o clave", r"solucionario|clave\s+de\s+respuesta|respuestas\s+correctas", True),
        ("Objetivo de aprendizaje", r"objetivo", True),
        ("Competencias", r"competencia", False),
        ("Tiempo estimado", r"tiempo\s+estimado|duraci[óo]n|minutos|horas", False),
        ("Producto entregable definido", r"entrega|producto|sube|adjunta|formato\s+de\s+entrega", False),
        ("Contexto realista", r"estudiantes|empresa|ciudad|encuesta|personas|clientes", False),
    ]
    for et, pat, crit in reqs:
        if re.search(pat, t, re.I):
            inf.ok(et)
        else:
            inf.falla(et, "no aparece en el documento", critico=crit)

    (inf.ok if n_ej >= 5 else inf.falla)("Volumen de ejercicios", f"{n_ej} detectados")
    return inf


# ------------------------------------------------------------ backup .mbz

def inventario_mbz(ruta: Path) -> tuple[list[Informe], dict]:
    """Extrae un backup de Moodle y audita lo que contenga."""
    informes: list[Informe] = []
    resumen: dict = {"curso": "", "secciones": 0, "actividades": {}}

    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp)
        try:
            with tarfile.open(ruta, "r:*") as tf:
                tf.extractall(destino, filter="data")
        except tarfile.ReadError:
            with zipfile.ZipFile(ruta) as zf:
                zf.extractall(destino)

        mb = destino / "moodle_backup.xml"
        if mb.exists():
            x = mb.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"<original_course_fullname>(.*?)</original_course_fullname>", x, re.S)
            if m:
                resumen["curso"] = html.unescape(m.group(1)).strip()
            for tipo in re.findall(r"<modulename>(.*?)</modulename>", x):
                resumen["actividades"][tipo] = resumen["actividades"].get(tipo, 0) + 1
            resumen["secciones"] = len(re.findall(r"<section>\s*<sectionid>", x))

        # Banco de preguntas
        for qf in destino.rglob("questions.xml"):
            x = qf.read_text(encoding="utf-8", errors="replace")
            n = len(re.findall(r"<question_bank_entry", x)) or len(re.findall(r"<question ", x))
            inf = Informe("Banco de preguntas del curso", "Banco Moodle XML")
            inf.datos = {"items": n}
            (inf.ok if n else inf.falla)("Contiene preguntas", f"{n}")
            retro = len(re.findall(r"<feedback[ >]", x))
            (inf.ok if retro else lambda c, d: inf.falla(c, d, critico=True))(
                "Retroalimentación en los ítems", f"{retro} bloques")
            num = len(re.findall(r"type=\"numerical\"", x))
            (inf.ok if num else inf.falla)("Ítems numéricos", f"{num}")
            informes.append(inf)

        # Archivos incrustados: el .mbz los guarda por hash, con files.xml de índice
        nombres_por_hash = {}
        fx = destino / "files.xml"
        if fx.exists():
            x = fx.read_text(encoding="utf-8", errors="replace")
            for bloque in re.findall(r"<file id=.*?</file>", x, re.S):
                h_ = re.search(r"<contenthash>(.*?)</contenthash>", bloque)
                n_ = re.search(r"<filename>(.*?)</filename>", bloque)
                if h_ and n_ and n_.group(1) != ".":
                    nombres_por_hash[h_.group(1)] = html.unescape(n_.group(1))

        for f in (destino / "files").rglob("*") if (destino / "files").exists() else []:
            if not f.is_file():
                continue
            nombre = nombres_por_hash.get(f.name, f.name)
            informes.append(auditar_archivo(f, nombre))

    return [i for i in informes if i], resumen


def auditar_archivo(f: Path, nombre: str | None = None) -> Informe | None:
    nombre = nombre or f.name
    ext = Path(nombre).suffix.lower()
    try:
        if ext in (".html", ".htm"):
            h = f.read_text(encoding="utf-8", errors="replace")
            es_taller = re.search(r"taller|ejercicios|actividad|pr[áa]ctica", nombre, re.I)
            return auditar_taller(nombre, h) if es_taller else auditar_guia(nombre, h)
        if ext == ".gift":
            return auditar_gift(nombre, f.read_text(encoding="utf-8", errors="replace"))
        if ext == ".h5p":
            return auditar_h5p(nombre, f.read_bytes())
    except Exception as e:                                     # noqa: BLE001
        inf = Informe(nombre, ext or "desconocido")
        inf.falla("Archivo legible", f"{type(e).__name__}: {e}", critico=True)
        return inf
    return None


# ------------------------------------------------------------ presentación

def render(informes: list[Informe], resumen: dict | None) -> str:
    out = ["# Auditoría de recursos", ""]
    if resumen and resumen.get("curso"):
        out += [f"**Curso:** {resumen['curso']}", ""]
        if resumen["actividades"]:
            out += ["| Tipo de actividad | Cantidad |", "| --- | ---: |"]
            out += [f"| {k} | {v} |" for k, v in sorted(resumen["actividades"].items())]
            out += [""]

    if not informes:
        out += ["_No se encontraron recursos auditables._"]
        return "\n".join(out)

    criticos = [(i, h) for i in informes for h in i.criticos]
    out += ["## Resumen", "",
            f"- Recursos auditados: **{len(informes)}**",
            f"- Cumplimiento medio: **{sum(i.pct for i in informes) / len(informes) * 100:.0f} %**",
            f"- Hallazgos críticos: **{len(criticos)}**", ""]

    if criticos:
        out += ["## Hallazgos críticos", "",
                "| Recurso | Criterio incumplido | Detalle |", "| --- | --- | --- |"]
        out += [f"| {i.nombre} | {h.criterio} | {h.detalle} |" for i, h in criticos]
        out += [""]

    out += ["## Detalle por recurso", ""]
    for i in sorted(informes, key=lambda x: x.pct):
        marca = "🔴" if i.criticos else ("🟡" if i.pct < 0.8 else "🟢")
        out += [f"### {marca} {i.nombre}", "",
                f"*{i.tipo} · {i.cumplidos}/{len(i.hallazgos)} criterios "
                f"({i.pct * 100:.0f} %)*", ""]
        if i.datos:
            out += ["  " + " · ".join(f"{k}: {v}" for k, v in i.datos.items()), ""]
        for h in i.hallazgos:
            s = "✅" if h.cumple else ("❌" if h.critico else "⚠️")
            out.append(f"- {s} **{h.criterio}**" + (f" — {h.detalle}" if h.detalle else ""))
        out += [""]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Audita recursos educativos digitales")
    ap.add_argument("ruta", help="backup .mbz de Moodle o carpeta con recursos")
    ap.add_argument("--md", help="archivo Markdown de salida")
    args = ap.parse_args()

    ruta = Path(args.ruta)
    if not ruta.exists():
        sys.exit(f"No existe: {ruta}")

    if ruta.is_file() and ruta.suffix.lower() == ".mbz":
        informes, resumen = inventario_mbz(ruta)
    elif ruta.is_dir():
        informes = [a for f in sorted(ruta.rglob("*")) if f.is_file()
                    for a in [auditar_archivo(f)] if a]
        resumen = None
    else:
        informes, resumen = [x for x in [auditar_archivo(ruta)] if x], None

    texto = render(informes, resumen)
    if args.md:
        Path(args.md).write_text(texto, encoding="utf-8")
        print(f"Informe escrito en {args.md}")
    else:
        print(texto)


if __name__ == "__main__":
    main()
