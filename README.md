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
