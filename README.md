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

When a browser hits /api/method/quickfix.api.get_job_summary - what Python
function handles this request and how does Frappe find it?
When a browser hits /api/method/quickfix.api.get_job_summary the frappe whitelist handles the custom api calls and executes the function
How does the frappe knows
when  a client makes a server requests through api method the function first looks into the app.py,so that app.py recieves the request and passes to the function execute_cmd in handler.py which then calls the frappe.get_attr() , the get_attr() from init.py is used to call the whitelisted python function and the function returns a json file
consider the scenario if we have a wrong function name provided then there shows up a traceback error from the handler.py 


When a browser hits /api/resource/Job Card/JC-2024-0001 - what happens
differently compared to /api/method/?
when  /api/method/ is called it uses the custom whitelisted python function that is written by developer 
but when a browser hits /api/resource/Job Card/JC-2024-0001 the rest api call is being processed that is there is no need of the custom functions ,it directly access the database ,fetches or modifies the database without the python custom function ,the rest api controlers directly access the job card doctype and the document jc-2024-000021 and returns the json data


When a browser hits /track-job - which file/function handles it and why?
when the browser hits the track-job ,app.py recieves the request ,then the request is sent to the handler.py ,so that the handler.py identifies the type of the request whether it is rest api call or the custom method then it extracts the method path and loads the execute_cmd in the handler.py file ,thenn the request is sent to the init.py to load the frappe.get_attr() function then the whitelist function is checked and the function is executed and the response is sent throught the json file

Open your Frappe site in browser devtools. Find the X-Frappe-CSRF-Token in a POST request. Where does this value come from and what would happen if you
omitted it?
After opening the frappe site in browser devtools ,while creating a new record or while saving the record the post request is made ,this post request value is a randomly generated value to store in the session id and we can encounter the csrf token under the request headers or in the bench console if we give frapp.csrf_token we can get the token .If the token is omitted the put post method doesnt havet he session id and it will not work ,if tokens are missing frappe will bolck the request for the security reasons

In bench console, run: import frappe; frappe.session.data and describe what it contains
frappe.session.data returns the null dictionary while the frappe.session returns the sid ,data and the user

With developer_mode: 1 - trigger a Python exception in one of your whitelisted methods. What does the browser receive?
returned a undefined variable in the python whitelisted function and the browser recived the nameerror
  File "apps/quickfix/quickfix/api.py", line 6, in execute
    return x
NameError: name 'x' is not defined

Set developer_mode: 0 - repeat. What does the browser receive now? Why is this
important for production?
here since we are running in local development when the developer mode is either 0 or 1 the error full be shown fully with the traceback
but when in the production mode ,when the developer mode is 0 the error will be shown as internal server error and not the full traceback will be shown 
this is important for production because while showing the detailled error this may expose the detailled code structure and information 

Where do production errors go if they are hidden from the browser?
the production errors which are hidden from browser are stored in log file 
the bench contains a folder log with frappe.log
