[![Build Status](https://travis-ci.org/Apkawa/django-multitype-file-field.svg?branch=master)](https://travis-ci.org/Apkawa/easy-thumbnails-admin)
[![Requirements Status](https://requires.io/github/Apkawa/django-multitype-file-field/requirements.svg?branch=master)](https://requires.io/github/Apkawa/easy-thumbnails-admin/requirements/?branch=master)
[![PyPI](https://img.shields.io/pypi/pyversions/easy-thumbnails-admin.svg)]()

# Install
```bash
pip install easy-thumbnails-admin
```

1. Append into `INSTALLED_APPS` settings before `easy-thumbnails` like:
    ```python
    INSTALLED_APPS = [
        # ...
        'easy_thumbnails_admin',
        'easy_thumbnails',
        'easy_thumbnails.optimize',
        # ...
    ]
    ```
    
2. Configure `THUMBNAIL_ALIASES` like here. Add `admin`.`help_text` if needed.
    ```python
    THUMBNAIL_ALIASES = {
        'example_app.Article.poster': {
            'small': {
                'size': (100, 100), 'crop': 'smart',
             # Here there
                'admin': {
                    "help_text": "Small thumbnail, showed on article list"
                },
            },
            'medium': {
                'size': (300, 200), 'crop': 'smart',
             # And here
                'admin': {
                    'help_text': 'A generic thumbnail'
                }
            }
         }
      }
    
    ```

## Usage

This library patched all fields with `ThumbnailField`.

1. Click on preview or link at field in admin

    ![Build Status](docs/screenshots/initial.png)
    
2. Aliases list 

    ![Build Status](docs/screenshots/thumbnail_list.png)
    
3. Edit alias

    ![Build Status](docs/screenshots/edit_thumbnail_alias.png)


# Contribute
## Run examples
```bash
# virtualenvwrapper
mkvirtualenv eta
workon eta
./tests/manage.py migrate
./tests/manage.py runserver 

```

## frontend
```bash
yarn # or npm
yarn watch 
yarn build # for release

```