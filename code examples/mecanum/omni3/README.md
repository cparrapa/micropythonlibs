<h1>HP Otto: Otto Omni3</h1> 

An omni wheel mod for HP Otto using 3 wheels

<img width="224" height="259" alt="Otto Omni3" src="https://github.com/user-attachments/assets/b8261ee3-10db-421c-9a2b-fe10d2e812a3" />

STL files and build instructions can be found on [printables.com](https://www.printables.com/model/1501370-hp-otto-otto-omni3)

**otto3wd.py** is a required library for Otto Omni3, it contains the code for 3 wheel drive movement.  

<img width="648" height="313" alt="wheel config" src="https://github.com/user-attachments/assets/1d893cca-ac04-4d9f-a1d9-aea1c5e799dd" />

The default configuration assumes left wheel on connector 10, the right wheel on connector 11 and the rear or back wheel on connector 8 .

**rc.py** is a modified version of rc.py enabling control of Otto Omni3 via the new HP Otto phone app (currently (Mar 2026) in beta test and only available to purchasers of the HP Otto Starter https://www.facebook.com/groups/ottodiy/posts/3923882564421879/)  

Additions and modifications to the base rc.py are all commented so that future releases of rc.py can be similarly modified.  

<img width="512" height="229" alt="omni phone control" src="https://github.com/user-attachments/assets/fef739b8-49ea-45c7-babf-a410c796d6e8" />

The joystick control controls movement in any given direction, the D-pad control controls rotation of the robot.

<h3>Principle of three wheel omni movement</h3>

<img width="538" height="503" alt="omni movement" src="https://github.com/user-attachments/assets/04ccad06-3a8e-4de9-9a62-428a96484ca7" />

v1 = -Vx + angle_v  
v2 = cos60 Vx - sin60 Vy + angle_v  
v3 = cos60 Vx + sin60 Vy + angle_v  

so for a desired speed in a given direction(dir_angle) with a given speed of rotation(angular_v)  

vx = -speed * sin(dir_angle)  
vy = speed * cos(dir_angle)  
v1 = -vx + angular_v  
v2 = 0.5 vx - √3 / 2 * vy + angular_v  
v3 = 0.5 vx +√3 / 2  * vy + angular_v


<h3>Instructions</h3>  
Just drop rc.py and otto3wd.py in Otto's root directory.

