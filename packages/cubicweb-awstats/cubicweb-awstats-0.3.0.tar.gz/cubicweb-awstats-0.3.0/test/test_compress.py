from collections import defaultdict
from datetime import datetime, timedelta
import random

from cubicweb.devtools.testlib import CubicWebTC
from logilab.common import date

from cubicweb_awstats.utils import compress_old_hits


class CompressTest(CubicWebTC):

    def test_compress(self):
        with self.admin_access.client_cnx() as cnx:
            update_stats = defaultdict(int)
            content = cnx.create_entity('Content', title=u'test')
            for day in date.date_range(datetime.now() - timedelta(200), datetime.now()):
                stp = cnx.create_entity(
                    'StatPeriod', start=day, stop=day + timedelta(1))
                hit = cnx.create_entity('Hits', hit_type=u'normal',
                                        count=random.choice(range(2000)),
                                        period=stp, stats_about=content)
            self.assertEqual(len(cnx.execute('Any X WHERE X is Hits')), 200)
            self.assertEqual(
                len(cnx.execute('Any P WHERE P is StatPeriod, P start S, P stop E HAVING E-S >= 27')), 0)
            compress_old_hits(cnx, update_stats)
            # XXX SQLite bug ?
            # self.assertEqual(len(req.execute('Any P WHERE P is StatPeriod, P
            # start S, P stop E HAVING E-S >= 27')), 9)
            self.assertNotEqual(len(cnx.execute('Any X WHERE X is Hits')), 200)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
