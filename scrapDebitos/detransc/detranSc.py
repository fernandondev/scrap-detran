from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from twocaptcha import TwoCaptcha
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import threading
import secrets
import json
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc


def rodarDetranSc(placa, renavam):

    totDeb=0.00
    totLicenciamento=0.00
    totIpva=0.00
    totMultas=0.00
    totDpvat=0.00

    driver = uc.Chrome()
    driver.get(f'https://www.detran.sc.gov.br/veiculos/consultas/')
    wait = WebDriverWait(driver, 10)



    input_placa=wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="form-field-placa"]')))
    for x in placa:
        input_placa.send_keys(x)

    input_renavam=wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="form-field-renavam"]')))
    for x in renavam:
        input_renavam.send_keys(x)
    botao_consultar1 =wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="post-2041"]/div/div/section[2]/div[2]/div/div/section[1]/div[2]/div[1]/div/div/div/form/div/div[3]/button/span/span[2]'))) 
    botao_consultar1.click()

    botao_consultar = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="form1"]/table[2]/tbody/tr[4]/td/fieldset/table/tbody/tr[4]/td/button')))
    sleep(3)
    botao_consultar.click()
    #procura onde estão os débitos
    tds=wait.until(ec.visibility_of_all_elements_located((By.XPATH, '//*[@id="div_servicos_03"]/table[2]/tbody/tr/td')))
    
    #Procura os debitos nesse td e armazena nas variáveis
    for td in tds:
        td_soup = BeautifulSoup(td.get_attribute('innerHTML'), 'html.parser')

        textos=td_soup.get_text('**', strip=True).split('**')
        if 'axas' in textos[0]: 
            totLicenciamento=float(textos[1].replace('.','').replace(',','.'))
        if 'DPVAT' in textos[0]:
            totDpvat=float(textos[1].replace('.','').replace(',','.'))
        if 'IPVA' in textos[0]:
            totIpva=float(textos[1].replace('.','').replace(',','.'))
        if 'ultas' in textos[0]:
            totMultas=float(textos[1].replace('.','').replace(',','.'))
        
    #Calcula o total dos débitos
    totDeb=totLicenciamento+totDpvat+totIpva+totMultas
    #Monta o dicionario
    dict={'TOTAL': totDeb, 'IPVA':totIpva, 'LICENCIAMENTO':totLicenciamento, 'MULTAS':totMultas, 'DPVAT':totDpvat}
    
    driver.close()
    return json.dumps(dict)

