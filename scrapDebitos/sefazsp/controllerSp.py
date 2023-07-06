import sys
from sefazsp.dpvat import pegarDpvat
from sefazsp.debitos import scrapSp
from sefazsp.dividaativa import dividaSp
from threading import Thread
from util.ThreadWithReturnValue import ThreadWithReturnValue
from flask import Flask, request
import json
from time import sleep



def rodarDebitosSp(placa,renavam):



    debitosret=ThreadWithReturnValue(target = scrapSp, args=(placa,renavam))
    ipva2ret=ThreadWithReturnValue(target = dividaSp, args=(renavam,))
    dpvatret=ThreadWithReturnValue(target = pegarDpvat, args=(renavam, 'SP', 60))

    debitosret.start()
    ipva2ret.start()
    dpvatret.start()


    retornoDebitos=debitosret.join()
    retornoIpva2=ipva2ret.join()
    retornoDpvat=dpvatret.join()
    sleep(1)
    if retornoDpvat['DPVAT'] =='Nao foi possivel consultar o dpvat':
        debitosIpva=retornoDebitos['IPVA']
        ipva2=retornoIpva2['IPVA2']     #ipva dívida ativa    
        totalIpva=debitosIpva+ipva2
        total1=retornoDebitos['TOTAL']
        total2=total1+ipva2     #Total depois de adicionar o ipva da dívida ativa(ipva2)
        #print('retornoDebitosipva: ' +debitosIpva)
        #print('retornoIpva2: ' +ipva2)
        #print('totalIpva: '+totalIpva)
        retornoDebitos.update({'DPVAT': 'Nao foi possivel consultar o dpvat'})
        retornoDebitos.update({'IPVA': totalIpva})
        retornoDebitos.update({'TOTAL': total2})
        jsonDebitos= json.dumps(retornoDebitos)

        #print(jsonDebitos)
        return jsonDebitos

    else:
        debitosIpva=retornoDebitos['IPVA']
        ipva2=retornoIpva2['IPVA2']
        totalIpva=debitosIpva+ipva2
        dpvatdeb=retornoDpvat['DPVAT']
        total1=retornoDebitos['TOTAL']
        total2=total1+ipva2+dpvatdeb
        #print('retornoDebitosipva: ' +debitosIpva)
        #print('retornoIpva2: ' +ipva2)
        #print('totalIpva: '+totalIpva)

        retornoDebitos.update({'IPVA': totalIpva})
        retornoDebitos.update({'DPVAT': retornoDpvat['DPVAT']})
        retornoDebitos.update({'TOTAL': total2})
        jsonDebitos= json.dumps(retornoDebitos)

        #print(jsonDebitos)
        return jsonDebitos



