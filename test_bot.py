import os, sys, time, datetime, re
import praw # helper reddit API packages
import prawcore

class TestBot(object):

  # before committing to github, do not include config.yaml, use an example  
  def __init__(self, reddit_client, subreddits, azure_client):
    self.__reddit_client = reddit_client
    self.__subreddits = subreddits
    self.__azure_client = azure_client   

  def validate_subreddits(self):
    reddit, subreddits = self.__reddit_client, self.__subreddits
    for sub in subreddits:
      try:
        reddit.subreddit(sub).id
      except prawcore.exceptions.Redirect:
        sys.exit("Invalid Subreddit: " + sub)
      # except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException) as exception:
      except praw.exceptions.PRAWException or prawcore.exceptions.PrawcoreException as exception:
        print("Reddit API Error: ")
        print(exception)

  def stream_submissions(self):
    # Monitor and process new Reddit submissions with the provided subreddits
    reddit, subreddits, azure_client = self.__reddit_client, self.__subreddits, self.__azure_client
    
    subs = subreddits.keys()
    subs_joined = "+".join(subs)
    subreddit = reddit.subreddit(subs_joined)
    
    # keep the app running
    while True:
      try:
        for submission in subreddit.stream.submisions(pause_after=None, skip_existing=True):
          process_submission(submission, subreddits, azure_client)
      except KeyboardInterrupt:
        sys.exit("\tStopping application...")
      except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException) as exception:
        print("Reddit API Error: \n" + exception)

  def process_submission(self):
    pass
    
  
