# Forpus API Client

This is a Python 3 client for the Forpus App Rest API.

Is has methods for feeding the web app with market data from a single data source.

It is possible to list, create, update, and delete:

- Securities
- Security Types
- Frequencies
- Price Types
- Prices
- Time Weights
- Time Volumes

There is also very simple method for filtering prices.

## Authenticating

There are two possible constructors:
         
The first one expects `user` and `password` strings for the Forpus Rest API.

```python
from forpus_api import Forpus
client = Forpus('user', 'password')
```

The second one expects to find environment variables:

- `FORPUSAPI_USER`
- `FORPUSAPI_PASSWORD`

```python
import os
from forpus_api import Forpus
client = Forpus(os.environ)
```

## Basic usage

The methods for dealing with the entities listed above are:

- `client.list_` (entities) `()`
- `client.create_` (entitiy) `(entity)`
- `client.update_` (entitiy) `(entity)`
- `client.delete_` (entitiy) `(entity_id)`

For instance, (entity) must be replaced by `security` and (entities) must be replaced by `securities` when dealing with this entity.

The 'list' functions provide a fair description of all entities, further explanation regarding to them will be provided soon.
