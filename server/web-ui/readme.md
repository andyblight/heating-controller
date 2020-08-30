# Not in the tutorial

## Set up

### Using venv

To create a new environment:

```bash
cd server/web-ui
python3 -m venv venv
```

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

## Development usage

### Start/stop web UI

To start the the web-ui, ensure that you are in the Python VEnv and then run
using `flask run`

To stop the app, press Ctrl+C.


