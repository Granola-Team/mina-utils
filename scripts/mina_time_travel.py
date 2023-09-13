'''
Conversion between different time units for the Mina Protocol

ISO-8601 <-> epochs <-> slots <-> ms ticks
'''

import json
import argparse
from datetime import datetime

# Notes on epochs
# - 1 month ~ 2 epochs
# - an epoch lasts 14 days, 21 hours
# - each slot lasts 3 minutes (180_000 ms)

SLOTS_PER_EPOCH = 7140
TICKS_PER_SLOT  = 180_000
TICKS_PER_EPOCH = TICKS_PER_SLOT * SLOTS_PER_EPOCH
GENESIS_TICKS   = 1615935600000

def iso8601_to_datetime(iso: str):
    '''
    Parse ISO-8601 DateTime string to datetime object

    Note: this function depends on your machine's local timezone. Adjust accordingly!
    '''
    return datetime.strptime(iso, '%Y-%m-%dT%H:%M:%SZ')

# convert everything to ms

def iso_to_ms(iso: str) -> int:
    """
    Converts ISO-8601 DateTime to ms

    Note: `iso8601_to_datetime` uses local timezone. Adjust accordingly!

    >>> gen_start = iso_to_ms("2021-03-16T19:00:00Z")
    >>> gen_start = GENESIS_TICKS
    """
    dt = iso8601_to_datetime(iso)
    # convert to ms
    return int(dt.timestamp() * 1000)

def epoch_slot_to_ms(epoch_slot: tuple[int, int]) -> int:
    '''
    Converts Mina `(epoch, slot)` to time (ms)
    '''
    epoch = epoch_slot[0]
    slot = epoch_slot[1]
    return GENESIS_TICKS + epoch * TICKS_PER_EPOCH + slot * TICKS_PER_SLOT

def gslot_to_ms(gslot: int) -> int:
    '''
    Converts global Mina slot to time (ms)
    '''
    return int(GENESIS_TICKS + gslot * TICKS_PER_SLOT)

# convert ms to everything

def ms_to_iso(ticks: int):
    '''
    Converts time (ms) to ISO-8601 DateTime
    '''
    # convert back from ms
    dt = datetime.fromtimestamp(ticks // 1000)
    return dt.isoformat()

def ms_to_epoch(ticks: int):
    '''
    Converts time (ms) to Mina `(epoch, slot)`
    '''
    epoch = (ticks - GENESIS_TICKS) // TICKS_PER_EPOCH
    rem_ticks = ticks - GENESIS_TICKS - epoch * TICKS_PER_EPOCH
    return (
        epoch,
        rem_ticks // TICKS_PER_SLOT   # local slot
    )

def ms_to_gslot(ticks: int):
    '''
    Converts time (ms) to global Mina slot
    '''
    return (ticks - GENESIS_TICKS) // TICKS_PER_SLOT

def ms_to_eslot(ticks: int):
    '''
    Converts time (ms) to local (current epoch) Mina slot
    '''
    ticks_into_epoch = (ticks - GENESIS_TICKS) % TICKS_PER_SLOT
    return ticks_into_epoch // TICKS_PER_SLOT

# cli

valid_args = ['e', 'es', 'gs', 'i', 'ms']
valid_cmds = ['epoch', 'slot', 'iso', 'ms']

def gen_from_ms(arg, value):
    '''
    Generic conversion from time (ms)
    '''
    assert arg in valid_args

    res = None
    if arg in {'e', 'es', 'epoch'}:
        res = ms_to_epoch(value)
    if arg in {'gs', 'slot'}:
        res = ms_to_gslot(value)
    if arg in {'i', 'iso'}:
        res = ms_to_iso(value)
    if arg == 'ms':
        res = value
    return res

def gen_to_ms(init_type, value) -> int:
    '''
    Converts the `value` of type `init_type` to ms
    '''
    assert init_type in valid_cmds
    res = value
    if init_type != 'ms':
        if init_type == "epoch":
            assert len(value) == 2
            res = epoch_slot_to_ms(value)
        if init_type == "iso":
            assert len(value) == 1
            res = iso_to_ms(value[0])
        if init_type == "slot":
            assert len(value) == 1
            res = gslot_to_ms(value[0])
    return res

def handlers(args) -> list[str]:
    '''
    The to-be-dispatched handlers for `args`
    '''
    res = []
    for arg in args.keys():
        if arg not in {'input', 'type'}:
            if args[arg]:
                res.append(arg)
    return res

def dispatch(args, res):
    '''
    Applies appropriate handlers

    # TODO: returning [None]
    '''
    args = vars(args)
    arg_t = args["type"]
    input = args["input"]
    # single value (only [0]) for everything except
    # `epoch` which has two values ([0] and [1])

    hdlrs = handlers(args)
    input_ms = gen_to_ms(arg_t, input)
    if not hdlrs:
        hdlrs = valid_args
    res = {}
    for hdlr in hdlrs:
        res[hdlr] = gen_from_ms(hdlr, input_ms)
    print(json.dumps(res, indent=4))
    return res

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # epoch - expand Mina epoch number
    # slot  - expand Mina global slot number
    # iso   - convert iso 8601 date/time to Mina time
    # tick  - convert ms to Mina time
    parser = argparse.ArgumentParser(description="Mina Time Travel Utility - so you don't have to 😎")
    parser.add_argument("-t", "--type", choices=['epoch', 'slot', 'iso', 'ms'], default='iso', help="input type")

    parser.add_argument("-e",  action="store_true", help="convert to Mina epoch number")
    parser.add_argument("-es", action="store_true", help="convert to Mina current epoch slot number")
    parser.add_argument("-gs", action="store_true", help="convert to Mina global slot number")
    parser.add_argument("-i",  action="store_true", help="convert to iso 8601")
    parser.add_argument("-ms", action="store_true", help="convert to ms")
    parser.add_argument("input", type=str, nargs="+")

    # setup results
    epoch = None
    eslot = None
    gslot = None
    ticks = None
    iso   = None
    res   = { "e" : epoch, "es" : eslot, "gs" : gslot, "i" : iso, "ms" : ticks }

    # parse and handle args
    args = parser.parse_args()
    dispatch(args, res)

#############
# resources #
#############
#
# - [Mina time machine](https://towerstake.com/mina-time-machine/)
