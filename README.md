# Heating Controller

Code to monitor and control a central heating system.

## Planned Implementation

The system is made up of:

* A number of temperature and humidity sensors.  DONE.
* A scraper that records temperature and wind data from a third party website
that publishes data taken from a weather station in my home town.  DONE.
* A server that:
  * Publishes the stored data on a web page.
  * Estimates when the central heating should be switched on and off.
    * The estimator should use the external temperature (and the possibly the
    forecast) to work out how long the heating needs to be on.
  * Has a nice user interface to program the on/off times for different days
  of the week etc.
  * A method of communicating with the central heating controller to:
    * Record the central heating on / off times.
    * Update the user programs.
    * Update variables, e.g. pre-heat times.
* A central heating controller that:
  * Turns the central heating on and off using:
    * Data from the temperature sensors.
    * The program set by the user (sent fromt he server).
    * Pre-heat times (how long the house takes ot heat up to the desired
    temperature so that the house is at the desired temerpature when we get
    home.)
  * Reports the central heating on /off times to the server.
  * A basic user interface to override the programmed settings, e.g.
    * boost - turn on heating for 1 hour.
    * cancel - turn off heating as too warm.  Resumes programmed settings after
    a preset time.
    * off - turn off heating as going on holiday or it's summer so is not
    needed.
    * A screen to display info, e.g. status, temperatures of all sensors, along
    with buttons to control the screen.

As you can see, there are few items that are DONE.  The rest is just me
dreaming until I get around to doing something about them.

## What is in the repo?

The repo contains the following:

* nodemcu - All the code and files needed to program the ESP8266 nodemcu.
* server - The code for the server.  This runs in a docker on the server so it
is easier to maintain and can be developed on other PCs.  This includes:
  * scrapers - The code to scrape external websites and store it in CSV files.
  * web-ui - Displays information gathered by the scrapers.

## Python Virtual Environment

This is pretty simple but there is very little documentation on using VEnv.
There doesn't need to be much but working this out took an hour or so.

### First time

To create a new environment:

```bash
cd server/web-ui
python3 -m venv venv
```

### Using venv

To start the environment: `. venv/bin/activate`

To set up the virtual environment for first time use, run

```bash
cd server/web-ui/scripts
./install_requirements.bash
```

To exit the venv session: `deactivate`

Note: after adding a new package to the VEnv, deactivate and activate to pick up
the change.

### Saving the venv in git

From here:
<https://stackoverflow.com/questions/6590688/is-it-bad-to-have-my-virtualenv-directory-inside-my-git-repository>

You do not want to save the full `venv` in git, so exclude the `venv` directory
in `.gitignore`.

Using the `requirements.txt` file works much better. The `scripts` directory
has scripts that do everything for you.

Use `save_requirements.bash` everytime you add another package to the `venv`.

Use `install_requirements.bash` to set up the `venv` on a new machine.

## Python linting and formatting

The linting is done using `flake8` and the formatting is done using `black`.
These are installed as part of the virtual enviroment along with `flake8-black`
that integrates the linter and formatter.  The settings for `flake8` are
modified to match `black` by values in setup.cfg.
