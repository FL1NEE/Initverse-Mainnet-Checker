# -*- coding: utf-8 -*-
import telebot
import requests
from openpyxl import Workbook

class InitVerseChecker(object):
    def __init__(self, ADDRESS: str) -> str:
        self.ADDRESS: str = ADDRESS

    def check_balance(self) -> int:
        headers: dict[str, str] = \
        {
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        }

        json_data: dict = \
        {
            "address": self.ADDRESS
        }

        balance: int = str(requests.post(
            "https://explorer-api.inichain.com/api/address/address_summary",
            headers = headers,
            json = json_data,
        ).json()["balance"])
        balance: float = float(f"{balance[:2]},{balance.split(balance[:2])[1]}")
        
        print(f"[INFO] WALLET: {self.ADDRESS} BALANCE: {balance}")
        return balance

if __name__ == '__main__':
    wb = Workbook() 
    ws = wb.active
    ws.title = "Wallet Balances"

    ws.append(["Address", "Balance"])

    with open("wallets.txt", "r", encoding="utf-8") as f:
        wallets = f.read().splitlines()

    for wallet in wallets:
        wallet = wallet.strip()
        if not wallet:
            continue
        try:
            checker = InitVerseChecker(wallet)
            result = checker.check_balance()
        except: 
            result = "ERROR"

        ws.append([wallet, str(result)])

    wb.save("wallet_balances.xlsx")
    print("✅ The data was successfully saved in wallet_balances.xlsx")
