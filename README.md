# Rotterdam Port app

## How to run the application
1. Install depndencies.
    `pip install -r requirements.txt`
2. Migrate models
`python manage.py migrate`
3. Run Django development sever
`python manage.py runserver`
4. Import demo data `python manage.py loaddata demo_data.json`
5. Browse to `http://127.0.0.1:8000/cargo/docks`
## Run tests
* To run full suite
``` bash
python runtests.py
```
* To run Django tests
``` bash
python manage.py test
```

## Assumptions
1. All data will be inserted via Django Admin.
2. When a ship enter to dock or exit from dock, a log will be created.