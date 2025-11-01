# This is the main log book/ Documenting or the whole process of the project

## Week 1
### Day 1: Primary Setup
    + Created folder called C-Connect, made the project folder structer
    + Made a conda environment named 'cconnect'
    + Connected the project with the Git repo named 'C-Connect'
    + Made the initial commit(s)
    + Learning about Flask and it's usages

        *Folder Structure*
        `C-Connect/
            │
            ├── app.py
            ├── project_document.md
            ├── database.db
            ├── /static/
            │     ├── css/
            │     └── js/
            ├── /testing/
            │     └── logic_testing.ipynb
            └── /templates/
                ├── signup.html
                └── login.html
        `

### Day 2: Project Skeleton
    + Created `requirements.txt` file for the conda env (using `conda freeze > requirements.txt`)
    + Learned a bit of basics of Flask concepts from `CodeAcademy` and coding from `youtube` (https://youtu.be/45P3xQPaYxc?si=t8Bti4wHVdkkio3J)
    + Learned about using  `render_template` and found we are supposed to name that base.html file's folder as 'templates' not as 'template'!!
    + Template inheritence is also being learned
    + Need to think in terms of the flow of the site

   ##### Tasks Completed:

    * Created a `requirements.txt` for environment tracking.
    * Learned Flask basics: HTTP flow, routing, `render_template()`, and template inheritance.
    * Fixed folder naming (`templates/` instead of `template/`).
    * Implemented core routes:

    * `/` → renders `base.html`
    * `/about` → renders `about.html`
    * `/contact` → renders `contact.html` with variable data
    * Added navigation links using `url_for()` and tested template inheritance.
    * Added a basic CSS test via `/static/css/style.css` (background = aqua).

   ##### Learnings & Insights:

    * Flask automatically searches for templates inside `/templates`.
    * Using `url_for()` avoids broken links when routes change.
    * Template inheritance (`{% extends %}` and `{% block %}`) keeps design consistent.
    * Development in `debug=True` helps rapid iteration.

   ##### Next Goals:

    * Create `base.html` layout with `{% block title %}` and a structured header/footer.
    * Add signup form and connect it to a SQLite database (Day 3).
    * Refine static file linking using `url_for('static', filename=...)`.



### Day 3: Signup page and (db + form integration)
    + Created two additional files - models.py and setup_db.py
    + in the app.py file, instance file created, db connected/configured and database was created (using create_all() function)
    + First only created teh setup_db.py file, which would define a db variable using SQLAlchemy and defines a class named User (defines the structure of db) and the CRUD help functions
    + But this introduced a cycle of calls between the two files giving error
    + So created an additional file named models.py which would define db and database structure
    + These were imported to the setup_db file and it's CRUD function was imported to the app.py file

    + It created instances folder, in which is database.db file (that is the actual db)
    + There is a form in the html, when filled with details, you can register new users
        work flow is like: base page or /add_user page -> add_user fn (in setup_db.py) 
                        -> (user added) and show_users page load -> showing all the users and detsails in db
    
    + Needs modification ------------
    


| Day 3     | Database & Models   | Add User model, initialize database.db, verify via sqlitebrowser  |
| Day 4     | Signup Page        | Create form, hash password, insert user in DB                    |
| Day 5     | Login Page         | Authenticate user, manage session via Flask-Login                |
| Day 6     | Logout & Basic Navigation | Add logout route + redirect + navbar linking                  |
| Day 7     | Polish + Push + Docs | CSS cleanup, error messages, commit + push + write README.md summary |
