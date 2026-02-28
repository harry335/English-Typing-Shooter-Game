# SciType Shooter: Academic Typing & Space Combat Game

An interactive educational game developed with **Python** and **Pygame**, designed to help students master academic vocabulary in STEM fields through an engaging Space Invaders-style experience.

## 🚀 Key Features
* **Academic Word Bank Integration**: Automatically scrapes professional terminology from the **National Academy for Educational Research** website, covering Mathematics, Physics, Chemistry, and Biology.
* **Dynamic Difficulty Scaling**: Enemy ship generation, word length, and falling speeds scale progressively over time to challenge the player.
* **Custom Hand-Drawn Assets**: All player spacecraft (X-Wing style) and enemy Star Destroyer designs were originally illustrated using **Procreate**.
* **Easter Egg Power-ups**: Features local cultural references (NTU and TNFSH Student IDs) as special items for HP and bullet recovery.

## 🛠 Technical Architecture
The system is built on a modular architecture to ensure scalability and maintainability:
* **Game Engine**: Pygame for real-time rendering and sprite management.
* **Data Scraper**: BeautifulSoup4 and Requests for harvesting academic word banks.
* **Persistence**: File-based storage (`.txt`) for player high scores and progression data.

## 🧠 Engineering Challenges & Solutions
I primarily architected the **Core System Template** and solved several algorithmic bottlenecks:

1.  **State Machine & Scene Switching**: 
    * **Challenge**: Managing transitions between complex menus and gameplay without crashing the main loop.
    * **Solution**: Implemented a function-based return message system (`word` messages) to decouple page logic from the main loop.
2.  **Advanced Font Rendering**: 
    * **Challenge**: Pygame's default rendering cannot handle multi-colored text within a single string for typing feedback.
    * **Solution**: Developed a custom rendering function that calculates character widths and overlays input text onto hint text in real-time.
3.  **Collision Avoidance in Spawning**: 
    * **Challenge**: Randomly generated words frequently overlapped.
    * **Solution**: Developed a **"Track-Based Occupancy"** algorithm using lists to track active screen lanes, ensuring new enemies only spawn in available tracks.

## 📂 Project Structure
* `src/`: Main game logic and web crawler script.
* `assets/`: Hand-drawn sprites and sound effects.
* `data/`: Scraped academic libraries and player records.

## 👥 Contributors (Team 18)
* **宋承軒 (Department of Mathematics, NTU)**: Core system template, layout design, and report documentation.
* **李承彥 (Department of Electrical Engineering, NTU)**: Main game logic, system flow, and crawler modification.
* **李柏宇 (Department of Electrical Engineering, NTU)**: Character and background digital illustrations.
* **戴瑞哲 (Department of Electrical Engineering, NTU)**: Initial crawler development and poster design.

## 📄 Documentation
* [Project Presentation (PDF)](docs/Project_Presentation.pdf) - Detailed overview of the project and design concepts.

## 📺 Gameplay Demo
[![Watch the Demo](https://img.youtube.com/vi/Jj1duX9HpQE/0.jpg)](https://youtu.be/Jj1duX9HpQE)
*點擊上方圖片即可觀看遊戲演示影片 (YouTube)*