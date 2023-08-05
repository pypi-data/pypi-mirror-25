from __future__ import unicode_literals

from ...models.base import BaseModel


class Feature(BaseModel):
    """ Common object amongst many dossiers. """

    _as_is_fields = ['code', 'label', 'description']
