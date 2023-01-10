import test_bot
import email_config
import re
import datetime

def main():
  user_inputs = get_user_inputs()
  user, pwd, email_input, after_date, remaining_time, run_frequency, search_terms = [user_inputs[i] for i in range(len(user_inputs))]

  # if we could not create a test_bot instance, exit
  # test_bot = test_bot.Test_Bot(username, password, search_terms, remaining_time)
  test_bot = test_bot.Test_Bot(search_terms, remaining_time)
  if test_bot is None or email is None:
    print('Incorrect username or password')
    return
  
  # if we could not configure the email address, exit
  email = email_config.Email_Configuration(email_input)
  if email is None:
    print('Could not confirm email address')
    return

  # built Test Bot and confirmed email, so we run different tests and methods from bot
  

  # get results from bot and store in a data structure
  
  
  # send results to email

def get_user_inputs():
  username = input('Input username: ')
  password = input('\nInput password: ')
  email_input = input('\nInput email to send results to: ')

  # worry about bot timer afterwards
  # time_range_input = input('\nHow long do you want the bot to run?')
  # frequency_input = input('\nHow often do you want to receive results?')

  # temporary fixed variables
  after_date = datetime.datetime(2023, 1, 7)
  running_time = 30
  run_frequency = 10
  search_terms = get_search_terms()
  
  return [username, password, email_input, after_date, running_time, run_frequency, search_terms]

# function that will split user input with regular expression matching
def get_search_terms():
  search_terms = [] # limit search terms to 5
  string_input = input('\nPlease provide at most 5 search terms (separate terms with at least one space\)').split(" ")
  input_regex = re.split('\s+', string_input)
  idx = 0
  while idx < 5 and idx < len(input_regex):
    search_terms.append(input_regex[idx])
    idx += 1
  return search_terms

main()