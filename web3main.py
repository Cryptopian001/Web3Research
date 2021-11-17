from web3 import Web3
from web3.exceptions import BlockNotFound
import requests
import time
import json
from datetime import datetime


class AddressMonitor:

    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/d7af83af047d4230805fec39b32597af'))
        self.api_key = 'FHA2FHG2E3GFZTQ26WRP6X46452U9Z8AQ7'
        self.slack_link = 'https://hooks.slack.com/services/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'
        with open('./address.json') as f:
            self.addresses = json.load(f)[0]
        self.latest_block = self.web3.eth.block_number - 1
        
        self.coin_address = {}
        coin_list = json.loads(requests.get('https://api.coingecko.com/api/v3/coins/list?include_platform=true').content)
        for coin in coin_list:
            if 'ethereum' in coin['platforms'].keys():
                addr = coin['platforms']['ethereum']
                self.coin_address[addr] = coin['id']

    def get_block_range(self):
        start_block = self.latest_block
        end_block = self.web3.eth.block_number
        self.latest_block = end_block
        return start_block, end_block

    def address_transaction_url_formatter(self, address):
        start_block, end_block = self.get_block_range()
        if start_block == end_block:
            return None
        return \
        'https://api.etherscan.io/api' \
        + '?module=account' \
        + '&action=txlist' \
        + f'&address={address}' \
        + f'&startblock={start_block}' \
        + f'&endblock={end_block}' \
        + '&sort=desc' \
        + f'&apikey={self.api_key}'
    
    def build_slack_payload(self, record):
        for address in record.keys():
            for item in record[address]:
                from_, to_ = item['from'], item['to']
                if from_ == address:
                    if to_ in self.coin_address.keys():
                        item['to'] = self.coin_address[to_]
                    item['from'] = self.addresses[from_]
                if to_ == address:
                    if from_ in self.coin_address.keys():
                        item['from'] = self.coin_address[from_]
                    item['to'] = self.addresses[to_]

        payload = '----------------------------------------'
        for address in record.keys():
            for item in record[address]:
                payload += f'\nfrom *{item["from"]}* to *{item["to"]}* for *{item["value"]}* ether\n'
                payload += '----------------------------------------\n'
        return payload

    def get_transactions(self):
        new_record = {}
        update = False
        for address in self.addresses.keys():
            url = self.address_transaction_url_formatter(address)
            if url:
                response = requests.get(url)
                response_obj = json.loads(response.content)
                new_record[address] = [{'hash': entry['hash'], 'from': entry['from'], 'to': entry['to'], 'value': float(entry['value'])/1e18} for entry in response_obj['result']]
                if response_obj['result']:
                    update = True
        if update:
            for k in list(new_record.keys()):
                if not new_record[k]:
                    del new_record[k]
            payload = self.build_slack_payload(new_record)
            response = requests.post(self.slack_link, data=json.dumps({'text': payload}, indent=4))
            print(response.content)

    def get_transactions_loop(self):
        while True:
            self.get_transactions()
            time.sleep(10)

if __name__ == '__main__':
    address_monitor = AddressMonitor()
    # with open('./sample.json') as f:
    #     data = json.load(f)
    # print(address_monitor.build_slack_payload(data))
    address_monitor.get_transactions_loop()