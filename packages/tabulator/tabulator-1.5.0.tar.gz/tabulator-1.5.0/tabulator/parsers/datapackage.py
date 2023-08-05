# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import datapackage
import six

from ..parser import Parser


# Module API

class DataPackageParser(Parser):
    """Parser to extract data from Tabular Data Packages.

    See: http://specs.frictionlessdata.io/
    """

    # Public

    options = [
        'resource',
    ]

    def __init__(self, loader, force_parse=False, resource=0):
        self.__force_parse = force_parse
        self.__resource = resource
        self.__extended_rows = None
        self.__datapackage = None
        self.__resource_iter = None
        self.__encoding = None

    @property
    def closed(self):
        return self.__resource_iter is None

    def open(self, source, encoding=None):
        self.close()
        self.__datapackage = datapackage.DataPackage(source)
        self.reset()

    def close(self):
        if not self.closed:
            self.__datapackage = None
            self.__resource_iter = None
            self.__extended_rows = None

    def reset(self):
        if isinstance(self.__resource, six.string_types):
            named_resource = next(iter(filter(
                lambda res: res.descriptor['name'] == self.__resource,
                self.__datapackage.resources
            )))  # TODO: use data_package.getResource(name) when v1 is released
            self.__resource_iter = named_resource.iter()
            self.__encoding = named_resource.descriptor.get('encoding')
        else:
            indexed_resource = self.__datapackage.resources[self.__resource]
            self.__resource_iter = indexed_resource.iter()
            self.__encoding = indexed_resource.descriptor.get('encoding')
        self.__extended_rows = self.__iter_extended_rows()

    @property
    def encoding(self):
        return self.__encoding

    @property
    def extended_rows(self):
        return self.__extended_rows

    # Private

    def __iter_extended_rows(self):
        for number, row in enumerate(self.__resource_iter, start=1):
            keys, values = zip(*sorted(row.items()))
            yield number, list(keys), list(values)
