from pathlib import Path


def write_words(parent_dir, subreddit, word_occurrences, 
                include_occurrences=False):
    write_path = Path(parent_dir).joinpath(f'{subreddit}_words.txt')
    with open(str(write_path), 'w') as handle:
        for word, occurrences in word_occurrences:
            if include_occurrences:
                line = f'{word}\t{occurrences}'
            else:
                line = word
            handle.write(f'{line}, ')
    return write_path
