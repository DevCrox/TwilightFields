# 🌙 Twilight Fields

A 2D action-adventure and chilling game built with Pygame where players explore a mystical world, battle enemies, and interact with NPCs in a beautifully crafted pixel environment.

## 🎮 Features

- **Dynamic Combat System**: Mouse-based attack mechanics with sound effects
- **Interactive World**: Multiple terrain types and destructible elements
- **NPC System**: Engage with characters through a rich dialog system
- **Progress Tracking**: Persistent statistics and achievement milestones
- **Smooth Animations**: Fluid character and combat animations
- **Camera System**: Dynamic zoom functionality for immersive gameplay

## 🛠️ Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd TwilightFields-main
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## 📋 Requirements

- Python 3.x
- Pygame 2.6.1

## 🎯 How to Play

### Controls
- **Arrow Keys**: Move character
- **Left Mouse Button**: Attack
- **E**: Interact with NPC
- **Arrow Keys**: Navigate UI elements

### Objectives
1. Explore the mystical world
2. Defeat enemies
3. Interact with NPCs
4. Complete objectives
5. Unlock achievements

## 📁 Project Structure

```
TwilightFields/
├── main.py           # Game entry point and core loop
├── config.py         # Game configuration and constants
├── sprites.py        # Game sprite classes
├── dialog.py        # Dialog system
├── database.py      # Game statistics handling
├── utils.py         # Utility functions
├── npc.py           # NPC behavior
├── win_screen.py    # Victory screen
├── dialogue.py      # Dialog content
├── requirements.txt  # Project dependencies
├── game_stats.db    # Game statistics database
├── img/             # Sprites and images
├── sounds/          # Audio files
├── Writing_Police/  # Custom fonts
└── NPC/             # NPC configurations
```

## 🔧 Core Components

### Game Engine (main.py)
- Window management (640x480 pixels)
- 60 FPS gameplay
- Layered sprite rendering
- Event handling
- Collision detection

### Sprite System (sprites.py)
- Sprite sheet management
- Character animations
- Enemy AI
- Combat mechanics

### Dialog System (dialog.py)
- Interactive dialog boxes
- Text animation
- Custom font rendering

### Database System (database.py)
- SQLite implementation
- Statistics tracking
- Achievement system

## 🎨 Assets

### Graphics
- Player character sprites
- Enemy sprites
- Terrain tiles
- NPC characters
- UI elements

### Audio
- Combat sound effects
- Background music
- Ambient sounds

### Fonts
- Arial (UI elements)
- SuperCaramel (Special text)

## 🏆 Achievement System

Unlock special achievements based on your victory count:
- 🎯 First Victory
- 🌟 5 Wins Achieved
- 💫 Veteran Player (10 wins)
- 👑 Champion Status (25 wins)
- 🏅 Legendary Hero (50 wins)
- 🌠 Master of All (100 wins)

## 🔄 Game States

1. **Intro Screen**
   - Title display
   - Play button
   - Game initialization

2. **Main Game**
   - World exploration
   - Combat
   - NPC interactions

3. **Victory Screen**
   - Win statistics
   - Achievement display
   - Replay option

4. **Game Over Screen**
   - Retry option
   - Statistics display

## 💾 Save System

- Automatic statistics saving
- Win count persistence
- Achievement tracking

## 🎵 Audio System

- Background music management
- Sound effect handling
- Volume control

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For support, please open an issue in the repository or contact me.

## 🎮 Game Preview

[Add screenshots or GIFs of your game here]

## 🔮 Future Updates

- [ ] ??
- [ ] ??
- [ ] ??
- [ ] ??
- [ ] ??

---

Made with ❤️ by [DevCrox]

*Last updated: [Current Date]* 
