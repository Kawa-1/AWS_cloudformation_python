from __future__ import annotations
import time

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

def top_ten_occupations(filename: str):
    pass

with open("others/uszips.csv", "r") as f:
    start = time.perf_counter()
    state_code = {}
    # skip header
    f.readline()
    for nr_row, line in enumerate(f):
        line = line.split(",")
        # indexes: 0 - postal_code; 4 - state_id
        state_code.update({line[0].strip("\""): line[4].strip("\"")})

    end = time.perf_counter()
    print(end - start)
    print(state_code)


with open("input_files/input1.txt", "r") as f:
    print(type(f))
    header = get_header(f)
    print(header)
    print(len(header))
    for line in f:
        line = line.split(';')
        line.pop()
        print(line[header.get("WORKSITE_STATE")], line[header.get("WORKSITE_POSTAL_CODE")], "|", line[header.get("SOC_NAME")],
            "?", line[header.get("NAICS_CODE")], sep=" ")
    

    
