# API Banco Python Flask

Este projeto é uma API simples desenvolvida com FastAPI para gerenciar contas bancárias e transações. A API permite a criação de contas, realização de depósitos e saques, além de consultar transações associadas a uma conta específica.

## Funcionalidades

- **Gerenciamento de Contas**: Criação de contas bancárias com um identificador único, proprietário e saldo inicial.
- **Transações**: Realização de depósitos e saques, com validação de saldo suficiente para saques.
- **Autenticação**: Implementação de autenticação via JWT (JSON Web Token) para proteger os endpoints de transações e consulta de transações.
- **Endpoints**:
    - `POST /accounts/`: Cria uma nova conta.
    - `POST /transactions/`: Realiza uma nova transação (depósito ou saque).
    - `GET /accounts/{account_id}/transactions/`: Recupera todas as transações de uma conta específica.
    - `POST /token`: Gera um token de acesso para autenticação.

## Requisitos

- Python 3.12 ou superior
- FastAPI
- Uvicorn
- Pydantic
- PyJWT

## Licença

Este projeto está licenciado sob a Licença MIT.