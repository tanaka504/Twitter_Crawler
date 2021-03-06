# -*- coding:utf-8 -*-

from requests_oauthlib import OAuth1, OAuth1Session
import json, config, time, requests, os, twitter

'''
コメントになっているコードは twiiter ライブラリを使おうとした夢の跡です
'''

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

def create_oath_session():
    oath = OAuth1Session(CK, CS, AT, ATS)
    # oath = twitter.OAuth(AT, ATS, CK, CS)
    return oath

# def create_oath_object():
#     auth = OAuth1(CK, CS, AT, ATS)
#     return auth

def get_user_tweets(count=5, user='KiSaSaGe_OU', max_id=None):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    if max_id is not None:
        params = {
            'include_rts': 'false',
            'count': count,
            'screen_name': user,
            'max_id': max_id
        }
    else:
        params = {
            'include_rts': 'false',
            'count': count,
            'screen_name': user,
        }


    oath = create_oath_session()
    #api = twitter.Twitter(auth=oath, retry=True)

    try:
        res = oath.get(url, params=params)
        # if max_id is not None:
        #     res = api.statuses.user_timeline(user_id=user, max_id=max_id, count=count)
        # else:
        #     res = api.statuses.user_timeline(user_id=user, count=count)
    except ConnectionError:
        time.sleep(180)
        res = oath.get(url, params=params)
        # if max_id is not None:
        #     res = api.statuses.user_timeline(screen_name=user, max_id=max_id, count=count)
        # else:
        #     res = api.statuses.user_timeline(screen_name=user, count=count)

    if res.status_code != 200:
        print('Error code : %d' % res.status_code, 'ID : ', user)
        return None
    else:
        tweet_list = json.loads(res.text)
        return tweet_list

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
    get_user_tweets()