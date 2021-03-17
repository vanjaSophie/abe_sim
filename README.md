# abe_sim
A little agent simulation in MORSE, to be used in a MUHAI pipeline to evaluate semspecs. (Very much a work in progress now.)

# Installation

## Dependencies

To try the current stuff out, you will first need to [install MORSE ](https://www.openrobots.org/morse/doc/stable/user/installation.html) and pip-install trimesh and python-fcl. For example, assuming you have pip3 as a command to install packages for a python3.4 or newer distribution, you can run:

```
sudo pip3 install trimesh python-fcl
```

## Setting up a workspace

Create a MORSE folder in your home directory. This is where you will store the abe_sim, and some other code. The list of commands shows you how you might do this on a Linux system, including setting up a link to the schemasim package so that you can access it when running abe_sim.

```
mkdir MORSE
cd ./MORSE
git clone https://github.com/mpomarlan/abe_sim
git clone https://github.com/mpomarlan/schemasim
ln -s ~/MORSE/schemasim/schemasim ~/MORSE/abe_sim/src/schemasim
```
# Running the simulation

Once the dependencies and the repositories above are installed/cloned, go to the folder in which you have placed the repositories (in the commands above, that would be the MORSE folder). Once there, run

```
morse import abe_sim # only required the first time
morse run abe_sim
```

and you should see the simulated environment appear in a blender game window. You can move the blue agent with the arrow keys, and the camera with wasd and ctrl+mouse move.

However we'd like to have the agent figure some stuff out without us having to guide it always. To do that, open a terminal and go to the repository folder, and then in its src folder (if you followed the commands above, go to MORSE/abe_sim/src). Once there, start a python3 instance and run the following code:

```python
from abe_sim.brain.midbrain import Midbrain
from pymorse import Morse
simu = None
while True:
    try:
        simu = Morse()
        break
    except OSError:
        continue

base = simu.robot.base
hands = simu.robot.hands
head = simu.robot.head
pose = simu.robot.pose
world = simu.robot.worlddump
mb = Midbrain(head, hands, base, pose, world, simu)
mb.updateNavigationMap()
mb.startOperations()

schs = mb.getObjectSchemas()

from schemasim.schemas.l11_functional_control import Support

bottle = schs['bottleOil'].unplace(mb.sim3D)
destspec = [Support(supporter=schs['table.000'],supportee=bottle),bottle]
mb.carryObject("bottleOil", destspec)
```

What you should see is that, after some time to start up its "brain", the agent is going to move towards the oil bottle near the top of the screen, pick it up, and deliver it to the table on the left of the screen. We can also place some other object, for example the potted herb, on a table. To place it on the table on the right of the screen, you would run (but ONLY AFTER the agent is finished with moving the bottle!):

```
plant = schs['plantSmall1'].unplace(mb.sim3D)
destspec = [Support(supporter=schs['table.002'],supportee=plant),plant]
mb.carryObject("plantSmall1", destspec)
```

We could also have a look at some auxiliary structures the agent maintains about the world. One such structure is the navigation map, which the agent uses to navigate around obstacles. We can have a look at how this map looks like:

```python
print(mb.cellMap)
```

You will see a grid of either "." (meaning, this square cell of the grid is free) or "#" (the cell is occupied and should not be walked through).

NOTE: the navigation grid is somewhat course, and encourages the agent to stay away from furniture objects. If you move the agent around using the keys, it is possible that you place it inside a cell it considers occupied on its navigation grid, and won't be able to get out using its navigation function. If you suspect this is the case, manually move the agent to a free area such as the center and resume giving it navigation goals afterwards.

Speaking of objects, what objects are there in the environment? We can obtain a printout of objects and some data about them, such as types and positions, using

```python
mb.listObjects()
```

This will give you a lot of text in the console, but supposing you want that information in a variable that you can use later in your program, you should run instead

```
objs = mb.cerebellum._retrieveObjects()
```

objs is a dictionary, where they keys are object names and the values are dictionaries containing information about these objects, such as their position, type, mesh filename and so on.
