#!/usr/bin/env python3
import os, sys, time, importlib.util, subprocess, base64

# === PASSWORD PROTEKSI ===
PASSWORD = "GUSTI123"  # ganti sesuai keinginan
MAX_ATTEMPT = 3

def auth():
    attempts = 0
    while attempts < MAX_ATTEMPT:
        pw = input("Masukkan password: ")
        if pw == PASSWORD:
            print("\033[92m[✓] Password benar, akses diberikan!\033[0m\n")
            return True
        else:
            print("\033[91m[✗] Password salah!\033[0m\n")
            attempts += 1
    print("\033[91m[!] Terlalu banyak percobaan gagal. Keluar...\033[0m")
    sys.exit()

# === CEK & INSTALL MODULE ===
modules = ["requests", "rich"]

def slow_print(text, delay=0.03):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def cek_module():
    os.system("clear")
    print("\033[96m============================")
    print("   Cek & Install Modules")
    print("============================\033[0m\n")

    for mod in modules:
        spec = importlib.util.find_spec(mod)
        if spec is None:
            slow_print(f"\033[91m[✗] {mod} belum terinstall...\033[0m")
            time.sleep(0.5)
            slow_print(f"\033[93m[!] Menginstall {mod}...\033[0m")
            subprocess.check_call([sys.executable, "-m", "pip", "install", mod])
            slow_print(f"\033[92m[✓] {mod} berhasil diinstall!\033[0m\n")
        else:
            slow_print(f"\033[92m[✓] {mod} sudah terinstall\033[0m\n")
        time.sleep(0.5)

    slow_print("\033[96mSemua modul sudah siap!\033[0m")
    time.sleep(1.5)

cek_module()

# === IMPORT SETELAH INSTALL ===
import requests
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
API_BASE = "https://kyami-rest-api.vercel.app/stalk"

# === LOADING SPINNER ===
def loading_request(url):
    with Progress(SpinnerColumn(), TextColumn("[cyan]Mengambil data..."), transient=True) as progress:
        task = progress.add_task("wait")
        try:
            r = requests.get(url, timeout=15).json()
            progress.update(task, advance=100)
            return r
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
            return None

# === BANNER ===
def banner():
    console.print("[bold cyan]\n============================[/]")
    console.print("[bold green]   OSINT TOOLS by Gusti[/]")
    console.print("[bold cyan]============================[/]\n")

# === MENU ===
def menu():
    banner()
    console.print("[yellow]1.[/] Instagram Stalk")
    console.print("[red]2.[/] TikTok Stalk")
    console.print("[blue]3.[/] GitHub Stalk")
    console.print("[pink]4.[/] NPM Package Stalk")
    console.print("[cyan]5.[/] Keluar\n")

    pilih = input("Pilih menu: ")
    if pilih == "1":
        user = input("Masukkan username IG: ")
        stalk_instagram(user)
    elif pilih == "2":
        user = input("Masukkan username TikTok: ")
        stalk_tiktok(user)
    elif pilih == "3":
        user = input("Masukkan username GitHub: ")
        stalk_github(user)
    elif pilih == "4":
        pkg = input("Masukkan nama package NPM: ")
        stalk_npm(pkg)
    else:
        sys.exit()

# === FUNGSI OSINT ===
def stalk_instagram(user):
    url = f"{API_BASE}/instagram?user={user}"
    r = loading_request(url)
    if r and r["status"]:
        data = r["result"]
        table = Table(title=f"Instagram OSINT: {user}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Name", data.get("name", "-"))
        table.add_row("Username", data.get("username", "-"))
        table.add_row("Bio", data.get("bio", "-"))
        table.add_row("Posts", str(data.get("posts", "-")))
        table.add_row("Followers", str(data.get("followers", "-")))
        table.add_row("Following", str(data.get("following", "-")))
        table.add_row("Avatar", data.get("avatar", "-"))

        console.print(table)
    else:
        console.print("[red]Gagal ambil data Instagram[/]")

def stalk_tiktok(user):
    url = f"{API_BASE}/tiktok?user={user}"
    r = loading_request(url)
    if r and r["status"]:
        data = r["result"]
        table = Table(title=f"TikTok OSINT: {user}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Unique ID", data.get("uniqueId", "-"))
        table.add_row("Nickname", data.get("nickname", "-"))
        table.add_row("Signature", data.get("signature", "-"))
        table.add_row("Followers", str(data.get("followerCount", "-")))
        table.add_row("Following", str(data.get("followingCount", "-")))
        table.add_row("Likes (Hearts)", str(data.get("heart", "-")))
        table.add_row("Verified", str(data.get("verified", "-")))
        table.add_row("Avatar", data.get("avatarLarger", "-"))

        console.print(table)
    else:
        console.print("[red]Gagal ambil data TikTok[/]")

def stalk_github(user):
    url = f"{API_BASE}/github?user={user}"
    r = loading_request(url)
    if r and r["status"]:
        data = r["result"]
        table = Table(title=f"GitHub OSINT: {user}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Username", str(data.get("username", "-")))
        table.add_row("ID", str(data.get("id", "-")))
        table.add_row("Node ID", str(data.get("nodeId", "-")))
        table.add_row("URL", str(data.get("url", "-")))
        table.add_row("Type", str(data.get("type", "-")))
        table.add_row("Public Repos", str(data.get("public_repo", "-")))
        table.add_row("Followers", str(data.get("followers", "-")))
        table.add_row("Following", str(data.get("following", "-")))
        table.add_row("Created At", str(data.get("ceated_at", "-")))
        table.add_row("Updated At", str(data.get("updated_at", "-")))
        table.add_row("Avatar", str(data.get("profile_pic", "-")))

        console.print(table)
    else:
        console.print("[red]Gagal ambil data GitHub[/]")

def stalk_npm(pkg):
    url = f"{API_BASE}/npm?q={pkg}"
    r = loading_request(url)
    if r and r["status"]:
        data = r["result"]
        table = Table(title=f"NPM OSINT: {pkg}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Name", str(data.get("name", "-")))
        table.add_row("Latest Version", str(data.get("versionLatest", "-")))
        table.add_row("Published Version", str(data.get("versionPublish", "-")))
        table.add_row("Update Count", str(data.get("versionUpdate", "-")))
        table.add_row("Publish Time", str(data.get("publishTime", "-")))
        table.add_row("Latest Publish Time", str(data.get("latestPublishTime", "-")))

        console.print(table)
    else:
        console.print("[red]Gagal ambil data NPM[/]")

# === MAIN LOOP ===
if __name__ == "__main__":
    auth()
    while True:
        menu()
