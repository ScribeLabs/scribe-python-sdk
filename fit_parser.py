from fitparse import FitFile
import pandas as pd

if __name__ == "__main__":

	file_path = '../../data_files/'
	file_name = '2570.fit' 
	output_file_name = '2570_python.csv'

	file_obj = open(file_path + file_name, 'rb')
	raw_fit_data = file_obj.read()
	fitfile  = FitFile(raw_fit_data)
	data_messages = fitfile.messages

	fields_name = dict([('253', "timestamp"), ('0', "footstep_num"), ('1', "footstep_type"), ('2', "debug_1"), ('3', "degug_2"),
				 ('4', "cycle_time"), ('5', "contact_time"), ('6', "foot_strike_max_pronation_time"), ('7', "pronation_velocity_max"), 
				 ('8', "braking_gs"), ('9', "impact_gs"), ('10', "pitch_max_quat_q0"), ('11', "pitch_max_quat_q1"), ('12', "pitch_max_quat_q2"),
				 ('13', "pitch_max_quat_q3"), ('14', "foot_strike_quat_q0"), ('15', "foot_strike_quat_q1"), ('16', "foot_strike_quat_q2"), 
				 ('17', "foot_strike_quat_q3"),('18', "max_pronation_quat_q0"), ('19', "max_pronation_quat_q1"), ('20', "max_pronation_quat_q2"), 
				 ('21', "max_pronation_quat_q3"), ('22', "toe_off_quat_q0"),('23', "toe_off_quat_q1"), ('24', "toe_off_quat_q2"), 
				 ('25', "toe_off_quat_q3"), ('26', "pitch_min_quat_q0"), ('27', "pitch_min_quat_q1"), ('28', "pitch_min_quat_q2"),
				 ('29', "pitch_min_quat_q3")])

	for key in fields_name.keys():
		fields_name["unknown_" + key] = fields_name.pop(key)

	data_dict = { fields_name[key]: []  for key in fields_name.keys() }

	for i in range(1, len(data_messages)):
		for j in range(0, len(data_messages[i].fields)):
			key = fields_name[data_messages[i].fields[j].name]
			data_dict[key].append(data_messages[i].fields[j].value)

	df = pd.DataFrame.from_dict(data_dict)

	df.to_csv(file_path + output_file_name)
