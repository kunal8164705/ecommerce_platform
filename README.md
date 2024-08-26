
# Ecommerce Platform - Django Project

This project is a simple Django-based ecommerce platform that allows for product management, user authentication, and data analysis. It includes functionalities for loading product data from a CSV file into a database, performing data cleaning, and generating a summary report. The project also features JWT-based authentication for secure access to certain endpoints.

## Features

- **Product Data Management**: Load product data from a CSV file into a database using a management command.
- **User Authentication**: Secure login and signup system using JWT tokens.
- **Data Cleaning**: Handle missing values and ensure data types are correct.
- **Summary Report**: Generate a summary report with total revenue, top product, and quantity sold per category.
- **RESTful API**: Expose endpoints for user authentication and summary report generation.

## Requirements

- Python 3.8+
- Django 4.x
- Django REST Framework
- Simple JWT
- Pandas
- SQLite (default) or PostgreSQL/MySQL for database

## Installation

1. **Clone the Repository:**

   ```bash
   git clone 
   cd ecommerce
   ```

2. **Set Up a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**

   Apply the migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

5. **Load Product Data:**

   Place your CSV file in the project directory and run the following command to load product data into the database:

   ```bash
   python manage.py load_products
   ```

6. **Run the Development Server:**

   Start the Django development server:

   ```bash
   python manage.py runserver
   ```

## Usage

### Endpoints

- **Signup**: `POST /account/signup/`

  Create a new user. Requires `username` and `password`.

  Example:
  ```json
  {
    "username": "user",
    "password": "password"
  }
  ```

- **Login**: `POST /account/login/`

  Log in an existing user. Requires `username` and `password`. Returns a JWT token.

  Example:
  ```json
  {
    "username": "user",
    "password": "password"
  }
  ```

- **Summary Report**: `GET /analysis/summary/`

  Generate and download a summary report. Requires an Authorization header with a JWT token.

  Example:
  ```bash
  curl -H "Authorization: Bearer <your_jwt_token>" http://127.0.0.1:8000/analysis/summary/
  ```

### Data Cleaning

The project automatically handles missing values during data loading:
- **Price and Quantity Sold**: Missing values are replaced with the median value of their respective columns.
- **Rating**: Missing values are replaced with the average rating of the category.

### JWT Token Authentication

The project uses JWT tokens to authenticate users. You must include the token in the `Authorization` header for protected endpoints.



