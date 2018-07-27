# -*- coding:utf-8 -*-

import config, os, re, time, twitter
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
    user = 'KiSaSaGe_OU'
    if not os.path.isdir('./data/{}'.format(user)):
        os.mkdir('./data/{}'.format(user))

    tweet_num = 0   #
    max_id = None
    index = 0
    t0 = time.time()
    flg = True

    # crawl tweets
    while flg:
        tweet_list = get_user_tweets(count=200, user=user, max_id=max_id)

        if tweet_list is not None:
            tweets = [text_preprocess(post) for post in tweet_list]
            # exit conditions
            if tweet_list[-1]['id'] == max_id:
                flg = False
            else:
                max_id = tweet_list[-1]['id']
        with open('./data/{}/data_{}.txt'.format(user, str(int(tweet_num / 1000))), 'a', encoding='utf-8') as f:
            tweet_set = {tweet['text'] + '\n' for tweet in tweets if len(tweet['entities']['urls']) == 0}
            f.write(''.join(tweet_set))
            tweet_num += len(tweet_set)
        tweets.clear()
        index += 1

        # time restricted
        if index % 100 == 0:
            t1 = time.time()
            if (900 - (t1 - t0)) > 0:
                print(900 - (t1 - t0), '[sec] time sleep for the next tweet crawl')
                time.sleep(900 - (t1 - t0))
            t0 = time.time()

        print(index, 'times crawl end')

    exe_time = time.time() - start
    print('Execution time : {0} [sec]'.format(exe_time))

if __name__ == '__main__':
    main()
