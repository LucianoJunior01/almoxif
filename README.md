# AlmoxIF — Sistema de Gestão de Almoxarifado

Projeto Integrador para gestão de estoque de almoxarifado, com integração 
a um sistema externo (Portal do Fornecedor) através de um banco de dados 
compartilhado na nuvem.

## Acesso direto
https://almoxif-production.up.railway.app

## Sistema integrado
Este sistema recebe dados de Notas Fiscais enviados pelo Portal do Fornecedor:
https://github.com/LucianoJunior01/portal-fornecedor

## Tecnologias utilizadas
- Python 3.12
- Flask
- PostgreSQL (Railway)
- Bootstrap 5

## Como executar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/LucianoJunior01/almoxif.git
cd almoxif
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a variável de ambiente DATABASE_URL
Aponte para um banco PostgreSQL.

### 4. Execute o sistema
```bash
python app.py
```

### 5. Acesse no navegador
http://127.0.0.1:8080

## Funcionalidades
- Cadastro de Produtos
- Cadastro de Fornecedores
- Entrada de Estoque vinculada à Nota Fiscal
- Saída de Estoque
- Dashboard com métricas em tempo real
- Relatórios com filtro por período