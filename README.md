# finland

To start testing:
1. open https://intense-scrubland-84863.herokuapp.com/
2. click any feature link you'd like to test

To start development:

Preparations:
- make sure python version 3.6 or greater is installed
- make sure pipenv is installed
- make sure git bash is installed
- make sure heroku is intalled and authentication passed. More information: https://devcenter.heroku.com/articles/getting-started-with-python#set-up

1. clone repo from heroku (this one is used for delpoyment):
git clone https://git.heroku.com/intense-scrubland-84863.git
2. cd to you project root
3. add remote gir repo:
git remote add origin https://github.com/shaurun/finland.git
4. create virtual env:
pipenv --three
pipenv install
5.run pipenv shell
pipenv shell
Note you may need to make this command 2 times unless you get some link where your env is runnging, like:
C:\Users\User\.virtualenvs\finance-SRN5JmJO
6. create your .env file:
echo "source C:\Users\User\.virtualenvs\finance-SRN5JmJO/bin/activate" >> .env
Use path from step 5.
7. Run your app locally with:
- on Windows:
 heroku local web -f Procfile.windows
- on Unix systems:
 heroku local web


Deployment:
after all code is commited use:
git push heroku master

Adding new dependencies:
pipenv install <your_dependency>

