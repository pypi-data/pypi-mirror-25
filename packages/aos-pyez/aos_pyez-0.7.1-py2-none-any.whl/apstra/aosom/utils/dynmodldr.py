# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula

import importlib

from apstra.aosom.exc import SessionError

__all__ = [
    'DynamicModuleOwner',
    'DynamicallyOwned']


class TypeDynamicModuleCatalog(type):

    @staticmethod
    def catalog_modules(clsdict, package, modules):
        if 'Catalog' not in clsdict:
            clsdict['Catalog'] = dict()

        clsdict['Catalog'].update({
            mod_name: "%s.%s" % (package, mod_file)
            for mod_name, mod_file in modules.items()
        })

    @classmethod
    def apply_conf(mcs, clsdict):
        clsdict_conf = clsdict['DynamicModuleConf']
        for conf_item in clsdict_conf:
            package = conf_item['package']

            if 'modules' in conf_item:
                mcs.catalog_modules(clsdict, package, conf_item['modules'])

            for _dir in conf_item.get('dirs') or []:
                # read the __init__ file which must contain a Catalog dictionary
                _dir_package = "%s.%s" % (package, _dir)
                mod_init = importlib.import_module(_dir_package)
                mod_conf = getattr(mod_init, 'DynamicModuleConf')
                cat_mod = mod_conf[0]['modules']

                # now setup the catalog for that.
                mcs.catalog_modules(clsdict, package=_dir_package, modules=cat_mod)

    def __new__(mcs, clsname, supers, clsdict):
        # check to see if we have a parent class that also has a Catalog, and if
        # so, then merge these down into this new class ; i.e. we are ~extending~
        # the parent class dynamic modules into this class.

        catalogs = filter(lambda s: hasattr(s, 'Catalog'), supers)
        if catalogs:
            clsdict['Catalog'] = {k: v for s in catalogs for k, v in s.Catalog.items()}

        if 'DynamicModuleConf' in clsdict:
            mcs.apply_conf(clsdict)

        return type.__new__(mcs, clsname, supers, clsdict)


class DynamicallyOwned(object):
    def __init__(self, owner):
        self.owner = owner


class DynamicModuleOwner(object):
    __metaclass__ = TypeDynamicModuleCatalog

    # ### ---------------------------------------------------------------------
    # ###
    # ###                         DYNAMIC MODULE LOADER
    # ###
    # ### ---------------------------------------------------------------------

    def __getattr__(self, name):
        mod_file = self.Catalog.get(name)
        if not mod_file:
            raise SessionError(message='request for unknown module: %s' % name)

        # import the module, bind the name to the instance and return the new
        # object instance.

        imp_mod = importlib.import_module(mod_file)
        cls = getattr(imp_mod, imp_mod.__all__[0])
        setattr(self, name, cls(owner=self))
        return getattr(self, name)
