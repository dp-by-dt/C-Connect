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




### Day 10: Profile Editing

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
* RotatingFileHandler() enabled 

4. Added `EditProfileForm` in the `auth/forms.py` file
5. Update `auth/routes.py` file:
* Added the `save_profile_picture()`
* Added `profile_edit()` segment with robust handling

6. Modified `auth/profile.html` to show the profile details from the table `profile`

7. Added `auth/profile_edit.html` file which shows the fields for editing (uses form.hidden_tag()) (but need more editing with ui) 
* Also the username is not loading in the field -- Solved by preloading all the data in the form (in `routes.py's` `profile_edit()` function) in the request.method == 'GET'

8. Added `UPLOAD_FOLDER` values in the `config.py` file and added it in the `.gitignore`
9. Since __table_args__ are already added, run the following commands:
> python -m flask --app "app:create_app()" db migrate -m "Add unique constraint and index to Connection"
> python -m flask --app "app:create_app()" db upgrade
(First command create migrate script accoding to db modificaiton (use the create_app) and the second command applies those changes)

10. Wired `Change Photo` button to profile/edit method



### Day 11: Connections and Profile Views


1. Added a new blueprint named `connections`, added it's route and init files and also in templates/connections added the file `list.html`
2. Added the content of these files routes.py and service.py (take care of the connection diffrent cases)
* registerd the blueprint in `factory_helpers.py`
3. Added list.html in connections blueprint
* but not yet connected it to routes

4. In `routes.py` added a segement `conn` defining if there is duplicate connections or connection at all, which passed to the profile page
In `profile.html` if the profile is theirs, show edit profile
else: according to conn value give an appropriate status. --------- !!! But this logic is wrong !!!

* The /profile shows own profile while /user/<id> show other other person's profile
Only in the latter we need to add the `conn`, not in /profile call. 

5. Added new route `/user/<id>` in the `main/routes.py`
* Also created a new file `main/user_profile.html` to show other user's profile
6. Added connection_list route to `connections/routes.py` (but the rendering is blank) --- It was a silly mistake: forgot to use `block body`, now it is perfect
* But after accepting the request, the end point is broken (but db is updated) -- This was due to not defining connections_disconnect, now updated with connections_list


7. Minor bug fixes to show the connected user's profile (but not fully developed profile, just the name)
8. Added link in the name in `discover.html` to each user's name to view their profile. 

9. Now shows the connection numbers in dashboard, as added a new `status` which determines the counts of accepted, pending and outgoing connections in the `main/routes.py` in `dashboard()`

10. For disconnecting an accepted conection:
* added disconnect_connection() in `service.py`
* conections_disconnect() in `connections/route.py`
* confirmation with `onsubmit` on `list.html` to give confirmation before disconnecting

11. Added link card in the dashboard to show the connection_list
  
* Did the manual testing and all seems to be working. 




### Day 12: Building Notification & UI/UX upgrade


1. Added `Notification()` model in `models.py`
It has:
    - id
    - user_id
    - sender_id
    - message
    - is_read
    - created_at
And migrate with commands:
> flask db migrate -m "Add Notification model"
> flask db upgrade


2. Created the blueprint `notifications` and added the file `notifications/notif_list.html`
Current structure:
    blueprints/
        notifications/
            __init__.py
            routes.py
            service.py
            templates/notifications/
                notif_list.html

3. Modified `blueprint/connections/routes.py` file to sent respective notification using the `create_nofication()` function from `blueprints/notifications/service.py` file

model: (done for request, accept, reject, cancelled, disconnected)
        create_notification(
            user_id=other_user_id,
            sender_id=current_user.id,
            message=f"{current_user.username} removed you from their connections"
        )

4. Created the `notifications/routes.py` file
* Also added the ui with the file `templates/notifications/notif_list.html`

5. In `base.html` template, added the notification to the nav bar (but not properly wired to the notifications list) --- Because the `conn` was not defined in the `connections/routes.py` which is now modified and corrected

6. Registered the blueprint (forgot earlier) in `factory_helpers.py`

