from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configurar o WebDriver do Chrome corretamente
chrome_driver_path = "C:/WebDriver/chromedriver.exe"  # 🔹 Altere para o caminho correto no seu PC
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    # Abrir o site
    driver.get("http://localhost:3000")

    # Encontrar os campos do formulário e preenchê-los
    driver.find_element(By.NAME, "nome").send_keys("Jorge Teste")
    driver.find_element(By.NAME, "email").send_keys("jorge@email.com")
    driver.find_element(By.NAME, "telefone").send_keys("44 4444-4444")
    driver.find_element(By.NAME, "cargo").send_keys("Analista de Testes")

    driver.find_element(By.NAME, "descricao").send_keys("Profissional com experiência em testes automatizados.")
    driver.find_element(By.NAME, "habilidades").send_keys("Selenium, Python, Testes Funcionais")
    driver.find_element(By.NAME, "formacao").send_keys("Engenharia de Software - 2027")

    # Submeter o formulário
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Esperar um pouco para ver a resposta
    time.sleep(2)

    # Verificar se a mensagem de sucesso apareceu
    success_message = driver.find_element(By.TAG_NAME, "p").text
    assert "Currículo de Jorge Teste salvo com sucesso!" in success_message, "Erro: Mensagem de sucesso não encontrada!"

    print("✅ Teste passou: Currículo salvo com sucesso!")

finally:
    # Fechar o navegador
    driver.quit()
