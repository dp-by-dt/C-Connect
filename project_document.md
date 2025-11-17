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

    + It can use db now. The flow is as follows:
        - The login.html page has form -> When data is entered it loads the database values as a dictionary -> Check there if the user exist (else error msg) and if yes, check if the password math -> If matches, redirects to profile dashboard and passes the username for the greeting (If any error occurs, it would give a flash error message)
    + Hashed password check is not implemented. But the flow works.
    + need to make it more secure too, and also do with best practices for the flow

    + added a logout button, also a will clean the session if the session state is not logged in



    + Enhanced the Flask app by adding user interactivity through form handling.
    + Implemented `login`, `dashboard`, and `logout` routes under the `auth` blueprint.
    + Connected login functionality with the database for credential validation.
    + Learned about Flask `POST` methods, blueprints, and route redirection.
    + Created separate templates for login and dashboard pages.
    + Gained conceptual understanding of user sessions and authentication flow.
    + Next steps: implement password hashing, session-based login persistence, and access control.




### Day 5: Secure Authentication & User Session Management

    + Added the password hashing and checking it
    + Added 'secret_key' too. It is in app.py file and also in config.py
    + deleted old db and created new db with all the passwords hashed
    + Modified the old sqlite3 db handling with new SQLAlchemy method
    + removed unwanted session data and clearing, and use user_id to verify logging status

    + still one can be logged in after refresh or gone back and forth

    + Updated the login mechanism to Flask-Login (which would handle the session cookies automatically, instead of defining manual logic with session mechanism)
    + Still testing is pending to see upto which extend would this work as intended. 
    + Now in the dev tools, once i delete the session cookies and refresh the page, the user is not logged in. 
    + And after logging out from the session would take you out of the profile/dashboard page to the login page, and refresh won't change anything. But one can go back to the logged in page even after that by pressing back. But if refreshed after getting in,the user is indeed out of the dashboard.
    + Later need to look on this further to make it more secure and implement best practices if required. 

    + (The flask-login was implemented by replacing the session mechanism)
    Need to make the secure_key more secure. It seems like there are two secure_keys defined in two different files. (Need to look on that more)
    + Also right now using flash() for messages

    ---- Update -----
    + Found the duplicate secret_key. One was in `app.py` and another in config.py
      Deleted the one in `app.py` and in that file, put `app.config....` command right after Flask app declaration. 
    + Added the following segment:
        `    @app.after_request
             def add_header(response):......`
        This prevents keeping cache after logged out. So no going back in the browser after loggin out allowed. It is applied to only selected sensitive pages only (but list can be extended)
    
    + Added a common system to show the flash msgs (in the base.html). Need to style it later with css

    ---------------------
    + In future need to set the login credential to email, instead of username (more conventional)
    + While signing up: validate:
        Non-empty username/email
        Email format (lightweight check)
        Password minimum length
    



### Day 6: Frontend Foundation & Template Structuring
    + Used Claude AI to produce the front end for the application and also refine the back end a bit to make the usages (of the variables and method names) more conventional

    + Now there is a robust UX with sleek UI (but needs more modifications in the design). right now the design feels more robotic or ai generated like, we need more calm and comforting/rewarding kind of minimal (less clutter) design. But we can take care of that later as right now the working is the main thing.

    + I have tested the new ui codes in a new branch in github and now need to merge that with the main one. (there is one more branch with another ui, but this one only is much better, we are to discard that other branch)

    + Now the cache and cookies of the site is much better and UX oriented. One can set `remember me` option which logging in. The signing up would take to the dashboard. There are lot's of options in the profile too
    + There is option to discover other users, follow them, a section for messages, profile settings option, contact or connect the developer, join a group, set schedule and such thigs. But all these are not connected to the back end point, since they need to be developed further. Now it has only dummy values or place holders. 
    + But this provides a solid base and framework. 

    + The file/folder structure is more developed now with more files included for usability and also used standard naming conventions. 
    The current folder structure is like:

    C-Connect/
        ├── .git/
        ├── blueprints/
        │   ├── auth/
        │   │   ├── static/
        │   │   │   ├── css/
        │   │   │   │   └── auth_style.css
        │   │   │   └── js/
        │   │   │       └── auth_script.js
        │   │   ├── templates/
        │   │   │   └── auth/
        │   │   │       ├── dashboard.html
        │   │   │       ├── login.html
        │   │   │       ├── profile.html
        │   │   │       └── signup.html
        │   │   ├── __init__.py
        │   │   └── routes.py
        │   └── main/
        │       ├── static/
        │       │   ├── css/
        │       │   │   └── main_style.css
        │       │   └── js/
        │       │       └── main_script.js
        │       ├── templates/
        │       │   └── main/
        │       │       ├── about.html
        │       │       ├── contact.html
        │       │       ├── discover.html
        │       │       ├── home.html
        │       │       ├── messages.html
        │       │       └── settings.html
        │       ├── __init__.py
        │       └── routes.py
        ├── static/
        │   ├── css/
        │   │   └── global.css
        │   └── js/
        │       └── global.js
        ├── templates/
        │   └── base.html
        ├── testing_old/
        │   ├── db_testing.sql
        │   └── logic_testing.ipynb
        ├── tests/
        │   ├── __init__.py
        │   ├── conftest.py
        │   └── test_db.py
        ├── .gitignore
        ├── app.py
        ├── config.py
        ├── models.py
        ├── project_document.md
        ├── requirements.txt
        └── setup_db.py


    + still needs to read and understand the code a bit more, but the general working is known. Additionally, now i have a cheatsheet file with the usages of css classes. As file name: `css_cheatsheet.md`

### Day 7: Interactive Dashboard Prototype

    Things already done while using frontend
        - created dashboard.html and discover.html
        - glass, hover, layout effects
        - theme toggle and browser cache
    
    Things to do on this day7 (remaining)
        1. move dashboard.html from ~auth/~ blueprint to ~main/~ blueprint folder (✅done)
        2. add more tables in the database (users:already exist, profiles, connections, visibility, etc.)(✅done)
            defined the classes for the tables *profile* and *connection*
            created the tables in flask shell using `db.create_all()` comment
        3. Populate these tables (✅done)
            Used a seeding python file (`seed.py`) to populate the table
            It adds dummy details for the users in the db
        4. Dynamically fetch the db data and show in the respective pages (discover page) (✅done)
            (The ui, i.e., discover.html already had the feature to load users dynamically from the table)
            Now it shows the user name, and email fetched from the db
            (later we might want to add a logical algo to sort or prioriotize which users we show to the user)
        5. confirmation for logout (done; partially)
            added a script in the base.html which asks confirmation when logout clicked
            But ui refinement needed for the confirmation window (can be added later)
            when use the tail url `/logout`, it is directly logging out, not asking confirmation (can be taken care of later)
        6. visual refinements (optional) - will do later



--------------------------------      FIRST WEEK COMPLETED -----------------------------------

