from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from web3 import Web3
import os

router = APIRouter()

w3 = Web3(Web3.HTTPProvider(os.getenv("ETHEREUM_RPC_URL", "http://localhost:8545")))


class WalletCreateResponse(BaseModel):
    address: str
    private_key: str


class TransactionRequest(BaseModel):
    from_address: str = Field(..., description="Sender address")
    to_address: str = Field(..., description="Recipient address")
    value_ether: float = Field(..., gt=0, description="Ether amount to send")
    private_key: str = Field(..., description="Private key for signing")


class SignMessageRequest(BaseModel):
    private_key: str = Field(..., description="Private key used to sign")
    message: str = Field(..., description="Message to sign")


class DeployContractRequest(BaseModel):
    abi: list = Field(..., description="Contract ABI")
    bytecode: str = Field(..., description="Compiled contract bytecode")
    from_address: str = Field(..., description="Address deploying the contract")
    private_key: str = Field(..., description="Private key for signing")
    args: list = Field(default_factory=list, description="Constructor arguments")


@router.get("/network")
def get_network():
    if not w3.is_connected():
        raise HTTPException(status_code=503, detail="Ethereum node is not reachable")
    return {
        "connected": True,
        "chain_id": w3.eth.chain_id,
        "latest_block": w3.eth.block_number,
    }


@router.get("/accounts")
def get_accounts():
    if not w3.is_connected():
        raise HTTPException(status_code=503, detail="Ethereum node is not reachable")
    return {"accounts": w3.eth.accounts}


@router.post("/wallet/create", response_model=WalletCreateResponse)
def create_wallet():
    account = w3.eth.account.create()
    return {
        "address": account.address,
        "private_key": account.key.hex(),
    }


@router.post("/wallet/send-transaction")
def send_transaction(payload: TransactionRequest):
    if not w3.is_connected():
        raise HTTPException(status_code=503, detail="Ethereum node is not reachable")

    value_wei = w3.to_wei(payload.value_ether, "ether")
    tx = {
        "chainId": w3.eth.chain_id,
        "from": payload.from_address,
        "to": payload.to_address,
        "value": value_wei,
        "gas": 21000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(payload.from_address),
    }

    signed_tx = w3.eth.account.sign_transaction(tx, payload.private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return {
        "transaction_hash": tx_hash.hex(),
        "status": "submitted",
    }


@router.post("/wallet/sign-message")
def sign_message(payload: SignMessageRequest):
    account = w3.eth.account.from_key(payload.private_key)
    signed = account.sign_message(payload.message.encode("utf-8"))
    return {
        "address": account.address,
        "signature": signed.signature.hex(),
        "message": payload.message,
    }


@router.post("/contract/deploy")
def deploy_contract(payload: DeployContractRequest):
    if not w3.is_connected():
        raise HTTPException(status_code=503, detail="Ethereum node is not reachable")

    contract = w3.eth.contract(abi=payload.abi, bytecode=payload.bytecode)
    account = w3.eth.account.from_key(payload.private_key)
    tx = contract.constructor(*payload.args).build_transaction({
        "from": payload.from_address,
        "gas": 3000000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(payload.from_address),
        "chainId": w3.eth.chain_id,
    })
    signed_tx = w3.eth.account.sign_transaction(tx, payload.private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return {
        "transaction_hash": tx_hash.hex(),
        "contract_address": tx_receipt["contractAddress"],
        "status": tx_receipt["status"],
    }


blockchain_router = router
