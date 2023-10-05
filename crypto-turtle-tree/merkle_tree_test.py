from merkle_tree import *
import hashlib
import struct
import random
from collections import Counter


def test_one_entry():
    m = MerkleTree()

    key = b"key"
    value = b"value"
    index = bits_to_bytes([0, 1, 0, 1])

    m.set(index, key, value)

    # Check right hash (empty node)
    h = hashlib.sha256(
        empty_node_identifier
        + m.nonce
        + bits_to_bytes([1])
        + struct.pack("<I", 1)
    ).digest()
    assert h == m.root.right_hash

    ap = m.get(index)
    assert ap.tree_nonce == m.nonce
    assert ap.lookup_index == index
    assert len(ap.pruned_tree) == 1
    assert ap.pruned_tree[0] == m.root.right_hash
    assert ap.leaf.index == index
    assert ap.leaf.level == 1
    assert ap.leaf.value == value

    # Check left hash (leaf node)
    h = hashlib.sha256(
        leaf_node_identifier
        + ap.tree_nonce
        + index
        + struct.pack("<I", 1)
        + value
    ).digest()
    assert h == m.root.left_hash
    assert hashlib.sha256(h + ap.pruned_tree[0]).digest() == m.root_hash

    # Verify authentication path
    result, error = ap.verify(value, m.root_hash)
    assert error == None
    assert result == True
    assert ap.proof_type() == AuthenticationPath.proof_of_inclusion

    # Test getting a key that doesn't exist in the tree
    ap = m.get(bits_to_bytes([0, 1]))
    assert len(ap.pruned_tree) == 1
    assert ap.pruned_tree[0] == m.root.right_hash
    assert ap.leaf.level == 1
    assert ap.leaf.value == value

    result, error = ap.verify(value, m.root_hash)
    assert result == True
    assert error == None
    assert ap.proof_type() == AuthenticationPath.proof_of_absence

    result, error = ap.verify(b"blah", m.root_hash)
    assert result == True
    assert error == None



def test_two_entries():
    m = MerkleTree()

    key1 = b"key1"
    value1 = b"value1"
    index1 = bits_to_bytes([1, 1, 0, 1])

    key2 = b"key2"
    value2 = b"value2"
    index2 = bits_to_bytes([1, 0, 0, 1])

    m.set(index1, key1, value1)
    m.set(index2, key2, value2)

    ap1 = m.get(index1)
    ap2 = m.get(index2)

    assert type(m.root.right_child) is InteriorNode
    assert type(m.root.right_child.left_child) is LeafNode
    assert m.root.right_child.left_child.key == key2
    assert type(m.root.right_child.right_child) is LeafNode
    assert m.root.right_child.right_child.key == key1

    assert ap1.leaf.value == value1
    assert ap2.leaf.value == value2

    result, error = ap1.verify(value1, m.root_hash)
    assert result == True
    assert error == None

    result, error = ap2.verify(value2, m.root_hash)
    assert result == True
    assert error == None


def test_three_entries():
    m = MerkleTree()

    key1 = b"key1"
    value1 = b"value1"
    index1 = bits_to_bytes([1, 1, 0, 1])

    key2 = b"key2"
    value2 = b"value2"
    index2 = bits_to_bytes([1, 0, 0, 1])

    key3 = b"key3"
    value3 = b"value3"
    index3 = bits_to_bytes([0, 0, 1, 1])

    m.set(index1, key1, value1)
    m.set(index2, key2, value2)
    m.set(index3, key3, value3)

    ap1 = m.get(index1)
    ap2 = m.get(index2)
    ap3 = m.get(index3)

    assert ap1.leaf.value == value1
    assert ap2.leaf.value == value2
    assert ap3.leaf.value == value3

    result, error = ap1.verify(value1, m.root_hash)
    assert result == True
    assert error == None

    result, error = ap2.verify(value2, m.root_hash)
    assert result == True
    assert error == None

    result, error = ap3.verify(value3, m.root_hash)
    assert result == True
    assert error == None


def test_random_entries():
    random.seed(0)

    m = MerkleTree()
    n_entries = 1024

    store = {}  # index -> (key, value)

    for i in range(n_entries):
        key = f"key{i}".encode()
        value = f"value{i}".encode()
        index = random.randbytes(2)
        m.set(index, key, value)

        h = m.root_hash
        m.ignore_stored_hashes = True
        assert h == m.root_hash
        m.ignore_stored_hashes = False

        store[index] = (key, value)

    for index in store:
        key, value = store[index]
        ap = m.get(index)
        assert ap.leaf.value == value

        result, error = ap.verify(value, m.root_hash)
        assert result == True
        assert error == None


def test_overwrite_entry():
    m = MerkleTree()

    key1 = b"key1"
    value1 = b"value1"
    index1 = bits_to_bytes([1, 1, 0, 1])

    key2 = b"key2"
    value2 = b"value2"
    index2 = bits_to_bytes([1, 0, 0, 1])

    key1_new = b"key1_new"
    value1_new = b"value1_new"

    m.set(index1, key1, value1)
    m.set(index2, key2, value2)
    m.set(index1, key1_new, value1_new)

    ap1 = m.get(index1)
    ap2 = m.get(index2)

    assert ap1.leaf.value == value1_new
    assert ap2.leaf.value == value2

    result, error = ap1.verify(value1_new, m.root_hash)
    assert result == True
    assert error == None

    result, error = ap2.verify(value2, m.root_hash)
    assert result == True
    assert error == None


def main():
    test_one_entry()
    test_two_entries()
    test_three_entries()
    test_overwrite_entry()
    test_random_entries()


if __name__ == "__main__":
    main()
