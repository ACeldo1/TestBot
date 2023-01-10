import praw
import re
import datetime
import time
import calendar

class Test_Bot(object):

  # build initalizing method after building working bot
  def __init__(self, username, password, search_terms, time_range):
    self.user_agent = "Test Bot 0.1"
    self.reddit = praw.Reddit(user_agent=self.user_agent)
    self.reddit.login(username,password)
    self.time_range = time_range
    self.search_terms = search_terms
    
    self.submission_list = []
    

    # self.last_day_of_current_month = 0
    # self.month_of_last_submission = 0
    # self.submission_for_month = False
  
  
  def __init__(self, search_terms, remaining_time):
    self.reddit = praw.Reddit() # uses praw.imi file config
    self.search_terms = search_terms
    self.remaining_time = remaining_time

  def create_submission_list(self):
    for search_term in self.search_terms:
      create_submission(search_term)

  def create_submission(search_term):
    


  # run at the end of every method to ensure that we exit on time
  # def check
  
