import os
import sys
import time
import datetime

from test_bot import TestBot
import email_config
import re
import datetime
import yaml
import praw

CONFIG_PATH = os.getenv("RPN_CONFIG", "config.yaml")
# LOGGING = ""

YAML_KEY_AZURE = "azure"
YAML_KEY_REDDIT = "reddit"
YAML_KEY_CLIENT = "client"
YAML_KEY_SUBREDDITS = "subreddits"
YAML_KEY_SECRET = "secret"
YAML_KEY_AGENT = "agent"

def main():
  # build configurations from config files
  config = app_config(CONFIG_PATH)
  reddit_config = config[YAML_KEY_REDDIT]
  # azure_config = config[YAML_KEY_AZURE]

  # get various clients
  azure_client = get_azure_client()
  reddit_client = get_reddit_client(
    reddit_config[YAML_KEY_CLIENT],
    reddit_config[YAML_KEY_SECRET],
    reddit_config[YAML_KEY_AGENT]
  )
  
  # other necessary objects
  subreddits = reddit_config[YAML_KEY_SUBREDDITS]

  # create reddit bot and pass clients to it
  test_bot = TestBot(reddit_client, subreddits, azure_client)
  test_bot.validate_subreddits()
  test_bot.stream_submissions()
  
# app configuration method with nested methods
def app_config(CONFIG_PATH):

  def check_config_file():
    # check if config file exists
    if not os.path.exists(CONFIG_PATH):
      sys.exit("Config file is missing: " + CONFIG_PATH)
    print("Using config file: " + CONFIG_PATH)
  
  def load_config_obj():
    # load config into memory
    with open(CONFIG_PATH, "r") as config_yaml:
      config = None
      try:
        config = yaml.safe_load(CONFIG_PATH)
      except yaml.YAMLError as exception:
        if hasattr(exception, "problem_mark"):
          mark = exception.problem_mark
          print("Invalid yaml, line %s column %s" % (mark.line+1, mark.column+1))
        sys.exit("Invalid config: yaml parsing failed")
      if not config:
        sys.exit("Invalid config: empty file")
    return config
  
  def validate_config(config):
    # Validate required config keys
    if YAML_KEY_REDDIT not in config or not isinstance(config[YAML_KEY_REDDIT], dict):
      sys.exit("Invalid config: missing reddit config")
    
    reddit = config[YAML_KEY_REDDIT]
    
    # check for required configs for reddit object
    if YAML_KEY_CLIENT not in reddit or not isinstance(reddit[YAML_KEY_CLIENT], str):
      sys.exit("Invalid config: missing reddit -> client config")
    
    if YAML_KEY_SECRET not in reddit or not isinstance(reddit[YAML_KEY_SECRET], str):
      sys.exit("Invalid config: missing reddit -> secret config")

    if YAML_KEY_AGENT not in reddit or not isinstance(reddit[YAML_KEY_AGENT], str):
      sys.exit("Invalid config: missing reddit -> agent config")

    if YAML_KEY_SUBREDDITS not in reddit or not isinstance(reddit[YAML_KEY_SUBREDDITS], dict):
      sys.exit("Invalid config: missing reddit -> subreddits config")
      
    print("Monitoring Reddit for:")
    
    # if there are subreddits listed, we need terms to aler the user for
    subreddits = reddit[YAML_KEY_SUBREDDITS]
    for conf in subreddits:
      currSub = subreddits[conf]
      if not isinstance(currSub, list) or not currSub:
        sys.exit("Invalid config: reddit -> subreddits -> \'" + currSub + "\' config requires a list of strings")
      if not all(isinstance(term, str) for term in currSub):
        sys.exit("Invalid config: reddit -> subreddits -> \'" + currSub + "\' config only takes string entries")
      subreddits[conf] = [x.lower() for x in currSub]
      print("r/" + conf + ": " + currSub + "\t")
  
    print("")
    reddit[YAML_KEY_SUBREDDITS] = {key.lower(): val for key, val in subreddits.items()}
    return config

  check_config_file()
  config = load_config_obj
  return validate_config(config)

# function that returns the reddit client through praw API
def get_reddit_client(client, secret, agent):
  return praw.Reddit(
    client_id = client,
    client_secret = secret,
    user_agent = agent
  )

# function that return the azure client for push notifications
def get_azure_client(client):
  return None