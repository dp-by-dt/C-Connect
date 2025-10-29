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


| Day       | Focus              | Deliverables                                                      |
|-----------|--------------------|------------------------------------------------------------------|
| Day 1     | (Today) Environment Setup | Install Miniconda + Git, create Conda env, install Flask + push repo |
| Day 2     | Flask Project Skeleton | Set up app.py, /templates, /static, and verify Hello World works |
| Day 3     | Database & Models   | Add User model, initialize database.db, verify via sqlitebrowser  |
| Day 4     | Signup Page        | Create form, hash password, insert user in DB                    |
| Day 5     | Login Page         | Authenticate user, manage session via Flask-Login                |
| Day 6     | Logout & Basic Navigation | Add logout route + redirect + navbar linking                  |
| Day 7     | Polish + Push + Docs | CSS cleanup, error messages, commit + push + write README.md summary |
