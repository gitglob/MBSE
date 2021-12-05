Repository for the course 02223: Model Based Systems Engineering

Simulation of co2 generation inside a 3d city environment and implementation of a sensor system that effectively (accuracy + low cost) measures the the co2 levels.

How to run:
1. Clone the repository
2. On a terminal, change to the project directory and type: `pip install -r requirements.txt`
3. To run the simulation: `python main.py`
[![gui3.png](https://i.postimg.cc/rp1rhztm/gui3.png)](https://postimg.cc/wtBMMq28)
 
4. * Press `START the Simulation`, if you want to execute the simulation with the default values:\
   `gui/gui.py -> lines: 5-12`.
   * Press `Set Parameters`, in order to modify the parameters of the simulation.
     * Remember to always click on the corresponding button of a parameter, after you set its desired value.
     * When you are done, just press `THE PARAMETERS ARE SET !!` and then you are ready to start the simulation with the desired parameters.
   * Press `Run Multiple Simulations`, in order to run our experiment plan. You can always modify the experiment plan in `main.py -> lines 28-30`
     * In the new window that appears you can set the days of the simulation.
     * Remember to always click on the corresponding button of a parameter, after you set its desired value.
     * When you are done, just press `THE PARAMETERS ARE SET !!` and then you are ready to start the simulation with the desired parameters.
   * Press `QUIT` if you want to exit the simulation and close all the windows.


Additional notes:
- In the folder "figures", after you run thesimulation with the "-s" parameter, there will be saved a number of proof of concept plots, as well some visualizations for the final results. However, it will take much much more time.
- In the folder "model_data", one can find the initial datasets regarding the weather in Copenhagen, which were used for the purposes of the project.
