from diskhash import Str2int, StructHash
from os import unlink

filename = 'testing.dht'

def test_insert_check():
    ht = Str2int(filename, 17, 'rw')

    items = [
            ('one', 1),
            ('two', 2),
            ('three', 3),
            ('four', 4),
            ('five', 5),
            ('six', 6),
            ('seven', 7),
            ('eight', 8),
            ('nine', 9),
            ('ten', 10),
            ('eleven', 11),
            ]

    for k,v in items:
        assert ht.lookup(k) is None

    for k,v in items:
        ht.insert(k, v)

    for k,v in items:
        assert ht.lookup(k) == v
    del ht

    ht = Str2int(filename, 17, 'r')
    for k,v in items:
        assert ht.lookup(k) == v
    del ht

    unlink(filename)

def test_insert_check_two_ints():
    ht = StructHash(filename, 17, 'll', 'rw')

    items = [
            ('one', (1,2)),
            ('two', (2,3)),
            ('three', (3,4)),
            ('four', (4,0)),
            ('five', (5,0)),
            ('six', (6,0)),
            ('seven', (7,0)),
            ('eight', (8,0)),
            ('nine', (9,0)),
            ('ten', (10,0)),
            ('eleven', (11,0)),
            ]

    for k,v in items:
        assert ht.lookup(k) is None

    for k,v in items:
        ht.insert(k, *v)

    for k,v in items:
        assert ht.lookup(k) == v
    del ht

    ht = StructHash(filename, 17, 'll', 'r')
    for k,v in items:
        assert ht.lookup(k) == v
    del ht

    unlink(filename)
