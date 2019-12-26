"""Assignment 1.
"""

import math

# Maximum number of characters in a valid tweet.
MAX_TWEET_LENGTH = 50

# The first character in a hashtag.
HASHTAG_SYMBOL = '#'

# The first character in a mention.
MENTION_SYMBOL = '@'

# Underscore is the only non-alphanumeric character that can be part
# of a word (or username) in a tweet.
UNDERSCORE = '_'

SPACE = ' '


def is_valid_tweet(text: str) -> bool:
    """Return True if and only if text contains between 1 and
    MAX_TWEET_LENGTH characters (inclusive).

    >>> is_valid_tweet('Hello Twitter!')
    True
    >>> is_valid_tweet('')
    False
    >>> is_valid_tweet(2 * 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    False

    """
    MAX_TWEET_LENGTH = 50
    
    if len(text) <= MAX_TWEET_LENGTH:
        return True

    # Complete the body of this function.


# Now define the other functions described in the handout.


# A helper function.  Do not modify this function, but you are welcome
# to call it.

def clean(text: str) -> str:
    """Return text with every non-alphanumeric character, except for
    HASHTAG_SYMBOL, MENTION_SYMBOL, and UNDERSCORE, replaced with a
    SPACE, and each HASHTAG_SYMBOL replaced with a SPACE followed by
    the HASHTAG_SYMBOL, and each MENTION_SYMBOL replaced with a SPACE
    followed by a MENTION_SYMBOL.

    >>> clean('A! lot,of punctuation?!!')
    'A  lot of punctuation   '
    >>> clean('With#hash#tags? and@mentions?in#twe_et #end')
    'With #hash #tags  and @mentions in #twe_et  #end'
    """

    clean_str = ''
    
    for char in text:
        if char.isalnum() or char == UNDERSCORE:
            clean_str = clean_str + char
        elif char == HASHTAG_SYMBOL or char == MENTION_SYMBOL:
            clean_str = clean_str + SPACE + char
        else:
            clean_str = clean_str + SPACE
    return clean_str

def compare_tweet_lengths(tweet1: str, tweet2: str) -> int:
    ''' Return 1 if the first tweet is longer than the second, -1 if the second tweet is longer than the first, or 0 if the tweets have the same length.
    
    compare_tweet_lengths('Divij', 'Vaibhav')
    -1
    compare_tweet_lengths('Divij', Divij')
    0
    '''
    
    if len(tweet1) > len(tweet2):
        return 1
    elif len(tweet1) == len(tweet2):
        return 0
    else:
        return -1
    
def add_hashtag(valid_tweet: str, tweet_word: str) -> str:
    ''' Appending a space, a hash symbol, and the tweet word to the end of the original tweet will result in a potential tweet.  
    
    '''
    result = valid_tweet + SPACE + HASHTAG_SYMBOL + tweet_word
    
    if is_valid_tweet(result):
        return result
    else:
        return valid_tweet
    
def contains_hashtag(valid_tweet: str, tweet_word: str) -> bool:
    ''' Returns True if and only if the tweet contains a hashtag made 
    up of the hash symbol and the tweet word.
    
   contains_hashtag('I like #csc108, #mat137, and #phl101', 'csc108')
   True
   
    '''
        
    if tweet_word in valid_tweet:
        return True
    else:
        return False
    
def is_mentioned(valid_tweet: str, tweet_word: str) -> bool:
    ''' Returns true if and only if the tweet contains a mention made up of the mention symbol and the tweet word.'''
    
    mention = MENTION_SYMBOL + tweet_word
    if mention in valid_tweet:
        return True
    else:
        return False
    
def add_mention_exclusive(valid_tweet: str, tweet_word: str) -> str:
    ''' If the potential tweet is valid, the original tweet contains the given tweet word, and the original tweet does not mention the given tweet word, the function should return the potential tweet. Otherwise, the function should return the original tweet.
    
    add_mention_exclusive('Go Raptors!', "Raptors')
    Go Raptors! @Raptors
    
    add_mention_exclusive('Go Raptors! @Raptors', 'Raptors')
    'Go @Raptors!'
    '''
    
    original_tweet = valid_tweet + SPACE + MENTION_SYMBOL + tweet_word
    
    if is_mentioned(valid_tweet, tweet_word):
        return valid_tweet
    else:
        return original_tweet

import math

def num_tweets_required(valid_tweet: str) -> int:
    ''' Return the minimum number of tweets that would be required to communicate the entire message.
    num_tweets_required('DivijSanjanwalaDivijSanjanwalaDivijSanjanwalaDivijSanjanwala')
    2
    num_tweets_required('Divij')
    1
    '''
    
    return math.ceil(len(valid_tweet) / MAX_TWEET_LENGTH)

def get_nth_tweet(messege: str, n: int) -> str:
    ''' If the message contains too many characters, it would need to be split up into a sequence of tweets. All of the tweets in the sequence, except possibly the last tweet, would be of length MAX_TWEET_LENGTH'''
    
        
    if n == num_tweets_required(messege): 
        return messege[(n - 1) * MAX_TWEET_LENGTH: len(messege)]
   
   
    
