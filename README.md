# Magic Formula Greenblatt

Script Python para implementar a estratégia de investimento Magic Formula de Joel Greenblatt. Esta estratégia foca em identificar ações de alta qualidade e baixo custo, com base em métricas financeiras específicas.

## Variação 1
Utilizando indicadores P/L e ROE.

## Variação 2
Utilizando indicadores EV/EBIT e ROIC (nessa variação, alguns setores são excluídos, como bancos e seguradoras).

## Preparando o ambiente
1. Crie um ambiente virtual: `python -m venv .venv`
2. Ative o ambiente virtual:
   - No Windows: `.venv\Scripts\activate`
   - No macOS/Linux: `source .venv/bin/activate`
3. Instale as dependências: `pip install -r requirements.txt`

## Como utilizar
Baixe os ativos do site do [Status Invest](https://statusinvest.com.br/acoes/busca-avancada) e salve o arquivo como `stocks.csv` na raiz do projeto. Em seguida, execute o script Python.