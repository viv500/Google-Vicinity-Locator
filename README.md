# Google Vicinity Locator

A small desktop app that finds establishments near a place and exports them to a spreadsheet, using the Google Places API.

## What it does

Give it a Google Place ID, a search radius, an optional keyword and your API key. It looks up the location, pages through Nearby Search results, and saves each place's name, address, Place ID, types and rating to an Excel file.

## Run it locally

You'll need Python 3 with Tkinter, and a Google Cloud API key with the Places API enabled.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python finder.py
```

## Tech stack

Python, Tkinter, Requests, Pandas and the Google Places API.

`nearby_places.xlsx` is an example of the output.
