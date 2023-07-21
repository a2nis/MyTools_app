from flask import Blueprint, render_template, request, send_file
from .Procesar import Procesar

mercado = Blueprint("mercado", __name__, static_folder="static")

# Lista de clientes para seleccionar
clientes = ['DISCO', 'FROG', 'KINKO', 'KINKO200', 'KINKO202', 'TATA', 'MAH', 'BAS']

@mercado.route('/', methods=['GET', 'POST'])
def formulario():
  sucursal_result = ""
  cajas_result = ""
  mostrar_alerta = False
  if request.method == 'POST':
    cliente = request.form['cliente']
    sucursal = request.form['sucursal']
    cajas = request.form['cajas']
    
    Procesar.elimina_archivos("Salida/")
    sucursal_result = Procesar(cliente, int(sucursal), int(cajas)).insert_sucursales()
    cajas_result = Procesar(cliente, int(sucursal), int(cajas)).insert_cajas()
    Procesar(cliente, int(sucursal), int(cajas)).imagen_qr()
    Procesar.comprime_archivos()
    Procesar.elimina_archivos("Salida/")
    mostrar_alerta = True
  return render_template('mercado_pago/formulario.html', clientes=clientes, sucursal=sucursal_result, cajas=cajas_result, mostrar_alerta=mostrar_alerta )

@mercado.route('/download', methods=['GET', 'POST'])
def download():
  # Especificar el nombre del archivo ZIP
  zip_file_name = "nombre_del_archivo.zip"
  # Enviar el archivo ZIP para descargar
  return send_file(zip_file_name, as_attachment=True)