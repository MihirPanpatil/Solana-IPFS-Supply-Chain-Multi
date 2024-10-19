import ipfshttpclient

def add_to_ipfs(data):
    with ipfshttpclient.connect() as client:
        res = client.add_json(data)
        return res  # This should return the hash directly

def get_from_ipfs(ipfs_hash):
    with ipfshttpclient.connect() as client:
        return client.get_json(ipfs_hash)
