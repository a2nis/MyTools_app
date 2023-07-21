import gspread
from .Sucursal import Sucursal
from .Caja import Caja

class Sheets:

  def data_sheets(self, excel_name):
    '''Devuelve listas con datos de `sucursal y cajas` 
    
      `@return`  [Lista de objetos de sucursal][Lista de objetos de caja]
    '''
    data_suc = []
    data_caja = []
    sa = gspread.service_account(filename="creds.json")
    sh = sa.open(excel_name)
    sucursales = sh.worksheet("Sucursales")
    cajas = sh.worksheet("Cajas y QR integrados")
    
    # Obtiene los campos `Store_ID y Identificador de sucursal externo`
    # del excel los agrega en una `lista de objetos`
    lista_sucursales = sucursales.get(f'B6:C{sucursales.row_count}')
    for i in range(len(lista_sucursales)):
      objeto_suc = Sucursal(int(lista_sucursales[i][0]), lista_sucursales[i][1])
      data_suc.append(objeto_suc)
    
    # Obtiene los campos `ID, External_id y QR Image`
    # del excel los agrega en una `lista de objetos`  
    lista_cajas = cajas.get(f'B6:J{cajas.row_count}')
    for i in range(len(lista_cajas)):
      objeto_caja = Caja(int(lista_cajas[i][0]), lista_cajas[i][2], lista_cajas[i][6], lista_cajas[i][8])
      data_caja.append(objeto_caja)
    return data_suc, data_caja