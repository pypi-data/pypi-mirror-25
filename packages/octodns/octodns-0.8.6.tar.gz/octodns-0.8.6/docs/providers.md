## NsOne notes

* 

## Creating a new provider

* mkdir config/
* create config/dev.yaml

```yaml
---
providers:
  # Primary source for manually configured data
  config:
    class: octodns.provider.yaml.YamlProvider
    directory: ./config

  # External
  nsone:
    class: octodns.provider.nsone.NsOneProvider
    api_key: env/NS_ONE_API_KEY

zones:
  githubtest.net.:
    sources:
      - config
    targets:
      - nsone
```

* create config/githubtest.net.yaml

```yaml
---
'':
  type: A
  value: 1.2.3.4
```

* Create bare minimum provider class

```python
#
#
#

from __future__ import absolute_import, division, print_function, \
    unicode_literals

from logging import getLogger
from nsone import NSONE

from .base import BaseProvider


class NsOneProvider(BaseProvider):
    '''
    NsOne provider

    nsone:
        class: octodns.provider.nsone.NsOneProvider
        api_key: env/NS_ONE_API_KEY
    '''
    SUPPORTS_GEO = False

    def __init__(self, id, api_key, *args, **kwargs):
        self.log = getLogger('NsOneProvider[{}]'.format(id))
        self.log.debug('__init__: id=%s, api_key=***', id)
        super(NsOneProvider, self).__init__(id, *args, **kwargs)
        self._client = NSONE(apiKey=api_key)
```

* `PYTHONPATH=. ./octodns/cmds/sync.py --config=./config/dev.yaml --doit`
* Start adding the stuff that's missing (exceptions thrown) using other providers as examples
* Once things are working add more records to the zone to cover the supported
    fucntionality see `tests/config/unit.tests.yaml` for a relatively thorough
    example
