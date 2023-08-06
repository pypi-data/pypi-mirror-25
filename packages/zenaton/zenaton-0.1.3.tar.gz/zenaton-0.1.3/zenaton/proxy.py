from __future__ import absolute_import, print_function, unicode_literals

from zenaton.serialization import (
    get_class_path,
    serialize,
)


class Signal:
    KILL = 'kill'
    PAUSE = 'pause'
    RUN = 'run'


class WorkflowProxy:

    def __init__(self, api, id, name):
        self.api = api
        self.id = id
        self.name = name

    def send_event(self, event):
        return self.api.send_event(
            workflow_name=self.name,
            event_name=get_class_path(event.__class__),
            event_input=serialize(event),
            custom_id=self.id,
        )

    def kill(self):
        return self._send_signal(Signal.KILL)

    def pause(self):
        return self._send_signal(Signal.PAUSE)

    def resume(self):
        return self._send_signal(Signal.RUN)

    def _send_signal(self, signal):
        return self.api.update_workflow_instance(self.id, self.name, signal)

    # def get_properties(self):
    #     res = self.api.get_workflow_instance(self.id, self.name)
    #     return deserialize(res['instance'])
