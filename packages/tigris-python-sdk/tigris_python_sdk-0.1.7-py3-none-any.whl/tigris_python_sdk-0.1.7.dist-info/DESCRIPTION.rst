# Jogral Tigris Python SDK

[![Build Status](https://travis-ci.org/jogral/tigris-python-sdk.svg?branch=dev)](https://travis-ci.org/jogral/tigris-python-sdk)

This is the official Python SDK for [Jogral Tigris](https://jogral.co/product).
This SDK will let you execute most of the functionality you would from the API,
and is an alternative to the stock UI.

## Why use this?

Suppose you want to extend the functionality/features of Tigris, e.g. integrating with your company intranet
or with a third party service. This SDK is a layer around the REST-like API powering Tigris, leaving you to
write software and not worry about forming your HTTP requests--just use native features!

We at Jogral are already using this API to build another product: our command line interface for Tigris.

## Installation

```
pip install tigris-python-sdk
```

## Usage

To get started:

```python
from tigrissdk.client import Client

client = Client(username=username, password=password, base_url=base_url)
print('My Username: {0}'.format(client.session.user.shortname))
```

Getting courses:

```python
# Get all courses
client.courses()

# You can use a dict as query params
client.courses({'slug': 'test'})

# You can create/retrieve/update, too
## New course
course_dict = {'title': 'title', ...}
course = client.course(course_dict) # Course is not created yet, but object is.
course = course.save(True) # Now course is added to Tigris, and has an ID.
print(course.id)

## Get/edit course
course = client.course({'id': 1}).get()
course.status = 1
updated_course = course.save()
```

More coming soon.

## Contributing

You should be able to git started by cloning our repo. We use [`virtualenv`](https://virtualenv.pypa.io/en/stable/)
and [`pyenv`](https://github.com/pyenv/pyenv) for development. Once you've cloned your repo, go to the repo path and run


```
virtualenv tigris-sdk-env
pip install -r requirements.txt
```


**NOTE:** You should be sure to have some flavor of Python 3. Due to support officially dropping for Python 2,
we do not support Python 2.

### Testing

Test coverage is still largely in progress. However, you can run _existing_
test cases by running

```
pytest
```

or

```
tox
```

## Support

Development, support, etc. is managed directly by [Jogral](https://jogral.co).
If you want to contact us directly, drop us a line at <code@jogral.io>. We welcome
you to open issues directly through GitHub and to use email for questions.

## License

The Tigris Python SDK is licensed under the Apache License 2.0. See LICENSE for details.


## TODO

- Increase test coverage to 100%.
- Make it clearer when sessions are expired.
- Create documentation from docstrings.
- Incorporate upcoming authorization updates to API into SDK.
- Flesh out roadmap.


