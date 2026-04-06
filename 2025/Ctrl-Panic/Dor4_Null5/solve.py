from pwn import *
from Crypto.Hash import SHA256, HMAC
from Crypto.Protocol.KDF import HKDF
from Crypto.Cipher import AES

def compute_path(navigation_key, challenge):
    state = bytearray(16) + bytearray(challenge)
    tracker = AES.new(navigation_key, AES.MODE_ECB)
    for step in range(8):
        scan = tracker.encrypt(bytes(state[step:step + 16]))
        state[16 + step] ^= scan[0]
    return bytes(state[-8:])

def solve_auth(secret_bytes, challenge_hex, server_token_hex):
    challenge = bytes.fromhex(challenge_hex)
    server_token = bytes.fromhex(server_token_hex)

    nav_key = HKDF(
        master=secret_bytes,
        key_len=16,
        salt=challenge + server_token,
        hashmod=SHA256
    )

    expected = compute_path(nav_key, challenge)
    h = HMAC.new(nav_key, expected, SHA256)
    mask = h.digest()[:8]
    
    response = bytes([expected[i] ^ mask[i] for i in range(8)])
    return response.hex()

HOST = 'dora-nulls.ctf.prgy.in'
PORT = 1337

# --- HIPÓTESIS NULL5 ---
# Intentamos con 64 bytes nulos (0x00)
SECRET = b"*" * 64 

io = remote(HOST, PORT, ssl=True)
io.sendlineafter(b"choose ", b"1")

my_challenge = "1122334455667788"
io.sendlineafter(b"challenge (hex): ", my_challenge.encode())
io.sendlineafter(b"username: ", b"Administrator")

io.recvuntil(b"server challenge: ")
server_token = io.recvline().strip().decode()
print(f"[*] Token: {server_token}")

resp_hex = solve_auth(SECRET, my_challenge, server_token)
print(f"[*] Response: {resp_hex}")

io.sendlineafter(b"response (hex): ", resp_hex.encode())
print(io.recvall(timeout=2).decode())
