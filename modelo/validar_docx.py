import zipfile, sys
from lxml import etree
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
SEC = {
 "pPr":  ["pStyle","keepNext","keepLines","pageBreakBefore","framePr","widowControl",
          "numPr","suppressLineNumbers","pBdr","shd","tabs","spacing","ind",
          "contextualSpacing","jc","outlineLvl","rPr","sectPr"],
 "rPr":  ["rStyle","rFonts","b","bCs","i","iCs","caps","smallCaps","strike","color",
          "spacing","w","kern","position","sz","szCs","highlight","u"],
 "tblPr":["tblStyle","tblpPr","tblOverlap","bidiVisual","tblW","jc","tblCellSpacing",
          "tblInd","tblBorders","shd","tblLayout","tblCellMar","tblLook"],
 "tcPr": ["cnfStyle","tcW","gridSpan","hMerge","vMerge","tcBorders","shd","noWrap",
          "tcMar","textDirection","tcFitText","vAlign","hideMark"],
}
def validar(f):
    z = zipfile.ZipFile(f)
    fallos = []
    if z.testzip(): fallos.append("ZIP corrupto")
    if z.namelist()[0] != "[Content_Types].xml":
        fallos.append("[Content_Types].xml no es la primera entrada")
    for n in z.namelist():
        try: etree.fromstring(z.read(n))
        except Exception as e: fallos.append(f"XML inválido en {n}: {e}")
    x = etree.fromstring(z.read("word/document.xml"))
    for padre, orden in SEC.items():
        for nodo in x.iter(W + padre):
            idx, prev = -1, None
            for h in nodo:
                nm = etree.QName(h).localname
                if nm not in orden: fallos.append(f"<w:{padre}> hijo no previsto <w:{nm}>"); continue
                i = orden.index(nm)
                if i < idx: fallos.append(f"<w:{padre}>: <w:{nm}> después de <w:{prev}>")
                idx, prev = i, nm
    for t in x.iter(W + "tbl"):
        hijos = [etree.QName(h).localname for h in t]
        if hijos[:2] != ["tblPr", "tblGrid"]: fallos.append("w:tbl sin tblPr+tblGrid: " + str(hijos[:3]))
        ncols = len(t.find(W+"tblGrid"))
        for tr in t.iter(W+"tr"):
            n = len([c for c in tr if etree.QName(c).localname == "tc"])
            if n != ncols: fallos.append(f"fila con {n} celdas pero tblGrid declara {ncols}")
    for tag in ("p", "r"):
        pr = tag + "Pr"
        for n in x.iter(W + tag):
            hijos = [etree.QName(h).localname for h in n]
            if pr in hijos and hijos[0] != pr: fallos.append(f"<w:{pr}> no es el primer hijo de <w:{tag}>")
    body = x.find(W + "body")
    if etree.QName(body[-1]).localname != "sectPr": fallos.append("sectPr no cierra el body")
    return fallos
for f in sys.argv[1:]:
    fa = validar(f)
    print(f"{f}: {'OK' if not fa else str(len(fa)) + ' fallos'}")
    for x in dict.fromkeys(fa): print("   ", x)
