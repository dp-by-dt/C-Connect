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



### Day 3: Database Integration and User Registration
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
    
    + Added .gitignore file
    + Add viewing for the database (added the 'sqlite' extension)
    + now can query on the db using the 'sqlite3 instance/database.db' command on `cmd`

    +The pages are more arranged now.
    + Now have the pages:
        - base (main)
        - about & - contact
        - signup (has the signup form)
        - signup_success (once signup done, show a success msg)
        - /show_users (not page, but for testing purpose)

    ------ New modification ------
    + Added password hashing
    + email uniqueness validation.

    + Implemented  BLUEPRINT structuring
        - It helps to arrange different features of the project in different blueprint folders
        - You can create independent and individual templates and other resources for each blueprint folder. Also there is seperate routes.py file for each
        - Only have to register these blueprints in the main app.py file
    
    Blueprint folder structure (sample):
    C-Connect/
        │
        ├── app.py                      # Main Flask app entry point (or factory function)
        ├── models.py                   # Central place for your database models
        ├── setup_db.py                 # Database setup and initialization
        ├── requirements.txt            # Python dependencies
        │
        ├── blueprints/                 # Containing all blueprints (modular app components)
        │   │
        │   ├── auth/                   # Authentication related routes & logic
        │   │   ├── __init__.py         # Blueprint setup
        │   │   ├── routes.py           # Route handlers (e.g., signup, login)
        │   │   ├── templates/          # Templates specific to auth feature
        │   │   │   └── auth/           # Namespace to avoid template name collisions
        │   │   │       ├── signup.html
        │   │   │       ├── login.html
        │   │   │       └── signup_success.html
        │   │   └── static/             # Static files for auth feature (if any)
        │   │
        │   ├── main/                   # Main/general pages like home, about, contact
        │   │   ├── __init__.py
        │   │   ├── routes.py           # Handlers for home, about, contact routes
        │   │   ├── templates/
        │   │   │   └── main/
        │   │   │       ├── base.html
        │   │   │       ├── about.html
        │   │   │       └── contact.html
        │   │   └── static/             # Static files for main blueprint (e.g., CSS)
        │   │
        │   ├── profile/                # User profile management section
        │   │   ├── __init__.py
        │   │   ├── routes.py           # Profile related routes
        │   │   ├── templates/
        │   │   │   └── profile/
        │   │   │       ├── profile_view.html
        │   │   │       └── edit_profile.html
        │   │   └── static/
        │   │
        │   ├── blog/                   # Blog or post related functionality
        │   │   ├── __init__.py
        │   │   ├── routes.py
        │   │   ├── templates/
        │   │   │   └── blog/
        │   │   │       ├── create_post.html
        │   │   │       ├── view_post.html
        │   │   │       └── edit_post.html
        │   │   └── static/
        │   │
        │   └── admin/                  # Admin panel related features
        │       ├── __init__.py
        │       ├── routes.py
        │       ├── templates/
        │       │   └── admin/
        │       │       ├── dashboard.html
        │       │       └── user_management.html
        │       └── static/
        │
        ├── static/                     # General static files (site-wide stylesheets, images)
        │   └── style.css
        │
        └── instance/                   # Instance folder for runtime files and db
            └── database.db



    
### Day 4: Making Login Page & Interactive
    + Added the login page and dashboard page
    + Now it would, when given a username and passowrd, loads the dashboard of the user (primitive page)
    + But doesn't user the db yet

    + ------- Learned about: -------------
        - POST and GET: these would modify db or take db data (respectively)
        - difference between: `request.args.get()` and `request.form.get()`
          First one takes data from the url. Only small data strings, not secure
          Takes data submitted to a html form. More complex data types possible, more secure
        - Learned the flow of working and requests too
    

    + Changed the strucre of css file from:
        ------------
        ├── static/                     
        │   └── style.css
        ------------
    to the following:
        -------------
        ├── static/ 
        |   └── css/                    # seems more best practice / conventional way
        │       └── style.css
        ----------------

    + 



| Day 4     | Signup Page        | Create form, hash password, insert user in DB                    |
| Day 5     | Login Page         | Authenticate user, manage session via Flask-Login                |
| Day 6     | Logout & Basic Navigation | Add logout route + redirect + navbar linking                  |
| Day 7     | Polish + Push + Docs | CSS cleanup, error messages, commit + push + write README.md summary |
