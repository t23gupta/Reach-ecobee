# Reach-ecobee
## A slack app that enlists your common interests with any user!

Steps to follow:

- Join the #connect channel in this workspace:
  https://reach-ecobee.slack.com/messages/CHHEMG79Q/

- Enter a few words about yourself and your interests as a message to that channel.

- Run Watson.py and then CommonInterests.py (required when one or more new users have added their description to the channel)

- Enter the name of any user that you want to know about your common interests with!

- You will receive a private message from the slack bot, giving you a list of all your common interests!

-----------------------------------------------------------------

The slack bot is programmed to send your message (starting with "About myself") to a remote MySQL database that stores your full name, job title and your description message.

The script, Watson.py, uses Natural Language Processing to pick keywords out of your description paragraph and stores them in another table.

The script, CommonInterests.py, makes all possible pairs of uses and stores all of their common interests in another table.

The slack bot is further programmed to query the MySQL table for a list of common interests between the current user and the user who's name has been sent as a message to the channel.
