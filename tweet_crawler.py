# -*- coding:utf-8 -*-

import config, os, re, time
from utils import get_user_tweets

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

def text_preprocess(post):
    text = post['text']
    text = re.sub(r'\n', r'', text)
    text = re.sub(r'\r\n', r'', text)
    text = re.sub(r'@(\w+)', r'', text)
    post['text'] = text
    return post

def main():
    start = time.time()

    # create indivisual dir for store tweets
    user = 'tkym1220'
    if not os.path.isdir('./data/{}'.format(user)):
        os.mkdir('./data/{}'.format(user))

    text_num = '0'
    max_id = None
    t0 = time.time()

    # crawl tweets
    for index in range(10):
        tweet_list = get_user_tweets(count=500, user=user, max_id=max_id)

        if tweet_list is not None:
            tweets = [text_preprocess(post) for post in tweet_list]
            max_id = tweet_list[-1]['id']
        with open('./data/{}/data_{}.txt'.format(user, text_num), 'a', encoding='utf-8') as f:
            f.write(''.join({tweet['text'] + '\n' for tweet in tweets if len(tweet['entities']['urls']) == 0}))
        tweets.clear()
        # next file name
        text_num = str(index + 1)

        # time restricted
        if (index + 1) % 90 == 0:
            t1 = time.time()
            if (900 - (t1 - t0)) > 0:
                print(900 - (t1 - t0), '[sec] time sleep for the next tweet crawl')
                time.sleep(900 - (t1 - t0))
            t0 = time.time()

        print(index + 1, 'crawl end')

    exe_time = time.time() - start
    print('Execution time : {0} [sec]'.format(exe_time))

if __name__ == '__main__':
    main()
