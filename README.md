# Game Player Nick Finder [![stability-wip](https://img.shields.io/badge/stability-wip-lightgrey.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#work-in-progress)

## Overview
Player Finder is a web application written in Django, allowing users to search for their old online gaming friends based on their nicknames. Users can also register on the platform to be found by other players. Additionally, users can add their gaming characters from various games, define descriptions, and specify the date range when they played under a particular nickname. The application also features a messaging system and email notifications.

## Installation and Running the Application
Before you proceed, ensure that your system has the following installed:
* Python (version 3.6 or newer)
* pip (Python package management tool)

### Step 1: Clone the Repository
Clone the repository to your local computer using the following git command:

```bash
git clone https://github.com/zentala/game_player_nick_finder
cd game_player_nick_finder
```

### Step 2: Install Dependencies
To install the required Python dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### Step 3: Configure the Database
The application uses SQLite as the default database, so there is no need to set up an additional database. You can simply perform the database migration:

```bash
python manage.py migrate
```

### Step 4: Create admin user
```bash
python manage.py createsuperuser
```

### Step 5: .env Configuration
Before using certain features, such as email notifications, you need to configure the environment variables. First, make a copy of the `.env.example` file and rename it to `.env`. Then, update the values with the correct configurations for your environment.

### Step 6: Run the Server
To start the Django development server, run the following command:

```bash
python manage.py runserver
```

The application should now be accessible at http://localhost:8000/
