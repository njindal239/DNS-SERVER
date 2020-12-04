import struct

"""
Decodes labels into strings according to DNS host name
rules
"""
def decode_labels(message, offset):
    labels = []
    while True:
        # Getting length of string.
        length, = struct.unpack_from("!B", message, offset)

        # Recursively calling this method if it points to another address.
        if (length & 0xC0) == 0xC0:
            pointer, = struct.unpack_from("!H", message, offset)
            offset += 2

            return labels + decode_labels(message, pointer & 0x3FFF)[0], offset

        # Calling this method if it's poiting to another address.
        if (length & 0xC0) != 0x00:
            # return labels + decode_labels(message, offset+1)[0], offset
            decode_labels(message,offset+1)

        offset += 1

        if length == 0:
            return labels, offset

        # Decoding string from hex.
        labels.append(*struct.unpack_from("!%ds" % length, message, offset))
        offset += length

"""
Splits a name into labels and then encodes it according to
DNS host name encoding rules
"""
def encode_labels(name):
    labels = name.split('.')

    encoded_label = b""
    for label in labels:
        length = int(len(label))
        encoded_label += length.to_bytes(1, byteorder='big')
        encoded_label += label.encode()
    
    encoded_label += (0).to_bytes(1, byteorder='big')
    return encoded_label


"""
Combines a list of labels to return a host name
"""
def combine_labels(labels):
    return b'.'.join(labels).decode()