# -*- coding: utf-8 -*-
# copyright 2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os.path as osp
from json import loads, dumps

from cubicweb import ValidationError
from cubicweb.devtools.testlib import CubicWebTC

HERE = osp.dirname(__file__)


class WiringTCMixin(object):

    def setup_database(self):
        super(WiringTCMixin, self).setup_database()
        with self.admin_access.cnx() as cnx:
            self.wl_eid = cnx.create_entity('WiringLanguage', name=u'wl').eid
            cnx.commit()


class WiringAddHookTC(WiringTCMixin, CubicWebTC):

    def test_name(self):
        'creating a wiring with no name should not crash but set it'
        with self.admin_access.cnx() as cnx:
            wiring = cnx.create_entity('Wiring', language=self.wl_eid,
                                       json=u'')
            cnx.commit()
            self.assertTrue(wiring.name)


class UpdateWiringLanguageHookTC(WiringTCMixin, CubicWebTC):

    def setup_database(self):
        super(UpdateWiringLanguageHookTC, self).setup_database()
        with self.admin_access.cnx() as cnx:
            wl = cnx.entity_from_eid(self.wl_eid)
            wl.cw_set(json=self._json_content('wlan.json'))
            self.wiring_eid = cnx.create_entity(
                'Wiring', json=self._json_content('wiring.json'),
                language=self.wl_eid).eid
            cnx.commit()

    def _json_content(self, fname):
        json = loads(open(osp.join(HERE, 'data', fname)).read())
        return unicode(dumps(json))

    def test_valid(self):
        'check a valid definition does not raise ValidationError'
        with self.admin_access.cnx() as cnx:
            wiring = cnx.entity_from_eid(self.wiring_eid)
            new_def = loads(wiring.json)
            new_def['toto'] = u'titi'
            wiring.cw_set(json=unicode(dumps(new_def)))
            cnx.commit()

    def test_invalid_module_list(self):
        'remove a module used by the wiring def and check ValidationError'
        with self.admin_access.cnx() as cnx:
            wl = cnx.entity_from_eid(self.wl_eid)
            wldef = loads(wl.json)
            del wldef['modules'][0]
            with self.assertRaises(ValidationError) as cm:
                wl.cw_set(json=unicode(dumps(wldef)))
                cnx.commit()
            cnx.rollback()
        self.assertIn('Invalid WiringLanguage change',
                      str(cm.exception))

    def test_invalid_module_definition(self):
        'change a container def used by the wiring and check ValidationError'
        with self.admin_access.cnx() as cnx:
            wl = cnx.entity_from_eid(self.wl_eid)
            wldef = loads(wl.json)
            wldef['modules'][0]['container']['title'] = u'changed_title'
            with self.assertRaises(ValidationError) as cm:
                wl.cw_set(json=unicode(dumps(wldef)))
                cnx.commit()
            cnx.rollback()
        self.assertIn('Invalid WiringLanguage change', str(cm.exception))


if __name__ == '__main__':
    import unittest
    unittest.main()
