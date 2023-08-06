import sys
import random
import hashlib
import getopt
import requests

appKey = '663e2a0ee8bbf090'
secretKey = 'QWXhZe8fp9tUnR2tLHuXTnF5IosRcDXN'

from_lang = 'ZH'
to_lang = 'zh-CHS'


def look_up(word):
    salt = random.randint(1, 65536)
    sign = appKey + word + str(salt) + secretKey
    sign = hashlib.md5(sign.encode('UTF-8')).hexdigest()
    request_url = 'https://openapi.youdao.com/api'
    payload = {
        'q': word,
        'from': from_lang,
        'to': to_lang,
        'appKey': appKey,
        'salt': salt,
        'sign': sign
    }
    try:
        r = requests.get(request_url, params=payload).json()
    except Exception as e:
        print(e)
    return r


def output(content):
    basic = content.get('basic')
    if basic:
        print('[', basic['us-phonetic'], ']', sep='')
        print('[', basic['uk-phonetic'], ']', sep='')
        explains = basic['explains']
        for explain in explains:
            print(explain)


def main():
    if len(sys.argv) >= 2 and not sys.argv[1].startswith('-'):
        word = sys.argv[1]
        response = look_up(word)
        if response['errorCode'] == '0':
            output(response)
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hvq:', ['help', 'version', 'query='])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for name, value in options:
        if name in ('-h', '--help'):
            print('lu dictionary')
        if name in ('-v', '--version'):
            print('0.1.0')
        if name in ('-q', '--query'):
            response = look_up(value)
            if response['errorCode'] == '0':
                output(response)


if __name__ == '__main__':
    main()
