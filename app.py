import os
from config import app
from flask import Flask, render_template, request, redirect,url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import DuplicateKeyError

from flask_login import login_user, logout_user, login_required
from config import login_manager
from datetime import datetime

from bson.objectid import ObjectId
from models.user import User





from bs4 import BeautifulSoup
from urllib2 import Request, urlopen

import urllib2


import xlsxwriter

from pymongo import MongoClient
client = MongoClient('localhost',27017)
database = client['hertz']
collection = database.user
collection2 = database.cars
collection3 = database.requisicao
collection4 = database.relatorio



@login_manager.user_loader
def load_user(id):
    u = collection.find_one({"_id": id})
    if not u:
        return None
    return User(u['_id'])

def load(id):
    u = collection.find_one({"_id": id})
    return u


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/operador/<usuario>',methods = ['GET'])
@login_required
def operador(usuario):
    user = load(usuario)
    if user and user['privilegios'] == "op":
        solicitacoes = collection3.find({'status':"Aguardando"})
        solicitacoes2 = collection3.find({'relatorio':"Aguardando"})
        solicitacoes3 = collection3.find({'relatorio':"Enviado"})




        return render_template('operadormain.html', usuario = usuario, solicita = solicitacoes , solicita2 = solicitacoes2, solicita3 = solicitacoes3)

    if user and user['privilegios'] == "user":
        target = 'http://www.precodoscombustiveis.com.br/postos/cidade/2568/mg/guaxupe'

        content = urllib2.Request(url=target)
        req = urllib2.Request(target)
        response = urllib2.urlopen(req)

        xhtml = response.read().decode('iso-8859-1')


        soup = BeautifulSoup(xhtml)



        data = []
        gasolina = soup.find("span", { "class" : "lead gasolina" })
        alcool = soup.find("span", { "class" : "lead alcool" })




        gasoza = gasolina.text
        alcoosa = alcool.text

        solicitacoes = collection3.find({'author':usuario,'status':"Aguardando"})
        solicitacoes2 = collection3.find({'author':usuario,'status':"Aprovado"})
        solicitacoes3 = collection3.find({'author':usuario,'status':"Reprovado"})
        return render_template('usermain.html', usuario = usuario , solicita = solicitacoes, solicita2 = solicitacoes2 , solicita3 = solicitacoes3, gasoza = gasoza, alcoosa = alcoosa)




@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('autenticacao'))




@app.route('/autenticacao', methods = ['GET', 'POST'])
def autenticacao():
    if request.method == 'GET':
        return render_template('autenticacao.html')





@app.route('/cadastrar', methods = ['GET', 'POST'])
def cadastrar():
    if request.method == 'GET':
        return render_template('autenticacao.html')

    try:
        collection.insert({
        '_id': request.form['login2'],
        'email':  request.form['email2'],
        'password': generate_password_hash(request.form['senha2']),
        'privilegios':'user'

        })
        user_obj = User(request.form['login2'])
        login_user(user_obj)
        return redirect(url_for('operador', usuario = request.form['login2'])
        )
    except DuplicateKeyError:
        return render_template('falhacad.html')







def check_password(self, password):
    return check_password_hash(self['password'], password)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print '1'
        user = collection.find_one({"_id": request.form['login']})
        #print '2'
        if user and User.validate_login(user['password'], request.form['senha']):
            #print '3'
            user_obj = User(user['_id'])
            login_user(user_obj)
            return redirect(url_for('operador', usuario = user['_id']))


    return render_template('falhalogin.html')


@login_manager.unauthorized_handler
def unauthorized_cb():
    return render_template('401.html')
    # return redirect('login')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')




@app.route('/operador/carros<usuario>' , methods=['GET', 'POST'])
@login_required
def cars(usuario):
    if request.method == 'GET':
        lista = collection2.find()
        #print lista
        return render_template("admin/carros.html",  lista = lista, usuario = usuario)


#-----------------------------------------------------------------------------

@app.route('/carros/add', methods = ['GET', 'POST'])
@login_required
def addcarros():
    try:
        collection2.insert({
        '_id': request.form['placa'],
        'chassi':  request.form['chassi'],
        'modelo': request.form['modelo'],
        'quilometragem': request.form['quilometragem'],
        'tipocomb': request.form['tipocomb'],
        'kmlitro': request.form['kmlitro'],
        'revisao': request.form['revisao'],
        'author': request.form['author'],
        'status': "livre"

            })

        return redirect(url_for('cars', usuario = request.form['author'] ))

    except DuplicateKeyError:
        return render_template('falhacad.html')


@app.route('/carros/remove<idi>', methods = ['POST'])
def carremove(idi):
    #print idi
    collection2.remove({
    '_id': idi
    })




    return redirect(url_for('cars', usuario = "admin"))


@app.route('/carros/edit<idi>', methods = ['get'])
@login_required
def caredit(idi):
     car = collection2.find_one({'_id':idi})
     return render_template('admin/carupdate.html', car = car)


@app.route('/carros/update<idi>', methods = ['POST'])
@login_required
def carupdate(idi):
    collection2.update(
    {'_id': idi },
    {
        '$set':{
            'chassi':  request.form['chassi'],
            'modelo': request.form['modelo'],
            'quilometragem': request.form['quilometragem'],
            'tipocomb': request.form['tipocomb'],
            'kmlitro': request.form['kmlitro'],
            'revisao': request.form['revisao'],
            'author': request.form['author']
    }
    })



    return redirect(url_for('cars', usuario = "admin"))


##################################################################################


@app.route('/user/solicita<usuario>' , methods=['GET'])
@login_required
def solicita(usuario):
    if request.method == 'GET':
        lista = collection2.find({'status':"livre"})
        return render_template("user/solicita.html",  lista = lista, usuario = usuario)


