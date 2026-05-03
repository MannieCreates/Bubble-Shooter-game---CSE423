![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenGL](https://img.shields.io/badge/OpenGL-Graphics-5586A4?style=for-the-badge&logo=opengl&logoColor=white)
![Computer Graphics](https://img.shields.io/badge/Computer%20Graphics-Algorithms-ff6f00?style=for-the-badge)
![PyOpenGL](https://img.shields.io/badge/PyOpenGL-Implementation-1f425f?style=for-the-badge)
![Algorithms](https://img.shields.io/badge/Midpoint%20Algorithms-Line%20%7C%20Circle-9b59b6?style=for-the-badge)
![2D Game](https://img.shields.io/badge/2D%20Game-Bubble%20Shooter-2ecc71?style=for-the-badge)
![Status](https://img.shields.io/badge/Project-Completed-success?style=for-the-badge)

This project is built to strengthen and demonstrate a clear understanding of core computer graphics concepts through actual implementation rather than relying on built-in drawing functions. It focuses on how basic rendering and geometric ideas come together to form a working interactive system. At the heart of the project are implementations of the Midpoint Line Algorithm and Midpoint Circle Algorithm, along with zone-based transformations to support drawing in all directions. These ideas are used directly in building the game visuals instead of using pre-defined shapes. The game also brings together real-time updates, collision detection using simple distance calculations, object spawning, and gradually increasing difficulty. Overall, it connects theoretical graphics concepts with practical game development in a simple and structured way.


⚙️ Game Logic & Rules
The game ends if a bubble collides with the shooter
The player loses if three bullets are missed
The player also loses after three bubbles fall off-screen
A pause/resume system allows controlled gameplay flow
A restart option resets all game states instantly

Collision detection is handled using Euclidean distance calculations between circular objects, ensuring accurate interaction between bullets and bubbles.


🎮 Controls
A / D → Move the shooter left and right
Space → Fire bullet
Mouse Click → Restart game, Pause / Resume, Exit game
