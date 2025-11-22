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




## Week 2

### Day 8: Architechture Improvements

Did some modifications in the code flow architechture.

Now the flow is:
1. app.py runs:
    allocation application (initiates it)
    app.config.from_object(Config) -> imports:
        SECRET_KEY, DB location, (global settings) etc
    initiates db & login_manager (models & authentication connected to app and activated)
    Register the blueprints
    Only on first run, create the db

    ----- All objects binded to the App
2. Listens to app.run() and creates development WSGI server
        * Running on http://127.0.0.1:5000/
3. In WSGI server, if it receives a http request (like /login)
    Flask generate a `request context` and calls that 


---> More modifications made in the architechture:
+ Direct blueprint & db initiation moved to `factory_helpers.py` file and calls it inside the app.py (so removed the direct initiation)
+ The above step helps to minimalise the `app.py` file
+ Set the secret key more securely
+ Add other minor architechture modifications
+ Modified the imports according to this re-structuring. 

--- These imporves the structure to production ready & scalable ---



### Day 9: Adding CSRF Token (for Security)

Day 9 focused on converting the login/signup system into a **production-grade, secure authentication flow** using Flask-WTF.
This added **form validation**, **password complexity rules**, **CSRF protection**, and overall improved the security foundation of the app.

---

#### **Files Added / Modified**

#### **🔹 Added**

* `blueprints/auth/forms.py`

  * Contains `SignupForm`, `LoginForm`, `EditProfileForm`
  * Added password validators, email validators, and custom password complexity rule
  * Central location for all authentication-related forms

#### **🔹 Modified**

* `blueprints/auth/routes.py`

  * Replaced manual request handling with FlaskForm processing
  * Switched `validate_on_submit()`
  * Added CSRF token validation
  * Added safe URL checking for redirects
  * Improved error handling & removed redirect-after-error behavior

* `signup.html` and `login.html`

  * Integrated `{{ form.hidden_tag() }}` to include CSRF token
  * Replaced `<input>` fields with WTForms rendering
  * Added error message blocks
  * Adjusted structure to support server-side validation feedback

* `extensions.py`

  * Added:

    ```python
    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect()
    ```
  * Integrated CSRF into `register_extensions()`

* `app.py` / `config.py`

  * Verified SECRET_KEY works correctly
  * Ensured CSRF loads before blueprints

---

#### **What Was Achieved**

* ✔ Full CSRF protection for all auth forms
* ✔ Clean, maintainable form classes
* ✔ Email-based login stable and secure
* ✔ Password complexity enforced
* ✔ Prevention of unsafe redirects using `is_safe_url()`
* ✔ Server-side validation implemented properly
* ✔ Duplicate email handling improved
* ✔ Successful account creation logs user in immediately
* ✔ Better error display after invalid form submissions

---

#### **Issues Faced & How They Were Solved**

#### **1️⃣ CSRF token missing (BIG issue)**

**Problem:** Login POST requests failed with *“Bad Request: CSRF Token missing”*.
**Cause:** `{{ form.hidden_tag() }}` was added in signup.html but **not** in login.html.
**Fix:** Added CSRF token to login.html → issue resolved.

---

#### **2️⃣ Error messages not showing inside fields**

**Problem:** Some Bootstrap validation icons overlapped toggle buttons and hid errors.
**Cause:** HTML + Bootstrap validation conflicting with our custom password UI.
**Fix:** Moved inline error messages below input groups.
**Future:** Fix UI/UX in Week 3.

---

#### **3️⃣ Password visibility toggle hidden during typing**

**Cause:** Bootstrap “valid/invalid” icon overlays the right side.
**Fix:** CSS/UI refinement postponed.

---

#### **4️⃣ Remember-me cookie behavior confusing**

**Explanation:** Browsers may persist session cookies even if “remember me” is unchecked.
**Conclusion:** Not a bug — cookie/session behavior will be fine-tuned in Week 3.

---

#### **Things to Improve Later (But Not Now)**

* Live client-side validation (JS) for email + password
* Better form error animations / UX
* Fix input-icon collision with Bootstrap validation icons
* Add friendly 400/401/403 error pages
* Add custom password-strength meter
* Add "terms and conditions" modal
* Improve safe redirect flow

---




### Day 10: 
“Profile System + Login Protection + Sessions + Dashboard logic”

You will:

Implement real login_required handling and redirect behavior

Add last login time, account metadata

Add a profile table integration

Add ‘Edit Profile’ form groundwork

Fix caching logic for protected pages

Add routing protections (anonymous access redirects)

This prepares the system for:

profile editing

user dashboard data

later features like friend requests, discovery, privacy settings



* On signup, we need to add the empty fields for the profile fields , like:
username & email(already added in the table named 'user')
bio, profile pic, dept, year, interests, location. (These would be addeed in the table named 'profile' - user identified by user_id)
connections (in the 'connection' table - identified by user_id field)

* Later whenever the user adds it, this empty locations would be filled
* When the user tries to edit the already existing value, they shoudl be edited in the respective tables. 


So the actual steps to take:
1. In stepup_db when add_user triggered, we would allocate the space for these fields in respective db tables (profile and connection)
2. When edit_profile (i don't think it is yet defined) is triggered, the respective page loads (need to create it), the fields can be edited (but all those will have sanity check). 
Once click save button, respective fields will be saved and updated in the db (i don't know if for updating, we need to implement Migrate() first, or we can simply edit it)
* Note: First these fields would be empty (since the user has never added/initiated it, (but internallly the fields was already allocated; if that is the best practice)) and the first time user adds these details, would be the first time we are editing it (but making the user think that they are adding it, but actually they are replacing the already allocated empty space with data!). And so on. 
 

------------------------------
1. Added columns in the table (`models.py`):
* `user` - created_at and last_login
* `profile` - location, visibility, updated_at
* `connection` - id, user_id, target_user_id, status, created_at
    Also added __table_args__ segment for uniqueness


2. Added Migrate() in the extensions.py file
Initialised it by the following commands (conda terminal):

from project root
>> python -m flask --app "app:create_app()" db init
>> python -m flask --app "app:create_app()" db migrate -m "Add Profile & Connection updates"
>> python -m flask --app "app:create_app()" db upgrade
(This creates the new columns)

-------- For wiping db totally and re-initalising -------
* Delete database.db
* Delete migrations/
* Run the following command:
>> python -c "from app import create_app; app=create_app(); \
>> from extensions import db; \
>> with app.app_context(): db.create_all(); print('DB created')"
(create fresh new db)


3. Added `to_ist()` function {to convert ust timestamp to ist} and `configure_logging()` fucntion {for loging in details to .log files} in the `factory_helpers.py` file
* Now creating new user notes the created_time
* Loggin in updates the last_login time in the `db`
* timestamp storing is in ust and later show it in ist in output

4. Added `EditProfileForm` in the `auth/forms.py` file
5. Update `auth/routes.py` file:
* Added the `save_profile_picture()`
* Added `profile_edit()` segment with robust handling

6. Modified `auth/profile.html` to show the profile details from the table `profile`

7. Added `auth/profile_edit.html` file which shows the fields for editing (uses form.hidden_tag()) (but need more editing with ui) 
* Also the username is not loading in the field

8. Added `UPLOAD_FOLDER` values in the `config.py` file and added it in the `.gitignore`
9. Since __table_args__ are already added, run the following commands:
> python -m flask --app "app:create_app()" db migrate -m "Add unique constraint and index to Connection"
> python -m flask --app "app:create_app()" db upgrade
(First command create migrate script accoding to db modificaiton (use the create_app) and the second command applies those changes)
