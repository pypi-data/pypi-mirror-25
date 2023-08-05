import os
import time
import threading
from oslo_log import log as logging
LOG = logging.getLogger(__name__)


class RemoteShell:
    _lock_known_hosts = threading.Lock()

    def __init__(self, host, user, pwd):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.cur_cmd = None

        self.expect_pwd = [
            'expect {',
            '"(yes/no)?"\n{send "yes\n"; exp_continue}',
            '"*assword:"\n{send "%s\n"; exp_continue}' % self.pwd,
            '"No such file or directory"\n{exit -1}',
            '"eof"\n{exit}',
            '}',
        ]

    def _make_expect(self, cmd):
        self.cur_cmd = cmd
        LOG.info('RemoteShell: %s', cmd)

        filename = 'expect.%s.%s.cmd' % (self.host, time.time())
        f = open(filename, 'w')

        f.write('#!/usr/bin/expect\nset timeout -1\n')
        f.write('spawn %s\n' % cmd)
        for item in self.expect_pwd:
            f.write(item)
            f.write('\n')
        f.write('exit\n')

        f.close()

        return filename

    def _do_expect(self, cmd):
        filename = self._make_expect(cmd)

        r = -1
        cmd = 'expect %s' % filename
        for i in range(5):
            r = os.system(cmd + ' >> /var/log/storagemgmt/expect.%s.log' % self.host)
            if r == 0:
                os.remove(filename)
                return
            else:
                LOG.error('RemoteShell execute {%s} [ctxt: %s] fail! Retry(%s)...', cmd, self.cur_cmd, i)
        raise Exception("execute cmd fail[%s](%s)!" % (cmd, r))

    def _remove_known_host(self):
        # Avoid offending key with old record
        r = -1
        try:
            self._lock_known_hosts.acquire()
            r = os.system("sed -i '/%s/d' /root/.ssh/known_hosts" % self.host)
        except Exception as e:
            LOG.error('RemoteShell _remove_known_host fail! (r=%s)(err=%s)', r, e)
            raise Exception("RemoteShell _remove_known_host fail!")
        finally:
            self._lock_known_hosts.release()

    def put(self, local_path, remote_path):
        self._remove_known_host()
        cmd = 'scp %s %s@%s:%s' % (os.path.expanduser(local_path), self.user, self.host, remote_path)
        self._do_expect(cmd)

    def get(self, remote_path, local_path):
        cmd = 'scp %s@%s:%s %s' % (self.user, self.host, remote_path, os.path.expanduser(local_path))
        self._do_expect(cmd)

    def execute(self, cmd):
        cmd = 'ssh %s@%s %s' % (self.user, self.host, cmd)
        self._do_expect(cmd)

# a = RemoteShell(host="10.20.0.10", user="root", pwd="lenovo")
# a.put("/tmp/InstallCeph-suse12.tar.gz","/tmp/InstallCeph-suse12.tar.gz")
