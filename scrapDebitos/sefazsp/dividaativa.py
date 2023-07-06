from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from twocaptcha import TwoCaptcha
import sys
import os
import json
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random
import requests
import sys
import threading
from selenium.common.exceptions import NoSuchElementException
import time
import undetected_chromedriver as uc


#--------------------------------------SCRAP PROPRIAMENTE DITO

def dividaSp(renavam):

    ipvaDividaAtiva=0.00

    driver = uc.Chrome()
    driver.implicitly_wait(1.5)
    driver.get('https://www.dividaativa.pge.sp.gov.br/sc/pages/pagamento/gareLiquidacao.jsf')
    wait = WebDriverWait(driver, 10)
    sleep(1.5)
    #cookie=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="modalPanelDebIpvaIDContentTable"]/tbody/tr/td/p/span')))
    #cookie.click()
    botao_renavam=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="adesaoForm:j_id70:2"]')))
    botao_renavam.click()

    campo_renavam=wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="adesaoForm:renavam"]')))
    campo_renavam.send_keys(renavam)


    def captcha():
        sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__name__))))

        api_key = 'd37c12d2559bd6f80e91e8cb8e1dad66'

        solver = TwoCaptcha(api_key)

        try:

                result = solver.recaptcha(
                    sitekey='6Le9EjMUAAAAAPKi-JVCzXgY_ePjRV9FFVLmWKB_',
                    url='https://www.dividaativa.pge.sp.gov.br/sc/pages/pagamento/gareLiquidacao.jsf')

        except Exception as e:
            sys.exit(e)

        else:
            return result

    wait.until(EC.presence_of_element_located((By.ID, 'g-recaptcha-response')))

    code = captcha()['code']
    print(code)
    driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML =" + "'"+ code + "'")
    sleep(1)




    botao_consultar=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="adesaoForm:pnlDocumentoPesquisa"]/input[2]')))
    botao_consultar.click()

    def checkExisteDebito():
        try:
            driver.find_element(By.XPATH, '//*[@id="messages"]/tbody/tr/td/span[2]')
            
        except NoSuchElementException:
            return True
        return False

    if checkExisteDebito():
        
        def checkVariosDebito():
            try:
                driver.find_element(By.XPATH, '//*[@id="gareForm:dataTable"]')

            except NoSuchElementException:
                return False
            return True
        variosDebitos=checkVariosDebito()

        if variosDebitos==True:
                
            trs=wait.until(EC.visibility_of_all_elements_located((By.XPATH,'//*[@id="gareForm:dataTable:tb"]/tr')))
            #print(trs)
            for tr in trs:
                tds=tr.find_elements(By.TAG_NAME, 'td' )
                tituloDebito= tds[2]
                valorDebito= tds[3]
                #print(valorDebito.text)
                if 'IPVA' in tituloDebito.text:
                    ipvaDividaAtiva+= float(valorDebito.text.replace('R$ ','').replace('.','').replace(',','.'))
        else:
            trs=wait.until(EC.visibility_of_all_elements_located((By.XPATH,'//*[@id="gareForm:j_id64_body"]/table/tbody/tr')))
            trs.pop(0)
            trs.pop(0)
            trs.pop(0)
            tds1=trs[0].find_elements(By.TAG_NAME, 'td')
            if 'IPVA' in tds1[1].text:
                tds2=trs[1].find_elements(By.TAG_NAME, 'td')
                ipvaDividaAtiva+=float(tds2[1].text.replace('R$ ','').replace('.','').replace(',','.'))


        dict={'IPVA2': ipvaDividaAtiva}

        return dict
    else:
        dict={'IPVA2': ipvaDividaAtiva}
        #print(dict)
        return dict
# iterar=[1,2,3,4,5,6,7,8,9]
# for x in iterar:
#print(dividaSp('01041094865'))


