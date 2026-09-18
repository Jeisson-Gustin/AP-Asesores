"""Genera el formulario de levantamiento de necesidades.

Produce `herramientas/formulario_necesidades.html` a partir de
`modelo/catalogo_oferta.json`. El mismo archivo sirve para llenar en pantalla
y para imprimir: las reglas @media print lo convierten en un formulario de
papel con casillas.

El PDF se obtiene imprimiendo ese HTML con Chromium (ver generar_pdf_formulario.mjs).

Uso:
    python3 modelo/generar_formulario.py
"""

from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).parent
RAIZ = BASE.parent
FECHA = "18 de septiembre de 2026"


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --------------------------------------------------------------- componentes

def campo(id_: str, etiqueta: str, ancho: str = "1", tipo: str = "text",
          pista: str = "", valor: str = "") -> str:
    return f"""<div class="campo" style="--col:{ancho}">
  <label for="{id_}">{esc(etiqueta)}</label>
  <input type="{tipo}" id="{id_}" name="{id_}" value="{esc(valor)}">
  {f'<span class="pista">{esc(pista)}</span>' if pista else ''}
</div>"""


def fila_item(fam_id: str, cod: str, nombre: str, detalle: str,
              tamanos: list | None = None) -> str:
    """Una fila de la tabla de selección. Con tamaños, una casilla por tamaño."""
    if tamanos:
        celdas = "".join(
            f'<td class="n"><input type="number" min="0" step="1" placeholder="0" '
            f'class="cant" data-fam="{fam_id}" data-cod="{cod}-{t["cod"]}" '
            f'id="c-{fam_id}-{cod}-{t["cod"]}" '
            f'aria-label="{esc(nombre)}, {esc(t["etiqueta"])}"></td>'
            for t in tamanos)
    else:
        celdas = (f'<td class="n"><input type="number" min="0" step="1" placeholder="0" '
                  f'class="cant" data-fam="{fam_id}" data-cod="{cod}" '
                  f'id="c-{fam_id}-{cod}" aria-label="{esc(nombre)}"></td>')
    return f"""<tr>
  <td class="cod">{cod}</td>
  <td><strong>{esc(nombre)}</strong><span class="det">{esc(detalle)}</span></td>
  {celdas}
</tr>"""


def bloque_familia(f: dict, letra: str) -> str:
    tamanos = f.get("tamanos")
    if tamanos:
        th = "".join(f'<th class="n">{esc(t["etiqueta"])}</th>' for t in tamanos)
        nota = ('<p class="nota-tam">Indique cuántas unidades necesita de cada tamaño. '
                'Puede combinar: por ejemplo, 4 de 10 preguntas y 2 de 20.</p>')
    else:
        th = '<th class="n">Cantidad</th>'
        nota = ""

    filas = "\n".join(
        fila_item(f["id"], it["cod"], it["nombre"], it["detalle"], tamanos)
        for it in f["items"])

    return f"""<section class="familia" id="fam-{f['id']}">
  <h2>{letra} · {esc(f['nombre'])}</h2>
  <p class="intro">{esc(f['intro'])}</p>
  {nota}
  <div class="marco">
    <table>
      <thead><tr><th class="cod">Cód.</th><th>Recurso</th>{th}</tr></thead>
      <tbody>
{filas}
      </tbody>
    </table>
  </div>
</section>"""


def construir() -> str:
    cat = json.loads((BASE / "catalogo_oferta.json").read_text(encoding="utf-8"))
    letras = "DEFGHIJKLM"
    familias = "\n\n".join(
        bloque_familia(f, letras[i]) for i, f in enumerate(cat["familias"]))
    sig = letras[len(cat["familias"])] if len(cat["familias"]) < len(letras) else "N"

    reqs = "\n".join(
        f'<label class="check"><input type="checkbox" id="req-{r["id"]}" '
        f'class="req"><span>{esc(r["texto"])}</span></label>'
        for r in cat["requerimientos"])

    datos = "\n".join([
        campo("inst", "Institución", "2"),
        campo("programa", "Programa o facultad", "2"),
        campo("curso", "Curso o asignatura", "2"),
        campo("codigo", "Código del curso"),
        campo("docente", "Docente titular"),
        campo("contacto", "Persona de contacto"),
        campo("correo", "Correo", tipo="email"),
        campo("telefono", "Teléfono", tipo="tel"),
    ])

    contexto = "\n".join([
        campo("estudiantes", "Estudiantes por cohorte", tipo="number",
              pista="Matriculados en el curso por periodo"),
        campo("cohortes", "Cohortes por año", tipo="number",
              pista="Según el calendario académico"),
        campo("semanas", "Semanas del curso", tipo="number"),
        campo("parciales", "Número de parciales", tipo="number"),
        campo("sesiones", "Sesiones por semana", tipo="number"),
        campo("inicio", "Fecha deseada de puesta en marcha", tipo="date"),
        campo("lms", "LMS y versión", "2", pista="Por ejemplo: Moodle 4.3"),
        campo("url", "URL del aula", "2", tipo="url"),
    ])

    return PLANTILLA.format(fecha=FECHA, datos=datos, contexto=contexto,
                            familias=familias, requerimientos=reqs,
                            sec_req=sig, sec_obs=chr(ord(sig) + 1))


