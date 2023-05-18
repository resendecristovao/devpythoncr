from devpythoncr import app, database
from devpythoncr.models import Usuarios, Registros
# with app.app_context():
#     database.create_all

# with app.app_context():
#     usuario = Usuarios(email='monica@206.com', senha='123456')
#     usuario2 = Usuarios(email='marceline@206.com', senha = '123456')
#     database.session.add(usuario)
#     database.session.add(usuario2)
#     database.session.commit()

# with app.app_context():
#     registro1 = Registros(nome='Lais', email='lais@miv.com.br', status='recusado', valor=789654, forma_pagamento='crédito', parcelas=10)
#     registro2 = Registros(nome='Marcelo', email='marcelo@miv.com.br', status='estornado', valor=36545, forma_pagamento='pix', parcelas=1)
#     registro3 = Registros(nome='Joaão', email='joao@miv.com.br', status='recusado', valor=1231, forma_pagamento='paypal', parcelas=5)
#     database.session.add(registro1)
#     database.session.add(registro2)
#     database.session.add(registro3)
#     database.session.commit()

# filtrado = Usuarios.query.filter_by(email='').all()

with app.app_context():
    meus_usuarios = Usuarios.query.all()
    print(meus_usuarios)

# with app.app_context():
#     database.drop_all()
#     database.create_all()