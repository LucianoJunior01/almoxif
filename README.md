# AlmoxIF — Sistema de Gestão de Almoxarifado

Sistema desenvolvido como Projeto Integrador, simulando a integração entre 
o sistema de emissão de Notas Fiscais (Sistema X) e o sistema de gestão 
de almoxarifado (Sistema Y).

## Tecnologias utilizadas
- Python 3.12
- Flask
- SQLite
- Bootstrap 5

## Como executar o projeto

### 1. Clone o repositório
git clone https://github.com/LucianoJunior01/almoxif.git
cd almoxif

### 2. Instale as dependências
pip install -r requirements.txt

### 3. Execute o sistema
python app.py

### 4. Acesse no navegador
http://localhost:8080

## Funcionalidades
- Cadastro de Produtos
- Cadastro de Fornecedores
- Entrada de Estoque vinculada à Nota Fiscal
- Saída de Estoque
- Dashboard com métricas em tempo real
- Relatórios com filtro por período