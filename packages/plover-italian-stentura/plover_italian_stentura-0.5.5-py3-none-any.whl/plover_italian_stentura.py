
import struct
import binascii

import plover.machine.base
from plover import log


STENO_KEY_CHART = (
    None, 'S-', 'T-', 'K-', 'P-', 'W-', 'H-', 'R-',
    None, 'A-', 'O-', '*' , '-E', '-U', '-F', '-R',
    None, '-P', '-B', '-L', '-G', '-T', '-S', '-D',
    None, '-Z', '#' , None, None, None, None, None,
)


def _decode(raw):
    stroke = []
    mask = struct.unpack('<I', raw)[0]
    if (mask & 1) == 0:
        return []
    for n, key in enumerate(STENO_KEY_CHART):
        if key is None:
            continue
        if (mask & (1 << n)) != 0:
            stroke.append(key)
    return stroke


class ItalianStentura(plover.machine.base.SerialStenotypeBase):

    KEYMAP_MACHINE_TYPE = 'Stentura'

    KEYS_LAYOUT = '''
        #  #  #  #  #  #  #  #  #  #
        S- T- P- H- * -F -P -L -T -D
        S- K- W- R- * -R -B -G -S -Z
              A- O-   -E -U
        ^
    '''

    def __init__(self, params):
        plover.machine.base.SerialStenotypeBase.__init__(self, params)

    def run(self):
        self._ready()
        while not self.finished.isSet():
            raw = self.serial_port.read(4)
            if not raw:
                continue
            log.debug('raw: %s', binascii.hexlify(raw))
            if len(raw) != 4:
                continue
            keys = _decode(raw)
            log.debug('keys: %r', keys)
            if not keys:
                continue
            steno_keys = self.keymap.keys_to_actions(keys)
            log.debug('steno keys: %r', steno_keys)
            if not steno_keys:
                continue
            self._notify(steno_keys)
