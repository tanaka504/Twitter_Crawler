# -*- coding:utf-8 -*-

from requests_oauthlib import OAuth1, OAuth1Session
import json, config, time, requests

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET



def create_oath_session():
    oath = OAuth1Session(CK, CS, AT, ATS)
    return oath


def create_oath_object():
    auth = OAuth1(CK, CS, AT, ATS)
    return auth

def get_user_tweets(count=5, user='tkym1220'):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        'include_rts': 'false',
        'count': count,
        'screen_name': user
    }

    oath = create_oath_session()
    res = oath.get(url, params=params)

    if res.status_code == 200:
        timelines = json.loads(res.text)
        for line in timelines:
            print('{}::{}'.format(line['user']['name'],line['text']))
            print(line['created_at'])
            print('--------------------------------')
    else:
        print('Failed: %d' % res.status_code)

def get_id_tweets(id=737994989884428293):
    url = 'https://api.twitter.com/1.1/statuses/show.json'
    params = {'id': id}
    oath = create_oath_session()
    res = oath.get(url, params=params)
    if res.status_code == 200:
        timelines = json.loads(res.text)
        print(timelines['text'])
    else:
        print('Failed: %d' % res.status_code)

def post_tweet():
    tweet = input('>> ')
    print('*******************************')

    url = "https://api.twitter.com/1.1/statuses/update.json"
    oath = create_oath_session()
    params = {'status': tweet}

    res = oath.post(url, params=params)

    if res.status_code == 200:
        print('Success, you tweet \" {} \"'.format(tweet))
    else:
        print('Failed: %d' % res.status_code)

if __name__ == '__main__':
    get_id_tweets()

