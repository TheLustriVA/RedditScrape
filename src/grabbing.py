import wget
import json
from auth import get_reddit_session
from pathlib import Path


def get_hot_subreddit(subreddit, output_dir, output_json, save_metadata=False):

    reddit = get_reddit_session()

    from_subreddit = reddit.subreddit(subreddit)

    hot_posts = from_subreddit.hot()

    out_dir = Path(output_dir)
    if out_dir.is_dir() is False:
        out_dir.mkdir(parents=True)

    if save_metadata:
        metadata_file = Path(out_dir / output_json)
        if metadata_file.is_file():
            with open(metadata_file, "r", encoding="utf-8") as f:
                data_everything = json.load(f)
        else:
            metadata_file.touch()
            data_everything = {
                "submissions" : [
                    
                ]
            }

    for submission in hot_posts:
        img_url = submission.url
        new_filename = f"{output_dir}/{submission.id}.{submission.url[submission.url.rindex('.')+1:]}"
        try:
            image_filename = wget.download(img_url, new_filename)
        except FileNotFoundError as fnferr:
            print(fnferr)
            continue
        print(f"Successfully downloaded {img_url} to {new_filename}")

        if save_metadata:
            submission_meta = { "submission_id" : submission.id, "submission_title" : submission.title, "submission_url" : submission.url, "submission_comments" : submission.comments }
            data_everything["submissions"].append(submission_meta)
    
    with open(metadata_file, "w", encoding="utf-8") as g:
        json.dump(data_everything, g, indent=4) 