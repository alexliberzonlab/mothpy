import json


def generate_job(char_time =3.5,amplitude =0.1,job_file='job.json'):
    const_dict={}
    const_dict['num_it'] = 1
    const_dict['t_max']=25.
    const_dict['char_time']=char_time
    const_dict['amplitude'] = amplitude

    const_dict['x_start'] = 450
    const_dict['y_start'] = 250
    const_dict['nav_type'] = 3
    
    
    

    with open(job_file, 'w') as outfile:
        json.dump(const_dict, outfile)

