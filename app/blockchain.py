import os
from web3 import Web3
from fastapi import APIRouter

router = APIRouter()

w3 = Web3(Web3.HTTPProvider(os.getenv("ETHEREUM_RPC_URL", "http://localhost:8545")))

@router.get("/network")
def get_network():
    return {
        "connected": w3.is_connected(),
        "chain_id": w3.eth.chain_id,
        "latest_block": w3.eth.block_number,
    }

@router.get("/accounts")
def get_accounts():
    return {"accounts": w3.eth.accounts}
