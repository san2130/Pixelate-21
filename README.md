<html>
<body>
    
<h1 align=center>Pixelate 2021 </h1>
    
<h4 align=center>Computer Vision based event organised by Robotics Club of IIT (BHU) Varanasi</h4><br>
    
<p align=center>
    <img src="https://github.com/san2130/Pixelate-21/blob/main/robo.jpg" width="30%"/>
</p>
    
<h3> Problem Statement</h3>

1. There are <b>two paths</b> in the Arena (INNER and OUTER Square) with <b>four connecting paths</b> of different colours.<br>
2. Bot can change between OUTER path and INNER path. It is allowed to move in <b> clockwise direction </b> only. 
3. The portion of the arena in <b> BLACK </b> colour is restricted for the movement of the bot.<br>
4. There are <b>three shapes</b> (Square, Circle and Triangle) of <b>two different colours</b> (Red and Yellow), distinguishing each block in the arena in six different ways. <br>
5. On the outermost path there will be <b>four black arrows</b> at the end of connecting paths pointing in clockwise direction. These arrows mark the <b>starting zone</b> where the bot will be placed initially.<br>
6. The centre of the arena is the <b>home zone</b>. The bot has to traverse the arena, complete a full round in a clockwise manner and finish at the home zone. <br>

<h3 align=center>Plan of Action</h3>

1. The bot is placed on one of the starting zones (represented by black arrows on the arena). <br>
2. Abbreviations which corresponds to a specific colour and shape are as follows<br>

<table align=center>
   <td align="center">
         <img src="https://i.gyazo.com/895b7ba241c10848fb4b664a480a36bf.png" width="100px;" alt=""/>
         <br />
         <sub>
             <b>TR : Red Triangle</b>
         </sub>
      <br />
   </td>
   <td align="center">
         <img src="https://i.gyazo.com/908678469cea8f95f04549d0d02dea6e.png" width="100px;" alt=""/>
         <br />
         <sub>
             <b>SR : Red Square</b>
         </sub>
      <br />
   </td>
   <td align="center">
         <img src="https://i.gyazo.com/e8d85fb4f53b58cd0d49655328ab909b.png" width="100px;" alt=""/>
         <br />
         <sub>
             <b>CR : Red Circle</b>
         </sub>
      <br />
   </td>
   <td align="center">
         <img src="https://i.gyazo.com/72ab1c3524c968f7f142526dd48487e7.pngg" width="100px;" alt=""/>
         <br />
         <sub>
             <b>CY : Yellow Circle</b>
         </sub>
      <br />
   </td>
   <td align="center">
         <img src="https://i.gyazo.com/9f9feec55eed87f775fd18e4ed92ef56.png" width="100px;" alt=""/>
         <br />
         <sub>
             <b>SY : Yellow Square</b>
         </sub>
      <br />
   </td>
   <td align="center">
         <img src="https://i.gyazo.com/32ee8196e737e9acf97434205d7a0445.png" width="100px;" alt=""/>
         <br />
         <sub>
             <b>TY : Yellow Triangle</b>
         </sub>
      <br />
   </td>
</table>
    
3. On start of each turn, a function returns a <b>random shape-color combination</b> from the above list. The bot then finds the block (with the corresponding shape and colour) which it can reach following a clockwise path and is at the least distance from its current position.<br>
4. As soon as the bot stops moving, bot has to ask for input using the function provided. <br>
5. This continues till the bot has completed a full round around the center, then it should move to home zone.<br>
6. On reaching the home zone the bot should signal that it has finished the task and process will terminate. <br>
    
<h3 align=center>Our Approach</h3>
    
- We used <b>Computer Vision</b> for Image Segmentation (extracting shapes of different colors from the arena) and <b>Djikstra</b> algorithm (on a weighted directed graph) to trace path. 

<h3 align=center>Team B11</h3>
    
<table align=center>
   <td align="center">
      <a href="https://github.com/san2130">
         <img src="https://avatars2.githubusercontent.com/u/60649618?s=460&v=4" width="100px;" alt=""/>
         <br />
         <sub>
            <b>Sandeepan Ghosh</b>
         </sub>
      </a>
      <br />
   </td>
   <td align="center">
      <a href="/">
         <img src="https://avatars.githubusercontent.com/u/98117481?v=4" width="100px;" alt=""/>
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
