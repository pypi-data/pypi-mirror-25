# google_play_reader

[![Build Status](https://travis-ci.org/luiscruz/google_play_reader.svg?branch=master)](https://travis-ci.org/luiscruz/google_play_reader)

Python3 library to get information about apps on Google Play Store.

## Install

```
$pip install git+https://github.com/luiscruz/google_play_reader.git
```

## Usage

```
from google_play_reader.models import AppEntry

app_entry = AppEntry("com.newsblur")
name = app_entry.get_name()
rating_value, rating_count = app_entry.get_rating()
downloads = app_entry.get_downloads()
category = app_entry.get_category()
# ...
```

## Contributing

Feel free to create pull requests.
Be sure that your code passes our checkers:

```
$tox -e py36
```
### Tests

Tests are still not being made properly.
So far you can check whether it is working by running:

```
$python -m google_play_reader.models
```