# ------------------------------------------------------------------ plantilla

PLANTILLA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Formulario de levantamiento de necesidades · Desarrollos AP</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=IBM+Plex+Mono:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{{
  --papel:#f5f7f9; --tarjeta:#ffffff; --tinta:#0e1d2a; --suave:#586b7b; --tenue:#8698a7;
  --linea:#dbe2e9; --linea-fuerte:#c2ccd6;
  --acento:#0a6357; --acento-suave:#e3efec; --acento-borde:#a6d0c7;
  --display:"Bricolage Grotesque","Segoe UI",system-ui,sans-serif;
  --texto:"IBM Plex Sans","Segoe UI",system-ui,sans-serif;
  --dato:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --papel:#0c151e; --tarjeta:#13202b; --tinta:#e4ecf3; --suave:#93a6b6; --tenue:#6d8093;
  --linea:#213040; --linea-fuerte:#33485c;
  --acento:#4fb8a4; --acento-suave:#10302a; --acento-borde:#1d564a;
}}}}
:root[data-theme="dark"]{{
  --papel:#0c151e; --tarjeta:#13202b; --tinta:#e4ecf3; --suave:#93a6b6; --tenue:#6d8093;
  --linea:#213040; --linea-fuerte:#33485c;
  --acento:#4fb8a4; --acento-suave:#10302a; --acento-borde:#1d564a;
}}
*{{box-sizing:border-box}}
body{{margin:0;padding:0 16px;background:var(--papel);color:var(--tinta);
  font:400 16px/1.55 var(--texto);-webkit-font-smoothing:antialiased}}
.hoja{{max-width:1080px;margin:0 auto;padding-block:30px 80px}}
h1,h2,h3{{font-family:var(--display);line-height:1.13;margin:0;font-weight:800;text-wrap:balance}}
h1{{font-size:clamp(1.6rem,3.4vw,2.2rem);letter-spacing:-.02em}}
h2{{font-size:1.22rem;letter-spacing:-.01em;color:var(--acento)}}
h3{{font-size:.95rem;font-weight:600}}
p{{margin:0}}

.cabecera{{border-bottom:3px solid var(--tinta);padding-bottom:18px;margin-bottom:8px}}
.marca{{font:600 .7rem/1.4 var(--texto);letter-spacing:.15em;text-transform:uppercase;
  color:var(--acento);margin-bottom:8px}}
.lead{{color:var(--suave);margin-top:10px;max-width:74ch;font-size:.95rem}}
.meta{{display:flex;flex-wrap:wrap;gap:6px 22px;margin-top:14px;font-size:.8rem;color:var(--tenue)}}

section{{margin-top:34px}}
.familia h2{{padding-bottom:7px;border-bottom:2px solid var(--acento-borde)}}
.intro{{color:var(--suave);font-size:.89rem;margin:10px 0 0;max-width:76ch}}
.nota-tam{{font-size:.82rem;color:var(--acento);background:var(--acento-suave);
  border:1px solid var(--acento-borde);border-radius:8px;padding:8px 12px;margin-top:12px}}

.campos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin-top:16px}}
.campo{{display:flex;flex-direction:column;gap:5px;grid-column:span var(--col,1)}}
.campo label{{font:600 .71rem/1.3 var(--texto);letter-spacing:.05em;text-transform:uppercase;color:var(--tenue)}}
.campo input{{width:100%;padding:9px 11px;border:1px solid var(--linea-fuerte);border-radius:8px;
  background:var(--tarjeta);color:var(--tinta);font:400 .93rem/1.3 var(--texto)}}
