from __future__ import annotations


class ZipCodesUS:

    @staticmethod
    def get_state_codes(path_to_uszip: str) -> dict:
        """Open the file coressponding to US Zip Codes to get dict where keys are postal_codes and values are
            state_ids

            Parameters
            -----------
            path_to_uszip: str
                path to uszips.csv

            Returns
            -------
            dict
                a dictionary with keys as postal codes and values as state_ids
        """

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
    """VisaApplications is the Class involved with analysis of US visa application"""

    def __init__(self, file_input: str, desired_case_status: str):
        """Parameters:
            ---------
                file_input: str
                    It is the path for the file involved with US visa application
                    which we want analyze. It must be colon-seperated file.
                desired_case_status: str
                    It is the attribute of person's visa application which we want to analyze in overall. We won't take
                    into consideration other applications which have different desired_case_status than we specified
        """
        self.file_input = file_input
        self.desired_case_status = desired_case_status
        
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
                >>> {'CASE_NUMBER': 1, 'CASE_STATUS': 2, 'CASE_SUBMITTED': 3,...}
        """

        header = header.readline()
        header = header.split(';')
        # removing unnecessary item from list - blank string
        header.pop(0)
        return {field.upper().rstrip('\n'): index
                for index, field in enumerate(header, start=1)}

    @staticmethod
    def get_percent(item: list, index: int, totality: int) -> list:
        """Add new coulumn to list which describes that certain attribute has in overall acceptance

        Parameters:
        ----------
        item: list
            Pass here list to which we want add additional column involved with percentage
        index: int
            Our interested column on which we calculate overall acceptance per record
        totality: int
            Sum of n-th column (n==index) for which we are interested

        Returns:
        -------
        item: list
            A list of a our record with new column - percentage
        """

        percent_col = "{:.1f}".format(item[1][index]/totality * 100)
        item[1].append(percent_col + "%")
        return item

    def write_top_10_occupations(self) -> NoReturn:
        """Writing to new file top 10 occupations based on desired case status"""
        output_headers = ("TOP_OCCUPATIONS", "NUMBER_{}_APPLICATIONS".format(self.desired_case_status), "PERCENTAGE")

        with open(self.file_input, "r") as file:
            header = self.get_header(file)
            soc_name_ind = header.get("SOC_NAME")
            case_status_ind = header.get("CASE_STATUS")
            naics_code_ind = header.get("NAICS_CODE")

            output_data = {}
            # Gather other occupations grouped by naics_code; {'54231.0': [["Some_occupaiton", 4], ["Another",2]]... }
            diff_soc_same_naics = {}
            # Gather additional occupationals in spite of this in output_data
            another_top_occupation = set()
            # naics_multi_occupations contains naics codes
            naics_multi_occupations = set()
            count_desired_case_status = 0

            for line in file:
                line = line.split(";")
                line.pop()
                # Percentage is being calculated on the same case_status
                if line[case_status_ind] == self.desired_case_status:
                    count_desired_case_status += 1
                    # Handling multiple occupations for same naics_code
                    if output_data.get(line[naics_code_ind]) and output_data.get(line[naics_code_ind])[0] != line[soc_name_ind]:
                       if diff_soc_same_naics.get(line[naics_code_ind]) and line[soc_name_ind] in another_top_occupation:
                           for occupation in diff_soc_same_naics.get(line[naics_code_ind]):
                               # occupation[0] is the soc_name and occupation[1] are the occurences of this specific soc_name
                               if occupation[0] == line[soc_name_ind].strip("\""):
                                   occupation[1] += 1
                                   break

                       # For the first occurence of different soc_name for by same naics_code which is output_data
                       elif not diff_soc_same_naics.get(line[naics_code_ind]):
                           diff_soc_same_naics.update({line[naics_code_ind]: []})
                           diff_soc_same_naics.get(line[naics_code_ind]).append([line[soc_name_ind].strip("\""), 1])
                           another_top_occupation.add(line[soc_name_ind])
                           naics_multi_occupations.add(line[naics_code_ind])

                       # If it is the first occurence of another occupation or same naics code
                       else:
                           diff_soc_same_naics.get(line[naics_code_ind]).append([line[soc_name_ind].strip("\""), 1])
                           another_top_occupation.add(line[soc_name_ind])
                           naics_multi_occupations.add(line[naics_code_ind])

                    elif not output_data.get(line[naics_code_ind]):
                        output_data.update({line[naics_code_ind]: []})
                        output_data.get(line[naics_code_ind]).extend([line[soc_name_ind].strip("\""), 1])

                    else:
                        output_data.get(line[naics_code_ind])[1] += 1

                else:
                    continue

            # Loop to find soc_name with most occurences by naics_code
            for naics in naics_multi_occupations:
                current_count_occup = output_data.get(naics)[1]
                for occupation in diff_soc_same_naics.get(naics):
                    # occupation lookalike ["Name_of_occupation", 4]
                    output_data.get(naics)[1] += occupation[1]
                    if occupation[1] > current_count_occup:
                        output_data.get(naics)[0] = occupation[0]
                        current_count_occup = occupation[1]
                    else:
                        continue


            # Desired sorting with descending number and ascending string, just in case if numbers are equal
            output_data = sorted(output_data.items(), key=lambda elem: (-elem[1][1], elem[1][0]))
            output_data = output_data[:10]
            # Adding column involved with percentage
            output_data = list(map(lambda x: self.get_percent(x, 1, count_desired_case_status), output_data))

            with open("top_10_occupations.txt", "w") as f_out:
                output_headers = ";".join(map(str, output_headers))
                f_out.write(output_headers + "\n")
                for data in output_data:
                    data = ";".join(map(str, data[1]))
                    f_out.write(data + "\n")

    def write_top_10_states(self) -> NoReturn:
        """"Write to new file top 10 states based on desired case status"""
        output_headers = ("TOP_STATES", "NUMBER_{}_APPLICATIONS".format(self.desired_case_status), "PERCENTAGE")

        with open(self.file_input, "r") as file:
            header = self.get_header(file)
            worksite_postal_code_ind = header.get("WORKSITE_POSTAL_CODE")
            case_status_ind = header.get("CASE_STATUS")
            state_code = ZipCodesUS.get_state_codes("others/uszips.csv")

            output_data = {}
            count_desired_case_status = 0
            for line in file:
                line = line.split(";")
                line.pop()
                if line[case_status_ind] == self.desired_case_status:
                    count_desired_case_status += 1

                    state = state_code.get(line[worksite_postal_code_ind])
                    if state in output_data:
                        output_data.update({state: [output_data.get(state)[0] + 1]})

                    else:
                        output_data.update({state: [1]})

            output_data = sorted(output_data.items(), key=lambda elem: (-elem[1][0], elem[0]))
            output_data = output_data[:10]
            output_data = list(map(lambda x: self.get_percent(x, 0, count_desired_case_status), output_data))

            with open("top_10_states.txt", "w") as f_out:
                output_headers = ";".join(map(str, output_headers))
                f_out.write(output_headers + "\n")
                for data in output_data:
                    state_id = data[0]
                    data = ";".join(map(str, data[1]))
                    f_out.write(state_id + ";" + data + "\n")


if __name__ == "__main__":
    ob = VisaApplications("input_files/input1.txt", "CERTIFIED")
    ob.write_top_10_states()
    ob.write_top_10_occupations()
