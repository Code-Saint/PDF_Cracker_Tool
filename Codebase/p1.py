import argparse
import pikepdf
from pikepdf import PasswordError
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import string
import itertools
import os
import sys

# 1. Generator to load passwords from a wordlist file
def load_passwords(wordlist_path):
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        print(f"[!] Wordlist file '{wordlist_path}' not found.")
        sys.exit(1)

# 2. Generator to generate brute-force passwords
def generate_passwords(chars, max_length):
    for length in range(1, max_length + 1):
        for combo in itertools.product(chars, repeat=length):
            yield ''.join(combo)

# 3. Function to try opening PDF with a given password
def try_password(pdf_path, password):
    try:
        with pikepdf.open(pdf_path, password=password):
            return password
    except PasswordError:
        return None
    except Exception as e:
        return None  # Ignore errors other than incorrect password

# def decrypt_pdf(pdf_path, passwords, max_workers=4):
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = [executor.submit(try_password, pdf_path, pwd) for pwd in passwords]
#         for future in as_completed(futures):
#             result = future.result()
#             if result:
#                 return result
#     return None

# 4. Decryption function using multithreading + tqdm
def decrypt_pdf(pdf_path, passwords, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_password = {
            executor.submit(try_password, pdf_path, pwd): pwd
            for pwd in passwords
        }
        for future in tqdm(as_completed(future_to_password), total=len(future_to_password), desc="Trying passwords"):
            result = future.result()
            if result:
                return result
    return None

# 5. Argument Parsing and Main Execution
def main():
    parser = argparse.ArgumentParser(description="PDF Password Cracker")
    parser.add_argument("pdf_file", help="Path to the password-protected PDF file")
    parser.add_argument("--wordlist", help="Path to a wordlist file")
    parser.add_argument("--generate", action="store_true", help="Use brute-force password generation")
    parser.add_argument("--max-length", type=int, default=3, help="Max length for brute-force generation (default=3)")
    parser.add_argument("--charset", type=str, default=string.ascii_letters + string.digits + string.punctuation, help="Characters to use in brute-force (default=lowercase letters)")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads to use (default=4)")
    args = parser.parse_args()

    # Check if PDF exists
    if not os.path.exists(args.pdf_file):
        print(f"[!] PDF file '{args.pdf_file}' not found.")
        sys.exit(1)

    # Select password source
    if args.wordlist:
        passwords = list(load_passwords(args.wordlist))
    elif args.generate:
        passwords = list(generate_passwords(args.charset, args.max_length))
    else:
        print("[!] Please provide a wordlist or use --generate to brute-force.")
        sys.exit(1)

    print(f"[*] Starting attack on: {args.pdf_file}")
    print(f"[*] Total passwords to try: {len(passwords)}")

    found_password = decrypt_pdf(args.pdf_file, passwords, max_workers=args.threads)

    if found_password:
        print(f"[+] Password found: '{found_password}'")
    else:
        print("[-] Password not found.")

# Run main if script is executed
if __name__ == "__main__":
    main()



