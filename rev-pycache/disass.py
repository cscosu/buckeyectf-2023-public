import dis
import marshal
import struct
import sys

print(sys.version)
ver = sys.version_info
with open(f'chal/__pycache__/backend.cpython-{ver[0]}{ver[1]}.pyc', 'rb') as f:  # Read the binary file
    magic = f.read(4)
    bitfield = f.read(4)
    timestamp = f.read(4)
    size = f.read(4)
    code = f.read()

# Unpack the structured content and un-marshal the code
magic = struct.unpack('<I', magic)
timestamp = struct.unpack('<I', timestamp)
size = struct.unpack('<I', size)
print(f"magic: {hex(magic[0])}, bitfield: {bitfield}, timestamp: {timestamp}, size: {size}")
print(f"")
print(f"code: {code}")


code = marshal.loads(code)
print(f"Code2: {code}")

# Verify if the magic number corresponds with the current python version
#struct.unpack('<H', imp.get_magic()[:2]) == magic


# Disassemble the code object
print(dis.dis(code))

