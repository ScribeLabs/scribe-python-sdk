from fitparse import FitFile
import pandas as pd

if __name__ == "__main__":

	file_path = '../../data_files/'
	file_name = 'P4S16B_REC3.fit' 
	output_raw_file_name = 'P4S16B_REC3_raw_python.csv'
	output_footsteps_file_name = 'P4S16B_REC3_footsteps_python.csv'

	file_obj = open(file_path + file_name, 'rb')
	raw_fit_data = file_obj.read()
	fitfile  = FitFile(raw_fit_data)
	data_messages = fitfile.messages

	footsteps_fields_name = dict([('253', "timestamp"), ('0', "footstep_num"), ('1', "footstep_type"), ('2', "debug_1"), ('3', "degug_2"),
				 ('4', "cycle_time"), ('5', "contact_time"), ('6', "foot_strike_max_pronation_time"), ('7', "pronation_velocity_max"), 
				 ('8', "braking_gs"), ('9', "impact_gs"), ('10', "pitch_max_quat_q0"), ('11', "pitch_max_quat_q1"), ('12', "pitch_max_quat_q2"),
				 ('13', "pitch_max_quat_q3"), ('14', "foot_strike_quat_q0"), ('15', "foot_strike_quat_q1"), ('16', "foot_strike_quat_q2"), 
				 ('17', "foot_strike_quat_q3"),('18', "max_pronation_quat_q0"), ('19', "max_pronation_quat_q1"), ('20', "max_pronation_quat_q2"), 
				 ('21', "max_pronation_quat_q3"), ('22', "toe_off_quat_q0"),('23', "toe_off_quat_q1"), ('24', "toe_off_quat_q2"), 
				 ('25', "toe_off_quat_q3"), ('26', "pitch_min_quat_q0"), ('27', "pitch_min_quat_q1"), ('28', "pitch_min_quat_q2"),
				 ('29', "pitch_min_quat_q3")])

	raw_fields_name = dict([('253', "timestamp"), ('0', "accel_x"), ('1', "accel_y"), ('2', "accel_z"), ('3', "gyro_x"), ('4', "gyro_y"), ('5', "gyro_z"), ('6', "quat_0"),
						('7', "quat_1"), ('8', "quat_2"), ('9', "quat_3")])

	for key in raw_fields_name.keys():
		raw_fields_name["unknown_" + key] = raw_fields_name.pop(key)

	for key in footsteps_fields_name.keys():
		footsteps_fields_name["unknown_" + key] = footsteps_fields_name.pop(key)		

	raw_data_dict = { raw_fields_name[key]: []  for key in raw_fields_name.keys() }
	footsetps_data_dict = { footsteps_fields_name[key]: [] for key in footsteps_fields_name.keys() }

	for i in range(1, len(data_messages)):
		if len(data_messages[i].fields) == 11 :
			for j in range(0, len(data_messages[i].fields)):
				key = raw_fields_name[data_messages[i].fields[j].name]
				raw_data_dict[key].append(data_messages[i].fields[j].value)
		else :
			for j in range(0, len(data_messages[i].fields)):
				key = footsteps_fields_name[data_messages[i].fields[j].name]
				footsetps_data_dict[key].append(data_messages[i].fields[j].value)

	raw_df = pd.DataFrame.from_dict(raw_data_dict)
	footsteps_df = pd.DataFrame.from_dict(footsetps_data_dict)

	raw_df.to_csv(file_path + output_raw_file_name)
	footsteps_df.to_csv(file_path + output_footsteps_file_name)
