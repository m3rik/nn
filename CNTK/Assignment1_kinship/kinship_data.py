import numpy as np
import pprint
import random

kinship_path = "../data/kinship/kinship.data"
DEBUG = True


def read_rawdata():
    f = open(kinship_path, 'rt')
    rows = f.readlines()
    f.close()

    #filtering blank lines
    rows = filter(lambda x: len(x) > 1, rows)

    #replacing characters with separator
    rows = map(lambda x: x.replace("(", "#").replace(")\n","").replace(", ", "#"), rows)

    #spliting by separator
    rows = map(lambda x: x.split("#"), rows)

    # reorganize as Person Relation Person
    rows = map(lambda x: [x[1], x[0], x[2]], rows)

    return list(rows)


def encoding(dataset, indexes):
    inst_set = set()
    for row in dataset:
        for i in indexes:
            inst_set.add(row[i])

    inst_set = list(inst_set) #set does not support indexing
    inst_set = sorted(inst_set)

    enc = {}
    enc_len = len(inst_set)

    for i in range(enc_len):
        e = np.zeros(enc_len, dtype=np.float32)
        e[i] = 1
        enc[inst_set[i]] = e

    return enc


def reverse_encoding(dict, value):
    for key in dict:
        if np.array_equal(dict[key], value):
            return key
    return None



def kinship_dataset(shuffle=True, verbose=True):
    dataset = {}
    rows = read_rawdata()

    p_enc = encoding(rows, [0, 2])
    r_enc = encoding(rows, [1])

    p1 = list(map(lambda x: p_enc[x[0]], rows))
    r = list(map(lambda x: r_enc[x[1]], rows))
    p2 = list(map(lambda x: p_enc[x[2]], rows))

    ds_len = len(rows)

    if shuffle:
        for i in range(ds_len):
            i1 = random.randint(0, ds_len - 1)
            i2 = random.randint(0, ds_len - 1)
            p1[i1], p1[i2] = p1[i2], p1[i1]
            r[i1], r[i2] = r[i2], r[i1]
            p2[i1], p2[i2] = p2[i2], p2[i1]


    dataset['raw'] = rows
    dataset['enc_persons'] = p_enc
    dataset['enc_relations'] = r_enc
    dataset['p1'] = np.array(p1).astype(dtype=np.float32)
    dataset['r'] = np.array(r).astype(dtype=np.float32)
    dataset['p2'] = np.array(p2).astype(dtype=np.float32)
    dataset['len'] = ds_len

    if verbose:
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(dataset)

        for i in range(ds_len):
            print(reverse_encoding(r_enc, r[i]) + " " + reverse_encoding(p_enc, p1[i]) + " " + reverse_encoding(p_enc, p2[i]))


    return dataset


if __name__ == '__main__':
    kinship_dataset()
