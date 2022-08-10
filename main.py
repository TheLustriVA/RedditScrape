import src.auth as sra
import src.scrape as srs
from pathlib import Path 

if __name__ == "__main__":
    def main():
        reddit = sra.get_reddit_session()
        results = srs.get_hot_subreddits(["favoritenude", "nsfw", "GodPussy", "WomenBendingOver"], "src/great", "metadata.json", save_metadata=True)
        return results
    
    main()
