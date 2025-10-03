import os
from dotenv import load_dotenv
from pathlib import Path
import hashlib
import base58
import requests
import random
import time
from ecdsa import SigningKey, SECP256k1
from multiprocessing import Process, Lock, cpu_count
from pybloom_live import BloomFilter

# Load .env from project root (if exists)
env_path = Path('.') / '.env'
load_dotenv(env_path)  # automatically reads .env and sets os.environ

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise RuntimeError("TELEGRAM_TOKEN or TELEGRAM_CHAT_ID not set in .env or environment.")

# === Load BIP39 wordlist ===
with open("english.txt", "r", encoding="utf-8") as f:
    WORDLIST = [word.strip() for word in f.readlines()]

# === Load Bloom filter for Legacy addresses (P2PKH) ===
BLOOM_FILTER_FILE = "legacy_addresses.bloom"
with open(BLOOM_FILTER_FILE, "rb") as bf_file:
    bloom = BloomFilter.fromfile(bf_file)

# === Telegram message ===
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[!] Telegram error: {e}")

# === Mnemonic → private key ===
def generate_mnemonic():
    return ' '.join(random.choices(WORDLIST, k=12))

def mnemonic_to_private_key(mnemonic: str) -> bytes:
    return hashlib.sha256(mnemonic.encode()).digest()

# === Public key ===
def private_key_to_public_key(priv_key: bytes) -> bytes:
    sk = SigningKey.from_string(priv_key, curve=SECP256k1)
    vk = sk.verifying_key
    return b'\x04' + vk.to_string()

# === Legacy (P2PKH) address ===
def public_key_to_legacy_address(pub_key: bytes) -> str:
    pub_sha256 = hashlib.sha256(pub_key).digest()
    ripemd160 = hashlib.new('ripemd160', pub_sha256).digest()
    payload = b'\x00' + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58.b58encode(payload + checksum).decode()

# === Check balance ===
def check_balance_and_activity(address: str):
    # Only check Bloom filter for Legacy addresses
    if not address.startswith('1'):
        return 0.0, False  # Ignore addresses not starting with '1'

    if address not in bloom:
        # Address not in filter — balance is definitely 0, no API call
        return 0.0, False

    try:
        url = f"https://blockstream.info/api/address/{address}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            d = r.json()
            funded = d["chain_stats"]["funded_txo_sum"]
            spent = d["chain_stats"]["spent_txo_sum"]
            mem_funded = d["mempool_stats"]["funded_txo_sum"]
            mem_spent = d["mempool_stats"]["spent_txo_sum"]
            balance = (funded - spent + mem_funded - mem_spent) / 1e8
            active = d["chain_stats"]["tx_count"] > 0
            return balance, active
    except Exception as e:
        # You can log e if needed
        pass
    return 0.0, False

# === Save found wallets ===
def save_wallet(filename, lock, mnemonic, priv_key, address, balance):
    message = (
        f"🔐 *Wallet found!*\n"
        f"`{filename}`\n"
        f"*Address:* `{address}`\n"
        f"*Balance:* `{balance}` BTC\n"
        f"*Mnemonic:* `{mnemonic}`\n"
        f"*Private key:* `{priv_key}`"
    )
    with lock:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"Mnemonic: {mnemonic}\n")
            f.write(f"Private Key (hex): {priv_key}\n")
            f.write(f"Address: {address}\n")
            f.write(f"Balance: {balance} BTC\n")
            f.write("="*60 + "\n")
        send_telegram(message)

# === Main worker function ===
def worker(lock, id):
    checked = 0
    while True:
        mnemonic = generate_mnemonic()
        priv_key = mnemonic_to_private_key(mnemonic)
        pub_key = private_key_to_public_key(priv_key)

        try:
            addr = public_key_to_legacy_address(pub_key)
        except Exception as e:
            print(f"[!] Address error: {e}")
            continue

        balance, active = check_balance_and_activity(addr)
        checked += 1
        print(f"[Thread {id}] Legacy | {addr} | Balance: {balance} BTC | Active: {active}")

        if balance > 0:
            save_wallet("found_wallets.txt", lock, mnemonic, priv_key.hex(), addr, balance)
            print(f"[✓] WITH BALANCE: {addr} → {balance} BTC")
        elif active:
            save_wallet("active_wallets.txt", lock, mnemonic, priv_key.hex(), addr, balance)
            print(f"[•] Active: {addr}")

        time.sleep(0.3)

# === Entry point ===
if __name__ == "__main__":
    send_telegram("🚀 Script started! Beginning phrase checks...")

    THREADS = min(cpu_count(), 4)
    lock = Lock()

    print(f"[💻] Starting {THREADS} process(es)...\n")
    Path("found_wallets.txt").touch()
    Path("active_wallets.txt").touch()

    processes = []
    for i in range(THREADS):
        p = Process(target=worker, args=(lock, i+1))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
