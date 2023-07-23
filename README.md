# Game Player Nick Finder [![stability-wip](https://img.shields.io/badge/stability-wip-lightgrey.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#work-in-progress)

## Overview
Game Player Nick Finder is a web application written in Django, allowing users to search for their old online gaming friends based on their nicknames. Users can also register on the platform to be found by other players. Additionally, users can add their gaming characters from various games, define descriptions, and specify the date range when they played under a particular nickname. The application also features a messaging system and email notifications.

## Installation and Running the Application Locally
Before you proceed, ensure that your system has the following installed:
* Python (version 3.6 or newer)
* pip (Python package management tool) [sudo apt install python3-pip]
* evnv (virtual Python environment) [sudo apt install python3-venv]

### Step 1: Clone the Repository
Clone the repository to your local computer using the following git command:

```bash
git clone https://github.com/zentala/game_player_nick_finder
cd game_player_nick_finder
```

### Step 2: Source venv

```bash 
source venv/bin/activate
```

### Step 3: Install Dependencies
To install the required Python dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Database
The application uses SQLite as the default database, so there is no need to set up an additional database. You can simply perform the database migration:

```bash
python manage.py migrate
```

### Step 5: Create admin user
```bash
python manage.py createsuperuser
```

### Step 6: .env Configuration
Before using certain features, such as email notifications, you need to configure the environment variables. First, make a copy of the `.env.example` file and rename it to `.env`. Then, update the values with the correct configurations for your environment.

### Step 7: Run the Server
To start the Django development server, run the following command:

```bash
python manage.py runserver
```

The application should now be accessible at http://localhost:8000/

My apologies for the oversight. Here's the section in markdown as you requested:

## Intallation and Deamonizing Application on Server
1) Follow all steps for local installation and startup. Verify that the application is running at http://localhost:8000/.
2) Copy `ecosystem.config.js.manage` or `ecosystem.config.js.wsgi` (recommended) into `ecosystem.config.js` and adjust paths in the configuration file.
3) Daemonize the server using the command `pm2 start ecosystem.config.js`. Ensure you have PM2 installed. If not, you can install it using the command `npm install pm2 -g`.
4) Configure the nginx server to handle requests under a specific domain and add an SSL Certificate. You can use Let's Encrypt for a free SSL certificate. Keep in mind that nginx configuration may vary depending on your operating system and specific requirements.

## Options in manage.py

`manage.py` is a script file in Django that allows you to manage the application and execute various commands. Here are several useful options provided by `manage.py`:

### `flush`

The `flush` command removes all data from the database while leaving the tables intact. This is useful during testing when you want to clear the database and start tests from a clean state.

Example usage:
```bash
python manage.py flush
```

### `migrate`

The `migrate` command executes database migrations. Migrations are a way to keep the database structure in sync with the data model in the application. It allows creating, modifying, and deleting tables and fields in the database based on changes in the models.

Example usage:
```bash
python manage.py migrate
```

### `makemigrations`

The `makemigrations` command is used to generate new migration files based on changes in the application's models. After making changes to the models, use this command to prepare new migrations before applying them with `migrate`.

Example usage:
```bash
python manage.py makemigrations
```

### `shell`

The `shell` command runs an interactive Python console with all Django models loaded. This allows for interactive data analysis and experimentation with database operations.

Example usage:
```bash
python manage.py shell
```

### `createsuperuser`

The `createsuperuser` command allows you to create a new superuser for the application. The superuser can log in to the Django admin panel and manage the application data.

Example usage:
```bash
python manage.py createsuperuser
```

### Other Commands

In addition to the ones mentioned above, there are many other commands available in `manage.py` that you can use for various purposes, such as managing users, generating reports, running tests, etc. To see a full list of commands and their descriptions, you can use the `help` command:

```bash
python manage.py help
```

Using this, you can get insights into the various options available in `manage.py` and how to use them to manage your Django application.