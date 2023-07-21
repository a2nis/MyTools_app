class Caja:
  
  def __init__(self, id, external_id, qr_image, qr_pdf):
    self.id = id
    self.external_id = external_id
    self.qr_image = qr_image
    self.qr_pdf = qr_pdf
    self.lista_cajas_excel = []
    
  def registrar_caja(self):
    self.lista_cajas_excel += (self.id, self.external_id, self.qr_image, self.qr_pdf)