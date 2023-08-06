import logging
import util
from settings import settings
import re
import threading
import time
from state import State
import subprocess
import shlex
import os

class Drasi:
    def __init__(self, *args, **kwargs):

        self.SSH_TARGET, self.PASS = kwargs.get("ssh_target")
        self.DIR = kwargs.get("directory")
        self.command = kwargs.get("command")
        self.user = kwargs.get("user")
        self.log_file = kwargs.get("log_file")

        self.start_cmd = 'ssh {}@{} "cd {} && {}"'.format(self.user, self.SSH_TARGET, 
                                                          self.DIR, self.command)
        self.mon_cmd = '{} {} --rate --count=2'.format(settings['drasi']['lwrocmon'], settings['readout']['hostname'])

        self.log_cmd = '{} {} --log="{}"'.format(settings['drasi']['lwrocmon'], settings['readout']['hostname'], self.log_file)

        FNULL = open(os.devnull, 'w')
        subprocess.Popen(shlex.split(self.log_cmd), close_fds=True, stdout=FNULL, stderr=FNULL)

        self.log = logging.getLogger("backend")

        self.start_process = None
      
        self._running = None
        self._stopped = None

        self._rate_events = 0
        self._rate_data = 0

        self.monitor()
        
        t = threading.Thread(target=self.do_watch)
        t.daemon = True
        t.start()

    def monitor(self):
        p = util.ReturningCommand(self.mon_cmd).run().get()
        if "Connection refused" in p[1]:
            self._running = False
            self._rate_events = self._rate_data = "Down"
        else:
            self._running = True
            s = p[0].split("\n")
            m = re.search("^\s*(\w*)\s*[0-9:]*\s*(\d*)\s*(\d*)\s*(\d+\.?\d*)[kM]?\s*(\d+\.?\d*)\%\s*(\d+.?\d*)[kM]?", s[4])
            if m is not None:
                self._rate_events = int(m.group(3))
                self._rate_data = float(m.group(4))
            else:
                self._rate_events = self._rate_data = "Parse error"

    def do_watch(self):
        while 1:
            try:
                self.monitor()        
            except:
                pass

    def is_running(self):
        return self._running

    def start(self):
        self._stopped = False
        if self._running is None:
            self.monitor()
        if self._running:
            self.log.info("Drasi already running!")
        else:
            self.log.info("Starting Drasi")
            self.start_process = util.ReturningCommand(self.start_cmd)
            self.start_process.run()
            start_time = time.time()
            while not self.is_running():
                t = time.time() - start_time
                self.log.debug("Waiting for drasi {}".format(t))
                if t > settings['readout']['start_up_timeout']:
                    self.log.warning("Drasi startup timed out (60s)")
                    return
                time.sleep(settings['readout']['wait_time'])

            self.log.info("Started Drasi")

    def stop(self):
        self.log.info("Stopping Drasi")
        self.start_process.terminate()
        self.start_process = None
        self._stopped = True
        self.log.info("Stopped Drasi")

    def status(self):
        return {'bl_r_events' : self._rate_events,
                'bl_r_kbyte'  : self._rate_data}

    def state(self):
        if self._stopped:
            if self.is_running():
                return State.STOPPING
            elif self._stopped is None:
                return State.STANDBY
            else:
                return State.STOPPED
        else:
            if self.is_running():
                return State.RUNNING
            else:
                return State.CRASHED


class MockDrasi:
    def __init__(self, **_):
        self.running = None
        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created MockDrasi")

    def stop(self):
        self.backend_log.info("Stopping MockDrasi")
        self.running = False
        self.backend_log.info("Stopping MockDrasi - done")

    def start(self):
        self.backend_log.info("Starting MockDrasi")
        self.running = True
        self.backend_log.info("Starting MockDrasi - done")

    def is_running(self):
        return self.running

    @staticmethod
    def status():
        interesting = ['bh_acqui_started', 'bh_acqui_running', 'bl_n_events',
                       'bl_n_kbyte', 'bl_n_strserv_kbytes', 'bl_r_events',
                       'bl_r_kbyte', 'bl_r_strserv_kbytes', 'bl_pipe_size_KB',
                       'bl_pipe_size_KB', 'bl_pipe_filled_KB']

        result = {}
        for i in interesting:
            result[i] = 0

        return result

    def state(self):
        if self.running is None:
            return State.STANDBY
        elif self.running:
            return State.RUNNING
        else:
            return State.STOPPED

