from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from twocaptcha import TwoCaptcha
from selenium.common.exceptions import NoSuchElementException
import sys
import os
import json
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random
import requests
import sys
import threading
import select
import time
import queue
from util.ThreadWithReturnValue import ThreadWithReturnValue
import undetected_chromedriver as uc

class dpvat:
    def __init__(self, pegarInfo, q):
        self.pegarInfo = pegarInfo
        self.q = q




    def contadorFunc(self,tempo):

         
        listaTempo=[]
        timeSleep=0
        

        for x in range(1,tempo+1):
            listaTempo.append(x)

        for y in listaTempo:
            #print(y)
            sleep(1)
            timeSleep+=1
        if timeSleep==tempo:
            dict={'DPVAT': 'Nao foi possivel consultar o dpvat'}
            self.q.put(dict)
            self.pegarInfo=True
 

    def rodarDpvat(self,renavam, uf):

            def split(renavam):
                return list(renavam)

            dpvatTotal=0.00
            listRenavam=split(renavam)
            #print(listRenavam)
            driver = uc.Chrome()
            driver.implicitly_wait(1.5)
            driver.get('https://pagamento.dpvatsegurodotransito.com.br/')
            wait = WebDriverWait(driver, 10)

            input_renavam=wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="renavam"]')))
            for x in listRenavam:
                input_renavam.send_keys(x)

            input_uf=wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="uf"]')))
            select = Select(input_uf)
            select.select_by_value(uf)




            def captcha():
                sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__name__))))

                api_key = 'd37c12d2559bd6f80e91e8cb8e1dad66'

                solver = TwoCaptcha(api_key)

                try:

                        result = solver.recaptcha(
                            sitekey='6LcY2SwUAAAAAA2gLq-S1yYOVZCKsarEBl6YFnan',
                            url='https://pagamento.dpvatsegurodotransito.com.br/')

                except Exception as e:

                    dict={'DPVAT': 'Nao foi possivel consultar o dpvat'}
                    self.q.put(dict)
                    self.pegarInfo=True
                    self.killThread=True

                else:
                    return result

            wait.until(EC.presence_of_element_located((By.ID, 'g-recaptcha-response')))

            code = captcha()['code']
            print(code)
            driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML =" + "'"+ code + "'")
            sleep(1)

            botao_avancar=wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="botaoPagamento"]')))
            botao_avancar.click()
            try:
                wait.until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div[1]/main/div/div/div[1]/div[2]/span')))
            except NoSuchElementException:
                dict={'DPVAT': 'Nao foi possivel consultar o dpvat'}
                self.q.put(dict)
                self.pegarInfo=True

            wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/main/div/div/div[1]/div[1]/span')))

            def checkNadaConsta():
                try:
                    driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/strong[2]')
                except NoSuchElementException:
                    return False
                return True

            if checkNadaConsta():
                dict={'DPVAT': dpvatTotal}
                #print(dict)

                self.q.put(dict)
                driver.close()
                self.pegarInfo=True

            else:

                trs=wait.until(EC.visibility_of_any_elements_located((By.XPATH, '/html/body/div[1]/main/div/div/table/tbody/tr')))
                trs.pop(0)
                for tr in trs:
                    tds=tr.find_elements(By.TAG_NAME, 'td')
                    dpvat=float(tds[1].text.replace('.','').replace(',','.'))
                    dpvatTotal+=dpvat

                dict={'DPVAT': dpvatTotal}
                #print(dict)
                self.q.put(dict)
                driver.close()
                self.pegarInfo=True

    # iterar=[1,2,3,4,5,6,7,8,9]
    # for x in iterar:
    #     rodarDpvat('01092482323', 'SP')
    #rodarDpvat( '01092482323', 'SP')

    def executarDpvat(self,renavam, uf, tempo):
        
            dpvatCerto = ThreadWithReturnValue(target = self.rodarDpvat, args=(renavam,uf))
            dpvatIndisponivel = ThreadWithReturnValue(target = self.contadorFunc, args=(tempo,))
            dpvatIndisponivel.start()
            dpvatCerto.start()
            while self.pegarInfo == False:
                sleep(0.0001)

            return self.q.get()


#executarDpvat('431342434', 'ES', 20)


def pegarDpvat(renavam, uf, timeout):

    d1 = dpvat(False, queue.Queue())
    return d1.executarDpvat(renavam, uf, timeout)


# dpvat1 = ThreadWithReturnValue(target = pegarDpvat, args=('00420481460','ES', 5))
# dpvat2 = ThreadWithReturnValue(target = pegarDpvat, args=('00420481460','ES', 10))

# dpvat1.start()
# dpvat2.start()
# retornodpvat1= dpvat1.join()
# retornodpvat2 = dpvat2.join()
# print(f"Retorno dpvat1: {retornodpvat1['DPVAT']}" )
# print(f"retorno dpvat2: {retornodpvat2['DPVAT']}")

