# MP-Reviews

Django reviews app.

### Installation

Install with pip:

```sh
$ pip install django-mp-reviews
```

Add reviews to settings.py:

```
INSTALLED_APPS = [
    'reviews',
]
```

Add reviews to urls.py:
```
urlpatterns = [
	url(r'^reviews/', include('reviews.urls', namespace='reviews')),
]
```

Add bower components:
```
BOWER_INSTALLED_APPS = (
	'jquery#1.11.1',
	'jquery-form',
	'jquery.rateit',
)
```

Add PIPELINE settings:
```
PIPELINE = {
	'STYLESHEETS': {
            'generic': {
                'source_filenames': (
                    'bower_components/jquery.rateit/scripts/rateit.css',
                ),
                'output_filename': 'cache/generic.css',
            }
        },
        'JAVASCRIPT': {
            'generic': {
                'source_filenames': (
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/jquery.rateit/scripts/jquery.rateit.js',
                    'bower_components/jquery-form/dist/jquery.form.min.js',
                    'reviews/reviews.js',
                ),
                'output_filename': 'cache/generic.js',
            }
        }
}
```

Install bower components:

```
$ python manage.py bower install
```

Run migrations:

```
$ python manage.py migrate
```

Create reviews list template 'templates/reviews/index.html' for 'reviews:index' url.

### Requirements

App require this packages:

* django-pure-pagination
