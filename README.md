### Quickfix

Assessment purpose

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit
# quickfix

common_site config file : the file is shared accross all the sites in the bench 
                          access the entire database host ,redis port etc

site_config file : the file is used to store configuration specifically for one site such as database name and database password etc

if a secret(password or api key) is accidently put in a common_site_config file ,since it is common to all sites in the bench, it becomes accessible to all sites in the bench ,this  may expose the secrets of the development site to other site

the bench start launches the following four processes:
1) Web
2)  worker
3)  Scheduler
4) Socket io 
WEB: handles the normal browser requests ,
      when an user opens the form ,saves form ,logins,api calls the web process handles it
WORKER: some tasks are heavy and slows down the ui ,so background jobs are introduced to make the heavy tasks run in background
        the queues seprates the jobs and assigns to the the workers to complete those tasks
Scheduler: it is a time of background job that is trigerred based on the time basis
Socket io: client browser communication that provides realtime notifications
