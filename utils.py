import struct

# To get string from message.
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

def encode_labels(name):
    labels = name.split('.')

    encoded_label = b""
    for label in labels:
        length = int(len(label))
        encoded_label += length.to_bytes(1, byteorder='big')
        encoded_label += label.encode()
    
    encoded_label += (0).to_bytes(1, byteorder='big')
    return encoded_label


## EXPERIMENTAL ENCODE LABELS WITH COMPRESSION
def new_encode_labels(name, all_packet_labels):
    labels = name.split('.')

    encoded_label = b""
    for label in labels:
        if (all_packet_labels[label] != None):
            # It means that label has been used before and we can use compression
            starting_byte = all_packet_labels[label]
            bytes_to_put = starting_byte & 0xc000
            encoded_label += bytes_to_put.to_bytes(2, byteorder='big')
            continue

        # label is not present already, so we add it now
        all_packet_labels[label] = len(encoded_label)
        length = int(len(label))
        encoded_label += length.to_bytes(1, byteorder='big')
        encoded_label += label.encode()
    
    encoded_label += (0).to_bytes(1, byteorder='big')
    return encoded_label


def combine_labels(labels):
    return b'.'.join(labels).decode()