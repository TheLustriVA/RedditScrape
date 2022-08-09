from pathlib import Path 

def do_not_have(filename):
    if Path(filename).exists() is False:
        return True
    else:
        return False

def not_in_metadata(submission, metadata):
    for record in metadata['submissions']:
        if record["submission_id"] == submission.id:
            return False
    return True