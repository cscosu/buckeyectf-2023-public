import coding


def freq_table(count, flag):
    table = coding.SimpleFrequencyTable([0] * count)
    for i in range(count):
        table.increment(i)
    for data in flag:
        table.increment(data)

    return table


def compress(data, output):
    frequencies = freq_table(
        128, b'bctf{gu3ss_fr3qu3ncy_compr3ss10n_1s_n0t_s3cur3_3n0ugh_y3t}')
    output = open(output, 'wb')
    outstream = coding.BitOutputStream(output)
    encode = coding.ArithmeticEncoder(32, outstream)

    encode.write(frequencies, data)
    encode.write(frequencies, 0)

    encode.finish()
    outstream.close()
    output.close()


if __name__ == '__main__':
    # text bytes
    text = ''
    for i in range(32, 127):
        text += chr(i)

    print(text)

    # encode text bytes
    for data in text:
        compress(ord(data), f'info/{ord(data)}.dat')
