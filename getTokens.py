import requests, json, csv, os, datetime

# make data directory
if not os.path.exists('data'):
    os.mkdir('data')

# make api call
url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
query = """{
    tokens(
    orderBy: txCount
    orderDirection:desc
    first:100
    ) {
        symbol
        name
        txCount
    }
}
"""
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)

# write data file
filename = 'data/Token_{}.csv'.format(
    datetime.datetime.now().strftime('%Y.%m.%d_%H:%M:%S')
)
with open(filename, mode='w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['토큰 심볼', '토큰 이름', '누적 transaction 수'])
    for data in json_data.get('data').get('tokens'):
        csv_writer.writerow([data.get('symbol'), data.get('name'), data.get('txCount')])