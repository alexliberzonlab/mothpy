import bars
import json
#part one - generate fake trajectories
def generate_tuple(success = True,t=0,x=0):
    #(x,y,T,odor,turning,state,success)
    return (x,0,t,0,0,0,success)
def generate_trajectory(length=10,success=True):
    diff_lst = [generate_tuple(success,0.01*i, 0.1*i) for i in range(length)]
    #print bars.calc_speed(lst)
    return diff_lst
import random
def generate_many(m=20,n=40,length =10):
    dict_list =[]
    for i in range(n):
            traj_dict = {}
            succ = m < i
            print succ
            traj_dict["diff_list{0}".format(0)] = \
            generate_trajectory(length,succ)
            dict_list.append(traj_dict)
    return dict_list


dict_list = [generate_many(0), generate_many(10),generate_many(20),generate_many(30)]
def create_json(dict_list,data_file_name,n=4):
    for i in range(n):
        with open(data_file_name+str(i)+'.json', 'w') as outfile:
            json.dump(dict_list[i], outfile)
create_json(dict_list,'data')
#print generate_many()
#part two - check  graphics respond properly 
"""

print bars.succuss_precentage(dict_list)
print bars.average_time_relative(dict_list)

"""
