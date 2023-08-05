#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zc.buildout recipe for writing various ZCML include slugs.
Originally based on collective.recipe.zcml, but modified to not
be rigid about the type of ZCML file requested and the
paths to which they are written. Also requires the
use of zc.recipe.deployment.

"""

from __future__ import print_function, absolute_import, division

import os
import re
import errno

import zc.buildout


class ZCML(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        if 'deployment' in options:
            options['etc'] = buildout[options['deployment']]['etc-directory']
        else:
            options['etc'] = options['etc-directory']

    def install(self):
        """Installer"""
        created = self.build_package_includes()
        return tuple(created)

    update = install

    def build_package_includes(self):
        """
        Create ZCML slugs.
        """
        options = self.options
        etc = options['etc']
        package_match = re.compile(r'\w+([.]\w+)*$').match
        out = []

        for key in (k for k in options if k.endswith('_zcml')):
            zcml = options[key] or ''

            slug_name = key[:-5]
            slug_path = options[slug_name + '_location']
            slug_default_filename = options.get(slug_name + '_file', 'configure')
            slug_features = options.get(slug_name + '_features', '')
            slug_features = slug_features.split()

            if not zcml and not slug_features:
                continue

            includes_path = os.path.join(etc, slug_path)
            if not os.path.exists(includes_path):
                try:
                    os.mkdir(includes_path)
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        raise zc.buildout.UserError(
                            "The parents of '%s' do not exist" % includes_path)
                    raise # pragma: no cover

            zcml = zcml.split()
            if '*' in zcml:
                zcml.remove('*')
            # We never need to remove the whole directory, buildout
            # will automatically uninstall any files we created in it
            # as needed

            if slug_features:
                features_zcml = ['\t<meta:provides feature="%s" />' % i
                                 for i in slug_features]
                features_zcml.insert(0,
                                     '<configure xmlns="http://namespaces.zope.org/zope"'
                                     ' xmlns:meta="http://namespaces.zope.org/meta">')
                features_zcml.append("</configure>")

                path = os.path.join(includes_path, '000-features.zcml')
                with open(path, 'w') as f:
                    f.write('\n'.join(features_zcml))
                out.append(path)


            for n, package in enumerate(zcml, 1):
                orig = package
                suff = slug_default_filename
                filename = None
                if ':' in package:
                    package, filename = package.split(':')

                if '-' in package:
                    package, suff = package.split('-')

                filename = filename or suff + '.zcml'

                if not package_match(package):
                    raise zc.buildout.UserError(
                        "Invalid package name: '%s' parsed as '%s'" % (orig, package))

                path = os.path.join(
                    includes_path,
                    "%3.3d-%s-%s.zcml" % (n, package, suff),
                )
                with open(path, 'w') as f:
                    f.write(
                        '<include package="%s" file="%s" />\n'
                        % (package, filename))
                out.append(path)
        return out
