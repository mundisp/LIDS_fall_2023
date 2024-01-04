## Important Commands for manage.py
- python3 manage.py makemigrations -> run this after inserting a new model into models.py. 
- python3 manage.py migrate -> basically commits updates based on changes you make to database
  - Recommended to run this command before running the server after working with database. It is basically harmless if there are no updates
- python3 manage.py sqlmigrate <app-name> 0001 -> not completely sure what this does at the moment. Seems to create a new table in the DB based on the new model class you entered in models.py

*Note: run the above commands in the order they're given, the first time. For sqlmigrate our <app-name> is 'dashboard'.
You may not need to do the 'sqlmigrate' commands since I pushed the 0001_initial.py to the repo under the 'migrations' folder.*

## Important files
- models.py -> where you define your 'models' which are the tables and their attributes that you wanna use
- views.py -> where you can define methods to insert into and retrieve data from the DB. I have a couple sample methods in there

Will add more to this later, this is just to get started