7. But now, the notif_list.html file is not loading. Notfication icon on the nav bar redirects to the home page. -- Solved by correcting the route to proper `/notifications_list` route

8. The disconnect_connections were giving error since the it was supposed to give 3 outputs. So added that. 
Now all seems working. Needs testing.

* There was a duplicate `/connections` url route in the `connectoins/routes.py`, both same content by the function name is like `connections_list` and `connections_home`. Now only using the `connections_home`. Modified that too in the `dashboard.html`

9. In the `notifications/routes.py` file added the option to mark it as read once the user opens it (not just on clicking on 'mark as read')

10. Added to_ist() in the initiation in the create_app() function while defining the FlaskApp()
This shows the ist time of the notification creation.
*Testings also done (can do a thorough checking later)

11. Notifications will only be marked as read:
* When the user views it and clicks back
* Or user clicks mark all as read
(This is done by adding `mark_all_read` function in `notifications/routes.py` file and conencting it with a button in html. Also added a script `addEventListner` at the end of the html to mark the notifications as read automatically once the user goes back the page).

12. Added auto deleting old notifications (older than 24 hours)
* notification cleaning func added to `notifications/service.py`
* triggering the function per day is added to `factory_helpers.py`
* registered the trigger function inside the `create_app()`




=================== UI UPGRADE (Corrections Needed) ===============

1. The slow loading (animation) should be removed. it is annoying
2. remember me box not visible clearly
3. In signup page:
    usename error not showing as text
    email validation not done(only shown after submitting)
    password strength check is not proper and error not shown (only shown after submitting)
4. In login page:
    email validation check not done, and error not shown (only shown after submitting)
    password strength not proper, no error shown
    The placeholders like the "Username", "Email" etc. are now having a white background while in dark mode. It is quite annoying. It was to blend with the surroundings, but yet legibly visible. 
    The view password button in the "password" section is not aligned in the middle, but a little towards bottom    
5. Messages block in dashboard link to messages page
6. No one's profile showing in discover (just the letter first)
7. For connected users too, the connection section showing 'Connect' option (not adapted)
8. After request sent, re-loads to page top, not stay there and update the card. 
9. Profile image not showing in the nav bar circle.
10. The text on the flash message gets overlapped with the cross symbol in the flash message (a little bit)
11. The left to right running kind of animation in the card which says "ready to build your campus network" is a little annoying. Remove it and add such to the following "Get Started" button, but just keep it subtle (like those in the google pages)
12. All the confirmation kind of boxes (like the logout confirmation) are now not styled. We might want to style it (now or later). 
13. Instead of writing "Get Started Free", just write "Get Started" (remove such free from else where too)
14. When clicking accept/reject to a connection, the page seems reloading, instead of updating the current state. That is annoying
15. On user profile, there shoudl be an option to connect to them or disconnect them
16. In the connections page, if a block is empyt, i.e., like Incoming requests, outgoing requests etc, then they should be collapsed with the simple button on their side, so that it don't interfere with other sections much

17. Dark mode is totally messy:
    Each time another page loads, it load in light mode for a fraction of second and then only goes to dark mode (totally annoying)
    Some texts and options are not clear properly. Especially all the text we type on any input box (like the login, search option etc.)
    The text on flash message is not visible in dark mode

18. Errors: (✅ All Solved)
    Edit profile: `profile` not defined (✅corrected)
    Cancalling request: not enough values to unpack (expected 3, got 2) - but get's cancelled later (✅corrected)



------------------
TOTAL UPGRADE FOR THE UI/UX IS REQUIRED

Reshape the UI/UX totally, BUT DO NOT BREAK ANYTHING IN THE BACKEND SIDE.
Keep on the corrections for the above points too. 
Keep in mind that, that would be a mobile first responsive application. And this is not a website or something, but an appication like the instagram or linkedIn. So keep that in mind while editing. 
And this should be very much nuanced and creative, for college students. So we need to keep the top cutting edge style of designing. I prefer minimal and sleek kind of design. This one feels like a little bit robotic or ai like.
I have provided below some other themes which i liked for different segments. You can take them as reference and adapt from there. 
Remember that no need to resemble any of this just keep the style for your reference. 


