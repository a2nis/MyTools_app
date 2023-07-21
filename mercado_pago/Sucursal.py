class Sucursal:
    
  def __init__(self, store_id, external_id_suc):
    self.store_id = store_id
    self.external_id_suc = external_id_suc
    self.lista_suc_excel = []
    
  def registrar_suc(self):
    self.lista_suc_excel += (self.store_id, self.external_id_suc)
  