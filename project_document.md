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



    

| Day 2     | Flask Project Skeleton | Set up app.py, /templates, /static, and verify Hello World works |
| Day 3     | Database & Models   | Add User model, initialize database.db, verify via sqlitebrowser  |
| Day 4     | Signup Page        | Create form, hash password, insert user in DB                    |
| Day 5     | Login Page         | Authenticate user, manage session via Flask-Login                |
| Day 6     | Logout & Basic Navigation | Add logout route + redirect + navbar linking                  |
| Day 7     | Polish + Push + Docs | CSS cleanup, error messages, commit + push + write README.md summary |
