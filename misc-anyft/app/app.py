import web3
import socket
import os
import threading
import secrets
import json
from dotenv import load_dotenv

load_dotenv()

with open("/app/aNyFT.json", 'r') as f:   
    data = json.load(f)
    contract_abi = data['abi']
    contract_addr = data['networks'][os.getenv("NETWORKID")]['address']

def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 1337))
    sock.listen(20)
    
    print("Started server on port 1337")
    return sock

def client(conn, addr):
    token = secrets.token_bytes(16)
    
    conn.send(f"Hello! The contract is running at {contract_addr} on the Sepolia Testnet.\nHere is your token id: 0x{token.hex()}\n".encode())
    conn.send(b"Are you ready to receive your flag? (y/n)\n")
    conn.settimeout(300.0)
    
    data = conn.recv(16)  
    if len(data) > 0 and data.decode("ascii").lower()[0] != 'y': 
        conn.send(b"Come back when you are ready for the flag\n")  
        conn.close()
        return
            
    if contractEmitsToken(token):
        print(f'Sent flag to {addr}')
        conn.send(f"Here is the flag: {flag}\n".encode())
    else:
        conn.send(b"Token not emitted by flag\n")
        
    conn.close()

def run_socket(sock):
    while True:
        conn, addr = sock.accept()
        print("Starting thread for", addr)
        threading.Thread(target=client, args=(conn,addr), daemon=True).start()

def contractEmitsToken(token):
    event_filter = contract.events.GetFlag.create_filter(fromBlock=w3.eth.block_number-10, toBlock=w3.eth.block_number)

    for i in event_filter.get_all_entries():   
        if i['event'] == 'GetFlag' and i['args'].flag[0:16] == token:
            return True
        
    return False
    
if __name__ == "__main__":
    flag = os.getenv("FLAG")
    
    provider = web3.providers.HTTPProvider(f'https://sepolia.infura.io/v3/{os.getenv("ACCESSTOKEN")}')
    w3 = web3.Web3(provider)

    contract = w3.eth.contract(address=contract_addr, abi=contract_abi)
    print("Contract loaded at", contract_addr)
    
    socket = create_socket()
    run_socket(socket)
    
