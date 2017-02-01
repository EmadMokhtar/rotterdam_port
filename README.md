# Rotterdam Port app

## How to run the application
1. Install depndencies.
    `pip install -r requirements.txt`
2. Migrate models
`python manage.py migrate`
3. Create superuser `python manage.py createuserpuser`
4. Run Django development sever
`python manage.py runserver`
5. Import demo data `python manage.py loaddata demo_data.json`
6. Browse to `http://127.0.0.1:8000/cargo/docks`

## Run tests
* To run full suite
``` bash
pip install -r requirements_dev.txt
python runtests.py
```
* To run Django tests
``` bash
python manage.py test
```

## Assumptions
1. All data will be inserted via Django Admin.
2. When a ship enter to dock or exit from dock, a log will be created.
3. Dock must be empty to assign a ship to it, if dock is occupied with  ship, this ship need to exit before assign anther ship to dock.
