from lib.comprobante_fiscal_sat import ComprobanteFiscal
from pathlib import Path

filepath = Path("C:\\Users\\evalli\\Downloads\\RECIBIDOS")

csv_content = "UUID;FECHA TIMBRADO;RFC EMISOR;EMISOR;RFC RECEPTOR;RECEPTOR;"
csv_content += "SERIE;FOLIO;IMPUESTOS RETENIDOS;IMPUESTOS TRASLADADOS;TOTAL\n"

for file in filepath.iterdir():
    c = ComprobanteFiscal.convertirxml(str(file))
    if c is not None:
        data = [
            c.timbrefiscal.UUID,
            c.timbrefiscal.FechaTimbrado,
            c.emisor.Rfc,
            c.emisor.Nombre,
            c.receptor.Rfc,
            c.receptor.Nombre,
            c.comprobante.Serie,
            c.comprobante.Folio,
            c.comprobante.TotalImpuestosRetenidos,
            c.comprobante.TotalImpuestosTrasladados,
            c.comprobante.Total
        ]
        data = [str(i) for i in data]
        csv_content += ";".join(data) + "\n"

with open('reporte_cfdi.csv', 'w', encoding='utf-8') as f:
    f.write(csv_content)