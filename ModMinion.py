import praw
import time
import csv
import os
from six import text_type

numberOfWatchedThread = 25
MESSAGE_LENGTH = 5000
minutesToWait = 10

subreddit = ""

r = praw.Reddit(user_agent='ModMinion')

word_list = []
user_list = []
mod_list = []

startOfMessage = " warnings were found. They are:  \nAbusive Language in comment:  \n"
userMessage = "  \nFlagged username:  \n"
submissionMessage = "  \nAbusive Submission Content:  \n"
endMessage = "  \n  \nIf you find a bug contact /u/bfish510"
continuedMessage = "Continued from last message because of length:  \n"

languageWarnings = []
userWarnings = []
submission_warnings = []

foundUserList = []

# Should be a dictionary from submission to a list of comment id's
# If a comment ID exists in the submissions comment list, we dont have to check this again.
# the advantage of this is that will allow us to get rid of comment id's that no longer 
# need to be checked because they aren't in the top 50 anymore. (though if two threads are bouncing around near the end of that list you will get repetitive messages.)
active_submissions = dict()

def checkAgainstWordBlackList(commentBody):
	for word in word_list:
		if word in commentBody:
			return True
	return False

def checkUsernameEnumeration(commentAuthor):
	authorStr = text_type(commentAuthor).lower()
	for user in user_list:
		if user in authorStr:
			print("Found possible: " + text_type(commentAuthor))
			return True
	return False

def checkCommentsInThread(thread):
	#get the list of comment ids that were checked by the program already (doesn't handle edited comments yet)
	commentIDList = active_submissions[thread.id]
	for comment in praw.helpers.flatten_tree(thread.comments):
		if comment.id not in commentIDList:
			commentIDList.append(comment.id)
			if not isinstance(comment, praw.objects.MoreComments):
				if checkAgainstWordBlackList(comment.body):
					addCommentWarningToNextModMail(comment)
				if text_type(comment.author) not in foundUserList and checkUsernameEnumeration(comment.author):
					addUserWarningToNextModMail(comment.author)
					foundUserList.append(text_type(comment.author))

def checkSubmission(submission):
	if checkUsernameEnumeration(submission.author):
		addUserWarningToNextModMail(submission.author)
	if checkAgainstWordBlackList(submission.selftext):
		addSubmissionContentToNextModMail(submission)

def addSubmissionContentToNextModMail(submission):
	print("adding submission")
	submission_warnings.append("- Submission with id " + submission.permalink + " has blacklisted content.\n")

def addCommentWarningToNextModMail(comment):
	print("adding comment")
	languageWarnings.append("- Comment by user " + text_type(comment.author)+ " with link [Here!](" + comment.permalink + ") has blacklisted content\n")

def addUserWarningToNextModMail(user):
	print("adding user")
	userWarnings.append("- User with flagged enumeration found: /u/" + text_type(user) + "\n")

def messageUpdate():
	print("Sending message to mods")
	warningCount = len(userWarnings) + len(languageWarnings) + len(submission_warnings)
	if warningCount > 0:
		message = str(warningCount) + startOfMessage + joinWarnings(languageWarnings) + userMessage + joinWarnings(userWarnings) + submissionMessage + joinWarnings(submission_warnings) + endMessage
		while len(message) > 0:
			messageToSend = message[:MESSAGE_LENGTH]
			message = message[MESSAGE_LENGTH:]
			r.send_message("/r/" + subreddit, "Issue Found", messageToSend)


def saveState():
	print("saved state")

def readPrefernceLists():
	readUserList()
	readWordList()
	readApprovedList()

def readUserList():
	if os.path.isfile('userList.csv'):
		with open('userList.csv', 'r', newline='') as f:
			global user_list
			reader = csv.reader(f)
			for row in reader:
				for item in row:
					user_list.append(item)

def readWordList():
	if os.path.isfile('wordList.csv'):
		with open('wordList.csv', 'r', newline='') as f:
			global word_list
			reader = csv.reader(f)
			for row in reader:
				for item in row:
					word_list.append(item)

def readApprovedList():
	if os.path.isfile('approvedList.csv'):
		with open('approvedList.csv', 'r', newline='') as f:
			global mod_list
			reader = csv.reader(f)
			for row in reader:
				for item in row:
					mod_list.append(item)


def saveUserList():
	with open('userList.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(user_list)

def saveWordList():
	with open('wordList.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(word_list)

def saveApprovedList():
	with open('approvedList.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(mod_list)

def checkForModMessage():
	messageList = r.get_unread()
	for message in messageList:
		if text_type(message.author).lower() in mod_list:
			command = message.body.split(' ')
			if(len(command) >= 3):
				if command[0].lower() == 'add':
					commandType = command[1].lower()
					toAdd = command[2].lower()
					if commandType == 'user' and toAdd not in user_list:
						user_list.append(command[2].lower())
						saveUserList()
						r.send_message(text_type(message.author), "user " + toAdd +" added to watch list", "user " + toAdd +" added to watch list")
					if commandType == 'word' and toAdd not in word_list:
						word_list.append(command[2].lower())
						saveWordList()
						r.send_message(text_type(message.author), "word " + toAdd +" added to watch list", "word " + toAdd +" added to watch list")
					if commandType == 'mod' and toAdd not in mod_list:
						mod_list.append(command[2].lower())
						saveApprovedList()
						r.send_message(text_type(message.author), "user " + toAdd +" added to approved list", "user " + toAdd +" added to approved list")
		message.mark_as_read()

def scanPosts():
	
	global languageWarnings
	languageWarnings = []
	global userWarnings
	userWarnings = []
	global submission_warnings
	submission_warnings = []

	subs = r.get_subreddit(subreddit).get_hot(limit=numberOfWatchedThread)
	submissions = [x for x in subs]
	submissionIds = [x.id for x in submissions]
	to_remove = []

	# find all active submission that arent in our new list
	for activeSub in active_submissions.keys():
		if activeSub not in submissionIds:
			to_remove.append(activeSub)

	#remove them from the active list to clear them from memory
	for remove in to_remove:
		del active_submissions[remove]

	# for each submission in the list
	for submission in submissions:
		if submission.id not in active_submissions.keys():
			active_submissions[submission.id] = []
			checkSubmission(submission)
		checkCommentsInThread(submission)

	messageUpdate()

def joinWarnings(listOfWarnings):
	if len(listOfWarnings) > 0:
		return '  \n' + '  \n'.join(listOfWarnings)
	else:
		return "  \nNone"

def startup():
	
	print("Username: ")
	username = input()
	print("Password: ")
	password = input()

	readPrefernceLists()

	global user_list
	global word_list
	global mod_list

	user_list = [item.lower() for item in user_list]
	word_list = [item.lower() for item in word_list]
	mod_list = [item.lower() for item in mod_list]

	if len(mod_list) == 0:
		ans = input("No approved mods found, would you like to add one. Type 'yes' to add. Otherwise this will skip.")
		if(ans.lower() == 'yes'):
			mod = input('Mod name:')
			mod_list.append(mod)
			saveApprovedList()

	try:
		r.login(username, password)
		print("logged in, starting Minion Mod")
		while True:
			checkForModMessage()
			scanPosts()
			print("Waiting " + str(minutesToWait) + " minutes")
			time.sleep(60 * minutesToWait)
	except praw.errors.InvalidUserPass:
		print("login failed, try again")

startup()