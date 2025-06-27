from lib.comprobante_fiscal_sat import ComprobanteFiscal
from pathlib import Path

filepath = Path("C:\\Users\\evalli\\Downloads\\VAME890407PG8_EMITIDOS_2024")

for file in filepath.iterdir():
    c = ComprobanteFiscal.convertirxml(str(file))

    print(c.complementos)