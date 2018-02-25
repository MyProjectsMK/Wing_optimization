# Wing optimization
The repository contains a tool dedicated to optimize an aircraft wing using gradient method. The program has been written in Python 2.7.
<br><br>

## Application
The program is dedicated to optimize an aircraft wing of any shape using gradient method. The goal of the optimization is to minimize drag coefficient using wingspan and standard mean chord as decision variables.

## How does it work?
The program consists of five files:

![Figure 1](https://github.com/MyProjectsMK/Wing_optimization/blob/master/README_figure1.jpg)

Its central point is the *wing_optimization.py* file - it incorporates the algorithmes responsible for the optimization. A user enters all parameters of a wing into this file and a number of iterations of the optimization procedure into the *number_of_iterations.txt* file. Two output files - *results.txt* and *results_of_the_last_iteration.txt* - provide a user with results of the optimization. The first one contains values of the decision variables in each iteration, while the second one contains the final parameters of the wing. Last but not least, the *figures.py* file is utilized to plot graphs of some selected parameters like objective function (look at the figure below).

![Figure 2](https://github.com/MyProjectsMK/Wing_optimization/blob/master/README_figure2.png)
