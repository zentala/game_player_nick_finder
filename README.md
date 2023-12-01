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
| DevOps      | ![GitHub Actions](https://img.shields.io/badge/-GitHubActions-2088FF?logo=githubactions&logoColor=white) |
| DBs         | ![SQLite](https://img.shields.io/badge/-SQLite-003B57?logo=sqlite&logoColor=white) |
| Marketing   | ![Google Analytics](https://img.shields.io/badge/-GoogleAnalytics-E37400?logo=googleanalytics&logoColor=white) |
| IDE         | ![VSCode](https://img.shields.io/badge/-Visual%20Studio%20Code-007ACC?logo=visualstudiocode&logoColor=white) |

## 🏗 Current & Planned App Architecture
### Current Backend: [Django Full-Stack App in `server` Directory](https://github.com/zentala/game_player_nick_finder/tree/master/server)
- Our current setup uses Django for server-side rendering, efficiently delivering static content and managing server-client interactions.
- Django's ORM is integral for database interactions, while Django Views handle business logic and data presentation.

#### Planned Transition to API-Driven Architecture
- The next phase involves shifting to Django REST Framework for API endpoints creation, setting the stage for a more dynamic, interactive frontend.
- These API endpoints will be consumed by a [Planned React.js Client](https://github.com/zentala/game_player_nick_finder/tree/master/client) for enhanced user experiences.

### Planed initial [Future React.js Client in `client` directory](https://github.com/zentala/game_player_nick_finder/tree/master/client)
- Contains the foundational setup for the future React.js application, awaiting development post-API integration.

### Current Development Focus
1) The immediate goal is to achieve MVP functionality, including character creation flows, friend search optimization, and user account panels for game and character management.
2) Current priorities include contact information sharing, friend request features, and notification systems for new user additions.
3) Long-term plans include implementing a user-to-user chat system.
4) The React.js development is deferred for now, focusing instead on completing the business logic and core functionalities.

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
