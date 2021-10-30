# from web3 import Web3

# w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/d7af83af047d4230805fec39b32597af'))
# balance = w3.eth.get_balance('0xDDa5d738fDcD721e34E83cD5D7d5596c8AAef549')

# print(balance)

import requests
import time
import json

api_key = 'FHA2FHG2E3GFZTQ26WRP6X46452U9Z8AQ7'

class AddressMonitor:

    def __init__(self):
        with open('./address.json') as f:
            self.addresses = json.load(f)[0]
        self.record = self.get_transactions()

    def address_transaction_url_formatter(self, address):
        return \
        'https://api.etherscan.io/api' \
        + '?module=account' \
        + '&action=txlist' \
        + f'&address={address}' \
        + '&startblock=0' \
        + '&endblock=99999999' \
        + '&sort=asc' \
        + f'&apikey={api_key}'

    def get_transactions(self):
        new_record = {}
        for alias in self.addresses.keys():
            address = self.addresses[alias]
            url = self.address_transaction_url_formatter(address)
            response = requests.get(url)
            response_obj = json.loads(response.content)
            new_record[address] = response_obj['result']
        return new_record
            
    def get_new_transactions(self):
        new_record = self.get_transactions()
        diff = {}
        for k in new_record.keys():
            print(new_record[k][-1]['hash'])
            for i, entry in enumerate(reversed(new_record[k])):
                if self.record[k][-1]['hash'] == entry['hash']:
                    self.record = new_record
                    break
                else:
                    print(entry['hash'], i)

    def get_new_transactions_loop(self):
        while True:
            self.get_new_transactions()
            time.sleep(1)

address_monitor = AddressMonitor()
address_monitor.get_new_transactions_loop()