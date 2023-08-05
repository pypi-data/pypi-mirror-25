def readfile(fileobject, chunk_size=1024):
    while True:
        data = fileobject.read(chunk_size)
        if not data:
            break
        yield data
