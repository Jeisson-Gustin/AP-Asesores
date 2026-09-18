/* Escritor de PDF sin dependencias.
   Genera PDF 1.4 con las fuentes base Helvetica y Helvetica-Bold, que no
   requieren incrustación. Suficiente para un reporte de cotización: texto,
   líneas, rectángulos y tablas. Evita depender de un CDN en tiempo de uso. */
var PDFMini = (function(){
  "use strict";

  /* Anchos AFM de Helvetica (unidades de 1/1000 em) para ASCII imprimible.
     Los caracteres acentuados usan el ancho de su letra base, que en
     Helvetica coincide. */
  var W_REG = [278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,
    556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,
    1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,
    667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,
    333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,
    556,556,333,500,278,556,500,722,500,500,500,334,260,334,584];
  var W_BOLD = [278,333,474,556,556,889,722,238,333,333,389,584,278,333,278,278,
    556,556,556,556,556,556,556,556,556,556,333,333,584,584,584,611,
    975,722,722,722,722,667,611,778,722,278,556,722,611,833,722,778,
    667,778,722,667,611,722,667,944,667,667,611,333,278,333,584,556,
    333,556,611,556,611,556,333,611,611,278,278,556,278,889,611,611,
    611,611,389,556,333,611,556,778,556,556,500,389,280,389,584];

  /* Letra base de cada acentuado, para tomar su ancho. */
  var BASE = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ü":"u","ñ":"n","Á":"A",
    "É":"E","Í":"I","Ó":"O","Ú":"U","Ñ":"N","¿":"?","¡":"!","°":"o","º":"o","·":"."};

  /* Caracteres fuera de WinAnsi que hay que sustituir antes de escribir. */
  function limpiar(s){
    return String(s == null ? "" : s)
      .replace(/[—–−]/g, "-")
      .replace(/[“”]/g, '"')
      .replace(/[‘’]/g, "'")
      .replace(/…/g, "...")
      .replace(/ /g, " ")
      .replace(/[ -‏]/g, " ");
  }

  function anchoChar(ch, bold){
    var c = ch.charCodeAt(0);
    if(c > 126){
      var b = BASE[ch];
      if(b) return anchoChar(b, bold);
      return bold ? W_BOLD[65] : W_REG[65];  // ancho medio de respaldo
    }
    if(c < 32) return 0;
    return (bold ? W_BOLD : W_REG)[c - 32];
  }

  function ancho(texto, size, bold){
    var t = limpiar(texto), s = 0;
    for(var i = 0; i < t.length; i++) s += anchoChar(t.charAt(i), bold);
    return s * size / 1000;
  }

  function escapar(s){
    return limpiar(s).replace(/\\/g, "\\\\").replace(/\(/g, "\\(").replace(/\)/g, "\\)");
  }

  /* --- documento --- */
  function Doc(opciones){
    var o = opciones || {};
    this.ancho = o.ancho || 612;      // carta
    this.alto  = o.alto  || 792;
    this.margen = o.margen || 54;
    this.paginas = [];
    this.pieDe = o.pieDe || null;     // función(doc, numero) para el pie
    this.nuevaPagina();
  }

  Doc.prototype.nuevaPagina = function(){
    this.ops = [];
    this.paginas.push(this.ops);
    this.y = this.margen;
    return this;
  };

  Doc.prototype.espacio = function(){ return this.alto - this.margen - this.y; };

  /** Salta de página si no caben `alto` puntos. */
  Doc.prototype.asegurar = function(alto){
    if(this.espacio() < alto) this.nuevaPagina();
    return this;
  };

  Doc.prototype.color = function(hex){
    var n = parseInt(hex.slice(1), 16);
    return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
  };

  /** Escribe una línea de texto. Devuelve el ancho ocupado. */
  Doc.prototype.texto = function(x, texto, op){
    op = op || {};
    var size = op.size || 10, bold = !!op.bold;
    var c = this.color(op.color || "#000000");
    var t = escapar(texto);
    var w = ancho(texto, size, bold);
    var px = x;
    if(op.align === "right") px = x - w;
    else if(op.align === "center") px = x - w / 2;
    var py = this.alto - (op.y != null ? op.y : this.y) - size;
    this.ops.push("BT /" + (bold ? "F2" : "F1") + " " + size + " Tf " +
      c[0].toFixed(3) + " " + c[1].toFixed(3) + " " + c[2].toFixed(3) + " rg " +
      px.toFixed(2) + " " + py.toFixed(2) + " Td (" + t + ") Tj ET");
    return w;
  };

  /** Texto con ajuste de línea dentro de un ancho dado. Avanza this.y. */
  Doc.prototype.parrafo = function(x, maxAncho, texto, op){
    op = op || {};
    var size = op.size || 10, bold = !!op.bold;
    var interlinea = op.interlinea || size * 1.42;
    var palabras = limpiar(texto).split(/\s+/).filter(Boolean);
    var linea = "";
    for(var i = 0; i < palabras.length; i++){
      var prueba = linea ? linea + " " + palabras[i] : palabras[i];
      if(ancho(prueba, size, bold) > maxAncho && linea){
        this.asegurar(interlinea);
        this.texto(x, linea, op);
        this.y += interlinea;
        linea = palabras[i];
      } else {
        linea = prueba;
      }
    }
    if(linea){
      this.asegurar(interlinea);
      this.texto(x, linea, op);
      this.y += interlinea;
    }
    return this;
  };

  Doc.prototype.linea = function(x1, y1, x2, y2, grosor, color){
    var c = this.color(color || "#cccccc");
    this.ops.push(c[0].toFixed(3) + " " + c[1].toFixed(3) + " " + c[2].toFixed(3) + " RG " +
      (grosor || 0.5) + " w " + x1.toFixed(2) + " " + (this.alto - y1).toFixed(2) + " m " +
      x2.toFixed(2) + " " + (this.alto - y2).toFixed(2) + " l S");
    return this;
  };

  Doc.prototype.rect = function(x, y, w, h, color){
    var c = this.color(color);
    this.ops.push(c[0].toFixed(3) + " " + c[1].toFixed(3) + " " + c[2].toFixed(3) + " rg " +
      x.toFixed(2) + " " + (this.alto - y - h).toFixed(2) + " " +
      w.toFixed(2) + " " + h.toFixed(2) + " re f");
    return this;
  };

  Doc.prototype.medir = ancho;

  /* --- serialización --- */
  function bytesLatin1(str){
    var out = [];
    for(var i = 0; i < str.length; i++){
      var c = str.charCodeAt(i);
      out.push(c > 255 ? 63 : c);   // '?' para lo que no cabe en un byte
    }
    return out;
  }

  Doc.prototype.blob = function(){
    var self = this;
    // Pie de página, una vez conocido el total de páginas.
    if(this.pieDe){
      var totalPag = this.paginas.length;
      this.paginas.forEach(function(ops, i){
        self.ops = ops;
        self.pieDe(self, i + 1, totalPag);
      });
    }

    var objetos = [];   // cuerpo de cada objeto, 1-indexado
    var nPag = this.paginas.length;
    var idPaginas = 2;
    var idContenido0 = 3;
    var idFuente1 = idContenido0 + nPag * 2;
    var idFuente2 = idFuente1 + 1;

    objetos.push("<< /Type /Catalog /Pages " + idPaginas + " 0 R >>");

    var kids = [];
    for(var i = 0; i < nPag; i++) kids.push((idContenido0 + i * 2) + " 0 R");
    objetos.push("<< /Type /Pages /Kids [" + kids.join(" ") + "] /Count " + nPag + " >>");

    for(var p = 0; p < nPag; p++){
      var idPag = idContenido0 + p * 2, idCont = idPag + 1;
      objetos.push("<< /Type /Page /Parent " + idPaginas + " 0 R /MediaBox [0 0 " +
        this.ancho + " " + this.alto + "] /Resources << /Font << /F1 " + idFuente1 +
        " 0 R /F2 " + idFuente2 + " 0 R >> >> /Contents " + idCont + " 0 R >>");
      var flujo = this.paginas[p].join("\n");
      objetos.push("<< /Length " + bytesLatin1(flujo).length + " >>\nstream\n" + flujo + "\nendstream");
    }

    objetos.push("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>");
    objetos.push("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>");

    var bytes = [], offsets = [];
    function empujar(s){ bytes = bytes.concat(bytesLatin1(s)); }

    empujar("%PDF-1.4\n%âãÏÓ\n");
    objetos.forEach(function(cuerpo, idx){
      offsets.push(bytes.length);
      empujar((idx + 1) + " 0 obj\n" + cuerpo + "\nendobj\n");
    });

    var inicioXref = bytes.length;
    var xref = "xref\n0 " + (objetos.length + 1) + "\n0000000000 65535 f \n";
    offsets.forEach(function(off){
      xref += ("0000000000" + off).slice(-10) + " 00000 n \n";
    });
    empujar(xref);
    empujar("trailer\n<< /Size " + (objetos.length + 1) + " /Root 1 0 R >>\nstartxref\n" +
      inicioXref + "\n%%EOF\n");

    return new Blob([new Uint8Array(bytes)], {type: "application/pdf"});
  };

  return { Doc: Doc, medir: ancho, limpiar: limpiar };
})();
