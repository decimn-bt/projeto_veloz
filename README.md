# Controle de Estoque

Sistema web desenvolvido em Django para gerar uma lista de compras de ingredientes de restaurante a partir das regras de negócio do desafio técnico.

## Regras de negócio

- Quando o estoque atual é suficiente para a meta, não há compra.
- Quando o estoque atual é menor que a meta, a compra normal é a diferença entre a meta e o estoque atual.
- Quando um ingrediente está vencido, todo o estoque é considerado inutilizável e a compra é igual à meta.
- Quando o ingrediente acabou durante o mês, a compra é calculada com base no consumo informado acrescido de 20%.
- O sistema identifica automaticamente uma situação de falta quando o consumo mensal é maior que o estoque atual e também maior que a meta.
- Cada ingrediente possui sua própria unidade de medida.
- Itens com quantidade zero ou negativa não aparecem na lista final.

## Segurança implementada

### SQL Injection

O acesso aos ingredientes utiliza o ORM do Django e filtros parametrizados. Não existem consultas SQL construídas por concatenação de entrada do usuário e não existem chamadas a `raw()`, `extra()` ou SQL manual na aplicação.

### Injeção de comandos no shell

A aplicação web não executa comandos de shell a partir de dados enviados por usuários. O processo de build do Render usa apenas comandos fixos do próprio projeto.

### Mass Assignment

A tela operacional aceita somente o campo `quantidade` para registrar consumo e usa uma operação de serviço dedicada. O formulário administrativo declara explicitamente os campos permitidos e não recebe campos arbitrários do request para atualização do modelo.

### Race Condition em estoque

O registro de consumo é executado dentro de `transaction.atomic()` e usa `select_for_update()` para bloquear a linha do ingrediente durante a operação. A atualização também usa uma condição `estoque_atual__gte` junto de `F()` para que o banco nunca aplique uma redução que levaria o estoque abaixo do valor disponível.

### Integridade dos dados

`meta`, `estoque_atual` e `consumo_mensal` não aceitam valores negativos pela validação do modelo e pelas constraints do banco.

### Proteções web

Em produção, o projeto utiliza HTTPS obrigatório, HSTS, cookies seguros, proteção CSRF do Django, `X-Frame-Options`, proteção contra MIME sniffing e WhiteNoise para arquivos estáticos.

## Funcionalidades

- Lista automática de compras.
- Busca segura por nome do ingrediente.
- Cadastro e manutenção pelo Django Admin.
- Registro autenticado de consumo.
- Detecção automática de consumo acima do estoque e da meta.
- Endpoint `/health/` para verificação de saúde da aplicação.
- PostgreSQL em produção.
- Arquivos estáticos preparados para Render.

## Requisitos

- Python 3.13 recomendado
- pip
- Git
- Conta no GitHub
- Conta no Render para hospedagem

## Instalação local

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env` se quiser manter as variáveis localmente. O projeto continua funcionando localmente com SQLite quando `DATABASE_URL` não está configurada.

Crie as tabelas:

```bash
python manage.py migrate
```

Crie o usuário administrador:

```bash
python manage.py createsuperuser
```

Execute:

```bash
python manage.py runserver
```

Acesse:

- Sistema: http://127.0.0.1:8000/
- Administração: http://127.0.0.1:8000/admin/
- Health check: http://127.0.0.1:8000/health/

## Testes

Execute:

```bash
python manage.py test
```

Os testes cobrem a reposição normal, ingrediente vencido, detecção automática de consumo acima do estoque e da meta e bloqueio de consumo superior ao estoque.

## Exemplo da nova detecção

Meta: `10 Kg`

Estoque atual: `2 Kg`

Consumo mensal: `15 Kg`

Como o consumo é maior que o estoque e maior que a meta, a aplicação identifica automaticamente a situação e aplica os 20% adicionais:

```text
Comprar: 18.00 Kg de Farinha
```

## Deploy no Render

O projeto já contém `render.yaml`, `build.sh`, `.python-version` e as configurações necessárias para o deploy.

### 1. Suba o projeto para o GitHub

Crie um repositório público no GitHub e envie todos os arquivos do projeto:

```bash
git init
git add .
git commit -m "Entrega inicial do controle de estoque"
git branch -M main
git remote add origin URL_DO_SEU_REPOSITORIO
git push -u origin main
```

Não envie `.env`, banco SQLite ou qualquer segredo para o repositório.

### 2. Conecte o GitHub ao Render

No Render, crie um Blueprint e selecione o repositório que contém `render.yaml`.

O blueprint cria:

- Um serviço web Django.
- Um banco PostgreSQL.
- `DATABASE_URL` ligado automaticamente ao banco.
- `SECRET_KEY` gerada automaticamente.
- Build usando `build.sh`.
- Health check em `/health/`.

O Render fornece uma URL pública `onrender.com` depois do deploy.

### 3. Crie o administrador em produção

Depois que o serviço estiver online, abra o Shell do serviço no Render e execute:

```bash
python manage.py createsuperuser
```

### 4. Verifique o sistema

Acesse a URL pública fornecida pelo Render e depois `/admin/` para cadastrar os ingredientes.

## Ambiente de produção

O projeto usa `DATABASE_URL` para conectar ao PostgreSQL, `SECRET_KEY` para segredo do Django e variáveis de ambiente para configuração. Essas informações não ficam gravadas no código.

A configuração também usa `RENDER_EXTERNAL_HOSTNAME` para permitir o domínio atribuído pelo Render e para configurar a origem confiável do CSRF.

## Estrutura

```text
controle_estoque/
├── build.sh
├── manage.py
├── render.yaml
├── requirements.txt
├── .python-version
├── .env.example
├── .gitignore
├── README.md
├── controle_estoque/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── estoque/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── templates/
│   └── estoque/
│       └── lista_compras.html
└── static/
    └── estoque/
        └── style.css
```
