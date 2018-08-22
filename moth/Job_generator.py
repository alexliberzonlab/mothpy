import json


def generate_job(char_time =3.5,amplitude =0.1,
                 job_file='job.json',threshold = 5000,
                 base_turn_angle=5, t_max =75., dt = 0.01,num_it =1, base_duration =0.2):
    const_dict={}

    #simulation
    const_dict['num_it'] = num_it
    const_dict['t_max']= t_max
    const_dict['dt'] = dt

    #wind meandering
    const_dict['char_time']=char_time
    const_dict['amplitude'] = amplitude

    #navigators
    const_dict['x_start'] = 300
    const_dict['y_start'] = 250
    const_dict['nav_type'] = 1
    const_dict['wait_type'] = 'crw'
    const_dict['base_turn_angle'] = base_turn_angle #for crw
    const_dict['threshold'] = threshold
    const_dict['duration'] = base_duration
    
    
    
    

    with open(job_file, 'w') as outfile:
        json.dump(const_dict, outfile)

