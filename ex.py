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

    @staticmethod
    def get_header(header: file_handler) -> dict:
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

    @staticmethod
    def get_percent(item: list, index: int, totality: int) -> list:
        percent_col = "{:.1f}".format(item[1][index]/totality * 100)
        item[1].append(percent_col + "%")
        return item

    def write_top_10_occupations(self):
    # TODO: implement method and invent idea for it
        output_headers = ("TOP_OCCUPATIONS", "NUMBER_{}_APPLICATIONS".format(self.desired_case_status), "PERCENTAGE")

        with open(self.file_input, "r") as f:
            header = self.get_header(f)
            soc_name_ind = header.get("SOC_NAME")
            case_status_ind = header.get("CASE_STATUS")
            naics_code_ind = header.get("NAICS_CODE")

            output_data = {}
            diff_soc_same_naics = {}
            # Used to determine if more than one occupation for top_10_occupation occurs for specific naics_code
            another_top_occupation = set()
            count_desired_case_status = 0

            for index, line in enumerate(f):
                line = line.split(";")
                line.pop()
                # Percentage is being calculated on the same case_status
                if line[case_status_ind] == self.desired_case_status:
                    count_desired_case_status += 1
                    # Handling multiple occupations for same naics_code

                    if output_data.get(line[naics_code_ind]) and output_data.get(line[naics_code_ind])[0] != line[soc_name_ind]:
                       if diff_soc_same_naics.get(line[naics_code_ind]) and line[soc_name_ind] in another_top_occupation:
                           for index, occupation in enumerate(diff_soc_same_naics.get(line[naics_code_ind])):
                               # occupation[0] is the soc_name and occupation[1] are the occurences of this specific soc_name
                               if occupation[0] == line[soc_name_ind].strip("\""):
                                   occupation[1] += 1
                                   break

                       elif not diff_soc_same_naics.get(line[naics_code_ind]):
                           diff_soc_same_naics.update({line[naics_code_ind]: []})
                           diff_soc_same_naics.get(line[naics_code_ind]).append([line[soc_name_ind].strip("\""), 1])
                           another_top_occupation.add(line[soc_name_ind])

                       # If it is the first occurence of another occupation or same naics code
                       else:
                           diff_soc_same_naics.get(line[naics_code_ind]).append([line[soc_name_ind].strip("\""), 1])
                           another_top_occupation.add(line[soc_name_ind])

                    elif not output_data.get(line[naics_code_ind]):
                        output_data.update({line[naics_code_ind]: []})
                        output_data.get(line[naics_code_ind]).extend([line[soc_name_ind].strip("\""), 1])

                    else:
                        output_data.get(line[naics_code_ind])[1] += 1

                else:
                    continue

            # TODO: Need to implement the loop to find soc_name with most occurences by naics_code

            # Desired sorting with descending number and ascending string, just in case if numbers are equal
            output_data = sorted(output_data.items(), key=lambda elem: (-elem[1][1], elem[1][0]))
            # Adding column involved with percentage
            output_data = list(map(lambda x: self.get_percent(x, 1, count_desired_case_status), output_data))

            with open("output.txt", "w") as f_out:
                output_headers = ";".join(map(str, output_headers))
                f_out.write(output_headers + "\n")
                for data in output_data:
                    data = ";".join(map(str, data[1]))
                    f_out.write(data + "\n")

        def get_top_10_states(self):
        # TODO: implement method and invent idea for it
        output_headers = ("TOP_STATES", "NUMBER_{}_APPLICATIONS".format(self.desired_case_status), "PERCENTAGE")
        with open(self.file_input, "r") as f:
            header = get_header(f)
            worksite_postal_code_ind = header.get("WORKSITE_POSTAL_CODE")
            case_status_ind = header.get("CASE_STATUS")
            state_code = ZipCodesUS.get_state_code("uszips.csv")
            output_data = {}
            count_desired_case_status = 0
            for index, line in enumerate(f):
                line = line.split(";")
                line.pop()
                if line[case_status_ind] == self.desired_case_status:
                    count_desired_case_status += 1
                    pass
    

    
