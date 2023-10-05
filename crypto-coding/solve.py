import coding


def unif_table(count):
    table = coding.SimpleFrequencyTable([0] * count)
    for i in range(count):
        table.increment(i)
    return table


def decompress():
    frequencies = unif_table(128)
    input = open('flag.compressed', 'rb')
    instream = coding.BitInputStream(input)
    decode = coding.ArithmeticDecoder(32, instream)
    flag = ''

    while True:
        data = decode.read(frequencies)
        if data == 0:
            break
        flag += chr(data)

    print(flag)

    instream.close()
    input.close()


if __name__ == '__main__':
    # decode flag
    decompress()
