# helping
Helping businesses find volunteers and contractors for small tasks.
## Setting up development environment
* pyenv work
  * Install pyenv, if not already installed in your PC. See: [pyenv installation and use guide](https://www.ostechnix.com/pyenv-python-version-management-made-easier/)
  * `pyenv update` to have the most up-to-date version of pyenv
  * `pyenv install 3.8.2` to install Python 3.8.2 (Django 3.0 supports 3.6,3.7,3.8).
  * `pyenv virtualenv 3.8.2 109project` to create a virtualenv (which will have its own version for all tools and packages, independent of the version installed in your PC) for this project
* [GitHub](https://github.com) work
  * If you do not already have a GitHub account, open one. You'll need to also set a SSH key. GitHub has guides for everything you'll need.
  * Clone the repository [tddpirate/helping](https://github.com/tddpirate/helping) into your account.
* Your PC work
  * Ensure that `git` is installed in your PC.
  * `mkdir` a directory where you'll work and `cd` to it.
  * Clone the repository in your account into your PC: `git clone git@github.com:youruser/helping.git` where `youruser` is your GitHub username.
  * Activate the virtualenv created above: `pyenv local 109project`
  * Install packages into the virtualenv: `pip install -r requirements.txt` - this will install Django, graphene_django (for GraphQL work) and several other packages.
  * Run the shell script: `./tools/clear_generated_files.sh`:
    * Select Yes to confirm both dialogs.
	* When asked for password, it is the Django website superuser (`admin`) password. You'll be prompted to enter it twice.
  * The aforementioned script does the following:
    1. Prepares the database.
	1. Moves your front-end files to a directory where they'll be found by the application.
	1. Creates the superuser.
* Now you are ready to play with the application.
  * `cd ./helping`
  * Activate the Django test webserver: `./manage.py runserver 0.0.0.0:8000`
  * Now you can play with the application by browsing [http://localhost:8000/static/tagiot/index.html]. If you browse from another PC, replace `localhost` by the IP address of the PC hosting the application files.
* How to modify the application
  * Stop the Django test webserver by hitting Ctrl-C.
  * The editable front-end files are in `./helping/tagiot/static/tagiot`.
  * After editing them:
    * run `./manage.py collectstatic` (it is one of the commands in `./tools/clear_generated_files.sh`).
	* restart the Django test webserver: `./manage.py runserver 0.0.0.0:8000`

## Good luck!
Of course, if you want your changes to be incorporated into the [tddpirate/helping](https://github.com/tddpirate/helping) repository, send a [pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests).
