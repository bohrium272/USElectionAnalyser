US Elections Analyser
---

Deployed at: precoguselections.herokuapp.com

*   Twitter Streamer can be started using ```python fetch.py``` or ```heroku run:detached python fetch.py``` on Heroku.
*   ```fetch.py``` used for managing database related functions.
*   ```analysis.py``` used for extracting tweets from database and carrying out analysis.
*   ```app.py``` used for Flask routing.