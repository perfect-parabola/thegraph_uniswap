import requests, json, sys, csv, os, datetime
from utils import toUnixtime, toString

# make data directory
if not os.path.exists('data'):
    os.mkdir('data')

# get system var
start_date = toUnixtime(sys.argv[1])
end_date = toUnixtime(sys.argv[2])

# make api call
url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
query = """{
    uniswapDayDatas(
    where: {
        date_gte: %s
        date_lte: %s
    }
    ) {
        id
        date
        dailyVolumeETH
        dailyVolumeUSD
        txCount
    }
}
""" %(start_date, end_date)

r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)

# write data file
filename = 'data/UniswapDayData_{}.csv'.format(
    datetime.datetime.now().strftime('%Y.%m.%d_%H:%M:%S')
)
with open(filename, mode='w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['날짜', '거래량(ETH)', '거래량(USD)', 'transaction 수'])
    for data in json_data.get('data').get('uniswapDayDatas'):
        csv_writer.writerow([
            toString(data.get('date')), data.get('dailyVolumeETH'),
            data.get('dailyVolumeUSD'), data.get('txCount')
        ])