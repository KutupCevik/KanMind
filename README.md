# 📘 KanMind API  
A collaborative Kanban-based task management API built with Django REST Framework.  
This project provides endpoints for authentication, board management, tasks, comments, and user utilities.

## 📂 Project Structure
```
core/
│── settings.py
│── urls.py
│
auth_app/
│── api/
│   │── serializers.py
│   │── views.py
│   │── urls.py
│
kanban_app/
│── api/
│   │── serializers/
│   │   │── board.py
│   │   │── task.py
│   │   │── comment.py
│   │── views/
│   │   │── board.py
│   │   │── task.py
│   │   │── comment.py
│   │── permissions.py
│   │── urls.py
│
.env               ← private file (ignored by Git)
.env.template      ← public template (committed)
requirements.txt
README.md
```

## 🚀 Installation
Follow the steps below to clone and run **KanMind** on your local machine.  
Both **Windows** and **macOS** installation instructions are included.

---
#💻 Windows Setup

```bash
# 1. Clone the repository
git clone https://github.com/KutupCevik/KanMind.git
cd KanMind

# 2. Create a virtual environment
python -m venv env

# 3. Activate the virtual environment
# If it does not work directly, open a new Command Prompt (cmd),
# navigate back into the project folder, then run:
"env\Scripts\activate"

# 4. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5. Create a .env file
# Copy the provided .env.template and rename it to .env
# Then generate your own SECRET_KEY using the command below

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Copy the printed key into your .env file, like this:
# SECRET_KEY=django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Example .env
# ------------------------------------
# SECRET_KEY=your-generated-key
# DEBUG=True
# ALLOWED_HOSTS=127.0.0.1,localhost
# CORS_ALLOWED_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
# DATABASE_NAME=db.sqlite3
# ------------------------------------

# 6. Apply migrations
python manage.py migrate

# 7. (Optional) Create an admin user
python manage.py createsuperuser

# 8. Run the development server
python manage.py runserver

# 9. Open the app in your browser
# → http://127.0.0.1:8000/
```
```bash
# Optional: Clean up cached files
# If you see __pycache__ folders marked for commit in VS Code,
# remove them from Git tracking and reapply .gitignore:

git rm -r --cached .
git add .
git commit -m "Remove cached files and apply .gitignore"
```

# 🍎 macOS Setup

```bash
# 1. Clone the repository
git clone https://github.com/KutupCevik/KanMind.git
cd KanMind

# 2. Create and activate a virtual environment
python3 -m venv env
source env/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create a .env file
# Copy the .env.template file and rename it to .env
# Then generate a new SECRET_KEY using the command below

python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Paste the key into your .env file:
# SECRET_KEY=django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Example .env
# ------------------------------------
# SECRET_KEY=your-generated-key
# DEBUG=True
# ALLOWED_HOSTS=127.0.0.1,localhost
# CORS_ALLOWED_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
# DATABASE_NAME=db.sqlite3
# ------------------------------------

# 5. Apply migrations
python3 manage.py migrate

# 6. (Optional) Create an admin user
python3 manage.py createsuperuser

# 7. Run the development server
python3 manage.py runserver

# 8. Open the app in your browser
# → http://127.0.0.1:8000/
```
```bash
# Optional: Clean up cached files
# If you see __pycache__ folders marked for commit in VS Code,
# remove them from Git tracking and reapply .gitignore:

git rm -r --cached .
git add .
git commit -m "Remove cached files and apply .gitignore"
```

# ⚙️ Notes

Make sure Python ≥ 3.10 and Git are installed.

Your .env file must include all environment variables such as:

SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost


Stop the server anytime with:

Windows: Ctrl + C

macOS: Cmd + C

## 🔐 Authentication
Token Authentication is used for all endpoints except registration and login.

| Method | Endpoint | Description |
|--------|-----------|--------------|
| POST | /api/registration/ | Register a new user |
| POST | /api/login/ | Login and receive Token |

Include in headers:
```
Authorization: Token <your_token>
```

## 🧩 Boards
| Method | Endpoint | Description | Permission |
|--------|-----------|-------------|-------------|
| GET | /api/boards/ | List all boards (owned or joined) | Authenticated |
| POST | /api/boards/ | Create a new board | Authenticated |
| GET | /api/boards/{board_id}/ | Get board details with members and tasks | Owner or Member |
| PATCH | /api/boards/{board_id}/ | Update title and members | Owner or Member |
| DELETE | /api/boards/{board_id}/ | Delete a board | Owner only |

## 🧠 Tasks
| Method | Endpoint | Description | Permission |
|--------|-----------|-------------|-------------|
| POST | /api/tasks/ | Create a new task within a board | Board Member |
| PATCH | /api/tasks/{task_id}/ | Update task fields | Board Member |
| DELETE | /api/tasks/{task_id}/ | Delete task | Task Creator or Board Owner |
| GET | /api/tasks/assigned-to-me/ | List tasks assigned to current user | Authenticated |
| GET | /api/tasks/reviewing/ | List tasks where current user is reviewer | Authenticated |

## 💬 Comments
| Method | Endpoint | Description | Permission |
|--------|-----------|-------------|-------------|
| GET | /api/tasks/{task_id}/comments/ | List all comments for a task | Board Member |
| POST | /api/tasks/{task_id}/comments/ | Add a new comment to a task | Board Member |
| DELETE | /api/tasks/{task_id}/comments/{comment_id}/ | Delete a comment | Comment Author |

## 🧾 Utility
| Method | Endpoint | Description | Permission |
|--------|-----------|-------------|-------------|
| GET | /api/email-check/?email=example@mail.de | Verify if an email exists | Authenticated |

## ✅ Permissions Overview
| Permission Class | Description |
|------------------|-------------|
| IsBoardMemberOrOwner | Access if user is board owner or member |
| IsBoardOwner | Access if user is board owner only |
| IsTaskCreatorOrBoardOwner | Access if user created the task or owns the board |
| IsCommentAuthor | Access if user wrote the comment |

## ⚙️ Development Notes
Code follows PEP8 and Django REST best practices.  
Default permissions and authentication are globally configured in `core/settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```