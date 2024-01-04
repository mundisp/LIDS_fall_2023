class Frame:

    def unpack(self, array):
        namesize = int(array[0:2])
        array = array[2:]
        name = array[:namesize].decode()
        array = array[namesize:]
        textsize = int(array[0:8])
        array = array[8:]
        text = array[:textsize]
        return name, text


    def pack(self, name, message):
        array = bytearray()
        array += (f'{len(name):02d}'.encode())
        array += (f'{name}'.encode())
        array += (f'{len(message):08d}'.encode())
        array += message
        return array
    


