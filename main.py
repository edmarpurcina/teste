import flask
from flask import request, jsonify
import dicionarios, time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dictpessoas = dicionarios.pessoas
dictbens = dicionarios.bens
dictempresas = dicionarios.empresas

@app.route('/', methods=['GET'])
def home():

    return" <h1>Olá Mundo</h1>"

@app.route('/api/v1/', methods=['GET'])
def api_all():
    return jsonify(dictpessoas)

def retorna_bens(cpf):
    posses = []
    for bem in dictbens:
        if bem['proprietario'] == cpf:
           posses.append(bem)

    return posses

def retorna_pessoas(cpf):
    dadospessoa = []
    for pessoa in dictpessoas:
        if pessoa['cpf'] == cpf:
            dadospessoa = pessoa
    if len(dadospessoa) <= 0:
        dadospessoa = "Cpf nao Encontrado"

    return dadospessoa

def lista_proprietarios(doc):
    dadosproprietario = []
    dicionario = {}
    for documentos in doc:
        if 'cpf' in documentos.keys():
            dados = retorna_pessoas(documentos['cpf'])
            dadosproprietario.append(dados)
            dicionario.update({'proprietario':dadosproprietario})
            print(dicionario)
        else:
            dados = retorna_dados_empresa(documentos['cnpj'])
            dadosproprietario.append(dados)
            dicionario.update({'proprietario': dadosproprietario})
            print(dicionario)

    return dadosproprietario

def retorna_dados_empresa(cnpj):
    dadosempresa = []
    for empresa in dictempresas:
        if empresa['cnpj'] == cnpj:
            proprietarios = empresa['proprietarios']
            empresaproprietarios = lista_proprietarios(empresa)

            dadosempresa = empresa
    #print(empresaproprietarios)
    return dadosempresa


@app.route('/api/v1/busca', methods=['GET'])
def api_busca():
    results = []
    if 'cpf' in request.args:
        if len(request.args['cpf']) != 11:
            return "Error: CPF Invalido"

        cpf = request.args['cpf']
        pessoa = retorna_pessoas(cpf)
        return jsonify(pessoa)

    elif 'cnpj' in request.args:
        if len(request.args['cnpj']) != 14:
            return "Error: CNPJ Invalido"

        cnpj = request.args['cnpj']
        dadosempresa = retorna_dados_empresa(cnpj)
        return jsonify(dadosempresa)

    else:
        return "Error: No CPF Provide"

    return jsonify(results)

app.run()