.campo input:focus-visible{{outline:2px solid var(--acento);outline-offset:-1px;border-color:var(--acento)}}
.pista{{font-size:.72rem;color:var(--tenue)}}

.marco{{overflow-x:auto;max-width:100%;margin-top:14px;border:1px solid var(--linea);
  border-radius:11px;background:var(--tarjeta)}}
table{{border-collapse:collapse;width:100%;min-width:560px;font-size:.88rem}}
th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid var(--linea);vertical-align:top}}
thead th{{font:600 .67rem/1.3 var(--texto);letter-spacing:.07em;text-transform:uppercase;
  color:var(--tenue);border-bottom:1.5px solid var(--linea-fuerte);background:var(--papel)}}
tbody tr:last-child td{{border-bottom:0}}
tbody tr:hover{{background:var(--acento-suave)}}
td.cod,th.cod{{font-family:var(--dato);font-size:.76rem;color:var(--tenue);width:52px;white-space:nowrap}}
td.n,th.n{{text-align:right;width:104px}}
.det{{display:block;color:var(--suave);font-size:.81rem;line-height:1.45;margin-top:3px;max-width:62ch}}
input.cant{{width:74px;padding:6px 8px;border:1px solid var(--linea-fuerte);border-radius:7px;
  background:var(--papel);color:var(--tinta);font:600 .88rem/1.2 var(--dato);text-align:right}}
input.cant:focus-visible{{outline:2px solid var(--acento);outline-offset:-1px;border-color:var(--acento)}}
input.cant.lleno{{background:var(--acento-suave);border-color:var(--acento);color:var(--acento)}}

.checks{{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:2px;
  margin-top:16px;background:var(--linea);border:1px solid var(--linea);border-radius:11px;overflow:hidden}}
.check{{display:flex;gap:11px;align-items:flex-start;padding:12px 14px;background:var(--tarjeta);
  cursor:pointer;font-size:.88rem;line-height:1.45}}
.check:hover{{background:var(--acento-suave)}}
.check input{{margin:3px 0 0;width:17px;height:17px;accent-color:var(--acento);flex-shrink:0}}

textarea{{width:100%;min-height:130px;padding:12px 14px;border:1px solid var(--linea-fuerte);
  border-radius:10px;background:var(--tarjeta);color:var(--tinta);
  font:400 .93rem/1.6 var(--texto);resize:vertical;margin-top:14px}}
textarea:focus-visible{{outline:2px solid var(--acento);outline-offset:-1px;border-color:var(--acento)}}

.resumen{{position:sticky;bottom:0;margin-top:40px;background:var(--tinta);color:var(--papel);
  border-radius:13px 13px 0 0;padding:16px 20px;display:flex;flex-wrap:wrap;gap:12px 28px;
  align-items:center;justify-content:space-between;box-shadow:0 -6px 24px rgba(0,0,0,.14)}}
.resumen .cifras{{display:flex;flex-wrap:wrap;gap:10px 26px}}
.resumen b{{display:block;font:800 1.5rem/1.1 var(--display);font-variant-numeric:tabular-nums}}
.resumen span{{font-size:.76rem;opacity:.72}}
.acciones{{display:flex;flex-wrap:wrap;gap:9px}}
.btn{{appearance:none;cursor:pointer;border:1px solid transparent;border-radius:9px;
  padding:10px 17px;font:600 .86rem/1 var(--texto)}}
