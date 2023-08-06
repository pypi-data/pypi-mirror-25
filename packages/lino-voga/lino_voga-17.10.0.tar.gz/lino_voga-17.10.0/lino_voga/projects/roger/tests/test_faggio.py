# -*- coding: utf-8 -*-
# Copyright 2013-2017 Luc Saffre
# This file is part of Lino Voga.
#
# Lino Voga is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Voga is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Voga.  If not, see
# <http://www.gnu.org/licenses/>.

"""Tests about generating automatic events of a course.  Look at the
source code!

To run just this test::

  $ cd lino_voga/projects/roger
  $ python manage.py test

"""

from __future__ import unicode_literals

from builtins import str
from lino.api.shell import cal
from lino.api.shell import courses
from lino.api.shell import users
from django.conf import settings

from lino.utils.djangotest import RemoteAuthTestCase
from lino.utils import i2d
from lino.modlib.users.choicelists import UserTypes


def create(model, **kwargs):
    obj = model(**kwargs)
    obj.full_clean()
    obj.save()
    return obj
    

class QuickTest(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        # Create a room, event type, series and a course
        
        room = create(cal.Room, name="First Room")
        lesson = create(cal.EventType, name="Lesson", event_label="Lesson")
        line = create(courses.Line, name="First Line", event_type=lesson)
        obj = create(
            courses.Course,
            line=line,
            room=room,
            max_events=5,
            monday=True,
            state=courses.CourseStates.active,
            start_date=i2d(20140110))
        self.assertEqual(str(obj), "Activity #1")

        # self.assertEqual(settings.SITE.kernel.site, settings.SITE)
        # self.assertEqual(settings.SITE, dd.site)
        # self.assertEqual(settings.SITE.plugins, dd.apps)
        # self.assertEqual(settings.SITE.plugins.extjs, dd.apps.extjs)

        settings.SITE.verbose_client_info_message = True
        users.User(username="robin",
                   user_type=UserTypes.admin,
                   language="en").save()
        ses = settings.SITE.login('robin')

        # utility function which runs update_events and checks whether
        # info_message and output of cal.EntriesByController are as
        # expected:        
        def check_update(obj, msg1, msg2):
            res = ses.run(obj.do_update_events)
            self.assertEqual(res['success'], True)
            self.assertEqual(res['info_message'].strip(), msg1.strip())
            ar = ses.spawn(cal.EntriesByController, master_instance=obj)
            s = ar.to_rst(column_names="when_text state summary", nosummary=True)
            # print s
            self.assertEqual(s.strip(), msg2.strip())
            
        # Run do_update_events a first time
        check_update(obj, """
Update Events for Activity #1...
Generating events between 2014-01-13 and 2020-05-22 (max. 5).
Update Guests for Activity #1 Lesson 1...
0 row(s) have been updated.
Update Guests for Activity #1 Lesson 2...
0 row(s) have been updated.
Update Guests for Activity #1 Lesson 3...
0 row(s) have been updated.
Update Guests for Activity #1 Lesson 4...
0 row(s) have been updated.
Update Guests for Activity #1 Lesson 5...
0 row(s) have been updated.
5 row(s) have been updated.""", """
================ =========== ===================
 When             State       Short description
---------------- ----------- -------------------
 Mon 13/01/2014   Suggested   Lesson 1
 Mon 20/01/2014   Suggested   Lesson 2
 Mon 27/01/2014   Suggested   Lesson 3
 Mon 03/02/2014   Suggested   Lesson 4
 Mon 10/02/2014   Suggested   Lesson 5
================ =========== ===================
""")
        
        # Decrease max_events and check whether the superfluous events
        # get removed.
        
        obj.max_events = 3
        check_update(obj, """
Update Events for Activity #1...
Generating events between 2014-01-13 and 2020-05-22 (max. 3).
2 row(s) have been updated.""", """
================ =========== ===================
 When             State       Short description
---------------- ----------- -------------------
 Mon 13/01/2014   Suggested   Lesson 1
 Mon 20/01/2014   Suggested   Lesson 2
 Mon 27/01/2014   Suggested   Lesson 3
================ =========== ===================
""")
        
        # Run do_update_events for 5 events a second time
        obj.max_events = 5
        check_update(obj, """
Update Events for Activity #1...
Generating events between 2014-01-13 and 2020-05-22 (max. 5).
Update Guests for Activity #1 Lesson 4...
0 row(s) have been updated.
Update Guests for Activity #1 Lesson 5...
0 row(s) have been updated.
2 row(s) have been updated.""", """
================ =========== ===================
 When             State       Short description
---------------- ----------- -------------------
 Mon 13/01/2014   Suggested   Lesson 1
 Mon 20/01/2014   Suggested   Lesson 2
 Mon 27/01/2014   Suggested   Lesson 3
 Mon 03/02/2014   Suggested   Lesson 4
 Mon 10/02/2014   Suggested   Lesson 5
================ =========== ===================
""")

        
        # Now we want to skip the 2nd event.  We click on "Move next"
        # on this event. Lino then moves all subsequent events
        # accordingly.

        ar = cal.EntriesByController.request(
            master_instance=obj,
            known_values=dict(
                start_date=i2d(20140120)))
        e = ar.data_iterator[0]
        self.assertEqual(e.state, cal.EntryStates.suggested)
        #
        res = ses.run(e.move_next)

        self.assertEqual(res['success'], True)
        expected = """\
Move down for Activity #1 Lesson 2...
Generating events between 2014-01-13 and 2020-05-22 (max. 5).
Lesson 2 has been moved from 2014-01-20 to 2014-01-27.
1 row(s) have been updated."""
        self.assertEqual(res['info_message'], expected)

        # The event is now in state "draft" because it has been
        # modified by the user.

        self.assertEqual(e.state, cal.EntryStates.draft)
        # e.full_clean()
        # e.save()

        check_update(obj, """
Update Events for Activity #1...
Generating events between 2014-01-13 and 2020-05-22 (max. 5).
Lesson 2 has been moved from 2014-01-20 to 2014-01-27.
0 row(s) have been updated.
""","""
================ =========== ===================
 When             State       Short description
---------------- ----------- -------------------
 Mon 13/01/2014   Suggested   Lesson 1
 Mon 27/01/2014   Draft       Lesson 2
 Mon 03/02/2014   Suggested   Lesson 3
 Mon 10/02/2014   Suggested   Lesson 4
 Mon 17/02/2014   Suggested   Lesson 5
================ =========== ===================
""")

        # Now we imagine that February 3 is the National Day in our
        # country. But that we create the rule for this only now.  So
        # we have a conflict because Lino created an appointment on
        # that date. Of course the National Day must *not* move to an
        # alternative date.

        et = create(cal.EventType, name="Holiday", all_rooms=True)
        national_day = create(
            cal.RecurrentEvent,
            name="National Day", event_type=et,
            start_date=i2d(20140203),
            every_unit=cal.Recurrencies.yearly)

        res = ses.run(national_day.do_update_events)
        self.assertEqual(res['success'], True)
        expected = """\
Update Events for National Day...
Generating events between 2014-02-03 and 2020-05-22 (max. 72).
Reached upper date limit 2020-05-22
Update Guests for Recurring event #1 National Day...
0 row(s) have been updated.
Update Guests for Recurring event #1 National Day...
0 row(s) have been updated.
Update Guests for Recurring event #1 National Day...
0 row(s) have been updated.
Update Guests for Recurring event #1 National Day...
0 row(s) have been updated.
Update Guests for Recurring event #1 National Day...
0 row(s) have been updated.
Update Guests for Recurring event #1 National Day...
0 row(s) have been updated.
Update Guests for Recurring event #1 National Day...
0 row(s) have been updated.
7 row(s) have been updated."""
        self.assertEqual(res['info_message'], expected)
        ar = ses.spawn(
            cal.EntriesByController, master_instance=national_day)
        s = ar.to_rst(column_names="when_text state", nosummary=True)
        # print s
        self.assertEqual(s, """\
================ ===========
 When             State
---------------- -----------
 Mon 03/02/2014   Suggested
 Tue 03/02/2015   Suggested
 Wed 03/02/2016   Suggested
 Fri 03/02/2017   Suggested
 Sat 03/02/2018   Suggested
 Sun 03/02/2019   Suggested
 Mon 03/02/2020   Suggested
================ ===========

""")

        # the national day is now conflicting with our Lesson 3:
        ce = ar[0]
        self.assertEqual(ce.summary, "National Day")
        self.assertEqual(ce.start_date.year, 2014)
        ar = ses.spawn(
            cal.ConflictingEvents, master_instance=ce)
        s = ar.to_rst(column_names="when_text state auto_type")
        # print s
        self.assertEqual(s, """\
==================== =========== =======
 When                 State       No.
-------------------- ----------- -------
 Mon 03/02/2014       Suggested   3
 **Total (1 rows)**               **3**
==================== =========== =======

""")

        # delete all lessons and start again with a virgin series

        cal.Event.objects.filter(event_type=lesson).delete()

        check_update(obj, """
Update Events for Activity #1...
Generating events between 2014-01-13 and 2020-05-22 (max. 5).
Lesson 4 wants 2014-02-03 but conflicts with <QuerySet [Event #8 ('Recurring event #1 National Day')]>, moving to 2014-02-10. 
Update Guests for Activity #1 Lesson 1...
0 row(s) have been updated.
Update Guests for Activity #1 Lesson 2...
0 row(s) have been updated.
Update Guests for Activity #1 Lesson 3...
0 row(s) have been updated.
Update Guests for Activity #1 Lesson 4...
0 row(s) have been updated.
Update Guests for Activity #1 Lesson 5...
0 row(s) have been updated.
5 row(s) have been updated.
""", """
================ =========== ===================
 When             State       Short description
---------------- ----------- -------------------
 Mon 13/01/2014   Suggested   Lesson 1
 Mon 20/01/2014   Suggested   Lesson 2
 Mon 27/01/2014   Suggested   Lesson 3
 Mon 10/02/2014   Suggested   Lesson 4
 Mon 17/02/2014   Suggested   Lesson 5
================ =========== ===================
""")

        # we move the first lesson one week down and set it to draft:
        
        e = cal.Event.objects.get(event_type=lesson, auto_type=1)
        e.state = cal.EntryStates.draft
        e.start_date = i2d(20140120)
        e.full_clean()
        e.save()

        check_update(obj, """
Update Events for Activity #1...
Generating events between 2014-01-27 and 2020-05-22 (max. 5).
Lesson 3 wants 2014-02-03 but conflicts with <QuerySet [Event #8 ('Recurring event #1 National Day')]>, moving to 2014-02-10. 
0 row(s) have been updated.
        """, """
================ =========== ===================
 When             State       Short description
---------------- ----------- -------------------
 Mon 20/01/2014   Draft       Lesson 1
 Mon 27/01/2014   Suggested   Lesson 2
 Mon 10/02/2014   Suggested   Lesson 3
 Mon 17/02/2014   Suggested   Lesson 4
 Mon 24/02/2014   Suggested   Lesson 5
================ =========== ===================
""")
        
