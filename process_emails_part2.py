import json
import dateutil.parser
from datetime import datetime
import calendar
import sys

SLICE_SIZE = "month"

def main():
	print "Starting loading old email json."
	emails_jsonobj = open("emails.json", "r")
	emails_dict = json.load(emails_jsonobj)
	emails_jsonobj.close()
	print "Done loading old email json.\n"
	users_dict = dict()
	users_overall_stats = dict()

	start_date = None
	end_date = None

	print "Starting processing time and users_overall_stats setup."
	for message_id in emails_dict:
		dateobj = dateutil.parser.parse(emails_dict[message_id]['date'])
		if dateobj.year == 1979:
			dateobj = datetime(1997, 01, 01, tzinfo=dateobj.tzinfo)
		if start_date:
			if dateobj < start_date:
				start_date = dateobj
		else:
			start_date = dateobj

		if end_date:
			if dateobj > end_date:
				end_date = dateobj
		else:
			end_date = dateobj
		emails_dict[message_id]['date'] = dateobj

		eaddrs = join_recipients(emails_dict[message_id])
		eaddrs.append(emails_dict[message_id]['from'])
		for eaddr in eaddrs:
			if eaddr not in users_overall_stats:
				users_overall_stats[eaddr] = {'name':eaddr,'sent':0,'received':0}
	print "Done processing time and users_overall_stats setup.\n"

	count = 0
	print "Counting user stats."
	sys.stdout.write("\t")
	for user in users_overall_stats:
		for message_id in emails_dict:
			count += 1
			if count % 100000 == 0:
				sys.stdout.write(" "+str(count))
				sys.stdout.flush()
			recips = join_recipients(emails_dict[message_id])
			if users_overall_stats[user]['name'] == emails_dict[message_id]['from']:
				users_overall_stats[user]['sent'] += 1
			elif users_overall_stats[user]['name'] in recips:
				users_overall_stats[user]['received'] += 1
	print "\nDone counting user stats.\n"

	count = 0
	# filtered_users = list()
	sorted_users = list()
	for eaddr in users_overall_stats:
		if users_overall_stats[eaddr]['sent'] == 0:
			continue
		if users_overall_stats[eaddr]['received'] == 0:
			continue
		if "@enron.com" not in eaddr:
			continue
		# count += 1
		# if count % 8 == 0:
		# 	filtered_users.append(eaddr)
		sorted_users.append([eaddr, users_overall_stats[eaddr]['sent']+users_overall_stats[eaddr]['received']])
	sorted_users.sort(reverse=True,key=lambda tup: tup[1])

	filtered_users = list()
	for i in range(0,100):
		filtered_users.append(sorted_users[i][0])

	# print len(filtered_users)

	for user in filtered_users:
		users_dict[user] = dict()

	print "Starting processing month-year pairs."
	year_month_pairs = get_months(start_date, end_date)
	print "Done processing month-year pairs.\n"

	print "Starting setting up users_dict with month-year pairs."
	for user in users_dict:
		for pair in year_month_pairs:
			users_dict[user][pair] = dict()
	print "Done setting up users_dict with month-year pairs.\n"


	count = 0
	print "Starting setting up other_user dicts."
	sys.stdout.write("\t")
	for chosen_user in users_dict:
		for pair in year_month_pairs:
			for other_user in filtered_users:
				count += 1
				if count % 100000 == 0:
					sys.stdout.write(" "+str(count))
					sys.stdout.flush()
				if other_user == chosen_user:
					continue
				users_dict[chosen_user][pair][other_user] = dict()
				users_dict[chosen_user][pair][other_user]["sent"] = dict()
				users_dict[chosen_user][pair][other_user]["sent"]["message_ids"] = list()
				users_dict[chosen_user][pair][other_user]["sent"]["count"] = 0
				users_dict[chosen_user][pair][other_user]["received"] = dict()
				users_dict[chosen_user][pair][other_user]["received"]["message_ids"] = list()
				users_dict[chosen_user][pair][other_user]["received"]["count"] = 0
	print "\nDone setting up other_user dicts.\n"


	count = 0
	print "Starting final computation."
	sys.stdout.write("\t")
	for chosen_user in users_dict:
		for message_id in emails_dict:
			count += 1
			if count % 100000 == 0:
				sys.stdout.write(" "+str(count))
				sys.stdout.flush()
			year_month_pair = datetime_to_year_month_pair(emails_dict[message_id]['date'])
			recipients = join_recipients(emails_dict[message_id])
			if chosen_user == emails_dict[message_id]['from']:
				for other_user in recipients:
					if other_user == chosen_user:
						continue
					if other_user not in users_dict.keys():
						continue
					# I don't like this...
					# print "sent"
					if message_id not in users_dict[chosen_user][year_month_pair][other_user]["sent"]["message_ids"]:
						users_dict[chosen_user][year_month_pair][other_user]["sent"]["message_ids"].append(message_id)
						users_dict[chosen_user][year_month_pair][other_user]["sent"]["count"] += 1
			if chosen_user in recipients:
				other_user = emails_dict[message_id]['from']
				if other_user == chosen_user:
					continue
				if other_user not in users_dict.keys():
					continue
				# print "received"
				if message_id not in users_dict[chosen_user][year_month_pair][other_user]["received"]["message_ids"]:
					users_dict[chosen_user][year_month_pair][other_user]["received"]["message_ids"].append(message_id)
					users_dict[chosen_user][year_month_pair][other_user]["received"]["count"] += 1
	print "\nDone with final computation.\n"

	count = 0
	print "Starting to trim the fat."
	sys.stdout.write("\t")
	for chosen_user in users_dict:
		for pair in year_month_pairs:
			for other_user in filtered_users:
				count += 1
				if count % 100000 == 0:
					sys.stdout.write(" "+str(count))
					sys.stdout.flush()
				if other_user == chosen_user:
					continue
				if (users_dict[chosen_user][pair][other_user]["sent"]["count"] == 0) and (users_dict[chosen_user][pair][other_user]["received"]["count"] == 0):
					del users_dict[chosen_user][pair][other_user]
			if len(users_dict[chosen_user][pair]) == 0:
				del users_dict[chosen_user][pair]
	print "\nDone trimming the fat.\n"

	for message_id in emails_dict:
		emails_dict[message_id]['date'] = str(emails_dict[message_id]['date'])

	data_dict = {'user_list': filtered_users, 'user_data': users_dict, 'emails': emails_dict, 'year_month_pairs': year_month_pairs, 'start_date': str(start_date), 'end_date': str(end_date)}

	data_jsonobj = open("data.json", "w")
	data_jsonobj.write(json.dumps(
	  data_dict,
	  indent=4,
	  sort_keys=True,
	  separators=(',', ': '),
	  encoding="utf-8"
	))
	data_jsonobj = open("user_data.json", "w")
	data_jsonobj.write(json.dumps(
	  users_dict,
	  indent=4,
	  sort_keys=True,
	  separators=(',', ': '),
	  encoding="utf-8"
	))

	data_jsonobj.close()
	data_jsonobj = open("filtered.json", "w")
	data_jsonobj.write(json.dumps(
	  filtered_users,
	  indent=4,
	  sort_keys=True,
	  separators=(',', ': '),
	  encoding="utf-8"
	))
	data_jsonobj.close()
	data_jsonobj = open("overall.json", "w")
	data_jsonobj.write(json.dumps(
	  users_overall_stats,
	  indent=4,
	  sort_keys=True,
	  separators=(',', ': '),
	  encoding="utf-8"
	))
	data_jsonobj.close()

def same_month(datetime1, datetime2):
	if datetime1.year == datetime2.year:
		return (datetime1.month == datetime2.month)
	return False

def datetime_to_year_month_pair(datetimeobj):
	month = calendar.month_abbr[datetimeobj.month]
	year = datetimeobj.year
	return str(year) + "-" + month

def get_months(datetime1, datetime2):
	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	years = list()
	start_year = datetime1.year
	end_year = datetime2.year
	for year in range(start_year, end_year + 1):
		years.append(year)
	year_month_pairs = list()
	for year in years:
		for month in months:
			pair_string = str(year) + "-" + month
			year_month_pairs.append(pair_string)

	return year_month_pairs

def join_recipients(email):
	recipients = []
	if email['to']:
		for eaddr in email['to']:
			recipients.append(eaddr)
	if email['cc']:
		for eaddr in email['cc']:
			recipients.append(eaddr)
	if email['bcc']:
		for eaddr in email['bcc']:
			recipients.append(eaddr)
	return recipients

main()