.btn.principal{{background:var(--acento);color:#fff}}
.btn.secundario{{background:transparent;color:var(--papel);border-color:rgba(255,255,255,.4)}}
.btn:hover{{filter:brightness(1.1)}}
.btn:focus-visible{{outline:2px solid #fff;outline-offset:2px}}

.pie{{margin-top:40px;border-top:1px solid var(--linea);padding-top:16px;
  color:var(--tenue);font-size:.79rem;line-height:1.6}}
.firma{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:26px;margin-top:30px}}
.firma div{{border-top:1px solid var(--linea-fuerte);padding-top:8px;font-size:.78rem;color:var(--tenue)}}

@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}

/* ---------------- impresión: se vuelve formulario de papel ---------------- */
@media print{{
  :root{{--papel:#fff;--tarjeta:#fff;--tinta:#000;--suave:#333;--tenue:#555;
        --linea:#bbb;--linea-fuerte:#888;--acento:#0a6357;--acento-suave:#fff;--acento-borde:#0a6357}}
  @page{{size:Letter;margin:14mm 13mm 16mm}}
  body{{padding:0;background:#fff;font-size:10.5pt}}
  .hoja{{max-width:none;padding:0}}
  .resumen,.acciones,.no-print{{display:none!important}}
  .familia{{break-inside:avoid-page;page-break-inside:avoid}}
  table{{min-width:0;font-size:9pt}}
  .marco{{overflow:visible;border-color:#888}}
  thead{{display:table-header-group}}
  tr{{break-inside:avoid;page-break-inside:avoid}}
  tbody tr:hover{{background:none}}
  .det{{font-size:8pt;max-width:none}}
  input.cant{{width:52px;border:1px solid #666;background:#fff;color:#000}}
  .campo input{{border:0;border-bottom:1px solid #666;border-radius:0;background:#fff;padding:4px 2px}}
  /* El selector nativo de fecha no tiene sentido en papel: queda una línea en blanco. */
  input[type=date]{{color:transparent}}
  input[type=date]::-webkit-calendar-picker-indicator,
  input[type=date]::-webkit-datetime-edit{{display:none}}
  /* Ninguna sección ni campo se parte entre páginas. */
  section{{break-inside:avoid-page;page-break-inside:avoid}}
  .campo{{break-inside:avoid;page-break-inside:avoid}}
  .checks{{break-inside:avoid;page-break-inside:avoid}}
  h2{{break-after:avoid;page-break-after:avoid}}
  .check input{{width:12px;height:12px}}
  .checks{{gap:0;background:#fff}}
  .check{{border:1px solid #ccc;margin:-0.5px}}
  textarea{{border:1px solid #666;min-height:90px;background:#fff}}
  h1{{font-size:19pt}} h2{{font-size:12.5pt}}
  .cabecera{{border-bottom:2.5px solid #000}}
  a{{color:#000;text-decoration:none}}
}}
</style>
</head>
<body>
<div class="hoja">

<header class="cabecera">
  <p class="marca">Desarrollos AP · Diseño y producción de cursos universitarios virtuales</p>
  <h1>Formulario de levantamiento de necesidades</h1>
  <p class="lead">Este formulario recoge lo que su curso necesita, recurso por recurso.
  No hay que llenarlo todo: marque únicamente las cantidades de lo que le interese y
  deje en blanco el resto. Con esta información preparamos una propuesta económica
  ajustada a su alcance real, sin partidas genéricas.</p>
  <div class="meta">
    <span>Versión {fecha}</span>
    <span>Tiempo estimado de diligenciamiento: 15 minutos</span>
    <span>Ninguna casilla es obligatoria</span>
  </div>
</header>

<section>
  <h2>A · Identificación</h2>
  <div class="campos">
{datos}
  </div>
</section>

<section>
  <h2>B · Contexto del curso</h2>
  <p class="intro">Estos datos determinan el tamaño del proyecto y permiten estimar el
  retorno de la inversión para la institución.</p>
  <div class="campos">
{contexto}
  </div>
</section>

<section>
  <h2>C · Punto de partida</h2>
  <p class="intro">Aprovechar material existente reduce el costo de forma sustancial:
  adecuar un recurso que ya tienen cuesta el 40 % de producirlo desde cero.</p>
  <div class="checks">
    <label class="check"><input type="checkbox" id="p-parcelacion"><span>Existe parcelación o microcurrículo oficial aprobado</span></label>
    <label class="check"><input type="checkbox" id="p-aula"><span>Ya existe un aula montada en el LMS</span></label>
    <label class="check"><input type="checkbox" id="p-material"><span>Hay material digital previo reutilizable</span></label>
    <label class="check"><input type="checkbox" id="p-videos"><span>Hay videos propios grabados</span></label>
    <label class="check"><input type="checkbox" id="p-banco"><span>Hay banco de preguntas existente</span></label>
    <label class="check"><input type="checkbox" id="p-h5p"><span>El LMS ya tiene el plugin H5P instalado y activo</span></label>
    <label class="check"><input type="checkbox" id="p-cero"><span>Se parte de cero: no hay material previo</span></label>
    <label class="check"><input type="checkbox" id="p-migracion"><span>El contenido está en otro LMS y hay que migrarlo</span></label>
  </div>
</section>

{familias}

<section>
  <h2>{sec_req} · Requerimientos especiales</h2>
  <p class="intro">Marque los que apliquen. Algunos cambian el esfuerzo de producción
  de forma significativa y conviene definirlos antes de cotizar.</p>
  <div class="checks">
{requerimientos}
  </div>
</section>

<section>
  <h2>{sec_obs} · Observaciones</h2>
  <p class="intro">Restricciones de presupuesto, plazos, decisiones ya tomadas,
  experiencias previas que no funcionaron, o cualquier cosa que debamos saber.</p>
  <textarea id="obs" placeholder="Escriba aquí…"></textarea>
</section>

<div class="firma">
  <div>Nombre y cargo de quien diligencia</div>
  <div>Fecha</div>
  <div>Firma</div>
</div>

<p class="pie">
  Desarrollos AP produce cada recurso con apoyo de inteligencia artificial para el
  borrador y el código base, y revisión profesional humana de todo lo generado:
  cada ejemplo se resuelve, cada ítem se responde y cada paquete se prueba en el LMS
  antes de entregarse. Dos de cada tres horas de producción son criterio humano.
  Este formulario no constituye una oferta comercial; con él se elabora la propuesta
  económica, que se entrega por separado.
</p>

<div class="resumen no-print" id="resumen">
  <div class="cifras">
    <div><b id="tTipos">0</b><span>tipos seleccionados</span></div>
    <div><b id="tUnidades">0</b><span>unidades en total</span></div>
    <div><b id="tReqs">0</b><span>requerimientos especiales</span></div>
  </div>
  <div class="acciones">
    <button type="button" class="btn secundario" id="btnLimpiar">Limpiar</button>
    <button type="button" class="btn secundario" id="btnImprimir">Imprimir o guardar PDF</button>
    <button type="button" class="btn principal" id="btnCopiar">Copiar resumen</button>
  </div>
</div>

</div>

<script>
(function(){{
  "use strict";
  var $ = function(id){{ return document.getElementById(id); }};
  var cants = [].slice.call(document.querySelectorAll(".cant"));
  var reqs  = [].slice.call(document.querySelectorAll(".req"));

  function guardar(){{
    try {{
      var d = {{}};
      [].forEach.call(document.querySelectorAll("input,textarea"), function(el){{
        if(!el.id) return;
        d[el.id] = el.type === "checkbox" ? el.checked : el.value;
      }});
      localStorage.setItem("ap-formulario", JSON.stringify(d));
    }} catch(e){{}}
  }}

  function restaurar(){{
    try {{
      var d = JSON.parse(localStorage.getItem("ap-formulario") || "{{}}");
      Object.keys(d).forEach(function(k){{
        var el = $(k);
        if(!el) return;
        if(el.type === "checkbox") el.checked = !!d[k]; else el.value = d[k];
      }});
    }} catch(e){{}}
  }}

  function recalcular(){{
    var tipos = 0, unidades = 0;
    cants.forEach(function(i){{
      var v = parseInt(i.value, 10);
      var hay = isFinite(v) && v > 0;
      i.classList.toggle("lleno", hay);
      if(hay){{ tipos++; unidades += v; }}
    }});
    $("tTipos").textContent = tipos;
    $("tUnidades").textContent = unidades;
    $("tReqs").textContent = reqs.filter(function(r){{ return r.checked; }}).length;
    guardar();
  }}

  function resumen(){{
    var L = [];
    var inst = $("inst").value.trim(), curso = $("curso").value.trim();
    L.push("SOLICITUD DE PROPUESTA · DESARROLLOS AP");
    if(inst)  L.push("Institución: " + inst);
    if(curso) L.push("Curso: " + curso);
    ["programa","docente","contacto","correo","telefono","estudiantes","cohortes",
     "semanas","parciales","sesiones","inicio","lms","url"].forEach(function(k){{
      var el = $(k);
      if(el && el.value.trim()){{
        var lab = el.previousElementSibling ? el.previousElementSibling.textContent : k;
        L.push(lab + ": " + el.value.trim());
      }}
    }});

    var partida = [];
    ["p-parcelacion","p-aula","p-material","p-videos","p-banco","p-h5p","p-cero","p-migracion"]
      .forEach(function(k){{
        var el = $(k);
        if(el && el.checked) partida.push(el.parentElement.textContent.trim());
      }});
    if(partida.length){{ L.push("", "PUNTO DE PARTIDA"); partida.forEach(function(p){{ L.push("  - " + p); }}); }}

    L.push("", "RECURSOS SOLICITADOS");
    var porFam = {{}};
    cants.forEach(function(i){{
      var v = parseInt(i.value, 10);
      if(!isFinite(v) || v <= 0) return;
      var tr = i.closest("tr");
      var fam = i.closest("section").querySelector("h2").textContent.trim();
      var nom = tr.querySelector("strong").textContent.trim();
      var th = i.closest("table").querySelectorAll("thead th");
      var idx = [].indexOf.call(tr.children, i.closest("td"));
      var etq = th[idx] ? th[idx].textContent.trim() : "";
      if(etq && etq.toLowerCase() !== "cantidad") nom += " (" + etq + ")";
      (porFam[fam] = porFam[fam] || []).push("  - " + nom + " x " + v +
        "   [" + i.dataset.cod + "]");
    }});
    Object.keys(porFam).forEach(function(f){{
      L.push("", f);
      porFam[f].forEach(function(l){{ L.push(l); }});
    }});
    if(!Object.keys(porFam).length) L.push("  (ninguno marcado)");

    var rs = reqs.filter(function(r){{ return r.checked; }})
                 .map(function(r){{ return "  - " + r.parentElement.textContent.trim(); }});
    if(rs.length){{ L.push("", "REQUERIMIENTOS ESPECIALES"); rs.forEach(function(l){{ L.push(l); }}); }}

    var o = $("obs").value.trim();
    if(o) L.push("", "OBSERVACIONES", o);

    L.push("", "Total: " + $("tTipos").textContent + " tipos, " +
           $("tUnidades").textContent + " unidades.");
    return L.join("\\n");
  }}

  cants.forEach(function(i){{ i.addEventListener("input", recalcular); }});
  reqs.forEach(function(r){{ r.addEventListener("change", recalcular); }});
  [].forEach.call(document.querySelectorAll("input,textarea"), function(el){{
    el.addEventListener("change", guardar);
    el.addEventListener("input", guardar);
  }});

  $("btnImprimir").addEventListener("click", function(){{ window.print(); }});

  $("btnCopiar").addEventListener("click", function(){{
    var t = resumen(), btn = this, txt = btn.textContent;
    function fin(ok){{
      btn.textContent = ok ? "Copiado" : "Copie manualmente";
      setTimeout(function(){{ btn.textContent = txt; }}, 2200);
    }}
    if(navigator.clipboard && navigator.clipboard.writeText){{
      navigator.clipboard.writeText(t).then(function(){{ fin(true); }}, function(){{ fin(false); }});
    }} else {{
      var ta = document.createElement("textarea");
      ta.value = t; document.body.appendChild(ta); ta.select();
      try {{ document.execCommand("copy"); fin(true); }} catch(e){{ fin(false); }}
      ta.remove();
    }}
  }});

  $("btnLimpiar").addEventListener("click", function(){{
    if(!confirm("¿Borrar todo lo diligenciado?")) return;
    [].forEach.call(document.querySelectorAll("input,textarea"), function(el){{
      if(el.type === "checkbox") el.checked = false; else el.value = "";
    }});
    try {{ localStorage.removeItem("ap-formulario"); }} catch(e){{}}
    recalcular();
  }});

  restaurar();
  recalcular();
}})();
</script>
</body>
</html>
"""


def version_artifact(doc: str) -> str:
    """El publicador de Artifacts envuelve la página: aquí se quita el envoltorio."""
    for fuera in ("<!DOCTYPE html>", '<html lang="es">', "<head>", "</head>",
                  "<body>", "</body>", "</html>",
                  '<meta charset="utf-8">',
                  '<meta name="viewport" content="width=device-width, initial-scale=1">'):
        doc = doc.replace(fuera, "")
    # En la galería de Artifacts el título es un nombre corto, no el del documento.
    doc = doc.replace(
        "<title>Formulario de levantamiento de necesidades · Desarrollos AP</title>",
        "<title>Levantamiento de Necesidades AP</title>")
    return "\n".join(l for l in doc.splitlines() if l.strip()) + "\n"


def main() -> None:
    doc = construir()
    salidas = {
        RAIZ / "herramientas" / "formulario_necesidades.html": doc,
        RAIZ / "herramientas" / "formulario_necesidades.artifact.html": version_artifact(doc),
    }
    for destino, contenido in salidas.items():
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(contenido, encoding="utf-8")
        kb = len(contenido.encode()) / 1024
        print(f"escrito {destino.relative_to(RAIZ)} ({kb:.1f} KB)")


if __name__ == "__main__":
    main()
