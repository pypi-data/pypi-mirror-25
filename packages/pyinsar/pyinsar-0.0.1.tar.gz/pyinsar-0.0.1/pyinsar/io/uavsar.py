import re
from collections import OrderedDict

def readUAVSARMetadata(in_filename):
    '''
    Parse UAVSAR metadata

    @param in_filename: Metadata filename (should end in .ann)

    @return OrderedDict of metadata
    '''

    with open(in_filename, 'r') as info_file:
        data_info = info_file.readlines()



    data_info = [line.strip() for line in data_info]


    # Function to convert string to a number
    def str_to_number(in_string):
        try:
            return int(in_string)
        except:
            return float(in_string)


    data_name = data_info[0][31:]


    meta_data_dict = OrderedDict()
    for line in data_info:
        # Only work on lines that aren't commented out
        if re.match('^[^;]',line) != None:
            # Get the data type ('&' is text)
            data_type = re.search('\s+\((.*)\)\s+=', line).group(1)
            # Remove data type from line
            tmp = re.sub('\s+\(.*\)\s+=', ' =', line)

            # Split line into key,value
            split_list = tmp.split('=',maxsplit=1)

            # remove any trailing comments and strip whitespace
            split_list[1] = re.search('[^;]*',split_list[1]).group().strip()
            split_list[0] = split_list[0].strip()

            #If data type is not a string, parse it as a float or int
            if data_type != '&':
                # Check if value is N/A
                if split_list[1] == 'N/A':
                    split_list[1] = float('nan')

                # Check for Raskew Doppler Near Mid Far as this
                # entry should be three seperate entries
                elif split_list[0] == 'Reskew Doppler Near Mid Far':
                    split_list[0] = 'Reskew Doppler Near'

                    second_split = split_list[1].split()
                    split_list[1] = str_to_number(second_split[0])

                    meta_data_dict['Reskew Doppler Mid'] = str_to_number(second_split[1])
                    meta_data_dict['Reskew Doppler Far'] = str_to_number(second_split[2])

                # Parse value to an int or float
                else:
                    split_list[1] = str_to_number(split_list[1])
            # Add key, value pair to dictionary        
            meta_data_dict[split_list[0]] = split_list[1]



    return meta_data_dict
