
# Copyright 2015 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Test fixtures.

.. versionadded:: 1.3
"""

import fixtures

from oslo_utils import timeutils


class TimeFixture(fixtures.Fixture):
    """A fixture for overriding the time returned by timeutils.utcnow().

    :param override_time: datetime instance or list thereof. If not given,
                          defaults to the current UTC time.

    """

    def __init__(self, override_time=None):
        super(TimeFixture, self).__init__()
        self._override_time = override_time

    def setUp(self):
        super(TimeFixture, self).setUp()
        timeutils.set_time_override(self._override_time)
        self.addCleanup(timeutils.clear_time_override)

    def advance_time_delta(self, timedelta):
        """Advance overridden time using a datetime.timedelta."""
        timeutils.advance_time_delta(timedelta)

    def advance_time_seconds(self, seconds):
        """Advance overridden time by seconds."""
        timeutils.advance_time_seconds(seconds)
