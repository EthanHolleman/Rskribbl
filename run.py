from args import get_args
from collect import top_n_words_subreddit_comments, create_reddit_instance
from io_utils import write_words
from pathlib import Path

def main():

    args = get_args()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    reddit = create_reddit_instance()
    for subreddit in args.subreddits:
        print(f'Pulling comments from r/{subreddit}')
        try:
            word_occurrences = top_n_words_subreddit_comments(subreddit, reddit, 
            n=args.number_words, post_limit=args.post_limit, 
            comment_limit=args.comment_limit, min_word_length=args.min_word_length
            )
        except Exception as e:
            print(f'Failed to get words from {subreddit} with error: {e}')
        write_words(args.output_dir, subreddit, word_occurrences, 
        include_occurrences=args.include_occurrences)
    
if __name__ == "__main__":
    main()
