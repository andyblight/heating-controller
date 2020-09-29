# Heating controller web server

## Run the code

### Start/stop web UI

To start the the web-ui, __ensure that you are in the Python VEnv__ and then
start the flask app using `flask run`.

To stop the app, press Ctrl+C.

### Run the tests

To run the tests, use:

```text
python3 -m unittest app/test/test_prepare_data.py
python3 -m unittest app/test/test_charts_load_data.py
```

## Development

### Design

The basic concept is that the scrapers write information to CSV files.  The use
of CSV files allows recent values to be read from the files as well as providing
datasets to run analysis programs on when time permits.

The most recent data from the CSV files can be used to decide if the heating
needs to be switched on or off.  Some trend analysis of the external temperature
readings can be performed to adjust the length of time that the heating is
turned on for.

One problem that also needs to be considered is that humans do things that
affect the heating system, e.g. leave windows and doors open.  Eventually,
sensors need to be fitted to every window and door to allow the heating
controller to make better decisions, remembering that humans are the masters.
After all, this system is only a servant trying to make the house comfortable
for the humans to live in.

#### Home page

This page shows an overview of the current status.

For each local sensor it shows:

* The last recorded temperature and humidity along with the time of data.
* Status of the sensor: online means that the last recorded data was recorded
less than a specified time limit ago.

The external sensor data records a lot more information, so this is presented
on the home page.  As a minimum it should show the latest value of tempterature
and humidity.

There will also be some indication of the central heating status, e.g.
off, on, hours on per day.

Nice to have: I would like a display to tell me if it is worth hanging the
clothes out on the washing line.  This should consider things like dew point,
wind speed and sun and give me an idea of how long clothes willl take to dry.

#### Charts page

The charts page shows the raw sensor data over different time ranges along with
the heating demand.  This can be used for manual verification of the algorithms
being used to control the heating.  It also looks cool!

When the charts page is requested, three CSV files are prepared for today and
the past 7 days.  The CSV generated files have dates encoded in the file names
so that the minimum work possible is done.  The charts page then shows the
collated CSV information in three charts.

### Notes

I tried flask-goolgecharts but I could not get it to run.  No decent help
either.

Trying this:
<https://developers.google.com/chart/interactive/docs/dev/gviz_api_lib>

Finally got something working.

Split out chart preparation from routes.py into charts.py.
Split out reading and processing of CSV files into prepare_data.py and added
unit tests as too difficult to debug when using flask.
HERE!!! Working on merging data.

