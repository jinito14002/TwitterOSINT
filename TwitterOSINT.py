import os
import sys
import re
import pandas as pd
import snscrape.modules.twitter as sntwitter
from win10toast_click import ToastNotifier
from datetime import date, datetime
from csv import reader

tweets = []
today = datetime.utcnow().date()
leak = 0
# Max number of tweets to scrape
limit = 1000

def notepad():
	os.system('notepad.exe ' + 'leak_' + str(today) + '.txt')
	return 1

def Search(query):

	for tweet in sntwitter.TwitterSearchScraper(query).get_items():
		dt = datetime.fromisoformat(str(tweet.date))
		date = dt.date()
		if len(tweets) == limit or (date != today):
			break
		else:
			print(tweet.date)
			print(tweet.user.username)
			print(tweet.rawContent)
			tweets.append([tweet.date, tweet.user.username, tweet.rawContent])

def main():

	# Insert keyword here. (e.g. your organization name)
	Search("Microsoft")

	df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
	df.to_csv('scraped-tweets'+ str(today) +'.csv', index=False, encoding='utf-8')
	print("\n\n-----Scraped " + str(len(tweets)) + " Tweets-----\n")
	print(today)

	# regex strings to look for inside tweet
	pattern = re.compile(r'leak|breach', re.IGNORECASE)

	# Iterate Scraped Tweets for regex pattern
	with open('scraped-tweets'+ str(today) +'.csv', 'r', encoding='utf-8', newline='') as csvfile:
		read = reader(csvfile)
		for row in read:
			row_str = ','.join(row)
			if pattern.search(row_str):
				leak = row[2]
				with open('leak_' + str(today) + '.txt', 'a', encoding='utf-8') as f:
					f.write("Username: " + row[1] + "\n" + row[2] + "\n\n-----------------------------------------------\n\n")
					f.close()
					
	# Send Window alert if data leak string found in tweet
	# Opens text of scraped tweet when clicking on notification
	if leak:
		try:
			toaster = ToastNotifier()
			toaster.show_toast(
				"Possible Data Leak?",
				leak,
				icon_path=None,
				duration=5,
				callback_on_click=notepad
			)
		except TypeError:
			pass
	input("Press Enter to end...")

if __name__ == '__main__':
	main()

