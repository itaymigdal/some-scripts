import frida
import threading
from frida_tools.application import Reactor

hook_script =  """
Interceptor.attach(
    Module.getExportByName("NTDLL.DLL", 'NtDelayExecution'), 
    {
        onEnter: function (args) 
        {
            console.log(`[i] NtDelayExecution`);
        }
    }
);
"""

class TreeHooker:
    
    def __init__(self):
        self._stop_requested = threading.Event()
        self._reactor = Reactor(run_until_return=lambda reactor: self._stop_requested.wait())
        self._device = frida.get_local_device()
        self._sessions = set()
        self._device.on("child-added", lambda child: self._reactor.schedule(lambda: self._on_child_added(child)))

    def run(self, program):
        self._reactor.schedule(lambda: self._start(program))
        self._reactor.run()

    def _start(self, program):
        pid = self._device.spawn(program)
        self._instrument(pid)

    def _stop_if_idle(self):
        if len(self._sessions) == 0:
            self._stop_requested.set()

    def _instrument(self, pid):
        print(f"[>] Attaching {pid}")
        session = self._device.attach(pid)
        session.on("detached", lambda reason: self._reactor.schedule(lambda: self._on_detached(pid, session, reason)))
        session.enable_child_gating()
        script = session.create_script(hook_script)
        script.load()
        self._device.resume(pid)
        self._sessions.add(session)

    def _on_child_added(self, child):
        self._instrument(child.pid)

    def _on_detached(self, pid, session, reason):
        print(f"[<] Detaching {pid}")
        self._sessions.remove(session)
        self._reactor.schedule(self._stop_if_idle, delay=0.5)


hooker = TreeHooker()
hooker.run("malware.exe")