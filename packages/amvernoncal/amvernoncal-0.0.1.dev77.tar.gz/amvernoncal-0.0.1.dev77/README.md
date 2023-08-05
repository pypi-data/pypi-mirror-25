# Arthur Murray Vernon Maching Learning Calendar
This Python package is great for taking Arthur Murray Vernon's Google Calendar
events and arrange them in a calendar structure in an Excel file.  That can
then be copy-and-pasted into Microsoft Office Publisher to create a printable
PDF calendar.

For those who want to go from the printable PDF calendars to a digital one,
you're in luck!  I use machine learning to parse through printable PDF
calendars and create JSONs out of them, where each event has a title,
dance_style and time (if applicable), ripe for creating Google Calendar events
from them.

While this project is geared towards use at Arthur Murray Dance Studios, feel
free to take a look at the source code and modify it for your own calendar's
needs.

Have fun!

## Setup from source code
1. Install [Python 3.x](https://www.python.org/downloads/) with pip.
2. Create and activate a virtual environment.
3. Install dependencies: ```pip install -r requirements.txt```.
4. Install the corpora ```python -m textblob.download_corpora```.
5. Profit!

## How to go from Google Calendar to an Excel file
1. Activate the Google Calendar API for your account and obtain your
```client_secret.json``` file.
2. Activate your virtual environment
3. Import the module that will use your client secret: 
```from amvernoncal import gcal_to_xlsx```.
4. Give the auth_and_get_events() function a path to your client secret,
a month and year to search, and the name of the Google Calendar you're 
converting from.
<br>Example: ```auth_and_get_events('client_secret.json', 'September 2017', 'Classes')```
5. That will then create 3 folders: JSONs, PDFs, and Output.  Your Excel file
will be in the Output folder.

## How to go from a printable PDF calendar to a JSON
1. Follow steps 1 and from above.
2. Import the function that will parse your calendar:
```from amvernoncal.pdfproc import pdf_to_json```
3. Give the parse_calendar() function a path to your calendar, named based on
the month and year, as well as tell it if you want to save to a JSON file or
just return the JSON.
<br>Example: ```pdf_to_json.parse_calendar('september_2017.pdf', to_file=True)```
