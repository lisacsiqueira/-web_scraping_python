# Scraper do site: Portal da Câmara dos Deputados

Este script automatiza a busca e extração de informações sobre leis diretamente do site da Câmara dos Deputados. Ele utiliza **Selenium** para navegar na página, coletar dados das leis e baixar os arquivos em PDF através da funcionalidade de impressão automática.

## 🚀 Funcionalidades
- Busca automatizada de leis.
- Extração de informações como **nome da lei, data, ementa, situação e link para o texto completo**.
- Download automático do texto original da lei em formato PDF.
- Salvamento dos dados em um arquivo CSV para fácil consulta.

## 📌 Tecnologias Utilizadas
- **Python**
- **Selenium** para automação de navegação na web
- **PyAutoGUI** para interações com a interface gráfica
- **Pyperclip** para manipulação de texto na área de transferência
- **CSV** para armazenamento estruturado dos dados coletados

## 📦 Instalação e Configuração
### 1️⃣ Pré-requisitos
Antes de rodar o script, certifique-se de ter:
- Python 3.x instalado
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome
- Dependências instaladas:

```sh
pip install selenium pyautogui pyperclip
```

### 2️⃣ Configuração do Locale (Para Reconhecimento de Datas)
- **Windows**: Já configurado no script para `Portuguese_Brazil`.
- **Linux/macOS**: Alterar manualmente no script para `pt_BR.utf8` caso necessário.

## 🔧 Como Usar
1. **Baixe o repositório** ou clone:
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```
2. **Execute o script**:
   ```sh
   python scraper_leis.py
   ```
3. O script irá navegar pelas páginas, coletar informações e salvar tudo no arquivo **`leis_bombeiro_militar.csv`**.

## 📂 Estrutura do CSV Gerado
| Nome da Lei | Data | Ementa | Situação | Palavra-chave | Link da Lei Completa | Arquivo Baixado? |
|------------|------|--------|----------|---------------|-----------------------|------------------|
| Lei XYZ | 10/01/2020 | Estabelece diretrizes... | Em vigor | Bombeiro militar | [Link](https://...) | Sim |

## ⚠️ Observações
- O script pode ser rodado com **modo headless** ativado, removendo a interface do Chrome (basta descomentar `options.add_argument("--headless")`).
- Certifique-se de que o **Google Chrome e ChromeDriver** estão atualizados para evitar erros de compatibilidade.

## 📌 Melhorias Futuras
- Melhor tratamento de erros para páginas sem PDF disponível.
- Suporte para diferentes navegadores.
- Interface gráfica para facilitar a configuração.

---
📌 **Criado por:** Lisa A. C. Siqueira 
📅 **Última atualização:** Fevereiro / 2025

