Certainly! Here's a simple README file in markdown format:

```markdown
# Django Project Setup Guide

This guide will help you set up a Django project, migrate the database, populate it with data using `genData.py`, create a superuser, run the development server, and access the Django admin interface.

## Prerequisites

- Python 3 installed on your machine
- pip (Python package installer)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Alvallesteros/Magis-Air
   cd MagisAir
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply database migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Run the `genData.py` script to populate the database:

   ```bash
   python genData.py
   ```

7. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to set a username, email, and password for the superuser.

8. Start the development server:

   ```bash
   python manage.py runserver
   ```

   The server will be running at http://127.0.0.1:8000/.

9. Access the Django admin interface:

   - Open a web browser and go to http://127.0.0.1:8000/admin/
   - Log in using the superuser credentials created in step 7.

You are now set up and ready to work on your Django project!
```