# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-basic-process-queuing entity's classes"""

from cubicweb.predicates import on_fire_transition
from cubicweb.server import hook


class RunCompleteHook(hook.Hook):
    __regid__ = 'processing.test.run.complete'
    __select__ = hook.Hook.__select__ & on_fire_transition('Run', 'wft_run_run')
    events =  ('after_add_entity',)

    def __call__(self):
        run = self.entity.for_entity
        # exec arbitrary python code if specified
        if run.exe.python_code:
            run.set_ovalues(o=eval(run.exe.python_code, {'run': run}))
