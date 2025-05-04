# Painel Bitget BTC/USDT

Dashboard em Streamlit para análise de trading de futuros de Bitcoin na Bitget.

## Estrutura
- **main.py**: orquestra o dashboard
- **fetch_data.py**: coleta e formata candles da API
- **indicators.py**: cálculo de indicadores técnicos
- **extract_info.py**: sinais de sentimento/tendência/força
- **charts.py**: render de gráficos e tabelas
- **gpt_analysis.py**: integrações com GPT-3.5
- **styles.py**: CSS para paleta light

## Como usar
1. Clone este repositório localmente.
2. Renomeie `.streamlit/secrets.toml` com suas chaves.
3. Crie e ative um virtualenv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Execute:
   ```bash
   streamlit run main.py
   ```

## Criando repositório no GitHub
```bash
# usando GitHub CLI
gh repo create your-organization/painel-trading-bitget --public --source=. --remote=origin
git push -u origin main
```
