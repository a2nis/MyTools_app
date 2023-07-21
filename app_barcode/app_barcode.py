from flask import Blueprint, render_template, request, redirect, send_file
import re
from werkzeug.utils import secure_filename
import os
from mercado_pago.Procesar import Procesar
from moviepy.editor import ImageSequenceClip
from PIL import Image

#python -c "import sys; print(sys.path)"
import sys
sys.path.append(r"/home/jose/Escritorio/Flask_Tes/env/lib/python3.10/site-packages")
import barcode
from barcode.writer import ImageWriter

app_barcode = Blueprint("app_barcode", __name__, static_folder="static")

def generate_ean(value):
  images_dir = 'static/app_barcode/images/'
  if len(value) == 6:
    upc_e = barcode.get_barcode_class('upce')
    convert_upc = upc_e(value, writer=ImageWriter()) 
    generated_qr = convert_upc.save(f'{images_dir}{value}')
  if len(value) == 8:
    ean_8 = barcode.get_barcode_class('ean8')
    convert_ean = ean_8(value, writer=ImageWriter()) 
    generated_qr = convert_ean.save(f'{images_dir}{value}')
  if len(value) == 12:
    upc_a = barcode.get_barcode_class('upca')
    convert_upc = upc_a(value, writer=ImageWriter()) 
    generated_qr = convert_upc.save(f'{images_dir}{value}')
  if len(value) == 13: 
    hr = barcode.get_barcode_class('ean13')
    Hr = hr(value, writer=ImageWriter())  
    generated_qr = Hr.save(f'{images_dir}{value}')
  if len(value) == 7 or len(value) == 9 or len(value) == 11:
    code39 = barcode.get_barcode_class('code39')
    convert_upc = code39(value, add_checksum=False, writer=ImageWriter()) 
    generated_qr = convert_upc.save(f'{images_dir}{value}')

def remove_leading_zero(string):
  string = re.sub("^0+", "", string)
  return string

def is_integer(number):
  '''Return True if number is a integer number'''
  return number.is_integer()

def eanCheck(ean):
    checksum = 0
    for i, digit in enumerate(reversed(ean)):
        checksum += int(digit) * 3 if (i % 2 == 0) else int(digit)
    return (10 - (checksum % 10)) % 10

# print("Digito de control: %d" %eanCheck(EAN))

def generar_pesable(codigo_articulo, precio):
  #Mapeo el precio en el formato 123.45
  precio_sin_cero_izquierda = str(precio).lstrip('0')
  precio_con_dos_ceros_derecha = precio_sin_cero_izquierda + '00'
  partes = precio_con_dos_ceros_derecha.split('.')
  parte_entera = partes[0].zfill(3)
  parte_decimal = partes[1][:2]  # Tomar solo los primeros dos dígitos decimales
  parte_sin_check = f"26{codigo_articulo}{parte_entera}{parte_decimal}"
  cod_barra = f'{parte_sin_check}{eanCheck(parte_sin_check)}'
  return cod_barra
                    
def generar_video(lista_imagenes):
  # Directorio donde se encuentran las imágenes
  directorio = "static/app_barcode/images"
  dir_video = "static/app_barcode/video"
  lista = []

  # Se inserta imagen en blanco entre cada codigo de barra de la lista
  for elemento in lista_imagenes:
    lista.append(elemento)
    lista.append('blanco')

  # Insertar imagen Ingrese_cliente.png en las posiciones 1, 2 ... 12
  for i in range(1,12):
    lista.insert(i, 'Ingrese_cliente')
  
  # Se agrega el final de la lista la imagen de Fin
  lista.append('FIN')
  
  for i in lista:
    # abrir la imagen  
    imagen = Image.open(os.path.join(directorio, f'{i}.png'))
    # cambiar el tamaño de la imagen a 523 × 280 pixels
    nueva_imagen = imagen.resize((523, 280))
    # guardar la nueva imagen
    nueva_imagen.save(f'{dir_video}/{i}.png')

  # Definir duración de cada imagen en el video (en segundos)
  duracion_imagen = 1

  # Crear objeto ImageSequenceClip
  clip = ImageSequenceClip([os.path.join(dir_video, f'{imagen}.png') for imagen in lista], fps=1/duracion_imagen)

  # Definir nombre y ubicación del archivo de salida
  nombre_salida = "video_salida.mp4"
  ruta_salida = os.path.join(dir_video, nombre_salida)

  # Guardar el video
  clip.write_videofile(ruta_salida, codec="libx264", fps=30, bitrate="5000k")
  
