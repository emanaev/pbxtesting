import errno
import os
import pty
import select
import signal
import subprocess


class OutStream:
    def __init__(self, fileno, tag=None):
        self._fileno = fileno
        self._buffer = b""
        self.tag = tag

    def read_lines(self):
        try:
            output = os.read(self._fileno, 1000)
        except OSError as e:
            if e.errno != errno.EIO: raise
            output = b""
        lines = output.split(b"\n")
        lines[0] = self._buffer + lines[0] # prepend previous
                                           # non-finished line.
        if output:
            self._buffer = lines[-1]
            finished_lines = lines[:-1]
            readable = True
        else:
            self._buffer = b""
            if len(lines) == 1 and not lines[0]:
                # We did not have buffer left, so no output at all.
                lines = []
            finished_lines = lines
            readable = False
        finished_lines = [line.rstrip(b"\r").decode()
                          for line in finished_lines]
        return finished_lines, readable

    def fileno(self):
        return self._fileno


class Monitor:
  def __init__(self):
      self.processes = dict()
      self.fds = list()
      signal.signal(signal.SIGINT, self.shutdown)
      signal.signal(signal.SIGTERM, self.shutdown)

  def shutdown(self, *args):
    print("=== GRACEFUL SHUTDOWN ==")
    for p in self.processes.values():
      p.terminate()

  def start(self, name, cmd):
    if name in self.processes:
      raise Exception('Process [%s] already started' % name)
    out_r, out_w = pty.openpty()
    err_r, err_w = pty.openpty()
    proc = subprocess.Popen(cmd, stdout=out_w, stderr=err_w)
    os.close(out_w)
    os.close(err_w)
    self.processes[name] = proc
    self.fds.append(OutStream(out_r, (name,1)))
    self.fds.append(OutStream(err_r, (name,2)))

  def process(self):
    while self.fds:
        # Call select(), anticipating interruption by signals.
        while True:
            try:
                rlist, _, _ = select.select(self.fds, [], [])
                break
            except InterruptedError:
                continue
        # Handle all file descriptors that are ready.
        for f in rlist:
            lines, readable = f.read_lines()
            for line in lines:
                yield (line, f.tag[0], f.tag[1])
            if not readable:
                self.fds.remove(f)
