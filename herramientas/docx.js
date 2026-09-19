/* Escritor de .docx sin dependencias.
   Un .docx es un ZIP con partes OOXML. Aquí se arman las cuatro partes mínimas
   que Word necesita y se empaquetan con un ZIP propio (método STORE, sin
   compresión), de modo que la página no depende de ninguna librería externa. */
var DocxMini = (function(){
  "use strict";

  /* ---------------------------------------------------------------- ZIP ---*/

  var TABLA_CRC = (function(){
    var t = new Uint32Array(256), c, n, k;
    for(n = 0; n < 256; n++){
      c = n;
      for(k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      t[n] = c >>> 0;
    }
    return t;
  })();

  function crc32(bytes){
    var c = 0xFFFFFFFF;
    for(var i = 0; i < bytes.length; i++){
      c = TABLA_CRC[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
    }
    return (c ^ 0xFFFFFFFF) >>> 0;
  }

  function utf8(str){
    if(typeof TextEncoder !== "undefined") return new TextEncoder().encode(str);
    var s = unescape(encodeURIComponent(str)), a = new Uint8Array(s.length);
    for(var i = 0; i < s.length; i++) a[i] = s.charCodeAt(i);
    return a;
  }

  /** Empaqueta [{nombre, datos}] en un ZIP sin compresión. */
  function zip(entradas){
    var partes = [], central = [], offset = 0;
    var d = new Date();
    var hora = ((d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() / 2)) & 0xFFFF;
    var fecha = (((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate()) & 0xFFFF;

    function u8(n){ return [n & 255]; }
    function u16(n){ return [n & 255, (n >>> 8) & 255]; }
    function u32(n){ return [n & 255, (n >>> 8) & 255, (n >>> 16) & 255, (n >>> 24) & 255]; }

    entradas.forEach(function(e){
      var nombre = utf8(e.nombre), datos = e.datos, crc = crc32(datos);
      var local = [].concat(
        u32(0x04034b50), u16(20), u16(0), u16(0),   // firma, versión, flags, método STORE
        u16(hora), u16(fecha), u32(crc),
        u32(datos.length), u32(datos.length),
        u16(nombre.length), u16(0));
      partes.push(new Uint8Array(local), nombre, datos);

      central.push([].concat(
        u32(0x02014b50), u16(20), u16(20), u16(0), u16(0),
        u16(hora), u16(fecha), u32(crc),
        u32(datos.length), u32(datos.length),
        u16(nombre.length), u16(0), u16(0), u16(0), u16(0),
        u32(0), u32(offset)));
      central[central.length - 1].nombre = nombre;
      offset += local.length + nombre.length + datos.length;
    });

    var inicioCentral = offset, tamCentral = 0;
    central.forEach(function(c){
      partes.push(new Uint8Array(c), c.nombre);
      tamCentral += c.length + c.nombre.length;
    });

    partes.push(new Uint8Array([].concat(
      u32(0x06054b50), u16(0), u16(0),
      u16(entradas.length), u16(entradas.length),
      u32(tamCentral), u32(inicioCentral), u16(0))));

    var total = partes.reduce(function(s, p){ return s + p.length; }, 0);
    var salida = new Uint8Array(total), pos = 0;
    partes.forEach(function(p){ salida.set(p, pos); pos += p.length; });
    return salida;
  }

  /* -------------------------------------------------------------- OOXML ---*/

  var NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main";
  var XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n';

  function esc(s){
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /** Un run: texto con formato. */
  function run(texto, op){
    op = op || {};
    // El orden de los hijos de <w:rPr> lo fija el esquema (CT_RPr):
    // rFonts, b, i, caps, color, sz. Alterarlo hace que validadores estrictos
    // rechacen el documento.
    var pr = "";
    if(op.font) pr += '<w:rFonts w:ascii="' + op.font + '" w:hAnsi="' + op.font + '"/>';
    if(op.bold) pr += "<w:b/>";
    if(op.italic) pr += "<w:i/>";
    if(op.caps) pr += "<w:caps/>";
    if(op.color) pr += '<w:color w:val="' + op.color.replace("#", "") + '"/>';
    if(op.size) pr += '<w:sz w:val="' + (op.size * 2) + '"/>';   // half-points
    if(pr) pr = "<w:rPr>" + pr + "</w:rPr>";
    // xml:space preserva los espacios de los extremos
    return "<w:r>" + pr + '<w:t xml:space="preserve">' + esc(texto) + "</w:t></w:r>";
  }

  function Doc(){
    this.cuerpo = [];
  }

  /** Párrafo. `op.runs` permite varios formatos en la misma línea. */
  Doc.prototype.parrafo = function(texto, op){
    op = op || {};
    // Orden fijado por el esquema (CT_PPr): pStyle, pBdr, shd, spacing, ind, jc.
    var pr = "";
    if(op.estilo) pr += '<w:pStyle w:val="' + op.estilo + '"/>';
    if(op.bordeInferior){
      pr += '<w:pBdr><w:bottom w:val="single" w:sz="' + (op.bordeGrosor || 6) +
            '" w:space="4" w:color="' + (op.bordeColor || "0A6357").replace("#", "") +
            '"/></w:pBdr>';
    }
    if(op.sombreado){
      pr += '<w:shd w:val="clear" w:fill="' + op.sombreado.replace("#", "") + '"/>';
    }
    if(op.espacioAntes || op.espacioDespues){
      pr += '<w:spacing' +
        (op.espacioAntes ? ' w:before="' + op.espacioAntes + '"' : "") +
        (op.espacioDespues ? ' w:after="' + op.espacioDespues + '"' : "") + "/>";
    }
    if(op.sangria) pr += '<w:ind w:left="' + op.sangria + '"/>';
    if(op.align) pr += '<w:jc w:val="' + op.align + '"/>';
    if(pr) pr = "<w:pPr>" + pr + "</w:pPr>";

    var contenido = op.runs
      ? op.runs.map(function(r){ return run(r[0], r[1]); }).join("")
      : run(texto, op);
    this.cuerpo.push("<w:p>" + pr + contenido + "</w:p>");
    return this;
  };

  Doc.prototype.titulo = function(t){
    return this.parrafo(t, {estilo: "Titulo", size: 26, bold: true, color: "16222E"});
  };

  Doc.prototype.h1 = function(t){
    return this.parrafo(t, {size: 13, bold: true, color: "0A6357", caps: true,
                            espacioAntes: 260, espacioDespues: 100});
  };

  Doc.prototype.espacio = function(alto){
    this.cuerpo.push('<w:p><w:pPr><w:spacing w:after="' + (alto || 120) +
                     '"/></w:pPr></w:p>');
    return this;
  };

  /**
   * Tabla. `filas` es una matriz de celdas; cada celda es string u objeto
   * {texto, bold, align, color, fondo, ancho}. `op.encabezado` marca la
   * primera fila como cabecera repetible.
   */
  Doc.prototype.tabla = function(filas, op){
    op = op || {};
    var anchos = op.anchos || null;
    var borde = (op.borde || "D6DEE5").replace("#", "");
    var xml = ['<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/>',
      '<w:tblBorders>',
      ['top', 'left', 'bottom', 'right', 'insideH', 'insideV'].map(function(l){
        return '<w:' + l + ' w:val="single" w:sz="' + (op.grosor || 4) +
               '" w:space="0" w:color="' + borde + '"/>';
      }).join(""),
      '</w:tblBorders>',
      '<w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/>',
      '<w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar>',
      '</w:tblPr>'];

    // El esquema OOXML exige <w:tblGrid>; sin él Word repagina mal las columnas
    // y los lectores estrictos rechazan el documento.
    var nCols = filas.reduce(function(m, f){ return Math.max(m, f.length); }, 0);
    if(nCols){
      var util = 12240 - 1021 - 1021;   // ancho de carta menos márgenes, en twips
      var pesos = [];
      var suma = 0;
      for(var i = 0; i < nCols; i++){
        var w = (anchos && anchos[i]) ? Number(anchos[i]) : (5000 / nCols);
        pesos.push(w); suma += w;
      }
      xml.push("<w:tblGrid>" + pesos.map(function(w){
        return '<w:gridCol w:w="' + Math.round(util * w / suma) + '"/>';
      }).join("") + "</w:tblGrid>");
    }

    filas.forEach(function(fila, iFila){
      var cabecera = op.encabezado && iFila === 0;
      xml.push("<w:tr>");
      if(cabecera) xml.push("<w:trPr><w:tblHeader/></w:trPr>");
      fila.forEach(function(celda, iCol){
        var c = (typeof celda === "object" && celda !== null) ? celda : {texto: celda};
        var tcPr = "";
        if(anchos && anchos[iCol]) tcPr += '<w:tcW w:w="' + anchos[iCol] + '" w:type="pct"/>';
        var fondo = c.fondo || (cabecera ? op.fondoEncabezado : null);
        if(fondo) tcPr += '<w:shd w:val="clear" w:fill="' + fondo.replace("#", "") + '"/>';
        tcPr += '<w:vAlign w:val="center"/>';
        var pPr = "";
        if(c.align) pPr = '<w:pPr><w:jc w:val="' + c.align + '"/></w:pPr>';
        xml.push("<w:tc><w:tcPr>" + tcPr + "</w:tcPr><w:p>" + pPr +
          run(c.texto, {bold: c.bold || cabecera, color: c.color,
                        size: c.size || op.size, caps: cabecera && op.capsEncabezado}) +
          "</w:p></w:tc>");
      });
      xml.push("</w:tr>");
    });
    xml.push("</w:tbl>");
    this.cuerpo.push(xml.join(""));
    // Word necesita un párrafo tras la tabla para no pegar el contenido siguiente.
    this.cuerpo.push('<w:p><w:pPr><w:spacing w:after="60"/></w:pPr></w:p>');
    return this;
  };

  Doc.prototype.vinieta = function(texto, op){
    op = op || {};
    return this.parrafo("•  " + texto, {
      sangria: op.sangria || 220, size: op.size || 10,
      color: op.color, espacioDespues: op.espacioDespues || 60});
  };

  Doc.prototype.xmlDocumento = function(){
    return XML + '<w:document xmlns:w="' + NS_W + '"><w:body>' +
      this.cuerpo.join("") +
      '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>' +          // carta
      '<w:pgMar w:top="1134" w:right="1021" w:bottom="1134" w:left="1021" ' +
      'w:header="567" w:footer="567" w:gutter="0"/></w:sectPr>' +
      "</w:body></w:document>";
  };

  var ESTILOS = XML +
    '<w:styles xmlns:w="' + NS_W + '">' +
    '<w:docDefaults><w:rPrDefault><w:rPr>' +
    '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>' +
    '<w:sz w:val="20"/><w:szCs w:val="20"/><w:lang w:val="es-CO"/>' +
    '</w:rPr></w:rPrDefault>' +
    '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/>' +
    '</w:pPr></w:pPrDefault></w:docDefaults>' +
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">' +
    '<w:name w:val="Normal"/><w:qFormat/></w:style>' +
    '<w:style w:type="paragraph" w:styleId="Titulo">' +
    '<w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/>' +
    '<w:pPr><w:spacing w:after="80"/></w:pPr>' +
    '<w:rPr><w:b/><w:sz w:val="52"/></w:rPr></w:style>' +
    '</w:styles>';

  var CONTENT_TYPES = XML +
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' +
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' +
    '<Default Extension="xml" ContentType="application/xml"/>' +
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>' +
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>' +
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>' +
    '</Types>';

  var RELS = XML +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>' +
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>' +
    '</Relationships>';

  var RELS_DOC = XML +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' +
    '</Relationships>';

  function propiedades(titulo, autor){
    var ahora = new Date().toISOString().replace(/\.\d+Z$/, "Z");
    return XML +
      '<cp:coreProperties ' +
      'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" ' +
      'xmlns:dc="http://purl.org/dc/elements/1.1/" ' +
      'xmlns:dcterms="http://purl.org/dc/terms/" ' +
      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
      "<dc:title>" + esc(titulo) + "</dc:title>" +
      "<dc:creator>" + esc(autor) + "</dc:creator>" +
      "<cp:lastModifiedBy>" + esc(autor) + "</cp:lastModifiedBy>" +
      '<dcterms:created xsi:type="dcterms:W3CDTF">' + ahora + "</dcterms:created>" +
      '<dcterms:modified xsi:type="dcterms:W3CDTF">' + ahora + "</dcterms:modified>" +
      "</cp:coreProperties>";
  }

  /** Devuelve el .docx como Blob. */
  Doc.prototype.blob = function(op){
    op = op || {};
    var entradas = [
      {nombre: "[Content_Types].xml", datos: utf8(CONTENT_TYPES)},
      {nombre: "_rels/.rels", datos: utf8(RELS)},
      {nombre: "docProps/core.xml",
       datos: utf8(propiedades(op.titulo || "Documento", op.autor || "Desarrollos AP"))},
      {nombre: "word/_rels/document.xml.rels", datos: utf8(RELS_DOC)},
      {nombre: "word/document.xml", datos: utf8(this.xmlDocumento())},
      {nombre: "word/styles.xml", datos: utf8(ESTILOS)}
    ];
    return new Blob([zip(entradas)], {
      type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    });
  };

  return {Doc: Doc, esc: esc};
})();
