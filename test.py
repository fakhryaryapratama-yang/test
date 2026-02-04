import os
import json
from datetime import datetime
from urllib import request

# ===============================
# KONFIGURASI VPS
# ===============================
SERVER_IP = "IP_VPS_KAMU"   # contoh: 103.xxx.xxx.xxx
PORT = 8000

# ===============================
# AMBIL USERNAME OS
# ===============================
def get_petugas():
    try:
        return os.getlogin()
    except:
        return os.environ.get("USERNAME") or os.environ.get("USER")

# ===============================
# LOAD DATA DARI SERVER
# ===============================
def load_data():
    with request.urlopen(f"http://{SERVER_IP}:{PORT}/data") as res:
        return json.loads(res.read().decode())

# ===============================
# SIMPAN TRANSAKSI KE SERVER
# ===============================
def save_data(transaksi):
    req = request.Request(
        f"http://{SERVER_IP}:{PORT}/tambah",
        data=json.dumps(transaksi).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    request.urlopen(req)

# ===============================
# HITUNG SALDO
# ===============================
def hitung_saldo(data):
    saldo = 0
    for t in data["kas"]:
        if t["jenis"] == "masuk":
            saldo += t["jumlah"]
        else:
            saldo -= t["jumlah"]
    return saldo

# ===============================
# INPUT KAS
# ===============================
def input_kas(jenis):
    petugas = get_petugas()
    keterangan = input("Keterangan      : ")
    jumlah = int(input("Jumlah (Rp)     : "))

    transaksi = {
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "petugas": petugas,
        "jenis": jenis,
        "keterangan": keterangan,
        "jumlah": jumlah
    }

    save_data(transaksi)
    data = load_data()

    print("\n✅ Transaksi berhasil dicatat")
    print(f"Saldo saat ini : Rp {hitung_saldo(data)}")

# ===============================
# LAPORAN KAS TAKMIR
# ===============================
def laporan():
    data = load_data()
    print("\n========== LAPORAN KAS TAKMIR ==========")

    if not data["kas"]:
        print("Belum ada transaksi.")
        return

    for t in data["kas"]:
        print(f"{t['tanggal']} | {t['jenis'].upper()} | Rp {t['jumlah']} | {t['keterangan']} | {t['petugas']}")

    print("---------------------------------------")
    print(f"Saldo Akhir : Rp {hitung_saldo(data)}")

# ===============================
# MENU UTAMA
# ===============================
def menu():
    petugas = get_petugas()

    print("======================================")
    print(" SISTEM PENGELOLAAN KAS TAKMIR ")
    print("======================================")
    print(f"Petugas : {petugas}")

    while True:
        print("\nMenu:")
        print("1. Input Kas Masuk")
        print("2. Input Kas Keluar")
        print("3. Lihat Laporan Kas")
        print("4. Keluar")

        pilih = input("Pilih menu (1-4): ")

        if pilih == "1":
            input_kas("masuk")
        elif pilih == "2":
            input_kas("keluar")
        elif pilih == "3":
            laporan()
        elif pilih == "4":
            print("\nAplikasi ditutup.")
            break
        else:
            print("Pilihan tidak valid!")

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    menu()
