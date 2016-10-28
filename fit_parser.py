from fitparse import FitFile
import pandas as pd

definition_map = {
'0' : 'file_id',
'49' : 'file_creator',
'35' : 'software',
'1' : 'capabilities',
'37' : 'file_capabilities',
'38' : 'mesg_capabilities',
'39' : 'field_capabilities',
'2' : 'device_settings',
'3' : 'user_profile',
'4' : 'hrm_profile',
'5' : 'sdm_profile',
'6' : 'bike_profile',
'7' : 'zones_target',
'12' : 'sport',
'8' : 'hr_zone',
'9' : 'power_zone',
'10' : 'met_zone',
'15' : 'goal',
'34' : 'activity',
'18' : 'session',
'19' : 'lap',
'20' : 'record',
'21' : 'event',
'23' : 'device_info',
'31' : 'course',
'32' : 'course_point',
'26' : 'workout',
'27' : 'workout_step',
'33' : 'totals',
'30' : 'weight_scale',
'51' : 'blood_pressure',
'65442' : 'motion_event_default',
'65453' : 'motion_event',
'65454' : 'footstep',
'65455' : 'footstep_quat'
}

definitions = {
'file_id' : {
'0' : "type",
'1' : "manufacturer",
'2' : "product",
'3' : "serial_number",
'4' : "time_created",
'5' : "number"
},

'file_creator' : {
'0' : "software_version",
'1' : "hardware_version" 
}
,
'software' : {
'254' : "message_index", 
  '3' : "version",
  '5' : "part_number"
}
,
'capabilities' : {
'0' : "languages",
'1' : "sports", 
'21' : "workouts_supported"  
}
,
'file_capabilities' : {
'254' : "message_index", 
  '0' : "type", 
  '1' : "flags",
  '2' : "directory", 
  '3' : "max_count", 
  '4' : "max_size"  
}
,
'mesg_capabilities' : {
'254' : "message_index", 
  '0' : "file", 
  '1' : "mesg_num", 
  '2' : "count_type", 
  '3' : "count" 
}
,
'field_capabilities' : {
'254' : "message_index", 
  '0' : "file", 
  '1' : "mesg_num", 
  '2' : "field_num", 
  '3' : "count" 
}
,
'device_settings' : {
'1' : "utc_offset"
}
,
'user_profile' : {
'254' : "message_index",
'0' : "friendly_name",
'1' : "gender", 
'2' : "age", 
'3' : "height", 
'4' : "weight", 
'5' : "language", 
'6' : "elev_setting", 
'7' : "weight_setting", 
'8' : "resting_heart_rate", 
'9' : "default_max_running_heart_rate",
'10' : "default_max_biking_heart_rate",
'11' : "default_max_heart_rate", 
'12' : "hr_setting", 
'13' : "speed_setting", 
'14' : "dist_setting", 
'16' : "power_setting", 
'17' : "activity_class", 
'18' : "position_setting", 
'21' : "temperature_setting", 
'22' : "local_id", 
'23' : "global_id"  
}
,
'hrm_profile' : {
'254' : "message_index", 
'0' : "enabled", 
'1' : "hrm_ant_id"  
}
,
'sdm_profile' : {
'254' : "message_index", 
'0' : "enabled", 
'1' : "sdm_ant_id",
'2' : "sdm_cal_factor", 
'3' : "odometer", 
'4' : "speed_source"   
}
,
'bike_profile' : {
'254' : "message_index",
' 0' : "name", 
'1' : "sport", 
'2' : "sub_sport", 
'3' : "odometer", 
'4' : "bike_spd_ant_id", 
'5' : "bike_cad_ant_id", 
'6' : "bike_spdcad_ant_id", 
'7' : "bike_power_ant_id", 
'8' : "custom_wheelsize", 
'9' : "auto_wheelsize", 
'10' : "bike_weight", 
'11' : "power_cal_factor", 
'12' : "auto_wheel_cal", 
'13' : "auto_power_zero", 
'14' : "id", 
'15' : "spd_enabled", 
'16' : "cad_enabled", 
'17' : "spdcad_enabled", 
'18' : "power_enabled"   
}
,
'zones_target' : {
'1' : "max_heart_rate", 
'2' : "threshold_heart_rate", 
'3' : "functional_threshold_power", 
'5' : "hr_calc_type", 
'7' : "pwr_calc_type"  
}
,
'sport' : {
'0' : "sport", 
'1' : "sub_sport", 
'3' : "name"  
}
,
'hr_zone' : {
'254' : "message_index", 
'1' : "high_bpm", 
'2' : "name"  
}
,
'power_zone' : {
'254' : "message_index", 
'1' : "high_value",
'2' : "name"  
}
,
'met_zone' : {
'254' : "message_index", 
  '1' : "high_bpm", 
  '2' : "calories", 
  '3' : "fat_calories"  
}
,
'goal' : {
'254' : "message_index", 
  '0' : "sport", 
  '1' : "sub_sport", 
  '2' : "start_date", 
  '3' : "end_date", 
  '4' : "type", 
  '5' : "value", 
  '6' : "repeat", 
  '7' : "target_value", 
  '8' : "recurrence", 
  '9' : "recurrence_value", 
 '10' : "enabled"  
}
,
'activity' : {
'253' : "timestamp", 
  '0' : "total_timer_time", 
  '1' : "num_sessions", 
  '2' : "type", 
  '3' : "event", 
  '4' : "event_type", 
  '5' : "local_timestamp", 
  '6' : "event_group"  
}
,
'session' : {
'254' : "message_index", 
'253' : "timestamp", 
  '0' : "event", 
  '1' : "event_type", 
  '2' : "start_time", 
  '3' : "start_position_lat", 
  '4' : "start_position_long", 
  '5' : "sport", 
  '6' : "sub_sport", 
  '7' : "total_elapsed_time", 
  '8' : "total_timer_time", 
  '9' : "total_distance", 
 '10' : "total_cycles", 
 '10' : "total_strides", 
 '11' : "total_calories", 
 '13' : "total_fat_calories", 
 '14' : "avg_speed", 
 '15' : "max_speed", 
 '16' : "avg_heart_rate", 
 '17' : "max_heart_rate", 
 '18' : "avg_cadence", 
 '18' : "avg_running_cadence", 
 '19' : "max_cadence", 
 '19' : "max_running_cadence", 
 '20' : "avg_power", 
 '21' : "max_power", 
 '22' : "total_ascent", 
 '23' : "total_descent", 
 '24' : "total_training_effect",
 '25' : "first_lap_index", 
 '26' : "num_laps", 
 '27' : "event_group", 
 '28' : "trigger", 
 '29' : "nec_lat", 
 '30' : "nec_long", 
 '31' : "swc_lat", 
 '32' : "swc_long"
}
,
'lap' : {
'254' : "message_index", 
'253' : "timestamp", 
  '0' : "event", 
  '1' : "event_type", 
  '2' : "start_time", 
  '3' : "start_position_lat", 
  '4' : "start_position_long", 
  '5' : "end_position_lat", 
  '6' : "end_position_long", 
  '7' : "total_elapsed_time", 
  '8' : "total_timer_time", 
  '9' : "total_distance", 
 '10' : "total_cycles", 
 '10' : "total_strides", 
 '11' : "total_calories", 
 '12' : "total_fat_calories", 
 '13' : "avg_speed", 
 '14' : "max_speed", 
 '15' : "avg_heart_rate", 
 '16' : "max_heart_rate", 
 '17' : "avg_cadence", 
 '17' : "avg_running_cadence", 
 '18' : "max_cadence", 
 '18' : "max_running_cadence", 
 '19' : "avg_power", 
 '20' : "max_power", 
 '21' : "total_ascent", 
 '22' : "total_descent", 
 '23' : "intensity", 
 '24' : "lap_trigger", 
 '25' : "sport", 
 '26' : "event_group"  
}
,
'record' : {
'253' : "timestamp", 
  '0' : "position_lat", 
  '1' : "position_long", 
  '2' : "altitude", 
  '3' : "heart_rate", 
  '4' : "cadence", 
  '5' : "distance", 
  '6' : "speed", 
  '7' : "power", 
  '8' : "compressed_speed_distance",
  '9' : "grade", 
 '10' : "resistance", 
 '11' : "time_from_course", 
 '12' : "cycle_length", 
 '13' : "temperature"  
}
,
'event' : {
'253' : "timestamp", 
  '0' : "event", 
  '1' : "event_type", 
  '2' : "data16", 
  '3' : "data", 
  '3' : "timer_trigger", 
  '3' : "course_point_index", 
  '3' : "battery_level", 
  '3' : "virtual_partner_speed", 
  '3' : "hr_high_alert", 
  '3' : "hr_low_alert", 
  '3' : "speed_high_alert", 
  '3' : "speed_low_alert", 
  '3' : "cad_high_alert", 
  '3' : "cad_low_alert", 
  '3' : "power_high_alert", 
  '3' : "power_low_alert", 
  '3' : "time_duration_alert", 
  '3' : "distance_duration_alert", 
  '3' : "calorie_duration_alert", 
  '3' : "fitness_equipment_state", 
  '4' : "event_group"  
}
 ,
'device_info' : {
'253' : "timestamp", 
  '0' : "device_index", 
  '1' : "device_type", 
  '2' : "manufacturer", 
  '3' : "serial_number", 
  '4' : "product", 
  '5' : "software_version", 
  '6' : "hardware_version", 
  '7' : "cum_operating_time", 
 '10' : "battery_voltage", 
 '11' : "battery_status",   
}
,
'course' : {
'4' : "sport", 
'5' : "name", 
'6' : "capabilities"  
}
,
'course_point' : {
'254' : "message_index", 
  '1' : "timestamp", 
  '2' : "position_lat", 
  '3' : "position_long", 
  '4' : "distance", 
  '5' : "type", 
  '6' : "name"  
}
,
'workout' : {
'4' : "sport",
'5' : "capabilities", 
'6' : "num_valid_steps", 
'8' : "wkt_name"  
}
,
'workout_step' : {
'254' : "message_index", 
  '0' : "wkt_step_name", 
  '1' : "duration_type", 
  '2' : "duration_value", 
  '2' : "duration_time", 
  '2' : "duration_distance", 
  '2' : "duration_hr", 
  '2' : "duration_calories", 
  '2' : "duration_step", 
  '2' : "duration_power", 
  '3' : "target_type", 
  '4' : "target_value", 
  '4' : "target_hr_zone", 
  '4' : "target_power_zone", 
  '4' : "repeat_steps", 
  '4' : "repeat_time", 
  '4' : "repeat_distance", 
  '4' : "repeat_calories", 
  '4' : "repeat_hr", 
  '4' : "repeat_power", 
  '5' : "custom_target_value_low", 
  '5' : "custom_target_speed_low", 
  '5' : "custom_target_heart_rate_low", 
  '5' : "custom_target_cadence_low", 
  '5' : "custom_target_power_low", 
  '6' : "custom_target_value_high", 
  '6' : "custom_target_speed_high", 
  '6' : "custom_target_heart_rate_high", 
  '6' : "custom_target_cadence_high", 
  '6' : "custom_target_power_high", 
  '7' : "intensity"
}
,
'totals' : {
'254' : "message_index", 
'253' : "timestamp", 
  '0' : "timer_time", 
  '1' : "distance", 
  '2' : "calories", 
  '3' : "sport", 
  '4' : "elapsed_time"  
}
 ,
'weight_scale' : {
'253' : "timestamp", 
  '0' : "weight",
  '1' : "percent_fat", 
  '2' : "percent_hydration", 
  '3' : "visceral_fat_mass", 
  '4' : "bone_mass", 
  '5' : "muscle_mass", 
  '7' : "basal_met", 
  '8' : "physique_rating", 
  '9' : "active_met", 
 '10' : "metabolic_age", 
 '11' : "visceral_fat_rating", 
 '12' : "user_profile_index"  
}
,
'blood_pressure' : {
'253' : "timestamp", 
  '0' : "systolic_pressure", 
  '1' : "diastolic_pressure", 
  '2' : "mean_arterial_pressure", 
  '3' : "map_3_sample_mean", 
  '4' : "map_morning_values", 
  '5' : "map_evening_values", 
  '6' : "heart_rate", 
  '7' : "heart_rate_type", 
  '8' : "status", 
  '9' : "user_profile_index"  
}
 ,
'motion_event_default' : {
'253' : "timestamp", 
  '0' : "event", 
  '1' : "event_type", 
  '2' : "data16", 
  '3' : "data", 
  '4' : "event_group"  
}
,
'motion_event' : {
'253' : "timestamp", 
  '0' : "accel_x", 
  '1' : "accel_y", 
  '2' : "accel_z", 
  '3' : "gyro_x",  
  '4' : "gyro_y", 
  '5' : "gyro_z", 
  '6' : "quat_0", 
  '7' : "quat_1", 
  '8' : "quat_2", 
  '9' : "quat_3"
}
 ,
'footstep' : {
 '253' : "timestamp", 
   '0' : "footstep_num", 
   '1' : "footstep_type", 
   '2' : "stride_length",
   '3' : "stride_pace", 
   '4' : "cycle_time", 
   '5' : "contact_time", 
   '6' : "pronation_velocity_max", 
   '7' : "pronation_excursion_fs_mp", 
   '8' : "pronation_excursion_mp_to", 
   '9' : "stance_excursion_fs_mp", 
  '10' : "stance_excursion_mp_to",
  '11' : "swing_excursion",
  '12' : "braking_gs",
  '13' : "impact_gs"  
}
,
'footstep_quat' : {
'253' : "timestamp", 
  '0' : "footstep_num", 
  '1' : "footstep_type", 
  '2' : "debug_1",
  '3' : "debug_2",  
  '4' : "cycle_time", 
  '5' : "contact_time", 
  '6' : "foot_strike_max_pronation_time", 
  '7' : "pronation_velocity_max", 
  '8' : "braking_gs",
  '9' : "impact_gs",
 '10' : "pitch_max_quat_q0", 
 '11' : "pitch_max_quat_q1", 
 '12' : "pitch_max_quat_q2", 
 '13' : "pitch_max_quat_q3", 
 '14' : "foot_strike_quat_q0", 
 '15' : "foot_strike_quat_q1", 
 '16' : "foot_strike_quat_q2", 
 '17' : "foot_strike_quat_q3", 
 '18' : "max_pronation_quat_q0", 
 '19' : "max_pronation_quat_q1", 
 '20' : "max_pronation_quat_q2", 
 '21' : "max_pronation_quat_q3", 
 '22' : "toe_off_quat_q0", 
 '23' : "toe_off_quat_q1", 
 '24' : "toe_off_quat_q2", 
 '25' : "toe_off_quat_q3", 
 '26' : "pitch_min_quat_q0", 
 '27' : "pitch_min_quat_q1", 
 '28' : "pitch_min_quat_q2", 
 '29' : "pitch_min_quat_q3"  
}
}

def append_unknown_to_keys(dictonary):
	for key in dictonary.keys():
		dictonary["unknown_" + key] = dictonary.pop(key)
	return dictonary

def replace_keys(data_dict, format_dict):
	for key in data_dict.keys():
		if key in format_dict.keys() :
			data_dict[format_dict[key]] = data_dict.pop(key)
		else:
			break
	return data_dict

if __name__ == "__main__":

  file_path = '../../data_files/python_sdk_example/'
  file_name = 'P4S16B_REC3.fit'
  output_file_1 = 'P4S16B_REC3_1.csv'
  output_file_2 = 'P4S16B_REC3_2.csv'

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
    format = definition_map[mesg_num]
    format_dict = definitions[format]
    data_dict = data_messages[i].get_values()
    data_dict = replace_keys(data_dict, format_dict)
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
    format = definition_map[mesg_num]
    format_dict = definitions[format]
    data_dict = data_messages[i].get_values()
    data_dict = replace_keys(data_dict, format_dict)
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


