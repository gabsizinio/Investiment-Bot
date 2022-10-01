import tweepy

consumer_key = "RHqvSUV1mgZn6zS5hYY3d3BzC"
consumer_secret = "jDE24WT5ewVsFDmp0wei8FyOwacqqv6YyYbxBE9PX90rUjiAke"
access_token = "1574481784812834818-GGdMBv5etDEj9NNy3DTzkzhrdfm2ge"
access_token_secret = "stvGErN3bJzd2wa5mbAO6ZnMkeB6EOCZCQZKBlk7JkgXA"




api = tweepy.Client(
    consumer_key= consumer_key,
    consumer_secret= consumer_secret,
    access_token= access_token,
    access_token_secret= access_token_secret
)

try:
  # tweet = api.create_tweet(text = "lula la, brilha uma estrela")
  # print(tweet)
  # tweets = api.get_users_tweets("1274547639107883009", max_results = 10, user_auth = True)
  
  
  
  api.retweet("1575691835338539008", user_auth = True)
  print("tweetei")
    # count += 1
except Exception as e:
  print(e)