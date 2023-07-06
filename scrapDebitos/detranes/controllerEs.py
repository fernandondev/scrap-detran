
import sys
from detranes.dpvat import pegarDpvat
from detranes.detranEs import rodarDetranEs
from threading import Thread
from flask import Flask, request
import json
from time import sleep
from util.ThreadWithReturnValue import ThreadWithReturnValue


def rodarDebitosES(placa,renavam):



    debitosret=ThreadWithReturnValue(target = rodarDetranEs, args=(placa, renavam))
    dpvatret=ThreadWithReturnValue(target = pegarDpvat, args=(renavam, 'ES', 30))

    debitosret.start()
    dpvatret.start()


    retornoDebitos=debitosret.join()
    retornoDpvat=dpvatret.join()

    sleep(1)
    if retornoDpvat['DPVAT'] =='Nao foi possivel consultar o dpvat':
        retornoDebitos.update({'DPVAT': 'Nao foi possivel consultar o dpvat'})

        jsonDebitos= json.dumps(retornoDebitos)

        #print(jsonDebitos)
        return jsonDebitos

    else:
        dpvatdeb=retornoDpvat['DPVAT']
        total1=retornoDebitos['TOTAL']
        total2=total1+dpvatdeb

        retornoDebitos.update({'DPVAT': retornoDpvat['DPVAT']})
        retornoDebitos.update({'TOTAL': total2})
        jsonDebitos= json.dumps(retornoDebitos)

        #print(jsonDebitos)
        return jsonDebitos

#print(rodarDebitosES('PVQ6A76','01037000010'))