@app.route('/user/newsolicita<car>,<usuario>' , methods=['GET', 'POST'])
@login_required
def newsolicita(car, usuario):
    if request.method == 'GET':
        return render_template("user/newsolicita.html", car = car , usuario = usuario)

    collection3.insert({

    'placa':  request.form['placa'],
    'destino': request.form['destino'],
    'datainicial': request.form['datainicial'],
    'datafinal': request.form['datafinal'],
    'horainicial': request.form['horainicial'],
    'horafinal': request.form['horafinal'],
    'status': "Aguardando",
    'author': request.form['author'],
    'relatorio':"naoenviado"


    })

    collection2.update(
    {'_id': car },
    {
        '$set':{
            'status': "Ocupado"
    }
    })

    return redirect(url_for('operador', usuario = usuario))



@app.route('/user/buscasolicita<usuario>' , methods=['GET', 'POST'])
@login_required
def solicitabusca(usuario):
    if request.method == 'GET':
        lista = collection3.find({'status': "Aguardando"})
        return render_template("admin/buscasolicita.html", lista = lista, usuario = usuario)



@app.route('/user/solicita/aprova<idi>,<usuario>', methods = ['POST'])
def aprova(idi, usuario):
    #print idi;
    collection3.update(
    {'_id': ObjectId(idi) },
    {
        '$set':{
            'status':"Aprovado",
            'relatorio':"Aguardando"
    }
    })



    return redirect(url_for('solicitabusca' ,usuario = usuario))



@app.route('/user/solicita/reprova<idi>,<usuario>', methods = ['POST'])
def reprovado(idi, usuario):
#    print idi;
    collection3.update(
    {'_id': ObjectId(idi) },
    {
        '$set':{
            'status':"Reprovado"
    }
    })



    return redirect(url_for('solicitabusca' , usuario = usuario))


@app.route('/user/relatorio<usuario>', methods = ['GET','POST'])
@login_required
def relatorio(usuario):
    if request.method == 'GET':
        solicitacoes = collection3.find({'author':usuario,'status':"Aprovado",'relatorio':"Aguardando"})
        return render_template("user/relatorio.html", usuario = usuario, solicita = solicitacoes)




@app.route('/user/relatar<idi>,<usuario>,<placa>', methods=['GET', 'POST'])
@login_required
def relatar(idi, usuario, placa):
    if request.method == 'GET':
        today = datetime.now()
        day = today.day
        month = today.month
        year = today.year
        data = str(day) + "/" + str(month)+ "/"+ str(year)
        return render_template("user/newrelatorio.html", usuario = usuario , idi = idi , data = data , placa = placa)

    #print "tes2te"
    collection4.insert({

    'author':       request.form['author'],
    'dgasolina':    request.form['dgasolina'],
    'drevisao':     request.form['drevisao'],
    'descricao':    request.form['descricao'],
    'kmfinal':      request.form['kmfinal'],
    'data':         request.form['data'],
    'idrequisicao': request.form['idrequisicao'],
    'placa':        request.form['placa'],
    'status': "naolida"

    })
    collection3.update(
    {'_id': ObjectId(idi) },
    {
        '$set':{
            'relatorio':"Enviado"
    }
    })



    return redirect(url_for('relatorio', usuario = usuario))


#####################3

@app.route('/operador/relatorios<usuario>' , methods=['GET', 'POST'])
@login_required
def buscarelata(usuario):
    if request.method == 'GET':
        today = datetime.now()
        day = today.day
        month = today.month
        year = today.year
        data = str(day) + "/" + str(month)+ "/"+ str(year)
        lista = collection4.find({'data':data,'status':"naolida"})

        return render_template("admin/buscarelata.html", lista = lista, usuario = usuario)








@app.route('/operador/liberarcarro<usuario>,<idir>,<idi>,<kmfinal>' , methods=['POST'])
@login_required
def liberarcarro(usuario, idir , idi , kmfinal):

    collection2.update(
    {'_id': idi},
    {
        '$set':{
            'status': "livre",
            'quilometragem': kmfinal

    }
    })



    collection3.update(
    {'_id': ObjectId(idir) },
    {
        '$set':{
            'relatorio':"Aprovado"
    }
    })



    collection4.update(


    {'idrequisicao': idir },
    {
        '$set':{
            'status': "lido"
    }
    })

    return redirect(url_for('buscarelata', usuario = usuario))

@app.route('/operador/relatorioss<usuario>' , methods=['GET', 'POST'])
@login_required
def relatorioss(usuario):
    if request.method == 'GET':
        return render_template('admin/relatorios.html', usuario = usuario)

    lista = collection4.find({'author':request.form['name']})

    return render_template('admin/relatorios.html',usuario= usuario, solicita =lista)


@app.route('/operador/relatorioss/excel<usuario>' , methods=['POST'])
@login_required
def excel(usuario):

    workbook = xlsxwriter.Workbook('PlanilhaRelatorio.xlsx')

    worksheet= workbook.add_worksheet()

    items = (
        ['Nome', request.form['author'] ],
        ['Placa', request.form['placa'] ],
        ['Data ',   request.form['data'] ],
        ['Gasolina' , request.form['dgasolina'] ],
        ['Revisao ', request.form['drevisao'] ],
        ['Km_Final' , request.form['kmfinal'] ],
        ['Descricao' , request.form['descricao'] ]
        )

    row = 0
    col = 0

    for item, qtd in (items):
        worksheet.write(row, col, item)
        worksheet.write(row, col +1, qtd)
        row += 1

    workbook.close()

    return redirect(url_for('relatorioss', usuario = usuario))










if __name__ == '__main__':
    app.run(host = app.config['HOST'], port = app.config['PORT'], debug = app.config['DEBUG'])
