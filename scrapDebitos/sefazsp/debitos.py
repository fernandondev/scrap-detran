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
import undetected_chromedriver as uc


def scrapSp(placa, renavam):
    
    total=0.00
    ipva=0.00
    licenciamento=0.00
    dpvat=0.00
    multas=0.00

    driver = uc.Chrome()
    driver.implicitly_wait(5)
    driver.get('https://www.ipva.fazenda.sp.gov.br/IPVANET_Consulta/')
    wait = WebDriverWait(driver, 10)



    input_renavam = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="conteudoPaginaPlaceHolder_txtRenavam"]')))

    input_renavam.send_keys(renavam)
    input_placa=wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="conteudoPaginaPlaceHolder_txtPlaca"]')))

    input_placa.send_keys(placa)

    #_------------------------------------captcha--------------------------------

    def captcha():
        sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__name__))))

        api_key = 'd37c12d2559bd6f80e91e8cb8e1dad66'

        solver = TwoCaptcha(api_key)

        try:

                result = solver.recaptcha(
                    sitekey='6Led7bcUAAAAAGqEoogy4d-S1jNlkuxheM7z2QWt',
                    url='https://www.ipva.fazenda.sp.gov.br/IPVANET_Consulta/Consulta.aspx')

        except Exception as e:
            sys.exit(e)

        else:
            return result

    wait.until(EC.presence_of_element_located((By.ID, 'g-recaptcha-response')))

    code = captcha()['code']
    print(code)
    driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML =" + "'"+ code + "'")
    sleep(1)
    botao_consultar=wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudoPaginaPlaceHolder_btn_Consultar"]')))

    botao_consultar.click()
#-----------------------------------------IPVA--------------------------------------------------------
    ipvaInscrito_html = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="conteudoPaginaPlaceHolder_txtValoraPagar"]')))
    ipvaInscritoFloat=float(ipvaInscrito_html.text.replace('.','').replace(',','.'))
    ipva+=ipvaInscritoFloat
    table=wait.until(EC.visibility_of_element_located((By.ID, 'conteudoPaginaPlaceHolder_tbIpvaPend')))
    tbody=table.find_element(By.TAG_NAME,'tbody')
    ipvaNaoInscritos_html=tbody.find_elements(By.TAG_NAME, 'tr')
    ipvaNaoInscritos_html.pop(0)
    if len(ipvaNaoInscritos_html)==1:
        ipvaNaoInscritos=0.00
    else:
        ipvaNaoInscritos_html.pop(0)
        for tr in ipvaNaoInscritos_html:
            tds=tr.find_elements(By.TAG_NAME, 'td')
            ipvaNaoInscritoFloat=float(tds[4].text.replace('.','').replace(',','.'))
            ipva+=ipvaNaoInscritoFloat

    print(ipva)
    #Fazer scrap debitos divida ativa www.dividaativa.pge.sp.gov.br
    # Fazer scrap dpvat http://www.seguradoralider.com.br/Pages/Saiba-como-pagar.aspx

#--------------------------------------------LICENCIAMENTO---------------------------------------------------
    #licenciamentoAtual_html= wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="conteudoPaginaPlaceHolder_tbTaxasDetalhe"]/tbody/tr[7]/td[1]/span')))
    #driver.switch_to.default_content()
    #licenciamentos_html= wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="conteudoPaginaPlaceHolder_tbTaxasDetalhe"]/tbody/tr')))

    table=wait.until(EC.visibility_of_element_located((By.ID, 'conteudoPaginaPlaceHolder_tbTaxasDetalhe')))
    tbody= table.find_element(By.TAG_NAME, 'tbody')
    licenciamentos_html = tbody.find_elements(By.TAG_NAME, 'tr')
    licenciamentos_html.pop(0)
    if len(licenciamentos_html)==1:
        licenciamento=0.00
    else:
        licenciamentos_html.pop(0)
        licenciamentoFatiado=licenciamentos_html[4:]
        for tr in licenciamentoFatiado:
            tds=tr.find_elements(By.TAG_NAME, 'td')
            licenciamentoFloat=float(tds[4].text.replace('.','').replace(',','.'))
            licenciamento+=licenciamentoFloat
    print(licenciamento)
#-----------------------------------------------MULTAS----------------------------------------------------------
    multas_html=wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="conteudoPaginaPlaceHolder_tbMultaResumo"]/tbody/tr')))

    if multas_html[0].text=='NADA CONSTA':
        multas=0.00
    else:
        multas_html.pop(0)
        for tr in multas_html:
            tds=tr.find_elements(By.TAG_NAME, 'td')
            multasFloat=float(tds[4].text.replace('.','').replace(',','.'))
            multas+=multasFloat
    
    total_html=wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="conteudoPaginaPlaceHolder_txtValorTotalDebitos"]')))
    total_confiavel= total_html.text
    total=multas+licenciamento+ipva
    dict={'TOTAL': total , 'TOTALPAGDEBITOS': total_confiavel ,'MULTAS': multas , 'LICENCIAMENTO':licenciamento ,'IPVA': ipva }
    # dict['TOTAL'].append(total)
    # dict['TOTALPAGDEBITOS'].append(total_confiavel)
    # dict['MULTAS'].append(multas)
    # dict['LICENCIAMENTO'].append(licenciamento)
    # dict['IPVA'].append(ipva)
    
    return dict
#scrapSp('FMV5J00', '01041094865')





