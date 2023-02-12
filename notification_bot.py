import os, sys, time, datetime, re
import praw, prawcore # helper reddit API packages

class NotificationBot(object):

  def __init__(self, reddit_client, subreddits, apprise_client, LOGGING):
    self.__reddit_client = reddit_client
    self.__subreddits = subreddits
    self.__apprise_client = apprise_client
    self.__LOGGING = LOGGING

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

  # run the app, "streaming" submissions
  def stream_submissions(self):
    # Monitor and process new Reddit submissions with the provided subreddits
    reddit, subreddits, apprise_client = self.__reddit_client, self.__subreddits, self.__apprise_client
    
    subs = subreddits.keys()
    subs_joined = "+".join(subs)
    allSubs = reddit.subreddit(subs_joined)
    
    print("\nNow streaming subreddits...")
    
    while True: # keep the app running!
      try:
        for submission in allSubs.stream.submissions(pause_after=None, skip_existing=True):
          self.__process_submission(submission, subreddits, apprise_client)
          print(submission.title, submission.id)
      except KeyboardInterrupt:
        sys.exit("\tStopping application...")
      except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException) as exception:
        print("Reddit API Error: \n" + exception)
        print("Resuming in one minute...")
        time.sleep(60)

  # check if any term in this search contains targeted term 
  def __process_submission(self, submission, subreddits, apprise_client):
    title = submission.title
    subName = submission.subreddit.display_name
    search_terms = subreddits[subName.lower()]
    
    if any(term in title.lower() for term in search_terms):
      self.__notify(apprise_client, title, submission.id)
      if self.__LOGGING != "FALSE":
        print(datetime.datetime.fromtimestamp(submission.created_utc),
        " " + "r/" + subName + ": " + title)
  
  # send push notifications to users
  def __notify(self, apprise_client, title, submission_id):
    apprise_client.notify(
      title = title,
      body = "https://www.reddit.com/" + submission_id
    )