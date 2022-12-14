import src.auth as sra
import src.scrape as srs
from pathlib import Path 

if __name__ == "__main__":
    def main():
        reddit = sra.get_reddit_session()
        results = srs.get_hot_subreddit("learnpython", "src/", save_metadata=True)
        return results
    
    main()

