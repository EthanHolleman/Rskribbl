import praw
import os
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOPWORDS = set(stopwords.words('english'))
STOPWORDS = STOPWORDS.union(set([
    'https', 'could', 'hawking'
]))


def create_reddit_instance():
    '''Create a Reddit instance using praw library

    Returns:
        Reddit: Reddit instance via Praw. Credentials set using environmental
        variables.
    '''
    return praw.Reddit(client_id=os.environ['PRAW_CLIENT_ID'],
                       client_secret=os.environ['PRAW_SECRET'],
                       user_agent=os.environ['PRAW_USER_AGENT']
                       )


def process_text(text, min_length=3):
    '''Process a string of text from a comment. Removes stopwords like "I",
    "me", and "the", sends all text to lower case and removes punctuation.

    Added a bunch of manual filters to remove things like usernames, subreddit
    names, links to images etc. 

    Args:
        text (str): String to prcess (redddit comment body)

    Returns:
        list: List of words
    '''
    pText = word_tokenize(text)
    pText = [w.lower()
            for w in pText if (w not in STOPWORDS and len(w) >= min_length 
            and 'youtube' not in w and 'reddit' not in w 
            and w[-2:] != 'ly' 
            and 'imgur' not in w and 'php' not in w
            and 'png' not in w and 'jpg' not in w
            and 'www' not in w and 'r/' not in w and '.com' not in w
            and 'u' not in w and 'id=' not in w and '.us' not in w)]
    return pText


def harvest_words_from_subreddit_comments(subreddit_name, reddit, n=100,
                                          comment_limit=10000, min_word_length=3):
    '''Harvest the bodies of the top level comments of the top n posts in a
    given subreddit.

    Args:
        subreddit_name (str): Name of subreddit to harvest from.
        reddit (Reddit): Reddit instance from Praw.
        n (int, optional): Number of posts. Defaults to 100.

    Yields:
        list: List of tokenized words from top comment bodies.
    '''
    i = 0
    for submission in reddit.subreddit(subreddit_name).top(limit=n):
        comments = submission.comments
        for each_top_level_comment in comments:
            if isinstance(each_top_level_comment, praw.models.MoreComments):
                continue
                # for each_additional_comment in each_top_level_comment.comments():
                #     yield process_text(each_additional_comment.body)
            else:
                yield process_text(each_top_level_comment.body, min_word_length)
                i += 1
                if i >= comment_limit:
                    return


def top_n_words_subreddit_comments(subreddit_name, reddit, n=25,
                                   post_limit=100, comment_limit=10000,
                                   min_word_length=3):
    '''Retrieve a list of the top n most frequently used words in top level
    comments of a specific subreddit.

    Args:
        subreddit_name (str): Name of subreddit to harvest from.
        reddit (Reddit): Praw Reddit instance.
        n (int, optional): Number or words to return. Defaults to 25.
        post_limit (int, optional): Max number of posts to harvest from. Defaults to 100.

    Returns:
        list: List of tuples of top n words. First value in each tuple is the
        word, second is the number of occurrences.
    '''
    word_gen = harvest_words_from_subreddit_comments(
        subreddit_name, reddit, post_limit, comment_limit, min_word_length)
    counter = {}
    for comment_words in word_gen:
        for word in comment_words:
            if word in counter:
                counter[word] += 1
            else:
                counter[word] = 1

    ranked_words = sorted(
        counter.keys(), key=lambda k: counter[k], reverse=True)

    return [(word, counter[word]) for word in ranked_words[:n]]
