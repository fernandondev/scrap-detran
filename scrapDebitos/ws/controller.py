import sys
from util.ThreadWithReturnValue import ThreadWithReturnValue
import queue
from flask import Flask, request
from detranes.controllerEs import rodarDebitosES
from sefazsp.controllerSp import rodarDebitosSp
from detransc.detranSc import rodarDetranSc
from time import sleep
import json
from datetime import datetime
import traceback


app=Flask(__name__)


@app.route('/debitos')
def rodarDebitos():

    placa= request.args['placa']
    renavam=request.args['renavam']
    uf=request.args['uf']
    
    ip_valor = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    nowInicio = datetime.now()
    dataInicio = nowInicio.strftime("%Y-%m-%d %H:%M:%S")


    

    def switch(uf):
        if uf.upper()=='SP':
            return rodarDebitosSp(placa,renavam)
        if uf.upper()=='ES':
            return rodarDebitosES(placa,renavam)
        if uf.upper()=='SC':
            return rodarDetranSc(placa, renavam)
    try:
        dictRetorno = json.loads(switch(uf))
        nowFim = datetime.now()
        dataFim = nowFim.strftime("%Y-%m-%d %H:%M:%S")

        dictRetorno.update({'PLACA': placa})
        dictRetorno.update({'RENAVAM': renavam})
        dictRetorno.update({'UF': uf})
        dictRetorno.update({'IP CLIENTE': ip_valor})
        dictRetorno.update({'DATA INICIO': dataInicio})
        dictRetorno.update({'DATA FIM': dataFim})

        jsonRetorno = json.dumps(dictRetorno)
        jsonRetornoBanco = jsonRetorno.replace('"', '\"')



        return jsonRetorno

    except Exception as e :
        nowErro = datetime.now()
        dataErro = nowErro.strftime("%Y-%m-%d %H:%M:%S")
        jsonErro = {"PLACA":placa ,"RENAVAM":renavam ,"UF":uf ,"MENSAGEM": "SISTEMA INDISPONIVEL","IP CLIENTE": ip_valor , "DATA INICIO": dataInicio, "DATA FIM": dataErro}
        jsonErro=json.dumps(jsonErro)
        jsonErroBanco=jsonErro.replace('"', '\"')
        traceback.print_exc


        return jsonErro

app.run(port=5000)


