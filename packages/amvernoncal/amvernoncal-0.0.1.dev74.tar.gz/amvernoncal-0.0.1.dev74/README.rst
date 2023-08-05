Arthur Murray Vernon Machine Learning Calendar
==============================================

This Python package is great for taking Arthur Murray Vernon's Google
Calendar events and arrange them in a calendar structure in an Excel
file. That can then be copy-and-pasted into Microsoft Office Publisher
to create a printable PDF calendar.

For those who want to go from the printable PDF calendars to a digital
one, you're in luck! I use machine learning to parse through printable
PDF calendars and create JSONs out of them, where each event has a
title, dance\_style and time (if applicable), ripe for creating Google
Calendar events from them.

While this project is geared towards use at Arthur Murray Dance Studios,
feel free to take a look at the source code and modify it for your own
calendar's needs.

Have fun!

Setup from source code (GitHub)
-------------------------------
1. Clone the repo.  ``git clone https://github.com/vincentchov/amvernon-cal.git``
2. Install `Python 3.x <https://www.python.org/downloads/>`__ with pip.
3. Install Java 8.
4. Create and activate a virtual environment.
5. Install the corpora ``python -m textblob.download_corpora``.
6. Install dependencies: ``pip install -r requirements.txt``.
7. Profit!

Setup from from PyPI (Pip)
--------------------------

1. Follow steps 2-5 from above.
2. Install amvernoncal from PyPI.  ``pip install amvernoncal``

How to go from Google Calendar to an Excel file
-----------------------------------------------

1. Activate the Google Calendar API for your account and obtain your ``client_secret.json`` file.
2. Activate your virtual environment.
3. Import the module that will use your client secret: ``from amvernoncal.gcal_to_xlsx import gcal_events_to_xlsx``.
4. Give the gcal\_events\_to\_xlsx() function a month and year to search, and the name of the Google
   Calendar you're converting from, making sure to surround each of the two arguments by quotes. 
   Example: ``gcal_events_to_xlsx('September 2017', 'Classes')``
5. That will then create 3 folders: JSONs, PDFs, and Output. Your Excel
   file will be in the Output folder.

How to go from a printable PDF calendar to a JSON
-------------------------------------------------

1. Follow steps 1 and from above.
2. Import the function that will parse your calendar: ``from amvernoncal.pdfproc.pdf_to_json import parse_calendar``
3. Give the parse\_calendar() function a path to your calendar, named
   based on the month and year, as well as tell it if you want to save
   to a JSON file or just return the JSON. 
   Example: ``parse_calendar('september_2017.pdf', to_file=True)``
