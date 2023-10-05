import coding


def unif_table(count):
    table = coding.SimpleFrequencyTable([0] * count)
    for i in range(count):
        table.increment(i)
    return table


def test_freq_table(count, total_freq, test_str):
    table = coding.SimpleFrequencyTable([0] * count)

    for i in range(count):
        table.increment(i)

    for data in test_str:
        table.increment(data)

    for _ in range(total_freq - count - len(test_str)):
        table.increment(count - 1)

    return table


def freq_table(count, flag):
    table = coding.SimpleFrequencyTable([0] * count)
    for i in range(count):
        table.increment(i)
    for data in flag:
        table.increment(data)

    return table


def test_total_freq(test_count, check, filename):
    frequencies = unif_table(test_count)
    input = open(filename, 'rb')
    instream = coding.BitInputStream(input)
    decode = coding.ArithmeticDecoder(32, instream)

    data0 = decode.read(frequencies)
    data1 = decode.read(frequencies)

    instream.close()
    input.close()

    if chr(data0) != check or data1 != 0:
        raise Exception()


def test_chr_freq(test_count, check, filename, test_str):
    frequencies = test_freq_table(128, test_count, bytes(test_str, 'ascii'))
    input = open(filename, 'rb')
    instream = coding.BitInputStream(input)
    decode = coding.ArithmeticDecoder(32, instream)

    data0 = decode.read(frequencies)
    data1 = decode.read(frequencies)

    instream.close()
    input.close()

    if chr(data0) != check or data1 != 0:
        raise Exception()


def decompress(flag_str):
    frequencies = freq_table(128, bytes(flag_str, 'ascii'))
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
    text = ''
    for i in range(33, 127):
        text += chr(i)

    # try to decode with total frequency = X
    total_freq = 128
    while True:
        try:
            test_total_freq(total_freq, ' ', f'info/32.dat')
            break
        except:
            total_freq += 1

    print(total_freq)

    # try to get individual character frequencies
    flag_str = ''
    for i in range(len(text)):
        new_str = str(flag_str)
        fail_count = 0
        while True:
            x = text[i]
            print(f'{total_freq}, flag {flag_str} str, {x}')
            try:
                test_chr_freq(total_freq, x, f'info/{ord(x)}.dat', new_str)
                flag_str = new_str
                break
            except:
                new_str += x
                fail_count += 1
                if fail_count > total_freq - 128:
                    flag_str += text[i-1]
                    new_str = str(flag_str)
                    fail_count = 0

    print(flag_str)

    # decode flag
    decompress(flag_str)
