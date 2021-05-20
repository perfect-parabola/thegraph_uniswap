import requests, json, sys, csv, os, datetime
from utils import toUnixtime, toString

# make data directory
if not os.path.exists('data'):
    os.mkdir('data')

# get system var
token_symbol = sys.argv[1]
start_date = toUnixtime(sys.argv[2])
end_date = toUnixtime(sys.argv[3])

# make api call
url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
query = """{
    tokens(
    orderBy: txCount
    orderDirection:desc
    first:1
    symbol:%s
    ) {
        id
        name
    }
}
""" %(token_symbol)
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)
token_id = json_data.get('data').get('tokens')[0].get('id')
token_name = json_data.get('data').get('tokens')[0].get('name')

query = """{
    tokenDayDatas(
    where: {
        token: "%s"
        date_gte: %s
        date_lte: %s
    }
    ) {
        id
        date
        dailyVolumeETH
        dailyVolumeUSD
        dailyVolumeToken
		priceUSD
    }
}
""" %(token_id, start_date, end_date)
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)

# write data file
filename = 'data/TokenDayData_{}_{}.csv'.format(
    token_symbol,
    datetime.datetime.now().strftime('%Y.%m.%d_%H:%M:%S')
)
with open(filename, mode='w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['날짜', '토큰', '거래량(ETH)', '거래량(USD)', '거래량(token)','USD가격'])
    for data in json_data.get('data').get('tokenDayDatas'):
        csv_writer.writerow([
            toString(data.get('date')), token_name,
            data.get('dailyVolumeETH'), data.get('dailyVolumeUSD'), data.get('dailyVolumeToken'),data.get('priceUSD')
        ])
