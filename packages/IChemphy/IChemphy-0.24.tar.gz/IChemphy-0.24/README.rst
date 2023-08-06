IChemPhy
--------

To use this package, simply install using pip install
Then do:

>>> import IChemPhy

1. PENDULUM SIMULATION
The function associated with the Animation of Pendulum is funcPendulum(L, m)
where the parameters are:
L = length of the pendulum
m = mass of the bob of the pendulum

For pendulum simulation simply do:

>>> IChemPhy.Physics.Dynamics.pendulum.funcPendulum(L,m)


2. ANIMATION FOR PROJECTILE MOTION
The function associated with Projectile Motion is funcProjectileMotion()
After calling the function, the user will be prompted to enter the values for the speed of the ball and the angle of the projection. The user input will be used to create a projectile motion animation.

For Projectile Motion animation simply do:
>>> IChemPhy.Physics.Dynamics.projectile.funcProjectileMotion()


3. ELECTRO - MAGNETIC TRAJECTORY SIMULATION
The function associated with the Electro-Magnetic Trajectory is funcElectroMagneticTrajectory(B,V0,A0,E,m,q)
where the parameters are:
B = Magnetic Field vector
V0 = Initial Velocity vector
A0 = Initial Position Vector
E = Electric Field Vector
m = Mass of the charged particle
q = Charge on the particle

For example, the function parameters will be funcElectroMagneticTrajectory([0,2,0], [4,5,6],[1,2,3], [4,5,6], 0.01, 6)

For ElectroMagnetic field trajectory simply do:
>>> IChemPhy.Physics.Dynamics.trajectory.funcElectroMagneticTrajectory(B,V0,A0,E,m,q)
