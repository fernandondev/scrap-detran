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
#Variaveis programa
chave='d37c12d2559bd6f80e91e8cb8e1dad66'


def rodarDetranEs(placa, renavam):
        constaDebito = True

    #Variaveis
        totDebIpva=float(0.00)
        totDebMultas=float(0.00)
        totDebLicenciamento=float(0.00)
        totDebPatio=float(0.00)
        indexVeiculo=[]
        indexDebitos=[]
        lista=[]
        listaVeiculo=[]
        listaDebitos=[]
        navegador = uc.Chrome()


    #Inicio do scrap
        navegador.implicitly_wait(1.5)
        navegador.get('https://publicodetran.es.gov.br/ConsultaVeiculo/NovoConsultaVeiculoES.asp')
        sleep(2)
        wait = WebDriverWait(navegador, 10)
        campo_placa =wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="placa"]')))
        campo_placa.send_keys(placa)

        campo_renavam = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="renavam"]')))
        campo_renavam.send_keys(renavam)

        token=secrets.token_hex()
        imagem = navegador.find_element(By.XPATH, '//*[@id="imgCaptcha"]')
        path=f'detranes\captchas\{token}.png'
        imagem.screenshot(path)
        solver=TwoCaptcha(chave)
        try:
            resultado = solver.normal(path)

        except Exception as e:
            print(e)
        #else:
            #print(resultado)

        os.remove(path)
        campo_cap = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="txtCaptcha"]')))

        campo_cap.send_keys(resultado['code'])
        sleep(0.5)
        botao = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="btnSubmit"]')))
        botao.click()
        debito = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="span_nome_div_servicos_03"]')))
        debito.click()
        
        def checkTabela():
            try:
                navegador.find_element(By.XPATH, '//*[@id="Integral"]/td/table/tbody/tr')               
            except NoSuchElementException as e:

                return False

            return True
        
        constaDebito = checkTabela()
        print(constaDebito)


        #-------------------------------FOR DOS DÉBITOS-------------------------------------
        if constaDebito==True:
            tabela=wait.until(ec.visibility_of_all_elements_located((By.XPATH, '//*[@id="Integral"]/td/table/tbody/tr')))
            tabela.pop(0)
            tabela.pop(0)            
            for tr in tabela:
                    tr_soup = BeautifulSoup(tr.get_attribute('innerHTML'), 'html.parser')

                    tituloDeb=tr_soup.find('td', attrs={'class': 'bordaEsquerdaFina bordaAbaixoFina celnlef'})
                    valorDebTag=tr_soup.find('td', attrs={'class': 'bordaEsquerdaFina bordaAbaixoFina bordaDireitaFina celnrig'})

                    if(tituloDeb and valorDebTag):
                        tituloDebText=tituloDeb.text.replace('\xa0\xa0','')
                        valorDeb=float(valorDebTag.text.replace('.','').replace(',','.'))

                        if 'IPVA' in tituloDebText:
                                        totDebIpva+=valorDeb
                        if 'Licenciamento' in tituloDebText:
                                        totDebLicenciamento+=valorDeb
                        if 'DETRAN-ES' in tituloDebText:
                                        totDebMultas+=valorDeb
                        if 'PM' in tituloDebText:
                                        totDebMultas+=valorDeb
                        if 'PRF' in tituloDebText:
                                        totDebMultas+=valorDeb
                        if 'DNIT' in tituloDebText:
                                        totDebMultas+=valorDeb
                        if 'DER' in tituloDebText:
                                        totDebMultas+=valorDeb
                        if 'Estadia' in tituloDebText:
                                        totDebLicenciamento+=valorDeb
                        if 'Rebocamento' in tituloDebText:
                                        totDebLicenciamento += valorDeb
                        if 'Km' in tituloDebText:
                                        totDebLicenciamento+=valorDeb
                        if 'Transferência' in tituloDebText:
                                        totDebLicenciamento+=valorDeb
                        if 'Alienação' in tituloDebText:
                                        totDebLicenciamento+=valorDeb
                        if 'Averbação' in tituloDebText:
                                        totDebLicenciamento+=valorDeb

        totDeb=totDebIpva+totDebMultas+totDebLicenciamento+totDebPatio

        dict={'TOTAL': totDeb, 'IPVA':totDebIpva, 'LICENCIAMENTO':totDebLicenciamento, 'MULTAS':totDebMultas}
        navegador.close()
        return dict


















