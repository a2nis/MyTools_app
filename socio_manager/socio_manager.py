from flask import Blueprint, render_template, request
from .grupo_form import GroupForm

socio_manager = Blueprint("socio_manager", __name__, static_folder="static")

@socio_manager.route('/', methods=['GET', 'POST'])
def inicio():
  lista_grupos = []
  socio = 0
  concateno_socio = ""
  
  form = GroupForm(request.form)
  if request.method == 'POST' and form.validate_on_submit():
    socio = form.no_socio.data
    lista_grupos = form.group.data.split(',')
    insert = "INSERT INTO SociosGrupos VALUES "
    socio_grupos = ','.join([f'("{i}",{socio},"TATA","null")' for i in lista_grupos])
    concateno_socio = insert + socio_grupos + ";"
  return render_template('socio_manager/index.html', form=form, lista_grupos=lista_grupos, concateno_socio=concateno_socio)