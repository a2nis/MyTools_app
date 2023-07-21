#!/usr/bin/env python3.10

from .Sheets import Sheets
from PIL import Image
import re
import urllib.request
import os
import zipfile

class Procesar():
  def __init__(self, comercio, sucursal, caja):
    self.comercio = comercio
    self.sucursal = sucursal
    self.caja = caja
    self.nombre_excel = obtener_data_comercio(self.comercio)
    self.lista_sucursal , self.lista_caja = Sheets().data_sheets(self.nombre_excel)
    self.coincide_caja = False
        
  def numeros_cadena(self, sentence):
    '''Devuelve en una `lista` los `números
      de string` dado
    '''
    s = [float(s) for s in re.findall(r'-?\d+\.?\d*', sentence)]
    return s
  
  def elimina_archivos(dir_path):
    '''`Elimina` archivos 
      del directorio `Salida`
    '''
    # Especificar el directorio del cual deseas eliminar los archivos
    # dir_path = "Salida/"
    # Recorrer todos los archivos del directorio y eliminarlos
    for file_name in os.listdir(dir_path):
      file_path = os.path.join(dir_path, file_name)
      try:
        if os.path.isfile(file_path):
          os.remove(file_path)
          print(f"{file_path} eliminado exitosamente.")
      except Exception as e:
        print(f"No se pudo eliminar {file_path}: {e}")
  
  def comprime_archivos():
    '''`Comprime` archivos 
      del directorio `Salida`
    '''
    # Especificar el directorio que deseas comprimir
    dir_path = "Salida/"
    # Especificar el nombre del archivo ZIP que se creará
    zip_file_name = "nombre_del_archivo.zip"

    # Crear un objeto ZipFile en modo escritura y agregar todos los archivos del directorio
    with zipfile.ZipFile(zip_file_name, "w") as zip_file:
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                zip_file.write(file_path, file_name)
    print(f"Todos los archivos en {dir_path} han sido comprimidos en {zip_file_name}.")  
  
  def insert_sucursales(self):
    '''Devuelve `string` con los insert 
      de la sucursal o sucursales 
    '''
    if len(self.lista_sucursal) > 0:
      comercio = self.comercio
      valores_insert = "INSERT INTO `MP_Sucursales`(`CodigoComercio`,`codigoSucursal`,`pz_external_store_id`,`mp_store_id`) VALUES "
      match comercio:
        case "DISCO" | "FROG" | "KINKO" | "KINKO200" | "KINKO202" | "MAH" | "BAS":
          for i in self.lista_sucursal:
            external_id_suc = self.numeros_cadena(i.external_id_suc)
            if not len(external_id_suc) > 0:
              continue
            if self.sucursal==999:
              valores_insert += f'("{comercio}", {int(external_id_suc[0])}, "{i.external_id_suc}", "{i.store_id}"),'
            elif int(external_id_suc[0])==self.sucursal:
              valores_insert += f'("{comercio}", {int(external_id_suc[0])}, "{i.external_id_suc}", "{i.store_id}"),'
        case "TATA":
          for i in self.lista_sucursal:
            external_id_suc = self.numeros_cadena(i.external_id_suc)
            if not len(external_id_suc) > 0:
              continue
            if self.sucursal==999 and int(external_id_suc[0]) > 199:
              valores_insert += f'("{comercio}", {int(external_id_suc[0])}, "{i.external_id_suc}", "{i.store_id}"),'
            elif self.sucursal==999 and int(external_id_suc[0]) < 199:
              valores_insert += f'("{comercio}", {int(external_id_suc[0]) - 100}, "{i.external_id_suc}", "{i.store_id}"),'
            elif int(external_id_suc[0])==self.sucursal and int(external_id_suc[0]) > 199:
              valores_insert += f'("{comercio}", {int(external_id_suc[0])}, "{i.external_id_suc}", "{i.store_id}"),'
            elif int(external_id_suc[0])==self.sucursal and int(external_id_suc[0]) < 199:
              valores_insert += f'("{comercio}", {int(external_id_suc[0]) - 100}, "{i.external_id_suc}", "{i.store_id}"),'
        case _:
            print("\033[1;32;48m -> Comercio no definido \033[0;37;48m")
      if len(valores_insert) > 107:
        self.coincide_caja = True        
        result = valores_insert.rstrip(valores_insert[-1]) + ";"
        with open("Salida/Insert_BD.txt", "w") as archivo:
          archivo.write(result)
          return result
      else:
        print("\033[1;32;48m -> Sucursal no definida \033[0;37;48m")
  
  def insert_cajas(self): 
    '''Devuelve `string` con los insert 
      de las cajas
    '''
    if len(self.lista_caja) > 0:
      comercio = self.comercio 
      valores_insert = "INSERT INTO `MP_Cajas`(`CodigoComercio`,`codigoSucursal`,`codigoCaja`,`pz_external_pos_id`,`mp_pos_id`,`mp_qr_image_url`,`mp_qr_pdf_url`) VALUES "
      match comercio:
        case "DISCO" | "FROG" | "KINKO" | "KINKO200" | "KINKO202" | "MAH" | "BAS":
          for i in self.lista_caja:
            external_id = self.numeros_cadena(i.external_id)
            if not len(external_id) == 2:
              continue
            if self.sucursal==999 :
              valores_insert += f'("{comercio}", {int(external_id[0])}, {int(external_id[1])}, "{i.external_id}", "{i.id}", "{i.qr_image}", "{i.qr_pdf}"),'
            elif int(external_id[0])==self.sucursal and self.caja==999:
              valores_insert += f'("{comercio}", {int(external_id[0])}, {int(external_id[1])}, "{i.external_id}", "{i.id}", "{i.qr_image}", "{i.qr_pdf}"),'
            elif int(external_id[0])==self.sucursal and external_id[1]==self.caja:
              valores_insert += f'("{comercio}", {int(external_id[0])}, {int(external_id[1])}, "{i.external_id}", "{i.id}", "{i.qr_image}", "{i.qr_pdf}"),'
        case "TATA":
          for i in self.lista_caja:
            external_id = self.numeros_cadena(i.external_id)
            if not len(external_id) == 2:
              continue
            if self.sucursal==999 and int(external_id[0]) > 199:
              valores_insert += f'("{comercio}", {int(external_id[0])}, {int(external_id[1])}, "{i.external_id}", "{i.id}", "{i.qr_image}", "{i.qr_pdf}"),'
            elif self.sucursal==999 and int(external_id[0]) < 199:
              valores_insert += f'("{comercio}", {int(external_id[0]) - 100}, {int(external_id[1])}, "{i.external_id}", "{i.id}", "{i.qr_image}", "{i.qr_pdf}"),'
            elif int(external_id[0])==self.sucursal and self.caja==999 and int(external_id[0]) > 199 :
              valores_insert += f'("{comercio}", {int(external_id[0])}, {int(external_id[1])}, "{i.external_id}", "{i.id}", "{i.qr_image}", "{i.qr_pdf}"),'
            elif int(external_id[0])==self.sucursal and external_id[1]==self.caja and int(external_id[0]) > 199 :
              valores_insert += f'("{comercio}", {int(external_id[0])}, {int(external_id[1])}, "{i.external_id}", "{i.id}", "{i.qr_image}", "{i.qr_pdf}"),'
            elif int(external_id[0])==self.sucursal and external_id[1]==self.caja and int(external_id[0]) < 199:
              valores_insert += f'("{comercio}", {int(external_id[0]) - 100}, {int(external_id[1])}, "{i.external_id}", "{i.id}", "{i.qr_image}", "{i.qr_pdf}"),'
            elif int(external_id[0])==self.sucursal and self.caja==999 and int(external_id[0]) < 199:
              valores_insert += f'("{comercio}", {int(external_id[0]) - 100}, {int(external_id[1])}, "{i.external_id}", "{i.id}", "{i.qr_image}", "{i.qr_pdf}"),'
        case _:
          print("\033[1;32;48m -> Comercio no definido \033[0;37;48m")
      if len(valores_insert) > 145:
        result = valores_insert.rstrip(valores_insert[-1]) + ";"
        with open("Salida/Insert_BD.txt", "a") as archivo:
          archivo.write('\n' +'\n' + result )
          return result
      else:
        print("\033[1;32;48m -> Cajas no definidas \033[0;37;48m")
        
  def descargar_ajusta_imagen(self, url_imagen, qr_pdf ,external_id): 
    '''Descarga `imagen QR` según criterio de entrada
    '''
    lista_numeros = self.numeros_cadena(external_id)
    if(lista_numeros[0] >= 100 and lista_numeros[0] < 200):
      titulo = int((lista_numeros[0]-100) * 100000 + 100000000 + lista_numeros[1])
    else:
      titulo = int(lista_numeros[0] * 100000 + 100000000 + lista_numeros[1])
      
    urllib.request.urlretrieve(f"{qr_pdf}", f"Salida/{external_id}.pdf")
    urllib.request.urlretrieve(f"{url_imagen}", "png_a_procesar.png")
    image = Image.open('png_a_procesar.png')
    resized = image.resize((135, 135))
    resized.save(f'Salida/QR_{titulo}.png')

  def imagen_qr(self): 
    '''Descarga `imagen QR` según criterio de entrada
    '''
    for i in self.lista_caja:
      external_id = self.numeros_cadena(i.external_id)
      if not len(external_id) == 2:
        continue
      if self.sucursal==999 :
        continue
      if int(external_id[0])==self.sucursal and (int(external_id[1]==self.caja) or self.caja==999):
        self.descargar_ajusta_imagen(i.qr_image, i.qr_pdf ,i.external_id)
    if os.path.exists('png_a_procesar.png'):
      os.remove('png_a_procesar.png')

def obtener_data_comercio(valor):
  '''Obtiene `User ID` del campo `B10`
     del excel para determinar `Comercio`
     @return \DIS\FROG...
  '''
  comercio = {
    "DISCO": "Mercado_Pago_DISCO",
    "FROG": "Mercado_Pago_FROG",
    "KINKO": "Mercado_Pago_KINKO",
    "KINKO200": "Mercado_Pago_KINKO200",
    "KINKO202": "Mercado_Pago_KINKO202",
    "TATA": "TATA_Mercado_Pago",
    "MAH": "MAH_Mercado_Pago",
    "BAS": "BAS_Mercado_Pago"
  }
  return comercio[valor]
