"template automatic tests"
import os
import os.path as osp
from six import text_type

from cubicweb.devtools import testlib

os.environ['HGRCPATH'] = os.devnull


class AutomaticWebTest(testlib.AutomaticWebTest):
    no_auto_populate = ('Repository', 'Revision')
    ignored_relations = set(('parent_revision',
                             'from_repository'))

    def to_test_etypes(self):
        return set(('Repository',
                    'Revision'))

    def custom_populate(self, how_many, cnx):
        cnx.create_entity('Repository', type=u'mercurial',
                          source_url=u'file://'+text_type(osp.join(self.datadir, 'testrepohg')),
                          encoding=u'latin1')


if __name__ == '__main__':
    import unittest
    unittest.main()
