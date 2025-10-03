# 🚀 Mnemonic Wallet Scanner

This project is an experimental Python script that:

* Generates random **BIP39 mnemonic** phrases
* Converts them into **Bitcoin Legacy (P2PKH) addresses**
* Checks balances and activity of addresses via the [Blockstream API](https://blockstream.info/api/)
* Saves found results into files
* Sends notifications via **Telegram** (using Bot API)

⚠️ **Important:** This code is intended for educational and research purposes only. Use responsibly and legally. Do **not** use it to access or attempt to access other people's wallets or funds — that is illegal.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/fh0enix/BIP.git
cd BIP
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📂 Project Files

```
.
├── main.py                # Main script
├── english.txt            # BIP39 wordlist (English)
├── legacy_addresses.bloom # Bloom filter of Legacy addresses
├── .env                   # Configuration keys (ignored by git)
├── requirements.txt       # Dependency list
└── README.md              # This file
```

---

## 🔑 `.env` Configuration

Before running, create a `.env` file in the project root with:

```
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

* Get your bot token from [@BotFather](https://t.me/BotFather).
* Find your chat ID using [@userinfobot](https://t.me/userinfobot).

**Important security steps**

* Do **not** commit `.env` to git. Add to `.gitignore`:

```
.env
```

* Set secure file permissions on `.env` (e.g., `chmod 600 .env` on Unix/WSL).
* For production use, prefer a secret manager (Vault, AWS Secret Manager, Azure Key Vault, etc.) rather than a file.

---

## ▶️ Running the Script

```bash
python main.py
```

Behavior:

* Console displays scanning status
* Found addresses are appended to `found_wallets.txt` and `active_wallets.txt`
* Notifications are sent to the configured Telegram chat

---

## ⚙️ Sample Output

```
[💻] Starting 4 process(es)...

[Thread 1] Legacy | 1L1b5x... | Balance: 0.0 BTC | Active: False
[Thread 2] Legacy | 1Khs7Q... | Balance: 0.0 BTC | Active: True
[•] Active: 1Khs7Q...
```

---

## ✅ requirements.txt

Add the following to `requirements.txt` (already prepared in repo):

```
python-dotenv
base58
ecdsa
requests
pybloom_live
```

Install with:

```bash
pip install -r requirements.txt
```

---

## ✅ .gitignore (suggested)

Add the following `.gitignore` entries to prevent committing secrets and caches:

```
# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Environment
venv/
.env

# Logs
*.log

# OS files
.DS_Store
Thumbs.db
```

---

## 🛡️ Security & Ethics

* **Do not use to hack** other people’s wallets — it is illegal and unethical.
* Use the project only for **testing**, research, and educational purposes (for example, testing Bloom filters, learning about address derivation pipelines, or monitoring *your own* addresses).
* Protect your secrets and any private keys you control. Never paste real private keys into public repositories or chats.

---

## 📌 Future Improvements (TODO)

* [ ] Add SegWit (bech32) address support
* [ ] Add support for Electrum seeds / other seed formats
* [ ] Dockerfile for easy deployment
* [ ] Use a local indexer / node (esplora/bitcoind) to reduce external API rate limits and increase performance
* [ ] Replace naive mnemonic→privkey (sha256 of text) with proper BIP39/BIP32 where appropriate for legitimate use cases

---
