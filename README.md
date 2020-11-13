# Snakes Evolution

## INTRODUCTION

- This is a simulation for natural selection process.
- The main idea of the simulation is to create a random initial population of snakes, each snake has a different random color and random name.
![Alt text](images/start.png?raw=true "Starting")
- with each generation the performance of the snakes should improve because the new generation is created using the best snakes of the last generation.
- The creation of the new generation is done be getting a snake of the last generation and imitate its brain with some changes.
- The process of selecting the parent of any snake is by random process, with the chances of selecting any snake depends on its performance.
- Each snake in the new generation have a color similar to its parent's color with small change.
- Each snake in the new generation have a name similar to its parent's name with small change.
- Each snake decides how it moves using a neural network.
- The neural network calculates the movement using 10 inputs (4 distance to the walls in the 4 main directions, the distance to the neares cell of of its body in the 4 main directions, and the horizintal and vertical distances to the apple).
- It is possible to choose either to show all the alive snakes or to show just one snake.
- During the simulation (when all snakes are showed), it is possible that more than one apple can be shown (apples for all alive snakes). Just the user can see all the apples at once, while for each snake, just one apple is available, and it cannot see the next apple until it gets the current one. 
- During the simulation the neural network of one snake (by defult the best snake of the last generation) is shown, with the inputs and outputs calculated and drawn in the real-time, in addition to that, more information about this snake, and more general information are shown to the right of the screen.
- The selected snake can be changed manually, accordingly, the shown neural network and other information change.


## CONTROLS
- P	: Pause and Unpause the simulation.
- Q	: Quit the simulation.
- N	: Stop the current generation and create the next generation.
- O	: Toggle between showing all the alive snakes or showing just one snake.
- Up, Down: Change the selected snake (the neural network and other information shown related to the 		selected snake will change)
- W	: Increase the growth rate for snakes (To get longer snakes faster)
- D	: Decrease the growth rate for snakes (Minimun is 1)



