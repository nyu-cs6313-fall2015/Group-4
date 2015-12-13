import email.parser
import json
import os

def parse_email(filepath):
  fileobj = open(filepath, "r")
  parser = email.parser.Parser()
  emailobj = parser.parse(fileobj)
  fileobj.close()

  revised_parsed_email = dict()

  revised_parsed_email['message_id'] = emailobj['Message-ID'].decode('cp1252').encode('utf-8')
  revised_parsed_email['subject'] = emailobj['Subject'].decode('cp1252').encode('utf-8')
  revised_parsed_email['date'] = emailobj['Date'].decode('cp1252').encode('utf-8')
  revised_parsed_email['from'] = emailobj['From'].decode('cp1252').encode('utf-8')
  revised_parsed_email['to'] = parse_email_addresses(emailobj['To'])
  revised_parsed_email['cc'] = parse_email_addresses(emailobj['Cc'])
  revised_parsed_email['bcc'] = parse_email_addresses(emailobj['Bcc'])
  revised_parsed_email['body'] = emailobj.get_payload().decode('cp1252').encode('utf-8')
  return revised_parsed_email

def parse_email_addresses(email_addresses_string):
  if email_addresses_string is None:
    return None
  else:
    address_list = email_addresses_string.split(",")
    for i in range(len(address_list)):
      address_list[i] = address_list[i].strip().decode('cp1252').encode('utf-8')
    return address_list

def walk_directory(dir_to_walk):
  # Dict to store all emails in
  emails_dict = dict()
  # Dict to store all users in
  users_dict = dict()
  # Open the file write the JSON data to 
  emails_json = open("../jsons/emails.json", 'w')
  users_json = open("../jsons/users.json", 'w')
  # The count of the emails we've grabbed
  email_count = 0
  # Recurse the given directory
  for dirpath, dirnames, filenames in os.walk(dir_to_walk):
    # Skip the discussion_threads folder as it doesn't have many useful emails
    if "discussion_threads" in dirpath:
      continue
    # Take 2% of the total number of files in the folder
    num_files = round(len(filenames) * .02)
    # Prevent division by zero
    if num_files > 0:
      # Create interval to read emails at
      interval = int(round(len(filenames)/num_files))
      # Go through filenames
      for i in range(0, len(filenames), interval):
        if filenames[i][0] == ".":
          continue
        email_count += 1
        full_path = os.path.join(dirpath,filenames[i])
        # print full_path
        # Parse the email
        parsed_email = parse_email(full_path)
        add_data_to_dicts(emails_dict, users_dict, parsed_email)

        # Show progress at 1000 email intervals
        if email_count % 1000 == 0:
          print email_count
  # Write the dictionaries in JSON format
  emails_json.write(json.dumps(
      emails_dict,
      indent=4,
      sort_keys=True,
      separators=(',', ': '),
      encoding="utf-8"
  ))
  users_json.write(json.dumps(
      users_dict,
      indent=4,
      sort_keys=True,
      separators=(',', ': '),
      encoding="utf-8"
  ))
  print email_count
  emails_json.close()
  users_json.close()

def add_data_to_dicts(emails_dict, users_dict, parsed_email):
  sender = parsed_email['from']
  if sender not in users_dict.keys():
    users_dict[sender] = dict()
    users_dict[sender]['emails_sent'] = list()
    users_dict[sender]['users_communicated_with'] = list()
  if parsed_email['to'] is not None:
    for user in parsed_email['to']:
      if (user not in users_dict[sender]['users_communicated_with']) and (user != sender):
        users_dict[sender]['users_communicated_with'].append(user)
  if parsed_email['cc'] is not None:
    for user in parsed_email['cc']:
      if (user not in users_dict[sender]['users_communicated_with']) and (user != sender):
        users_dict[sender]['users_communicated_with'].append(user)  
  if parsed_email['bcc'] is not None:
    for user in parsed_email['bcc']:
      if (user not in users_dict[sender]['users_communicated_with']) and (user != sender):
        users_dict[sender]['users_communicated_with'].append(user)
  if parsed_email['message_id'] not in users_dict[sender]['emails_sent']:
    users_dict[sender]['emails_sent'].append(parsed_email['message_id'])
  # Add the email if it is not a duplicate
  if parsed_email['message_id'] not in emails_dict.keys():
    emails_dict[parsed_email['message_id']] = parsed_email

walk_directory("../maildir")
