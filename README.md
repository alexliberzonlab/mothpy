`mothpy` is a NumPy based implementation of moth-inspired navigation strategies that uses 
`pompy` library to create the puff, wind and concentration models. see `pompy/Readme.md` 
for details

### What is this repository for?

This Python package allows simulation moth-like navigators in dynamic 2D odour 
concentration fields spread in turbulent flows 

### Installation and requirements

    Python 2.7
    Numpy
    Scipy
    Matplotlib
    Pompy

### Example usage

``` 

python compare_navigators_in_different_wind_conditions.py

```

![Demo flight](moth/Demonstration_of_different_navigation_strategies.png)






## How to build the figures for the paper

#### Set up the navigators (optional) 
The file Casting_competition initiates the navigators to compete in the simulation. Four loops initiate four equal sized groups of navigators, their properties can be changed within these loops - navigation and casting strategies, location, and so on. 
For more information about navigators check out the models file. 
#### Set up the wind and plume conditions (optional) 
The file Compare_navigtors... initiates the main loop. For each iteration a new plume and wind model are initiated for the simulation to occur in. The function generate_job dictates the terms of the simulation in terms of wind and plume partameteres. In order to set the simulation enter the required parameters as input for generate_job. For example here - 
```
    for i in range(4):
        job_file_name = 'job'+ str(i)+ '.json'
        data_file_name = 'data'+ str(i)+ '.json'
        #titles_file_name = 'titles'+ str(i)+ '.json'       
        generate_job(char_time = 3.5, amplitude =0.1, job_file = job_file_name,
                     t_max =15, puff_release_rate = 100,
                     puff_spread_rate = 0.0001*(1+i),
                     dt = 0.01, num_it = 1)
```
The only value that changes is the puff spread rate, varying from 0.0001 to 0.0004.
Make sure that only one variable of the simulation changes with each iteration. Multivaribale changes will create problems later on.
#### Run Comapare_navigators... 
When the file is run the wind and plume paramters that have been set are saved into "job" files, one JSON file for each iteration (job0.JSON, job1.JSON...). 
The trajectories of the navigators are saved as "data" files, (data0.JSON, data1.JSON), on which the later analyses will be made. 
Notice the following line - 
```
#save_plot(job_file_name,data_file_name,title,navigator_titles)
```
deleting the # mark would instruct the code to save an image for each navigation attempt in the deafulat settings, that mean 800 pictures). That could supply useful input in some cases. 
#### Run Line_graphs 
The file line_graphs plots bar graphs of the four different simulations. It read from the Data and Job files, so those could be replaced and . There is no need to set up anything for this file, just run it.
The output should look like this: 

![Success Percentage vs Puff Spread Rate](moth/spVSpsr.png)
![Average Navigation Time vs Puff Spread Rate](moth/spVSpsr.png)


## how to manage and design navigators
### initiating  a navigator
Let us look at this example from the casting_competition file:
```
navigator1 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'], cd['nav_type'] , cd['cast_type'], cd['wait_type'])
```
The navigator is initiated with it's initial x and y coordinates and the modes of navigating, casting and waiting. 
### wait, cast and nav types
A navigator is an object of the ```moth_modular``` class. It has an attribute to define each movement type, ```wait_type, cast_type, nav_type```. 
The attribute itself can be an integer or a string, it doesn't matter, but it should correlate to a signifier inside of the corresponding function. For example, let's look at the casting function -
```
def cast(self,wind_vel_at_pos):
        if self.state != 'cast' :
            #if this is the beginging of a new casting phase
            self.change_direction()
            
        if self.cast_type == 0:
            self.u=0
            self.v=0
            
        if self.cast_type == 1:
            self.calculate_wind_angle(wind_vel_at_pos)
            self.u = -self.speed*np.cos(self.gamma+self.wind_angle)
            self.v = self.speed*np.sin(self.gamma+self.wind_angle)

        if self.cast_type == 2:
            #define different betas for different casting patterns
            self.cast2(wind_vel_at_pos)
```
The function, like all movement functions, takes as input the parameters of the navigator and the wind velocity at the position (as calculated by the wind model).
The first conditional changes the direction of casting from the previous direction. This has nothing to with the cast type. 
The second, third and fourth conditionals are dependant on the cast type, and use it as an indicator as to how to move. Note that the function can call upon other functions. The stracture of the ```wait``` and ```navigate``` are very similar - The function sets the velocity (u,v) of the navigator. The actual time step is performed in the update function.
#### defining new movement types
In order to create a new waiting, casting or navigation, first enter the models file. For example, let's say we would like to design a new waiting mode. First, we sould define a condition within the waiting function. 
```
<<<<<<< HEAD
    def wait(self,wind_vel_at_pos):
        if wait_type == 'example wait type':
=======
pip install pompy
>>>>>>> 8bba8138c43800e22ddc23107f10b06e5df69860
```
Now, if the navigator was initiated to so its wait type attribute is 'example wait type' the wait function will be directed into the actions we define under that conditional. Secondly, define the changes in you would like to be made to the velocity of the navigator:
```
    def wait(self,wind_vel_at_pos):
        if wait_type == 'example wait type':
            u *= 1.1
            v *= 1.1
```
The same approach should be applied to any of the movement functions. 
After we defined the new conditional, we can use it when initiatin a new navigator:

```
navigator1 = models.moth_modular(sim_region, cd['x_start'], cd['y_start'], cd['nav_type'] , cd['cast_type'], 'example wait type')
```