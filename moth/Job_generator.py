import json


def generate_job(char_time =3.5,amplitude =0.1,job_file='job.json',base_turn_angle=5):
    const_dict={}
    const_dict['num_it'] = 1
    const_dict['t_max']=100.
    const_dict['char_time']=char_time
    const_dict['amplitude'] = amplitude

    const_dict['x_start'] = 250
    const_dict['y_start'] = 250
    const_dict['nav_type'] = 3

    const_dict['base_turn_angle'] = base_turn_angle
    
    
    

    with open(job_file, 'w') as outfile:
        json.dump(const_dict, outfile)

