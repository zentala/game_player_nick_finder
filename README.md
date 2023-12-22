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
* pip (Python package management tool) [sudo apt install python3-pip]
* pipenv (Python packaging tool for virtual environments) [pip install pipenv]

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
python manage.py migrate
```

#### Step 5: Create admin user
```bash
python manage.py createsuperuser
```

#### Step 6: Apply fixtures
```bash
python manage.py loaddata app/fixtures/categories_fixtures.json
python manage.py loaddata app/fixtures/games_fixtures.json
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
3) Daemonize the server using the command `pm2 start ecosystem.config.js`. Ensure you have PM2 installed. If not, you can install it using the command `npm install pm2 -g`.
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

