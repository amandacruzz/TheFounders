import json

import requests as r
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('token', nargs='+', type=str)

    def getPairId(self, token):
        url = 'https://graph.v2b.testnet.pulsechain.com/subgraphs/name/pulsechain/pulsex'
        query1 = """
            {
            pairs(first: 1000, skip: 0, orderBy: totalTransactions, orderDirection: desc, where: {token1: "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"}) {
                id,
                token0 {
                  id,
                  symbol,
                  name
                },
                token1 {
                  id,
                  symbol
                }
                }
            }
            """
        query2 = """
            {
            pairs(first: 1000, skip: 0, orderBy: totalTransactions, orderDirection: desc, where: {token0: "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"}) {
                id,
                token0 {
                  id,
                  symbol,
                  name
                },
                token1 {
                  id,
                  symbol
                }
                }
            }
            """

        pair_id = None

        for query in [query1, query2]:
            pairs = r.post(url, json={'query': query}).json()['data']['pairs']

            for i in pairs:
                if i['token0']['symbol'] == token:
                    return i['id'], i['token0']['id'], False  # if false that means that USDC is not token0
                elif i['token1']['symbol'] == token:
                    return i['id'], i['token1']['id'], True

        raise Exception("Token pair not found")

    def handle(self, *args, **options):
        if options['token']:
            token = options['token'][0]

            json_data = ""
            with open("valids.json") as valids:
                valids = json.load(valids)
                json_data = valids

                for i in valids['valids']:
                    if i['token'] == token:
                        raise Exception("Token is already in valids")

            pair_id, id, usdc_token0 = self.getPairId(token)

            json_data['valids'].append({"token": token, "pair_id": pair_id, "id": id, "usdc_token0": usdc_token0})

            file = open("valids.json", "w")
            json.dump(json_data, file)
