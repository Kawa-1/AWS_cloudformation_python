from __future__ import annotations

def get_header(header: file_handler) -> dict:
    """Read first line of file (header) to get the attributes of corresponding fields from data

        Parameters
        ----------
        header: file_handler, _io.TextIOWrapper
            We are passing just opened file

        Returns
        -------
        dict
            a dictionary of attributes as keys and corresponding indexes in data section as value
            >>> {'CASE_NUMBER': 1, 'CASE_STATUS': 2, 'CASE_SUBMITTED': 3,...}"""
    
    header = header.readline()
    header = header.split(';')
    # removing unnecessary item from list; blank string
    header.pop(0)
    return {field.upper().rstrip('\n'): index
              for index, field in enumerate(header, start=1)}

print(help(get_header))

with open("input1.txt", "r") as f:
    header = get_header(f)
    print(header)
    print(len(header))
    for line in f:
        line = line.split(';')
        line.pop()
        print(line[header.get("CASE_STATUS")])
    

    
