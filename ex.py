from __future__ import annotations

def get_header(header: file_handler) -> dict:
    header = header.readline()
    header = header.split(';')
    header.pop(0)
    return {field.upper().rstrip('\n'): index
              for index, field in enumerate(header, start=1)}

with open("input1.txt", "r") as f:
    header = get_header(f)
    print(header)
    print(len(header))
    for line in f:
        line = line.split(';')
        line.pop()
        print(line)
        break
    

    