----------------
Updates are corrections done
* patched up the end point errors in : `edit profile` & `cancel request`
* added ajax in the global js, for updating connection number instantly






### Day 13: Robustness

------ Prelim modifications and checkups -------
1. Added `.env` file for secrets and loads it to the `config.py` file
2. Input sanitization for long text fields using bleach() - bio, interest
3. Added `limiter` function in `extension.py` and initiated it in th`factory_helper.py`
   - Added these limits to: login, profile, sending connection
   - Added /ping for exempt health cheks
   - Limited connection request to same target 3 times in an day and one person can only send max 25 requests per hour (in `connections/routes.py`)

4. Added Content Security Policy (CSP) as 'set_secure_headers()' in `factory_helpers.py` and registered it in `app.py`
5. Added `templates/components/flash.html` for flash messages in signup pages
6. Added content policy was blocking some css styles. Now corrected it.

7. `static/favicon.ico` added (for showing the symbol)
8. Error: (✅Fixed)
    - Once the login or signup button is clicked, it stays loading... not resets (✅corrected) - It was the problem with the script section added at the end of `base.html` file. Now that section is removed
9. 95% opacity given to .alert in `global.css`



 ---------- Modifications --------
10. Added ProfileVisit() model in `models.py`
11. Added this section in `main/routes.py` file so that when any user visits another profile, it gets recorded in the new table `profile_visit`. But it spams the db (triggers even when page refreshed)


12. No refresh spamming in the profile_visit db table now. Added a time threshold (30 min) validation 
    - Use `datetime.now(timezone.utc)` instead of `datetime.utcnow()`
13. Initialised this automatic clearing in `create_app()` in `app.py`. Now clears profile_visits older than 7 days, this deletion check runs every hour. And logs in when it deletes.
14. Implemented offset pagination for the discovery page in it's `routes.py`. Users' card were sorted as per their last activity timing
15. Added next and previous page guiding buttons (primitive ui)
16. Problems with pagination nav:
    - page query greater than total pages was allowed (but showed blank) - like `discover?page=100` (✅fixed)
    - Inactive users were not shown in the discover page (✅fixed- by using `case()` and `outerjoin()`)


17. Added the mechanism for `/search` a user using backend searching - For that added `main/search.html` file and it uses `search.py` instead of `routes.py`
    *Problems* :
    * Search algo needs to be modified
    * No option to access this searching (except by url)
    * `/api/search` end point is open (seems)
    * Search result card not working (the connect button). 
    * Shows own profile, Some users view profile on here is breaks into an opening
18. Added search section in the nav (primitive UI)


19. Made the cards in discover clickable
    Made their buttons dynamic (but ui primitive styles)

20. Tried to make the profile pic viewable in the cards. But couldn't (✅working now)
21. Made a common section for user_cards in the templates/ folder in the root
22. Now test the ajax searching feature on the /search page (later replace /discover page with this code)

23. Building on /search page (towards /discover page)
    - Modified `search.html` page to return the search results and imporved the logic in `search.py`
    - Logic improved in `renderConnectionButton()` in `main_script.js`
    - The cards were not visible (but clickable)... So fixed by putting `animate-on-scroll:opacity` to 90%
    - 

+ Need modifications:
    - When page loads in dark theme there happens a white theme flicker (maybe style loading delay)
    - In the flash messages, the close button overlaps with the text (allocate different divs or sections)
    - The ui search doesn't work across the other pages in pagination in discover
    - in profile_edit page, the profile pic not loading (⚠️Seems fixed: Try after correcting the pic urls on the db)
    - User image loading in the pages discover, profile_edit, view_profiles (✅Fixed: by removing the usage of absolute path while saving the profile pic, from edit profile)
    - The /search feature is not working properly on one or two letters searched


=========‼️Problem that troubled for 3 days!:===========
⚠️The infinite scroll was not ending and trying unwanted loading and causing console error
    
