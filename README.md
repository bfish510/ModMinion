ModMinion
=========

This bot was made to help moderators by letting them know when something happens. In subs that aren't all that active it can be hard to keep checking and adding more mods doesn't always help.

This is a tool that scans a single subreddit (for now) and will message the mods when specific events happen. These events include: 
- When certain users post 
- When certain words are posted. 

Approved moderators can also send messages to the account to add new rules. The bot does not require mod privileges. The account relies on messaging to work, so the account the bot uses needs some link karma to work.

Setup
=========

ModMinion was made with 3.4 in mind but should work on on earlier versions as long as you can install praw and six (which praw has a dependency anyway). 

You can find installation instructions here: https://praw.readthedocs.org/en/v2.1.16/#installation

You will also need a reddit account that has enough link karma that it can send mesages without a captcha being filled out. I recommend /r/freekarma for this, or a post in your subreddit asking users to upvote a bots post of a kitten or something.

This bot should not need mod privledge, but I can see additional features being added in the future for mods such as checking the mod queue for new posts stuck in the spam filter.
