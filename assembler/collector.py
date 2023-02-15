import reader
import writer

PROGRAMM = []

for entry in reader.ent:
    PROGRAMM.append(getattr(writer, entry[1])(*entry[2]))

programm = writer.flatten(PROGRAMM)