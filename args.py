import argparse

def get_args():

    parser = argparse.ArgumentParser(description='Harvest frequently words from subreddit comments using Praw')

    parser.add_argument('-r', '--subreddits', type=str, nargs='+', help='List of subreddits to pull comments from')
    parser.add_argument('-n', '--number_words', type=int, default=25, help='Number of words to return per subreddit. Defaults to 25.')
    parser.add_argument('-mc', '--comment_limit', type=int, default=10000, help='Max number of comments to harvest per subreddit. Defaults to 10,000')
    parser.add_argument('-o', '--output_dir', type=str, default='comment_harvest', help='Output directory to write results to.')
    parser.add_argument('-f', '--include_occurrences', action='store_true', help='Include the number of times each word appears in the final output')
    parser.add_argument('-p', '--post_limit', default=50, help='Max number of posts to harvest from. Defaults to 50.')
    parser.add_argument('-l', '--min_word_length', type=int, default=3, help='Min word length. Defaults to 3 characters.')
    args = parser.parse_args()
    return args
