# Game Player Nick Finder [![stability-wip](https://img.shields.io/badge/stability-wip-lightgrey.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#work-in-progress)

## 🌏 Project Overview
Welcome to the "Game Player Nick Finder" - a unique platform to reconnect with your old online gaming friends deployed at [gpnf.zentala.io](https://gpnf.zentala.io/).

### 🎮 Key Features
- **Search by Nicknames**: Easily find your old gaming friends using their nicknames.
- **User Registration**: Join the community and let others find you.
- **Character Profiles**: Create detailed profiles for your gaming characters with descriptions and timelines.
- **Messaging System**: Communicate directly with your old friends on the platform.
- **Email Notifications**: Stay updated on new friend requests and messages.

## 🛠 Technical Stack Overview

| Category    | Technology                                                                                   |
| :---------- | :------------------------------------------------------------------------------------------- |
| Front-end   | ![Bootstrap](https://img.shields.io/badge/-Bootstrap-563D7C?logo=bootstrap&logoColor=white) &nbsp; ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?logo=css3&logoColor=white) |
| Back-end    | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) &nbsp; ![Django](https://img.shields.io/badge/-Django-092E20?logo=django&logoColor=white) |
| Environment | ![Dotenv](https://img.shields.io/badge/-Dotenv-000000?logo=dotenv&logoColor=white) &nbsp; ![PM2](https://img.shields.io/badge/-PM2-2B037A?logo=pm2&logoColor=white) |
| DBs         | ![SQLite](https://img.shields.io/badge/-SQLite-003B57?logo=sqlite&logoColor=white) |
| Marketing   | ![Google Analytics](https://img.shields.io/badge/-GoogleAnalytics-E37400?logo=googleanalytics&logoColor=white) |
| IDE         | ![VSCode](https://img.shields.io/badge/-Visual%20Studio%20Code-007ACC?logo=visualstudiocode&logoColor=white) |

## Code quality status

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=zentala_game_player_nick_finder&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=zentala_game_player_nick_finder)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=zentala_game_player_nick_finder&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=zentala_game_player_nick_finder)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=zentala_game_player_nick_finder&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=zentala_game_player_nick_finder)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=zentala_game_player_nick_finder&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=game_player_nick_finder) [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=zentala_game_player_nick_finder&metric=bugs)](https://sonarcloud.io/summary/new_code?id=zentala_game_player_nick_finder)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=zentala_game_player_nick_finder&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=zentala_game_player_nick_finder)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=zentala_game_player_nick_finder&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=zentala_game_player_nick_finder) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=zentala_game_player_nick_finder&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=zentala_game_player_nick_finder) [![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=zentala_game_player_nick_finder&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=zentala_game_player_nick_finder)

Detailes App Stack: Python 3.10, Django + DRF, SQLite, Bootstrap 5, Django Templates, Gunicorn, django-allauth, django-crispy-forms, python-dotenv, PM2

## 🤝 Join the Community!

### 👾 ...of Old Forgotten Gaming Friends

Join the "Game Player Nick Finder" platform by registering at [gpnf.zentala.io](https://gpnf.zentala.io/accounts/register/). Fill out your gaming history, the more players join, the greater the chances of reconnecting with old gaming friends. Let's build a thriving community together!

### 🖥️ ...of App Developers Community

Contribute to the "Game Player Nick Finder" project by:
* Starring & Watching this repo to stay updated with the latest features and releases.
* Picking tasks in our [GitHub Project](https://github.com/zentala/game_player_nick_finder/projects).
* Sharing your suggestions and reporting bugs in the [Issues](https://github.com/zentala/game_player_nick_finder/issues) section.

Your input helps us evolve and improve the platform for the benefit of all gamers.

### Installation and Running the Application Locally
Before you proceed, ensure that your system has the following installed:
* Python (version 3.6 or newer)
* pip (Python package management tool):
```bash
sudo apt install python3-pip
```
* pipenv (Python packaging tool for virtual environments):
```bash
sudo apt install pipenv
```
* pyenv (Python version manager):
    * [Installation instruction](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

#### Step 1: Clone the Repository
Clone the repository to your local computer using the following git command:

```bash
git clone https://github.com/zentala/game_player_nick_finder
cd game_player_nick_finder
```

#### Step 2: Setup pipenv
To set up the pipenv environment and install dependencies, run the following command:

```bash
pipenv install
```

This will create a `Pipfile` and `Pipfile.lock` if they don't exist and install all required dependencies.

#### Step 3: Activate pipenv Environment
To activate the pipenv environment, use:

```bash
pipenv shell
```

#### Step 4: Configure the Database
The application uses SQLite as the default database, so there is no need to set up an additional database. You can simply perform the database migration:

```bash
python manage.py migrate sites
python manage.py migrate
```

#### Step 5: Create admin user
```bash
python manage.py createsuperuser
```

#### Step 6: Apply fixtures
```bash
# Using helper scripts (recommended)
# Windows:
.\load_fixtures.ps1
# Unix/Linux/MacOS:
./load_fixtures.sh

# Or manually:
python manage.py loaddata app/fixtures/categories_fixtures.json
python manage.py loaddata app/fixtures/games_fixtures.json
python manage.py loaddata app/fixtures/users_and_characters.json
```

#### Step 7: .env Configuration
Before using certain features, such as email notifications, you need to configure the environment variables. First, make a copy of the `.env.example` file and rename it to `.env`. Then, update the values with the correct configurations for your environment.

#### Step 8: Run the Server
To start the Django development server, run the following command:

```bash
python manage.py runserver
```

The application should now be accessible at http://localhost:8000/

### Intallation and Deamonizing Application on Server
1) Follow all steps for local installation and startup. Verify that the application is running at http://localhost:8000/.
2) Copy `ecosystem.config.js.manage` or `ecosystem.config.js.wsgi` (recommended) into `ecosystem.config.js` and adjust paths in the configuration file.
3) Daemonize the server using the command `pm2 start ecosystem.config.js`. Ensure you have PM2 installed. If not, you can install it using the command `pnpm add -g pm2`.
4) Configure the nginx server to handle requests under a specific domain and add an SSL Certificate. You can use Let's Encrypt for a free SSL certificate. Keep in mind that nginx configuration may vary depending on your operating system and specific requirements.

### Options in manage.py

`manage.py` is a script file in Django that allows you to manage the application and execute various commands. Here are several useful options provided by `manage.py`:

#### `flush`

The `flush` command removes all data from the database while leaving the tables intact. This is useful during testing when you want to clear the database and start tests from a clean state.

Example usage:
```bash
python manage.py flush
```

#### `migrate`

The `migrate` command executes database migrations. Migrations are a way to keep the database structure in sync with the data model in the application. It allows creating, modifying, and deleting tables and fields in the database based on changes in the models.

Example usage:
```bash
python manage.py migrate
```

#### `makemigrations`

The `makemigrations` command is used to generate new migration files based on changes in the application's models. After making changes to the models, use this command to prepare new migrations before applying them with `migrate`.

Example usage:
```bash
python manage.py makemigrations
```

#### `shell`

The `shell` command runs an interactive Python console with all Django models loaded. This allows for interactive data analysis and experimentation with database operations.

Example usage:
```bash
python manage.py shell
```

#### `createsuperuser`

The `createsuperuser` command allows you to create a new superuser for the application. The superuser can log in to the Django admin panel and manage the application data.

Example usage:
```bash
python manage.py createsuperuser
```

#### Other Commands

In addition to the ones mentioned above, there are many other commands available in `manage.py` that you can use for various purposes, such as managing users, generating reports, running tests, etc. To see a full list of commands and their descriptions, you can use the `help` command:

```bash
python manage.py help
```

Using this, you can get insights into the various options available in `manage.py` and how to use them to manage your Django application.

## Project Status

**📊 Current Status: 85% Complete (MVP Features)**

**MUST READ FOR DEVELOPERS**:
- 📋 **[TASKS.md](TASKS.md)** - Developer roadmap with detailed task breakdowns and specifications
- 📊 **[Technical Audit 2025-12-28](TECHNICAL_AUDIT_2025-12-28.md)** - Complete project audit, findings, and corrections
- ✅ **[Project Status Summary](docs/PROJECT_STATUS_SUMMARY.md)** - What's implemented vs what's pending
- 📖 **[Status Report](docs/STATUS_REPORT.md)** - Detailed feature-by-feature status

**Quick Summary**:
- ✅ All 7 Epics FULLY implemented (Messaging+POKE, Friends, Profiles, Blocking, Identity Reveal, Layout Switcher)
- ✅ 24 E2E tests written (need verification)
- ❌ Missing: Screenshots/Memories UI (backend ready)
- ⚠️ Needs: Test verification, mobile responsiveness polish

**Quick Status:**
- ✅ **Epic 1**: Enhanced Messaging with Privacy Controls (Backend + UI complete)
- ✅ **Epic 2**: Character-Based Friend System (Backend + UI complete)
- ✅ **Epic 3**: User Profile System (Backend + UI complete)
- ✅ **Epic 4**: Character Custom Profile (Basic version complete)
- ⚠️ **Testy Playwright**: Napisane, wymagają weryfikacji
- ❌ **Conversation Management UI**: Backend ready, UI needed
- ❌ **Screenshots & Memories UI**: Backend ready, UI needed

**See [docs/PROJECT_STATUS_SUMMARY.md](docs/PROJECT_STATUS_SUMMARY.md) for complete status breakdown.**

## Tech Stack

- Django 5.1.4
- Bootstrap 5
- SQLite (development) / PostgreSQL (production)
- Django Rest Framework

## Documentation

**📚 For developers**: See [docs/README.md](docs/README.md) for complete documentation index.

**Key Documents**:
- **[Project Status Summary](docs/PROJECT_STATUS_SUMMARY.md)** - Current project status and pending tasks
- **[Status Report](docs/STATUS_REPORT.md)** - Implementation status of all features
- **[Implementation Guide](docs/architecture/implementation-guide.md)** - Step-by-step guide for mid-level developers
- **[Detailed Tasks](docs/scrum/detailed-tasks.md)** - Detailed implementation tasks with code examples

## Development Setup

### Prerequisites

- Python 3.10+
- pipenv

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/game_player_nick_finder.git
   cd game_player_nick_finder
   ```

2. Set up the virtual environment
   ```bash
   pipenv install
   pipenv shell
   ```

3. Set up the database
   ```bash
   python manage.py migrate
   ```

4. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server
   ```bash
   python manage.py runserver
   ```

## Database Management

### Loading Fixtures

The project contains the following fixtures for development:
- `app/fixtures/categories_fixtures.json` - Game categories
- `app/fixtures/games_fixtures.json` - Game definitions
- `app/fixtures/users_and_characters.json` - Sample users and their characters

Load them in the correct order:

```bash
# Using helper script (recommended)
pnpm load:fixtures
# Or: .\load_fixtures.ps1 (Windows) / ./load_fixtures.sh (Unix)

# Or manually in this exact order to maintain data integrity
python manage.py loaddata app/fixtures/categories_fixtures.json
python manage.py loaddata app/fixtures/games_fixtures.json
python manage.py loaddata app/fixtures/users_and_characters.json
```

**Note**: Fixtures are mandatory before running E2E tests. See [docs/TEST_FIXTURES.md](docs/TEST_FIXTURES.md) for complete documentation.

### Database Reset

If you need to reset the database completely:

```bash
# Remove migrations
rm app/migrations/000*.py

# Remove database
rm db.sqlite3

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Load fixtures (required before running E2E tests)
pnpm load:fixtures
# Or: .\load_fixtures.ps1 (Windows) / ./load_fixtures.sh (Unix)

# Create superuser
python manage.py createsuperuser
```

## Project Structure

- `app/` - Main application code
  - `models.py` - Database models (User, Character, Game, etc.)
  - `views.py` - View controllers
  - `forms.py` - Form definitions
  - `api_views.py` - API endpoints
  - `templates/` - HTML templates
  - `fixtures/` - Sample data for development
  - `migrations/` - Database migrations

- `game_player_nick_finder/` - Project configuration
  - `settings.py` - Django settings
  - `urls.py` - URL routing

## Key URLs

- `/` - Home page
- `/accounts/profile/` - User profile
- `/characters/` - Character list
- `/character/add/` - Add new character
- `/character/<nickname>-<hash_id>/` - Character details
- `/games/` - Games list
- `/admin/` - Admin panel

## Development Guidelines

- Follow PEP 8 for Python code
- Use Django's class-based views when possible
- Add docstrings to all functions and classes
- Create unit tests for all new features
- Keep the database schema in sync with models

## Common Tasks

### Adding a New Model

1. Define the model in `app/models.py`
2. Create and run migrations
3. Update admin registration if needed
4. Create relevant views and templates

### Creating New Fixtures

```bash
# Export data from a specific model
python manage.py dumpdata app.ModelName --indent 4 > app/fixtures/model_fixtures.json

# Export data from multiple related models
python manage.py dumpdata app.ModelOne app.ModelTwo --indent 4 > app/fixtures/related_fixtures.json
```

## Troubleshooting

### Migration Issues

If you encounter migration issues, try:
```bash
python manage.py migrate --fake
```

Or reset the database completely following the steps in the "Database Reset" section.

### Template Rendering Issues

Check for:
1. Missing context variables
2. Incorrect URL patterns
3. Missing template files

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add some amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## Development Environment

### Required Tools
- **Python 3.10**: Required for running the application (use pyenv to manage Python versions)
- **pyenv**: For managing Python versions
- **pipenv**: For managing project dependencies and virtual environments

### Development Scripts
All development scripts are located in the `scripts/` folder:

1. **scripts/build.sh**: Main build script that installs dependencies, collects static files, runs migrations, and seeds the database
2. **scripts/first_time_seed.sh**: Script to populate the database with initial data
3. **scripts/reset_db.sh**: Script to reset the database (development only)
4. **scripts/render_reset_db.sh**: Script to reset the database on Render deployment

To run these scripts, use:
```bash
# First, make sure you have the right Python version
pyenv local 3.10.x

# Then use pipenv to manage dependencies
pipenv install

# Finally run scripts as needed
bash scripts/build.sh
```

## Render Deployment

This project can be deployed to Render.com. We've added the necessary configuration files:

1. **render.yaml**: Blueprint for Render deployment
2. **scripts/build.sh**: Build script for the deployment process
3. **Procfile**: Specifies the command to run the application

### Deploying to Render

1. Sign up for a [Render account](https://render.com/)
2. Connect your GitHub repository to Render
3. Click "New Blueprint Instance" from the Render dashboard
4. Select the repository with this project
5. Render will detect the `render.yaml` file and set up the services
6. Configure the environment variables in the Render dashboard:
   - `DJANGO_SECRET_KEY`
   - `EMAIL_HOST`
   - `EMAIL_PORT`
   - `EMAIL_USE_TLS`
   - `EMAIL_HOST_USER`
   - `EMAIL_HOST_PASSWORD`
   - `DEFAULT_FROM_EMAIL`
7. Deploy the service and wait for the build to complete

Render will automatically set up a PostgreSQL database and connect it to your application.
