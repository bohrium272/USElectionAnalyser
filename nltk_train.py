from nltk.corpus import twitter_samples

pos_strings = twitter_samples.strings('positive_tweets.json')
neg_strings = twitter_samples.strings('negative_tweets.json')
pos_tweets = []
neg_tweets = []

for tweet in pos_strings:
    pos_tweets.append(tuple([tweet, 'positive']))

for tweet in neg_strings:
    neg_tweets.append(tuple([tweet, 'negative']))

tweets = []
for word, sentiment in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

word_features = get_word_features(get_words_in_tweets(tweets))

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features
