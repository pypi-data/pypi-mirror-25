[![Build Status](https://travis-ci.org/Apkawa/django-multitype-file-field.svg?branch=master)](https://travis-ci.org/Apkawa/django-multitype-file-field)

[![Requirements Status](https://requires.io/github/Apkawa/django-multitype-file-field/requirements.svg?branch=master)](https://requires.io/github/Apkawa/django-multitype-file-field/requirements/?branch=master)
[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]()

Project for merging different file types, as example easy thumbnail image and unpacking archive in one field

# Installation

```bash
pip install django-multitype-file-field

```

or from git

```bash
pip install -e git+https://github.com/Apkawa/django-multitype-file-field.git#egg=django-multitype-file-field
```

# Usage

## models.py

```python
from django.db import models

from multitype_file_field.fields import MultiTypeFileField

# as example, with easy_thumbnails
from easy_thumbnails.fields import ThumbnailerImageField


class FileModel(models.Model):
    file = MultiTypeFileField(upload_to='test_archive',
        fields={
            None: models.FileField, # Fallback
            'image/svg+xml': models.FileField, # high priority,
            'image': (
                ThumbnailerImageField, 
                dict(resize_source=dict(size=(100, 100), sharpen=True, crop='smart'))
                ), # tuple, Field and args
            
        }
    )
```
```python
from tests.models import TestModel
from django.core.files.base import ContentFile
model = TestModel()
model.file # => <FieldFile: None>
model.file = ContentFile('', name='example.png')
model.file # => <ImageFieldFile: example.png>
model.file = ContentFile('', name='example.txt')
model.file # => <FieldFile: example.txt>

```

# Contributing

## run tests

```bash
pip install -r requirements.txt
./test/manage.py migrate
pytest
tox
```

## publish pypi

```bash
python setup.py sdist upload -r pypi
```






