# 🚀 Mnemonic Wallet Scanner

This project is an experimental Python script that:
- Generates random **BIP39 mnemonic** phrases
- Converts them into **Bitcoin Legacy (P2PKH) addresses**
- Checks balances and activity of addresses via the [Blockstream API](https://blockstream.info/api/)
- Saves found results into files
- Sends notifications via **Telegram** (using Bot API)

⚠️ **Important:** This code is intended for educational and research purposes only. Use responsibly!



## 📦 Installation

### 1. Clone the repository

git clone https://github.com/your-username/mnemonic-wallet-scanner.git
cd mnemonic-wallet-scanner
2. Create and activate a virtual environment


python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
3. Install dependencies


pip install --upgrade pip
pip install -r requirements.txt
📂 Project Files


.
├── main.py                # Main script
├── english.txt            # BIP39 wordlist (English)
├── legacy_addresses.bloom # Bloom filter of Legacy addresses
├── .env                   # Configuration keys (ignored by git)
├── requirements.txt       # Dependency list
└── README.md              # This file
🔑 .env Configuration
Before running, create a .env file in the project root:



TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
Get your bot token from @BotFather

Find your chat ID using @userinfobot

⚠️ Do not commit .env to git! Add it to .gitignore:



.env
▶️ Running the Script


python main.py
On run:

Console displays scanning status

Found addresses are saved to found_wallets.txt and active_wallets.txt

Notifications are sent to Telegram

⚙️ Sample Output


[💻] Starting 4 process(es)...

[Thread 1] Legacy | 1L1b5x... | Balance: 0.0 BTC | Active: False
[Thread 2] Legacy | 1Khs7Q... | Balance: 0.0 BTC | Active: True
[•] Active: 1Khs7Q...
🛡️ Security & Ethics
Do not use to hack other people’s wallets — it is illegal

This project is for testing Bloom filters and demonstrating Bitcoin API usage

Keep your .env secrets safe

📌 TODO
 Add SegWit (bech32) address support

 Support for Electrum seeds

 Dockerfile for easy deployment




---

### 2️⃣ `requirements.txt`
python-dotenv
base58
ecdsa
requests
pybloom_live




---

### 3️⃣ `.gitignore`
Python cache
pycache/
*.pyc
*.pyo
*.pyd

Environment
venv/
.env

Logs
*.log

OS files
.DS_Store
Thumbs.db
