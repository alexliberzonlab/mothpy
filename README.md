`moth` is a NumPy based implementation of moth-inspired navigation strategies that uses 
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

### Example usage

``` 

python compare\ navigators\ in\ different\ wind\ conditions.py

```

![Demo flight](moth/demo.png)






## How to build the figures for the paper

#### Set up the navigators (optional) 
The file Casting_competition initiates the navigators to compete in the simulation. Four loops initiate four equal sized groups of navigators, their properties can be changed within these loops - navigation and casting strategies, location, and so on. 
For more information about navigators check out the models file. 
#### Set up the wind and plume conditions (optional) - 
The file Compare_navigtors... initiates the main loop. For each iteration a new plume and wind model are initiated for the simulation to occur in. 
Make sure that only one variable of the simulation changes with each iteration. Multivaribale changes will create problems later on.
#### Run Comapare_navigators... -
The wind and plume paramters that have been set are saved into "job" files, one JSON file for each iteration (job0.JSON, job1.JSON...) 
The trajectories of the navigators are saved as "data" files, (data0.JSON, data1.JSON), on which the later analyses will be made. 
#### Run Line_graphs - 
The file line_graphs plots bar graphs of the four different simulations. There is no need to set up anything for this file, just run it.
The output should look like this: 

[Success Percentage vs Puff Spread Rate](moth/spVSpsr.png)
[Average Navigation Time vs Puff Spread Rate](moth/spVSpsr.png)
