# CineReview - Film Review Application
A simple full-stack web application inspired by Letterboxd for managing films and reviews, built with a Django backend and Vue.js (Options API) frontend, as part of Coursework 2 for ECS639 Web Programming.

## Core requirements and advanced features
The following table shows how all the coursework requirements were met, alongside things I did to push myself and go beyond the requirements listed on LearnOuts.

| Criteria | Core implementation | Advanced features added |
|--------|----------|-------------|
| 1. PEP8 compliance | All Python code adheres strictly to the PEP 8 style guide. All functions and classes include docstrings. | Included type hints on all function signatures and used `flake8` for analysis of code formatting such as trailing whitespace, PEP8 compliance and unused imports, and `black` to auto-format |
| 2. Data modelling | Implemented Movie and Review models in api/models.py with a one-to-many relationship and utilisation of all required field types (CharField, IntegerField, DateField, BooleanField, etc.). | Added validators (e.g., min/max rating), custom model methods (e.g., for star display), Meta classes for database indexing and default ordering and a URLField for an image of a movie poster. |
| 3. Vue Options API | Used the Vue Options API for all components (App.vue, MovieItem.vue, etc.), with clear data flow managed by Props (parent-to-child) and $emit (child-to-parent). | Implemented computed properties for dynamic data (e.g., average rating), watchers for handling prop changes, and custom prop validators. |
| 4. Ajax with fetch API | Implemented the Fetch API in App.vue to handle all four HTTP methods (GET, POST, PUT, DELETE) for both Movie and Review models. | Implemented loading states and skeleton screens and included comprehensive network error handling with graceful fallbacks. |
| 5. Bootstrap components | Used Bootstrap accordions for the film list display and Bootstrap modals for all add/edit forms. | Added confirmation modals for deletions, integrated toast notifications for all CRUD success/error messages and overrided styling for Bootstrap components for a more personal touch as I wasn't a fan of the default styling. |


## Installation and quick start
### Prerequisites
- Python 3.10 or higher (for Django)
- Node.js 16 or higher (for Vue/Vite)

### Quick start (concurrent servers)
The `package.json` file in frontend features a custom script using the `concurrently` dependency to run both the Vue and Django API development server simultaneously.

1. Setup environments
```console
$ cd backend
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ cd frontend
$ npm install
$ npm run dev:all
```
The Django server will run on `http://localhost:8000/`

The application will run on `http://localhost:5173/`