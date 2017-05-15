# encoding; utf-8

from . import util

__author__ = "BetaS"

BATMAN_MTU = 1532


class BATMAN:
    def __init__(self, name="bat0"):
        self.name = name
        self.iface = {}

    def _run(self, cmd=[]):
        proc = ["batctl", "-m", self.name]
        proc.extend(cmd)
        return util.run_command(proc)

    def status(self):
        msg = self._run(["if"])
        lines = list(map(lambda x: list(map(lambda y: y.strip(), x.split(":"))), msg))
        return dict((v[0], v[1]) for v in lines)

    def if_add(self, dev):
        if dev in self.iface:
            return True

        result = self._run(["if", "add", dev])

        if len(result) == 0:
            self.iface[dev] = {"mtu": util.mtu_get(dev)}
            return True
        else:
            return False

    def if_del(self, dev):
        result = self._run(["if", "del", dev])

        if len(result) == 0:
            return True
        else:
            return False

    def is_up(self):
        pass

    def nodes(self):
        msg = self._run(["o"])
        for line in msg:
            print(line)


if __name__ == "__main__":
    batman = BATMAN("bat0")
    print(batman.status())
    batman.if_add("wlan0")