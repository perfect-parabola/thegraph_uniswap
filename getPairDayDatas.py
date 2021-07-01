import requests, json, sys, csv, os, datetime
from utils import toUnixtime, toString

# make data directory
if not os.path.exists('data'):
    os.mkdir('data')

# get system var
token0_symbol = sys.argv[1]
token1_symbol = sys.argv[2]
start_date = toUnixtime(sys.argv[3])
end_date = toUnixtime(sys.argv[4])

# make api call
url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
query = """{
    tokens(
    orderBy: txCount
    orderDirection:desc
    first:1
    where: {
        symbol:"%s"
    }
    ) {
        id
        name
    }
}
""" %(token0_symbol)
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)
token0_id = json_data.get('data').get('tokens')[0].get('id')
token0_name = json_data.get('data').get('tokens')[0].get('name')
print(token0_id)
print(token0_name)

query = """{
    tokens(
    orderBy: txCount
    orderDirection:desc
    first:1
    where: {
        symbol:"%s"
    }
    ) {
        id
        name
    }
}
""" %(token1_symbol)
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)
token1_id = json_data.get('data').get('tokens')[0].get('id')
token1_name = json_data.get('data').get('tokens')[0].get('name')
print(token1_id)
print(token1_name)

query = """{
    pairDayDatas(
    where: {
        token0: "%s"
        token1: "%s"
        date_gte: %s
        date_lte: %s
    }
    ) {
        date
        reserve0
        reserve1
        totalSupply
        reserveUSD
        dailyVolumeToken0
        dailyVolumeToken1
        dailyVolumeUSD
    }
}
""" %(token0_id, token1_id, start_date, end_date)
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)

# write data file
filename = 'data/PairDayData_{}_{}_{}.csv'.format(
    token0_symbol, token1_symbol,
    datetime.datetime.now().strftime('%Y.%m.%d_%H:%M:%S')
)
with open(filename, mode='w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([
        'date', 'token0', 'token1',
        'reserve0', 'reserve1', 'totalSupply',
        'reserveUSD', 'dailyVolumeToken0', 'dailyVolumeToken1'
        'dailyVolumeUSD'
    ])
    for data in json_data.get('data').get('pairDayDatas'):
        csv_writer.writerow([
            toString(data.get('date')), token0_name, token1_name,
            data.get('reserve0'), data.get('reserve1'), data.get('totalSupply'),
            data.get('reserveUSD'), data.get('dailyVolumeToken0'), data.get('dailyVolumeToken1'),
            data.get('dailyVolumeUSD')
        ])
