import os
import csv
import time
import pyautogui
import pyperclip
import locale
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys




# Configura o locale para reconhecer meses em português
#locale.setlocale(locale.LC_TIME, "pt_BR.utf8")  # Para Linux/macOS
locale.setlocale(locale.LC_TIME, "Portuguese_Brazil")  # Para Windows 

# Configuração do Selenium
options = webdriver.ChromeOptions()
options.add_argument("--kiosk-printing")  # Ativa a impressão silenciosa
# options.add_argument("--headless")  # Descomente para rodar sem interface gráfica
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# URL Base
URL_BASE = "https://www.camara.leg.br/legislacao/busca?geral=bombeiro+militar&ano=&situacao=N%C3%A3o+consta+revoga%C3%A7%C3%A3o+expressa&abrangencia=&tipo=&origem=Poder+Executivo&numero=&ordenacao=data%3AASC"
CSV_PATH = "leis_bombeiro_militar.csv"

# Acessar a página de busca
driver.get(URL_BASE)
time.sleep(3)  # Aguarda o carregamento

dados = []  # Dados a serem salvos no CSV
contador = 0  # Contador de leis processadas

while True:  # Loop para continuar até não haver mais páginas
    # Capturar os resultados da busca
    resultados = driver.find_elements(By.CSS_SELECTOR, "li.busca-resultados__item")

    for resultado in resultados:
        try:
            contador += 1
            print(f"Processando {contador}ª lei...")

            # Extrair Nome completo (incluindo a data dentro)
            link_elemento = resultado.find_element(By.CSS_SELECTOR, "h3.busca-resultados__cabecalho a")
            nome_completo = link_elemento.text.strip()
            link_lei = link_elemento.get_attribute("href")

            # Extrair apenas a Data (últimas palavras do nome)
            partes_nome = nome_completo.split(" ")
            data_lei = " ".join(partes_nome[-5:])  # Pega os últimos 5 elementos do nome
            
            # Converter o texto para o formato de data
            try:
                data_lei = datetime.strptime(data_lei, "%d de %B de %Y").strftime("%d/%m/%Y")
            except ValueError:
                data_lei = "Data inválida"

            # Extrair Ementa
            ementa = resultado.find_element(By.CSS_SELECTOR, "p.busca-resultados__descricao").text.replace("Ementa:", "").strip()

            # Extrair Situação
            situacao = resultado.find_element(By.CSS_SELECTOR, "p.busca-resultados__situacao").text.replace("Situação:", "").strip()

            # Palavra-chave fixa
            palavra_chave = "Bombeiro militar"

            # Abrir o link da lei em uma nova aba
            driver.execute_script("window.open(arguments[0], '_blank');", link_lei)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)

            # Tentar encontrar o link do "Texto - Publicação Original"
            try:
                link_texto_original = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'publicacaooriginal')]")))
                nova_url = link_texto_original.get_attribute("href")
                
                # Abrir o link do texto original
                driver.execute_script("window.open(arguments[0], '_blank');", nova_url)
                driver.switch_to.window(driver.window_handles[2])
                time.sleep(3)
                
                # Acionar a impressão (Ctrl + P)
                pyautogui.hotkey('ctrl', 'p')
                time.sleep(4)
                pyautogui.press('enter')
                time.sleep(6)

                # Clicar no campo do nome do arquivo no canto superior direito (ajuste as coordenadas se necessário)
                pyautogui.click(x=200, y=379)  # Ajuste conforme a resolução da tela
                time.sleep(1)

                # Verifica se o nome_completo está vazio e, se sim, usa a palavra "tipo"
                nome_a_ser_usado = nome_completo if nome_completo else "ajustar" + str(contador)

                # Coloca o nome da lei ou "tipo"
                pyperclip.copy(nome_a_ser_usado)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(7)
                pyautogui.press('enter')

                # Arquivo baixado com sucesso
                arquivo_baixado = "Sim"

                # Fechar aba do texto original
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
            except:
                nova_url = "Indisponível"
                arquivo_baixado = "Não"

            # Fechar a aba secundária e voltar para a principal
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Adicionar ao CSV
            dados.append([nome_completo, data_lei, ementa, situacao, palavra_chave, nova_url, arquivo_baixado])

        except Exception as e:
            print(f"Erro ao processar a {contador}ª lei: {e}")
            continue

    # Verifica se o botão "Próxima" existe e clica nele, se não, termina o loop
    try:
        proxima_pagina = driver.find_element(By.XPATH, "//a[contains(text(), 'Próxima')]")
        proxima_pagina.click()
        time.sleep(4)  # Aguarda a nova página carregar
    except:
        print("Fim da lista de leis!")
        break  # Sai do loop quando não houver mais página "Próxima"

# Salvar os dados no CSV corretamente
with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Nome", "Data", "Ementa", "Situação", "Palavra-chave", "Link da Lei completa", "Arquivo Baixado?"])
    writer.writerows(dados)

print(f"Processo concluído! {contador} leis processadas. CSV salvo em: {CSV_PATH}")