@app_barcode.route('/')
def inicio():
  global no_file
  no_file = False
  return render_template('app_barcode/formulario.html', no_file=no_file)

@app_barcode.route('/imagenes')
def mostrar_imagenes():
  global mostrar_boton_video
  no_ticket = False
  with open('Salidapazosnuevo.txt', 'r') as f:
    tickets = {}
    barcodes = {}
    separator = {
      True : '#',
      False : '|'
    }
    for line in f:
      if not line.strip():
        continue
      if "#" in line:
        numeral_symbol = True
      if "|" in line:
        numeral_symbol = False
      values_line = line.split(separator[numeral_symbol])
      if (values_line[0] == "C" and values_line[1] == "1" and values_line[3] == number) or (values_line[0] == "C" and values_line[1] == "1"):
        ticket_number = values_line[3]
        tickets[ticket_number] = {'cashier_code': values_line[2], 'number_of_items': values_line[7], 'total_to_pay': values_line[8], 'qr_code': [], 'barcodes': []}
      
      elif values_line[0] == "L" and values_line[2] == "1" and values_line[17] == "0" and values_line[25][0:2] == "26":
        tickets[ticket_number]['qr_code'].extend([remove_leading_zero(values_line[25])])
      
      elif values_line[0] == "L" and values_line[2] == "1" and values_line[17] == "0" and not is_integer(float(values_line[5])):
        tickets[ticket_number]['qr_code'].extend([generar_pesable(values_line[4][0:5], values_line[5])])
        print(generar_pesable(values_line[4][0:5], values_line[5]))
      
      elif values_line[0] == "L" and values_line[2] == "1" and values_line[17] == "0":
        tickets[ticket_number]['qr_code'].extend([remove_leading_zero(values_line[25])] * int(float(remove_leading_zero(values_line[5]))))
  #Elimino el directorio antes de generar las imagenes
  # Procesar.elimina_archivos('static/app_barcode/images/')
  if number:
    if number in tickets:
      qr_codes_ticket = tickets[number]['qr_code']
      for qr_code in qr_codes_ticket:
        generate_ean(qr_code)
      generar_video(qr_codes_ticket)
      mostrar_boton_video = True
      for clave in list(tickets.keys()):
        if clave != number:
          del tickets[clave]
    else:
      no_ticket = True
      return render_template('app_barcode/formulario.html', no_ticket=no_ticket, number=number)
  else:
    for objeto in tickets.values():
      qr_codes = objeto['qr_code']
      for qr_code in qr_codes:
        generate_ean(qr_code)
        # print(qr_code)
    mostrar_boton_video = False
  
  return render_template('app_barcode/template.html', tickets=tickets, mostrar_boton_video=mostrar_boton_video)

@app_barcode.route('/upload', methods=['GET', 'POST'])
def upload_file():
  global number 
  number = request.form['number']
  f = request.files['file']
  if f:
    filename = secure_filename(f.filename)
    location_file = os.path.join(os.getcwd(), 'Salidapazosnuevo.txt')
    f.save(location_file)
    return redirect('imagenes')
  no_file = True
  return render_template('app_barcode/formulario.html', no_file=no_file)

@app_barcode.route('/video', methods=['GET', 'POST'])
def video():
  # Especificar el nombre del archivo ZIP
  file_video = "static/app_barcode/video/video_salida.mp4"
  # Enviar el archivo ZIP para descargar
  return send_file(file_video, as_attachment=True)