from fitparse import FitFile
from definitions import get_definition_map
from definitions import get_definitions

def append_unknown_to_keys(dictonary):
	for key in dictonary.keys():
		dictonary["unknown_" + key] = dictonary.pop(key)
	return dictonary

def remove_unknown_to_keys(word):
  return word[8:]

def replace_keys(data_dict, format_dict):
	for key in data_dict.keys():
		if key in format_dict.keys() :
			data_dict[format_dict[key]] = data_dict.pop(key)
		else:
			break
	return data_dict

def fit_to_csv(file_path, file_name):
  definitions = get_definitions()
  definition_map = get_definition_map()

  output_file_1 = file_name[0:file_name.index('.')] + '_1.csv'
  output_file_2 = file_name[0:file_name.index('.')] + '_2.csv'

  file_obj = open(file_path + file_name, 'rb')
  raw_fit_data = file_obj.read()
  fitfile  = FitFile(raw_fit_data)
  data_messages = fitfile.messages

  all_data_dict = {}

  for key in definition_map.keys():
    format = definition_map[key]
    definitions[format] = append_unknown_to_keys(definitions[format])

  f = open(file_path + output_file_1, 'w')
  num_of_fields = len(data_messages[0].get_values())
  string = ''

  all_mesg_num = []
  header_list = []
  file_id = []

  for i in range(0, len(data_messages)):
    mesg_num = str(data_messages[i].mesg_num)
    if mesg_num in definition_map.keys():
      format = definition_map[mesg_num]
      format_dict = definitions[format]
      data_dict = data_messages[i].get_values()
      data_dict = replace_keys(data_dict, format_dict)
    else:
      format = data_messages[i].name
      data_dict = data_messages[i].get_values()

    if mesg_num not in all_mesg_num:
      all_mesg_num.append(mesg_num)
      if mesg_num != '0':
        header_list = header_list + data_dict.keys()
    if format == "file_id" :
      file_id = data_dict
    else :
      all_data_dict[str(i)] = data_dict
    row_str = mesg_num + ',' + format
    for key in data_dict.keys(): 
      if row_str :
        row_str = row_str + ',' + key + ',' + str(data_dict[key])
      else :
        row_str = row_str + key + ',' + str(data_dict[key])
    row_str = row_str + "\n"
    string = string + row_str
    if len(data_dict) > num_of_fields:
      num_of_fields = len(data_dict)

  header_str = 'Local Number, Message'
  for i in range(1,num_of_fields + 1):
    if header_str :
      header_str = header_str + ',' + 'Field ' + str(i) + ',' + 'Value ' + str(i)
    else :
      header_str = header_str + 'Field ' + str(i) + ',' + 'Value ' + str(i)
  header_str = header_str + "\n"
  string = header_str + string
  f.write(string)
  f.close()

  
  f = open(file_path + output_file_2, "w")
  string = ''
  header_list = list(set(header_list))
  for header in header_list:
    string = string + header + ','
  string  = string + "\n"

  for i in range(1, len(data_messages)):
    mesg_num = str(data_messages[i].mesg_num)
    if mesg_num in definition_map.keys():
      format = definition_map[mesg_num]
      format_dict = definitions[format]
      data_dict = data_messages[i].get_values()
      data_dict = replace_keys(data_dict, format_dict)
    else:
      data_dict = data_messages[i].get_values()

    row = ''
    for header in header_list:
      if header in data_dict.keys():
        row = row + str(data_dict[header]) + ','
      else:
        row = row + ','
    row = row + "\n"
    string = string + row
  f.write(string)
  f.close()


if __name__ == "__main__":

  file_path = '../../data_files/python_sdk_example/'
  file_name = 'P4S16B_REC3.fit'
  fit_to_csv(file_path, file_name)
