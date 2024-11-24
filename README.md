# Travel Booking App
<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

## About <a name = "about"></a>

This is a Django-based tour and travel application used for booking hotels, flights, and tours. It uses Django as the backend framework and Django REST framework (DRF) for building API functionalities.

## Project Status

This project is currently a work in progress and may lack some essential features. Future updates are planned to enhance functionality and address existing limitations. Contributions and suggestions are welcome!


## Getting Started <a name = "getting_started"></a>
- Clone the repository to your local machine:
    ```
    git clone https://github.com/alireza-v/travel_agency.git
    ```

- Create and activate the virtual environemnt:

    On windows:
    ```
    python -m venv venv
    .\env\Scripts\activate
    ```

    On macOS/Linux:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

- Install dependencies
    ```
    pip install requirements.txt
    ```

- Set up environment variable:
    ```
    user= your-database-user
    name= your-database-name
    password= your-database-password
    email_host_user= your_email_host_user
    email_host_password= your_email_host_user
    ```

- Set up the database:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

- Run the development server:
    ```
    python manage.py runserver
    ```

##  Running the tests <a name = "tests"></a> (Optional)

To run the tests and ensure everything is working as expected, use either of the following commands.

Display more detailed test information:
```
pytest -v
```
Stop at the first caught error:
```
pytest --maxfail=1
```

## Dependencies
The full list of dependencies can be found in the [requirements.txt](requirements.txt) file.

Some key libraries:

[![Django](https://img.shields.io/badge/Django-4.2-brightgreen)](https://docs.djangoproject.com/en/4.2/)

[![DRF](https://img.shields.io/badge/DRF-3.15.2-blue)](https://www.django-rest-framework.org/)

[![Djoser](https://img.shields.io/badge/Djoser-2.3.1-blue)](https://djoser.readthedocs.io/)