✅Later found it was db table inconsistency
- The first users in the `User` table was not in the `Profile` table
- After deleting them using `flask shell` on the vs code cmd, the problem persist
- Later also found that the problem was with interests column in the `Profile` table
    There were some `str` interests and some `JSON`
    This was breaking as JSONdata error
✅ Solved it by repalcing the `str` value with proper `JSON` values
    Now the cards in the `/search` page loads without any glitch or console error
=========================================================


* Further more, the `main_script.js` in the `main` blueprint was not loading. ✅fixed it by adding `static_url_path='/main/static'` in the `__init__.py` file of it
* The same is added for the other blueprints too. (HAVEN'T ADDED FOR OTHER FILES EXCEPT `AUTH`)
So from here, the loading of different files can be done as below:
+ For root global.js: <script src="{{ url_for('static', filename='js/global.js') }}"></script>
+ For blueprint's auth_script.js: <script src="{{ url_for('auth.static', filename='js/auth_script.js') }}"></script>


* when the db was cleaned to correct the inconsistency, some of the already conneected users were deleted. This caused error in the `/connections` page
✅ This was handled by using the if condition to check if the user exists before fetching their detials

* Deleted the section of searching and dashboard from the `main_script.js` file (because it was clashing with the current search mechanism)
+ replaced the route `discover` with `search`






--------------------------------      SECOND WEEK (KIND OF) COMPLETED -----------------------------------




## Week 3
Now instead of days we are going for features

### Feature 1: Posting 


* FOLDER STRUCTURE
🖥️ d:\C-Connect
📂 C-Connect
├── 📂 blueprints/
│   ├── 📂 auth/
│   │   ├── 📂 static/
│   │   │   ├── 📂 css/
│   │   │   │   └── 📄 auth_style.css
│   │   │   └── 📂 js/
│   │   │       └── 📄 auth_script.js
│   │   ├── 📂 templates/
│   │   │   └── 📂 auth/
│   │   │       ├── 📄 login.html
│   │   │       ├── 📄 profile.html
│   │   │       ├── 📄 profile_edit.html
│   │   │       └── 📄 signup.html
│   │   ├── 📄 __init__.py
│   │   ├── 📄 forms.py
│   │   └── 📄 routes.py
│   ├── 📂 connections/
│   │   ├── 📂 templates/
│   │   │   └── 📂 connections/
│   │   │       └── 📄 list.html
│   │   ├── 📄 __init__.py
│   │   ├── 📄 routes.py
│   │   └── 📄 service.py
│   ├── 📂 main/
│   │   ├── 📂 static/
│   │   │   ├── 📂 css/
│   │   │   │   └── 📄 main_style.css
│   │   │   └── 📂 js/
│   │   │       └── 📄 main_script.js
│   │   ├── 📂 templates/
│   │   │   └── 📂 main/
│   │   │       ├── 📄 about.html
│   │   │       ├── 📄 contact.html
│   │   │       ├── 📄 dashboard.html
│   │   │       ├── 📄 discover.html
│   │   │       ├── 📄 home.html
│   │   │       ├── 📄 messages.html
│   │   │       ├── 📄 search.html
│   │   │       ├── 📄 settings.html
│   │   │       └── 📄 user_profile.html
│   │   ├── 📄 __init__.py
│   │   ├── 📄 routes.py
│   │   └── 📄 search.py
│   ├── 📂 notifications/
│   │   ├── 📂 templates/
│   │   │   └── 📂 notifications/
│   │   │       └── 📄 notif_list.html
│   │   ├── 📄 __init__.py
│   │   ├── 📄 routes.py
│   │   └── 📄 service.py
│   └── 📂 posts/
│       ├── 📂 templates/
│       │   └── 📂 posts/
│       │       └── 📄 feed.html
│       ├── 📄 __init__.py
│       └── 📄 routes.py
├── 📂 logs/
│   └── 📄 cconnect.log
├── 📂 migrations/
├── 📂 services/
│   └── 📄 recommend.py
├── 📂 static/
│   ├── 📂 css/
│   │   └── 📄 global.css
│   ├── 📂 images/
│   │   └── 📄 avatar-placeholder.jpg
│   ├── 📂 js/
│   │   └── 📄 global.js
│   └── 📄 favicon.ico
├── 📂 templates/
│   └── 📂 components/
│       ├── 📄 flash.html
│       ├── 📄 user_card.html
│       └── 📄 user_card_action_btn.html
│   └── 📄 base.html
├── 📂 testing_old/
│   ├── 📄 db_testing.sql
│   └── 📄 logic_testing.ipynb
├── 📂 tests/
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py
│   ├── 📄 routes.py
│   ├── 📄 test_db.py
│   └── 📄 test_search_and_conn.py
├── 📄 .gitignore
├── 📄 app.py
├── 📄 config.py
├── 📄 css_cheatsheet.md
├── 📄 extensions.py
├── 📄 factory_helpers.py
├── 📄 models.py
├── 📄 project_document.md
├── 📄 removed.py
├── 📄 requirements.txt
├── 📄 seed.py
└── 📄 setup_db.py


+ Added `Post` and `PostLike` classes in the `models.py` file
    (db migration pending)
+ New blueprint named `posts` is created
+ Created __init__.py file for the new `posts` blueprint
    blueprint registered as `posts_bp`
    (url_prefix added for this one)
+ Added entry point to `/feed` in the dashboard
+ Added csrf token for `feed.html` file
+ addd `url_prefix` for the posts

+ Profile shows on other's respective profile page (plus like count and time)
    adding a return value of post from db in the `user_profile` route
    returning that back to the `user_profile.html` and displaying

+ Notification of likes for the posts 
    - Added to the `toggle_like` in the `routes.py` file, if liked, sends a nofication and adds to the db
+ Own post deletion added
    - A button to delete own posts (asks confirmation) and deletes and give flash message
    - Does by the route `delete_post()`

+ Added the section for `type` and `ref_id` columns for the notification table
    eg: type = 'connection_request' or 'post_like'
        ref_id = connection.id or post_likes.id
For this, deleted the notification table from the db
    # Run this on cmd to open sqlite:
    sqlite3 instance/database.db
    DROP TABLE notification;
    .quit

    flask db stamp head
    flask db migrate -m "add notifications type ref_id"
    flask db upgrade

The above two columns helps pin point the notification and delete that only

+ modified the `/search` page to load the cards with correct connection status (requested, incoming or connected)


- like count doesn't update (✅fixed by adding the relation to the models.py)
- The time is not in ist (✅set to ist using `to_ist()` function )
- The page was going blank once i go back to `/search` page after visiting a profile (✅fixed by correcting `beforeunload` JS function)






### Feature 2: Messaging


+ Added `Message` class in the `model.py` for one-to-one chatting
+ New `messages` blueprint added
    - Added helper function `cleanup_expired_messages` for clearing expired messages
    - __init__.py file added
    - added routes `inbox` and `chat` and their html files
    - registered the blueprint in `factory_helpers`
    - Added entry point

+ The messages page loads connected users
    filter with accepted/connected/pending
+ It also shows incoming requests and option to connect and chat or reject (need test with db)
    uses csrf token





❌Prblems/Bugs-------------------
1. Some projects with `/search` page cards' connection status ==== Need thorough testing
    when the user sends a request A to B, and when B looks on the card, the option is just showing Connect, not to accept (in the search page). Like that two connections (A to B, and B to A exist at same time: race condition)
2. Test rate limits
3. Do test for deleted users (connection with deleted user, notfications etc)







-----------------
Later modifications
1. add 400.html and 500.html error pages
2. Add `No result` in the `/search` page
3. Make the hover size of the `/search` page cards more subtle
4. Posts:
    - Photo/video posting
    - AJAX usage (updates likes without reloading)
5. Delete accoutn feature
6. Refractoring models into seperate files (optional, but cleaner)
7. Caching (optional but recommended)



-------
Later features 
1. forget password
1. Delete uploaded images (user profile) if it is not the one currently used by the user (saves space, if that is a thing!)
3. Stories
4. Games
5. Polls
6. Campus events
7. Anonymous confessions
