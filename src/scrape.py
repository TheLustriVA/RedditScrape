from urllib.error import HTTPError
import wget
import json
from time import sleep
from src.auth import get_reddit_session
from pathlib import Path
from src.routing import do_not_have, not_in_metadata, init_new_subreddit_folder


def get_hot_subreddit(subreddit, output_dir, save_metadata=False):
    """
    It takes a subreddit name, an output directory, and an output json file name, and downloads the hot
    posts from the subreddit to the output directory, and saves the metadata to the output json file
    
    Args:
      subreddit: The subreddit to download from.
      output_dir: The directory to save the images to.
      save_metadata: If True, will save the metadata of the submission to a JSON file. Defaults to False
    
    Returns:
      A tuple of the metadata file and a list of the downloaded files.
    """

    reddit = get_reddit_session()

    from_subreddit = reddit.subreddit(subreddit)

    hot_posts = from_subreddit.hot()

    out_dir = Path(output_dir)
    if out_dir.is_dir() is False:
        out_dir.mkdir(parents=True)

    if save_metadata:
        metadata_file = Path(out_dir / subreddit / "metadata.json")
        if metadata_file.is_file():
            print(metadata_file)
            try:
                with open(metadata_file, "r", encoding="utf-8") as f:
                    data_everything = json.load(f)
            except json.decoder.JSONDecodeError:
                data_everything = {"submissions" : []}
        else:
            init_new_subreddit_folder(subreddit, out_dir)
            print(f"New: {metadata_file}")
            try:
                with open(metadata_file, "r", encoding="utf-8") as f:
                    data_everything = json.load(f)
            except json.decoder.JSONDecodeError:
                data_everything = {"submissions" : []}
    download_check = []
    # TODO: Include an Alive_Bar with an indication of total progress through the subreddit.
    # Iterating through the hot posts in the subreddit.
    for submission in hot_posts:
        img_url = submission.url
        new_filename = f"{output_dir}/{subreddit}/{submission.id}.{submission.url[submission.url.rindex('.')+1:]}" # FIXME: This needs to be tested that it actually goes to the new Subreddit folder.
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
        # Checking if the submission is already in the metadata file.
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
                            # Replacing the "More Comments" button with the actual comments.
                            submission.comments.replace_more()
                            break
                        except Exception:
                            print("Handling replace_more exception")
                            sleep(1)
                    comments_list.append( { "id" : comment.id, "body" : comment.body, "replies" : []} )
                    if len(comment.replies) > 0:
                        for reply in comment.replies:
                            # Appending the replies to the replies list.
                            replies_list.append( { "id" : reply.id, "body" : reply.body } )
                        comments_list[-1]["replies"] = replies_list
                # TODO: Write a Reader-object handler so that all metadata includes Author data for later cross-checking.
                submission_meta = { "subreddit": subreddit, "submission_id" : submission.id, "submission_title" : submission.title, "submission_url" : submission.url, "submission_download" : submission_meta, "submission_comments" : comments_list }
            else:
                submission_meta = { "subreddit": subreddit, "submission_id" : submission.id, "submission_title" : submission.title, "submission_url" : submission.url, "submission_download" : submission_meta, "submission_comments" : [] }
            data_everything["submissions"].append(submission_meta)
    # TODO: Abstract all saving and downloading to a separate function and call it from routes.py.
    with open(metadata_file, "w", encoding="utf-8") as g:
        json.dump(data_everything, g, indent=4)
    return (metadata_file, download_check)
    
def get_hot_subreddits(subreddit_list, output_dir, save_metadata=False):
    """
    It takes a list of subreddits, and returns a list of the top 25 posts from each subreddit
    
    Args:
      subreddit_list: a list of subreddits to scrape
      output_dir: The directory where you want to save the images.
      save_metadata: If True, will save the metadata of the posts in a json file. Defaults to False
    
    TODO: Include an Alive_Bar with an indication of which subreddit is being scraped.
    
    Returns:
      A list of the subreddit names that were successfully downloaded.
    """
    check_list = []
    for subreddit in subreddit_list:
        check_list.append(get_hot_subreddit(subreddit, output_dir, save_metadata))
    return check_list

