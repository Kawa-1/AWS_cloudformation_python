from __future__ import annotations
# Probably defaultdict will be useful in my case...
from collections import defaultdict

class ZipCodesUS:

    @staticmethod
    def get_state_code(path_to_uszip: str) -> dict:
        """Open the file coressponding to US Zip Codes to get dict where keys are postal_codes and values are
            state_ids

            Parameters
            -----------
            path_to_uszip: str
                path to uszips.csv

            Returns
            -------
            dict
                a dictionary with keys as postal codes and values as state_ids"""

        with open(path_to_uszip, "r") as f:
            state_code = {}
            # skip header
            f.readline()
            for index, line in enumerate(f):
                line = line.split(",")
                # 0 - postal_code; 4 - state_id
                state_code.update({line[0].strip("\""): line[4].strip("\"")})

            return state_code

class VisaApplications:

    def __init__(self, file_input: str):
        self.file_input = file_input

    def get_header(self, header: file_handler) -> dict:
        """Read first line of colon-seperated value file (header) to get the attributes of corresponding fields from data

            Parameters
            ----------
            header: _io.TextIOWrapper (file_handler)
                We are passing just opened file

            Returns
            -------
            dict
                a dictionary of attributes as keys and corresponding indexes in data section as value
                >>> {'CASE_NUMBER': 1, 'CASE_STATUS': 2, 'CASE_SUBMITTED': 3,...}"""

        header = header.readline()
        header = header.split(';')
        # removing unnecessary item from list - blank string
        header.pop(0)
        return {field.upper().rstrip('\n'): index
                for index, field in enumerate(header, start=1)}

    def get_top_10_occupations(self):
        # TODO: implement method and invent idea for it
        output_headers = ("TOP_OCCUPATIONS", "NUMBER_{}_APPLICATIONS".format(self.desired_case_status), "PERCENTAGE")
        with open(self.file_input, "r") as f:
            header = self.get_header(f)
            soc_name_ind = header.get("SOC_NAME")
            case_status_ind = header.get("CASE_STATUS")
            naics_code_ind = header.get("NAICS_CODE")
            # output = defaultdict(list)
            output = {}
            diff_soc_same_naics = defaultdict(list)
            for index, line in enumerate(f):
                line = line.split(";")
                line.pop()
                if line[case_status_ind] == self.desired_case_status:
                    if not output.get(line[naics_code_ind]):
                        # output[line[naics_code_ind]].append([line[soc_name_ind].strip("\""), 1])
                        output.update({line[naics_code_ind]: []})
                        output.get(line[naics_code_ind]).append(line[soc_name_ind].strip("\""))
                        output.get(line[naics_code_ind]).append(1)

                    else:
                        output.get(line[naics_code_ind])[1] += 1

            print(output)

    def get_top_10_states(self):
        # TODO: implement method and invent idea for it
        pass
    

    
