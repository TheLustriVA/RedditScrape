from pathlib import Path 
import json

def do_not_have(filename):
    """
    If the file does not exist, return True. Otherwise, return False.
    
    Args:
      filename: The name of the file you want to check.
    
    Returns:
      True or False
    """
    if Path(filename).exists() is False:
        return True
    else:
        return False

def not_in_metadata(submission, metadata):
    """
    It returns True if the submission is not in the metadata, and False otherwise
    
    Args:
      submission: the submission object
      metadata: the metadata file that we're going to be updating
    
    Returns:
      A list of submissions that are not in the metadata.
    """
    for record in metadata['submissions']:
        if record["submission_id"] == submission.id:
            return False
    return True
  
def init_new_subreddit_folder(subreddit, output_dir):
    """
    It initializes a new folder for a subreddit.
    
    Args:
      subreddit: The subreddit to initialize.
      output_dir: The directory to initialize the folder in.
    
    Returns:
      The name of the new folder.
    """
    new_folder = Path(output_dir) / subreddit
    if new_folder.is_dir() is False:
        new_folder.mkdir(parents=True)
    with open(new_folder / "metadata.json", "w", encoding="utf-8") as f:
        json.dump({
            "submissions" : []
        }, f, indent=4)
    return new_folder