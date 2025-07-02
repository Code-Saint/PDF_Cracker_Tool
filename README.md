# 🔓 PDF Cracker Tool – Password Brute-Force Utility

## 🔍 Overview

This Python-based tool is designed to **brute-force password-protected PDF files** using a user-provided password list. The tool attempts each password from the wordlist until it successfully opens and decrypts the PDF. This project simulates how attackers or red teamers may attempt to crack weakly secured documents.

⚠️ This tool is developed purely for **educational, legal, and internal penetration testing use only**.

---

## 💡 Features

- 🧠 Dictionary-based brute-force using a custom wordlist
- 📄 Supports both encrypted and owner-locked PDFs
- ⚙️ Multi-threaded version available for faster processing
- 🛠️ Graceful handling of failed attempts and corrupted PDFs
- 📥 Displays and optionally saves the cracked password

---

## ⚙️ Technologies Used

- Python 3.x
- `PyPDF2` or `pikepdf` – for PDF parsing and password handling
- `argparse` – for CLI-based usage
- `threading` – (optional) for multi-threaded brute-force

---
## 🚀 Usage

### Install Dependencies:
```bash
pip install pikepdf
```

## 🛠 Run the Tool:

```bash
python pdf_cracker.py -f protected.pdf -w passwords.txt
```
