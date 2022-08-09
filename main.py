import src.auth as sra
import src.scrape as srs
from pathlib import Path 

if __name__ == "__main__":
    def main():
        reddit = sra.get_reddit_session()
        results = srs.get_hot_subreddits(["gonewild18", "barelylegalteens", "18_19", "legalteens"], "src/fun/", "metadata.json", save_metadata=True)
        return results
    
    main()
