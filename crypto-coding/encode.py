import coding


def unif_table(count):
    table = coding.SimpleFrequencyTable([0] * count)
    for i in range(count):
        table.increment(i)
    return table


def compress(flag):
    frequencies = unif_table(128)
    output = open('flag.compressed', 'wb')
    outstream = coding.BitOutputStream(output)
    encode = coding.ArithmeticEncoder(32, outstream)

    for data in flag:
        encode.write(frequencies, data)
    encode.write(frequencies, 0)

    encode.finish()
    outstream.close()
    output.close()


if __name__ == '__main__':
    # read flag
    with open(file='flag.txt', mode='rb') as f:
        flag = f.read()

    # encode flag
    compress(flag)
