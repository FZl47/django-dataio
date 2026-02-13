# django-dataio

`django-dataio` is a Django utility package for **data import and export**.  
It allows you to easily export your Django model data into Excel, CSV, JSON, etc., and import data from these formats back into your models.  


## Installation

```bash
    pip install django-dataio
```

## Features

- Export Django models using configurable fields.
- Import data into Django models from Excel (and more formats in the future).
- Extensible architecture: add your own exporters/importers.


## How to Use

django-dataio provides a mixin `DjangoDataIOModelMixin` that allows your Django models to export and import data based on configurable fields (`ModelField`).

`You simply inherit the mixin in your model and define ModelField entries for the fields you want to manage.`

#### 1. Add **DjangoDataIOModelMixin** to your model
```python
from django.db import models
from django_dataio.mixins import DjangoDataIOModelMixin

class Customer(DjangoDataIOModelMixin, models.Model): # -> Here!
first_name = models.CharField(max_length=50)
last_name = models.CharField(max_length=50)
email = models.EmailField(unique=True)
```
   

#### 2. Register fields in **ModelField**
```python
from django.contrib.contenttypes.models import ContentType
from django_dataio.models import ModelField
from my_app.models import Customer

customer_type = ContentType.objects.get_for_model(Customer)

ModelField.objects.create(name="first_name", model=customer_type, xp=1)
ModelField.objects.create(name="last_name", model=customer_type, xp=2)
ModelField.objects.create(name="email", model=customer_type, xp=3)

# xp is the position/order of the field in export/import files.
```
   
#### 3. Export data
```python
from pathlib import Path
from my_app.models import Customer

# Export all customers to Excel
file_path: Path = Customer.data_export('excel')
print(f"Exported file: {file_path}")
```
   
#### 4. Import data
 ```python
from pathlib import Path
from my_app.models import Customer

file_to_import = Path("/tmp/customers.xlsx")

# Import data back into the model
imported_count = Customer.data_import(file_to_import, import_name='excel')
print(f"{imported_count} records imported")
```

---   

#### You can add custom exporters or importers by subclassing the base classes:
```python
    from django_dataio.handlers.imports import BaseImporter
    from django_dataio.handlers.exports import BaseExporter

    class CSVExporter(BaseExporter):
        ...
    
    class CSVImporter(BaseImporter):
        ...
```
Check the [Export](https://github.com/FZl47/django-dataio/blob/main/src/django_dataio/handlers/exports/base.py) | [Import](https://github.com/FZl47/django-dataio/blob/main/src/django_dataio/handlers/imports/base.py) handlers implementation for details.

---
#### [TODO / Update](https://github.com/FZl47/django-dataio/blob/main/todo.txt)