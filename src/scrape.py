from urllib.error import HTTPError
import wget
import json
from time import sleep
from src.auth import get_reddit_session
from pathlib import Path
from src.routing import do_not_have, not_in_metadata


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
            print(metadata_file)
            with open(metadata_file, "r", encoding="utf-8") as f:
                data_everything = json.load(f)
        else:
            metadata_file.touch()
            data_everything = {
                "submissions" : [
                    
                ]
            }
            
    download_check = []

    for submission in hot_posts:
        img_url = submission.url
        new_filename = f"{output_dir}/{submission.id}.{submission.url[submission.url.rindex('.')+1:]}"
        if do_not_have(new_filename):
            try:
                image_filename = wget.download(img_url, new_filename)
                print(f"Successfully downloaded {img_url} to {new_filename}")
                download_check.append(new_filename)
            except FileNotFoundError as fnferr:
                print(fnferr)
                continue
            except HTTPError as herr:
                print(herr)
                continue
        else:
            print(f"{new_filename} already exists")
        submission_meta = {}
        new_filename = Path(new_filename)
        if save_metadata and not_in_metadata(submission, data_everything):
            if new_filename.exists():
                submission_download = { "filename" : new_filename, "success" : True }
            else:
                submission_download = { "filename" : new_filename, "success" : False }
            comments_list = []
            replies_list = []
            if len(submission.comments) > 0:
                for comment in submission.comments:
                    while True:
                        try:
                            submission.comments.replace_more()
                            break
                        except Exception:
                            print("Handling replace_more exception")
                            sleep(1)
                    comments_list.append( { "id" : comment.id, "body" : comment.body, "replies" : []} )
                    if len(comment.replies) > 0:
                        for reply in comment.replies:
                            replies_list.append( { "id" : reply.id, "body" : reply.body } )
                        comments_list[-1]["replies"] = replies_list
                submission_meta = { "submission_id" : submission.id, "submission_title" : submission.title, "submission_url" : submission.url, "submission_download" : submission_meta, "submission_comments" : comments_list }
            else:
                submission_meta = { "submission_id" : submission.id, "submission_title" : submission.title, "submission_url" : submission.url, "submission_download" : submission_meta, "submission_comments" : [] }
            data_everything["submissions"].append(submission_meta)
            print(data_everything)
    
    with open(metadata_file, "w", encoding="utf-8") as g:
        json.dump(data_everything, g, indent=4)
    return (metadata_file, download_check)
    
def get_hot_subreddits(subreddit_list, output_dir, output_json, save_metadata=False):
    check_list = []
    for subreddit in subreddit_list:
        check_list.append(get_hot_subreddit(subreddit, output_dir, output_json, save_metadata))
    return check_list