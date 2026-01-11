from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import jwt
import uvicorn

# Configurações
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

app = FastAPI()


# Modelos de Dados
class Transaction(BaseModel):
    id: int
    account_id: int
    amount: float = Field(..., gt=0)
    transaction_type: str  # "deposit" ou "withdraw"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Account(BaseModel):
    id: int
    owner: str
    balance: float = Field(default=0)
    transactions: List[Transaction] = []


# Simulação de Banco de Dados
accounts = {}
transactions = []

# Autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


# Endpoints
@app.post("/accounts/", response_model=Account)
async def create_account(account: Account):
    if account.id in accounts:
        raise HTTPException(status_code=400, detail="Account already exists")
    accounts[account.id] = account
    return account


@app.post("/transactions/", response_model=Transaction)
async def create_transaction(
    transaction: Transaction, token: str = Depends(oauth2_scheme)
):
    user = verify_jwt_token(token)
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    if (
        transaction.transaction_type == "withdraw"
        and accounts[transaction.account_id].balance < transaction.amount
    ):
        raise HTTPException(status_code=400, detail="Insufficient funds")
    if transaction.transaction_type == "deposit":
        accounts[transaction.account_id].balance += transaction.amount
    elif transaction.transaction_type == "withdraw":
        accounts[transaction.account_id].balance -= transaction.amount
    transactions.append(transaction)
    return transaction


@app.get("/accounts/{account_id}/transactions/", response_model=List[Transaction])
async def get_transactions(account_id: int, token: str = Depends(oauth2_scheme)):
    user = verify_jwt_token(token)
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return [t for t in transactions if t.account_id == account_id]


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Aqui você deve validar o usuário e senha
    # Para fins de exemplo, vamos considerar que o login é sempre bem-sucedido
    token_data = {"sub": form_data.username}
    token = create_jwt_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


# Executar o servidor
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
