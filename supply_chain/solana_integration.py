import json
import base58
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.keypair import Keypair # type: ignore
import asyncio

# Function to load keypair from a file
def load_keypair(filepath):
    with open(filepath, 'r') as f:
        secret_key = json.load(f)
        return Keypair.from_bytes(bytes(secret_key))

# Load keypair from file
# WARNING: This is for educational purposes only. In a real application, use secure key management.
keypair = load_keypair('new-keypair.json')

async def send_transaction(transaction_hash):
    async with AsyncClient("https://api.devnet.solana.com") as client:
        # Create a simple JSON message to store on-chain
        message = json.dumps({"transaction_hash": transaction_hash})

        # Get a recent blockhash
        recent_blockhash = await client.get_recent_blockhash()

        # Create a transfer instruction
        transfer_instruction = transfer(TransferParams(
            from_pubkey=keypair.public_key,
            to_pubkey=keypair.public_key,  # Sending to self for this example
            lamports=1000  # 0.000001 SOL
        ))

        # Create a transaction
        transaction = Transaction()
        transaction.add(transfer_instruction)
        transaction.recent_blockhash = recent_blockhash['result']['value']['blockhash']
        transaction.sign(keypair)

        # Send the transaction
        try:
            result = await client.send_transaction(transaction, keypair)
            print(f"Transaction sent to Solana network: {result['result']}")
            return result['result']
        except Exception as e:
            print(f"Error sending transaction to Solana network: {str(e)}")
            return None

def send_transaction_sync(transaction_hash):
    return asyncio.run(send_transaction(transaction_hash))

# Function to display keypair information
def display_keypair_info():
    public_key = keypair.public_key
    secret_key = keypair.secret_key
    print(f"Public Key: {public_key}")
    print(f"Secret Key: {base58.b58encode(bytes(secret_key)).decode('ascii')}")


# Call this function to display keypair information
# display_keypair_info()

# Function to load keypair from secret key
def load_keypair_from_secret(secret_key):
    decoded_secret_key = base58.b58decode(secret_key)
    return Keypair.from_bytes(decoded_secret_key)
# Example usage:
# secret_key = input("Enter your secret key: ")
# keypair = load_keypair_from_secret(secret_key)

