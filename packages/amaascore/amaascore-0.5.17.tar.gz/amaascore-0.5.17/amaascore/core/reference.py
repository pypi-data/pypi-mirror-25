from __future__ import absolute_import, division, print_function, unicode_literals

from amaascore.core.amaas_model import AMaaSModel


class Reference(AMaaSModel):

    def __init__(self, reference_value, *args, **kwargs):
        self.reference_value = reference_value
        super(Reference, self).__init__(*args, **kwargs)
