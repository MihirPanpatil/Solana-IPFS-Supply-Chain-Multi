import ipfshttpclient
import json

def add_to_ipfs(data):
    try:
        with ipfshttpclient.connect() as client:
            res = client.add_json(data)
            return res
    except Exception as e:
        print(f"Error adding data to IPFS: {str(e)}")
        return None

def add_file_to_ipfs(file):
    try:
        with ipfshttpclient.connect() as client:
            res = client.add(file)
            return res['Hash']
    except Exception as e:
        print(f"Error adding file to IPFS: {str(e)}")
        return None

def get_from_ipfs(ipfs_hash):
    with ipfshttpclient.connect() as client:
        return client.cat(ipfs_hash)