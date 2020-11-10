import flask
from flask import request, jsonify, session
import dicionarios, time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dictpessoas = dicionarios.pessoas
dictbens = dicionarios.bens
dictempresas = dicionarios.empresas

@app.route('/', methods=['GET'])
def home():

    return" <h1>Olá Mundo</h1>"

@app.route('/api/v1/all', methods=['GET'])
def api_all():
    return jsonify(dictpessoas, dictempresas, dictbens)

def retorna_pessoas(cpf):
    dadospessoa = []
    for pessoa in dictpessoas:
        if pessoa['cpf'] == cpf :
            dadospessoa = pessoa
    if len(dadospessoa) <= 0:
        dadospessoa = "Cpf nao Encontrado"

    return dadospessoa

def lista_proprietarios(proprietarios, empresa):
    pessoa = []
    for proprietario in proprietarios:
        if len(proprietario) is 11:
            pessoa.append(retorna_pessoas(proprietario))
            empresa.update({'proprietarios': pessoa})
        elif len(proprietario) is 14:
            pessoa.append(retorna_dados_empresa(proprietario))
            empresa.update({'proprietarios': pessoa})
        else:
            break

    return empresa

def retorna_dados_empresa(cnpj):
    dadosempresa = []
    for empresa in dictempresas:
        if empresa['cnpj'] == cnpj:
            proprietarios = empresa['proprietarios']
            dadosempresa = lista_proprietarios(proprietarios, empresa)

    return dadosempresa

def retorna_bens(cpf):
    posses = []
    for bem in dictbens:
        if bem['proprietario'] == cpf:
           posses.append(bem)
    #retorna nome e cnpj da empresa
    for empresa in dictempresas:
        if cpf in empresa['proprietarios']:
            posses.append({'nome da empresa': empresa['nome da empresa'], 'cnpj': empresa['cnpj']})

    return posses

@app.route('/api/v1/busca', methods=['GET'])
def api_busca():
    if 'cpf' in request.args:
        if len(request.args['cpf']) != 11:
            return "Error: CPF Invalido"
        cpf = request.args['cpf']
        results = retorna_pessoas(cpf)
    elif 'cnpj' in request.args:
        if len(request.args['cnpj']) != 14:
            return "Error: CNPJ Invalido"
        cnpj = request.args['cnpj']
        results = retorna_dados_empresa(cnpj)
    elif 'posses' in request.args:
        if len(request.args['posses']) != 11:
            return "Error: CPF Invalido"
        busca = request.args['posses']
        results = retorna_bens(busca)
    else:
        return "Error: No Data Provide"

    return jsonify(results)

app.run()

