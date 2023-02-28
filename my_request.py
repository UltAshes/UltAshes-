import requests

headers = {
    'Accept': ',application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.1637941648.1616934252; uname3=qq1616934321; t3kwid=131286315; '
              'websid=1488073791; pic3=""; t3=qq; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1617949101,'
              '1618127723,1618579672,1619099581; _gid=GA1.2.1505163314.1619099581; '
              'Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1619100738; _gat=1; kw_token=XM5GXCP8M5',
    'csrf': 'XM5GXCP8M5',
    'Host': 'www.kuwo.cn',
    'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'}

headers2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.198582091.1676855750; _gid=GA1.2.1609254583.1676955448; '
              'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1677041666,1677059136,1677077477,1677113852; '
              'Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1677113886',
    'Host': 'sr.sycdn.kuwo.cn',
    'If-None-Match': '5d1b28bd-39ede2',
    'Range': 'bytes=0-1048575',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36 Edg/110.0.1587.50',
}


def pachong(text):
    global data

    url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn=1&rn=10&httpsStatus=1&reqId=da11ad51-d211-11ea-b197-8bff3b9f83d2e'.format(
        text)
    response = requests.get(url=url, headers=headers)
    response = response.json()
    music_list = response["data"]["list"]
    list_data = []
    for music in music_list:
        data = {
            'name': music['name'],
            'artist': music['artist'],
            'album': music['album'],
            'duration': music['duration'],
            'rid': music['rid']
        }
        list_data.append(data)
    return list_data


def pachong2(rid):
    url = f'https://link.hhtjim.com/kw/{rid}.mp3'
    response = requests.get(url=url, headers=headers2)
    return response.content
