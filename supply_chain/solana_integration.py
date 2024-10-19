import json
import base58
import random
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.keypair import Keypair # type: ignore
import asyncio
from solana.exceptions import SolanaRpcException
import logging

# Function to load keypair from a file
def load_keypair(filepath):
    with open(filepath, 'r') as f:
        secret_key = json.load(f)
        return Keypair.from_bytes(bytes(secret_key))

# Load keypair from file
# WARNING: This is for educational purposes only. In a real application, use secure key management.
keypair = load_keypair('new-keypair.json')

async def send_transaction(transaction_hash, max_retries=5, initial_delay=1):
    async with AsyncClient("https://api.devnet.solana.com") as client:
        keypair = load_keypair('new-keypair.json')
        
        for attempt in range(max_retries):
            try:
                await request_airdrop(client, keypair.pubkey())
                
                message = json.dumps({"transaction_hash": transaction_hash})
                
                recent_blockhash = await client.get_latest_blockhash()
                
                transfer_instruction = transfer(TransferParams(
                    from_pubkey=keypair.pubkey(),
                    to_pubkey=keypair.pubkey(),
                    lamports=1000
                ))
                
                transaction = Transaction()
                transaction.add(transfer_instruction)
                transaction.recent_blockhash = recent_blockhash.value.blockhash
                transaction.sign(keypair)
                
                result = await client.send_transaction(transaction, keypair)
                print(f"Transaction sent to Solana network: {result['result']}")
                return result['result']
            except SolanaRpcException as e:
                if "429 Too Many Requests" in str(e) and attempt < max_retries - 1:
                    delay = initial_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"Rate limit exceeded. Retrying transaction in {delay:.2f} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logging.debug(f"Error sending transaction to Solana network: {str(e)}")
            except Exception as e:
                logging.debug(f"Unexpected error sending transaction: {str(e)}")
    return None

def send_transaction_sync(transaction_hash):
    return asyncio.run(send_transaction(transaction_hash, max_retries=5, initial_delay=1))

# Function to display keypair information
def display_keypair_info():
    public_key = keypair.pubkey()
    secret_key = keypair.secret_key()
    print(f"Public Key: {public_key}")
    print(f"Secret Key: {base58.b58encode(bytes(secret_key)).decode('ascii')}")

# Function to load keypair from secret key
def load_keypair_from_secret(secret_key):
    decoded_secret_key = base58.b58decode(secret_key)
    return Keypair.from_bytes(decoded_secret_key)

async def request_airdrop(client, public_key, amount=1000000000, max_retries=5, initial_delay=1):
    for attempt in range(max_retries):
        try:
            airdrop_tx = await client.request_airdrop(public_key, amount)
            await client.confirm_transaction(airdrop_tx['result'])
            print(f"Airdrop of {amount/1000000000} SOL requested for {public_key}")
            return airdrop_tx['result']
        except SolanaRpcException as e:
            if "429 Too Many Requests" in str(e) and attempt < max_retries - 1:
                delay = initial_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limit exceeded. Retrying airdrop in {delay:.2f} seconds...")
                await asyncio.sleep(delay)
            else:
                logging.debug(f"Error requesting airdrop: {str(e)}")
        except Exception as e:
            logging.debug(f"Unexpected error requesting airdrop: {str(e)}")
    return None