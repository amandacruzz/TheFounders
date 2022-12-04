import requests
from django.core.management import BaseCommand
from datetime import datetime
from plots.models import HistoricalPrices
import json

class Command(BaseCommand):
    def getPairs(self, skip):
        url = "https://graph.v2b.testnet.pulsechain.com/subgraphs/name/pulsechain/pulsex"

        pairs = ''

        with open("valids.json") as valids:
            valids = json.load(valids)

            for i in valids['valids']:
                pairs += '"' + i['pair_id'] + '"' + ","


        query = f"""{{
                      pairHourDatas(skip: {skip}, first: 1000, orderBy: hourStartUnix, orderDirection: desc, 
                        where: {{pair_in: [{pairs}]}}){{
                        pair {{
                          id,
                          token0 {{
                            id,
                            symbol,
                            derivedUSD
                          }},
                          token1 {{
                            id,
                            symbol,
                            derivedUSD
                          }}
                        }}
                        reserve0,
                        reserve1,
                        reserveUSD,
                        hourlyTxns,
                        totalSupply,
                        hourStartUnix,
                        hourlyVolumeUSD
                      }}
                    }}
                    """

        r = requests.post(url, json={'query': query}).json()['data']['pairHourDatas']

        return r
    def handle(self, *args, **options):
        skip = 0

        pairs = self.getPairs(skip)

        for i in HistoricalPrices.objects.all():
            i.delete()

        while pairs:
            for i in pairs:
                if i['pair']['token0']['symbol'] == 'USDC':  # in this case USDC is token0
                    h = HistoricalPrices(intTime=i['hourStartUnix'], token=i['pair']['token1']['symbol'],
                                         price=float(i['reserve0']) / float(i['reserve1']))
                    h.save()

                elif i['pair']['token1']['symbol'] == 'USDC':  # in this case USDC is token1
                    h = HistoricalPrices(intTime=i['hourStartUnix'], token=i['pair']['token0']['symbol'],
                                         price=float(i['reserve1']) / float(i['reserve0']))
                    h.save()

            skip += 1000
            pairs = self.getPairs(skip)
