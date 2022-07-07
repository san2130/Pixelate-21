<html>
<body>
    
<h1 align=center>Pixelate 2021 </h1>
    
<h4 align=center>Computer Vision based event organised by Robotics Club of IIT (BHU) Varanasi</h4><br>
    
<p align=center>
    <img src="https://github.com/san2130/Pixelate-21/blob/main/robo%20(1).jpg" width="30%"/>
</p>
    
<h3> Problem Statement</h3>

- There is a **12*12** Grid made up of cells of different colors **white, black, blue, green, yellow, red, pink**.
- There are exactly **2 pink tiles** one with a **dark blue circle** and the other, a **dark blue square** on top of it. There are exactly **2 light blue tiles** one with a **dark blue circle** and the other, a **dark blue square** on top of it. 
- **Circle** on **pink** tile represents a **covid patient** and **circle** on a **blue tile** represents **covid hospital** while similarly the **square** corresponds to **non covid patients and hospitals**.
- Each colored tile has a certain cost with it **red-4, yellow-3, green-2, white-1, black-invalid cell**.
- There are certain cells which can be entered from only **one direction** specified by a **red triangle** on top of it. 
- Basically our bot has to go to each patient and take it to the corresponding hospital(covid/non-covid) while taking the valid path with **minimum cost**. 
- The bot has an **ArUco marker** on top of it and we are given a **static overhead camera feed**. 
<br> 

<h2 align="center">The Pybullet Arena<br><br><img src="https://github.com/san2130/Pixelate-21/blob/main/Arena.png" width="70%"/></h2> 
<br>
    
### Approach

- We used **Computer Vision OpenCV** functions to read the camera image and preprocess the grid data by creating a custom **mask** for every colour and segmenting it out and then applying **shape detection** on it to detect a square, circle and triangle. 
- Following that a **12*12 adjacency matrix** was made representing a **directed weighted graph**. 
- The minimum path to each patient is caluclated using **Djikstra's Algorithm**, and then the bot is made to move towards it. 
- After picking up the patient, we check whether the patient is covid/non-covid by removing the pink cover and then he is taken to the appropriate hospital, again following the minimum path. 
- The program terminates after both the patients have been taken to their respective hospitals. 
- For movement of the bot, on every cell the camera feed is called and the **position** of the bot and its **orientation** are detected using **OpenCV** functions, based on which the **Proportional Controller** calculates the torque to be given, to each wheel.  
    
<br>

### Working
You can check out the final video of the Pybullet simulation [here](https://drive.google.com/file/d/1RNXEZoWE4vzxKnGCpUiqtI4abuo0aFy0/view?usp=sharing).  
<br>
<br>
### Setup  
- Clone the repo and create a virtual environment and activate it using 
```
python3 -m venv venv
source venv/bin/activate
```
- Then execute the folowing command
``` 
pip install -e pixelate_arena
```  
- Execute our solution b11.py using 
```
python3 b11.py
```
<br>
<br>  

<h3 align=center>Team B11</h3>
    
<table align=center>
   <td align="center">
      <a href="https://github.com/san2130">
         <img src="https://avatars.githubusercontent.com/u/88130555?v=4" width="150px;" alt=""/>
         <br />
         <sub>
            <b>Sandeepan Ghosh</b>
         </sub>
      </a>
      <br />
   </td>
   <td align="center">
      <a href="https://github.com/raghavansh">
         <img src="https://avatars.githubusercontent.com/u/78599181?v=4" width="150px" alt=""/>
         <br />
         <sub>
            <b>Raghavansh Singla</b>
         </sub>
      </a>
      <br />
   </td>
</table>
 
</body>
</html>
