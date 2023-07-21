from flask import Flask, render_template
from home.home import home
from mercado_pago.mercado import mercado
from app_barcode.app_barcode import app_barcode
from socio_manager.socio_manager import socio_manager

app = Flask(__name__)
app.register_blueprint(home, url_prefix="/")
app.register_blueprint(mercado, url_prefix="/mercado")
app.register_blueprint(app_barcode, url_prefix="/app_barcode")
app.register_blueprint(socio_manager, url_prefix="/socio_manager")

# Nivel de plano error 404
@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html"), 404

app.config['SECRET_KEY'] = 'your secret key'

if __name__ == '__main__':
   app.run()
