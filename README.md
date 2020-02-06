Tinder bot

- Use this bot at your own risk. This was created for educational purposes (learning how to work with selenium and handling data with python). It is not recommended to use as you run the risk of getting banned.
- The bot will login to Tinder, and auto swipe for you.
- By default the bot will dislike if the user has one or no images, no bio, no age, or the bio is less the 5 characters. These can be changed in the settings.py file.
- The bot can also check the bio for words you don't want to swipe on. Like if you don't want to swipe on someone that has `married`, `premium`, or `cashapp` in their bio then you can change the `stop_words` variable in the settings.py file to dislike if it finds those words.
- It is friendly with slower internet connections. Tested on 0.5Mb upload/download speeds.
- Logs information about the profile to the `.\logs\raw_data\` folder along with any errors it comes across.
- Can parse the users bio to find keywords into `.\logs\parsed\profiles.log` with parse_logs.py
- Urls for users profile pictures and can be listed into `.\logs\parsed\picture_urls.log` with parse_logs.py
- Random wait times to help prevent bot detection.
- If you want to swipe in a different area then your local area use a vpn and select a vpn server where you want to swipe.

To install:

- download/install python 3+
- no need to install the chromedriver as chromedriver_binary will do it for us
- cd to the folder you want to install the bot in
- `pip install virtualenv`
- `virtualenv venv`
- `.\venv\scripts\activate`
- Install dependencies:
- `pip install -r requirements.txt`

To setup:
Create a secrets.py file with variables:

```
 username = 'your_username'
 password = 'your_password'
```

Configure:

Change the settings in settings.py to your liking.

To run:

- Run bot: `python .\tinder_bot.py`
- Run log parser: `python .\parse_logs.py`

To stop the bot just spam/hold down `ctrl + c` until it stops.

Known bugs:

- If a popup comes up while swiping thru pictures then the bot will stop swiping the pictures and won't continue untill it tries to go thru all of the pictures and tries to open a new profile. It will fail to open a new profile but will continue swiping thru the pictures and like/dislike after.
- parse_logs.py adds duplicate urls in the `picture_url_file.log` file. This issue doesn't seem to happen with every url but adding `sleep()` in the loop will fix the issue but makes it slower.

Feature ideas:

- Add a script to take all of the urls from the `.\logs\parsed\picture_urls.log` file and download all of them.
- Add the ability for the bot to save the images to the harddrive directly from the users profile.

please add more features to this, would be awesome to see what you can come up with

cheers
