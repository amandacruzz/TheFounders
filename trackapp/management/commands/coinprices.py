from django.conf import settings
from django.core.management.base import BaseCommand
from trackapp.models import *
from sqlalchemy import create_engine
import requests
import json
import pandas as pd



class Command(BaseCommand):

    def handle(self, *args, **options):

        url = 'https://graph.v2b.testnet.pulsechain.com/subgraphs/name/pulsechain/pulsex'
        query = """
        {
        tokens(first: 30, orderBy:totalTransactions, orderDirection:desc ) {
        symbol
        name
        derivedUSD
        }
        }
        """

        r = requests.post(url, json={'query': query})
        print('Fetched New Price Data')
        data = json.loads(r.text)
        df = pd.json_normalize(data['data']['tokens'])
        df1 = df[['symbol', 'name', 'derivedUSD']]

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
            user=user,
            password=password,
            database_name=database_name,
        )

        engine = create_engine(database_url, echo=False)
        df1.to_sql(coinPrices._meta.db_table, if_exists='replace', con=engine, index=False)