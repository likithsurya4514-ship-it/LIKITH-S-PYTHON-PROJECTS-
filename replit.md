# Hero's Destiny 🎮⚔️

A polished 2D action game built with Python and pygame where you survive waves of enemies in epic arcade-style combat!

## Overview

Hero's Destiny is a complete action game featuring:
- **Smooth 60 FPS gameplay** with responsive controls
- **Progressive difficulty** that increases with your score
- **Multiple enemy types**: Normal, Fast, and Tank enemies
- **Combat system** with melee attacks and energy projectiles
- **Particle effects** for visual polish
- **Three game states**: Start Menu, Active Gameplay, and Game Over

## Recent Changes

### October 25, 2025
- **Wave System Implementation**: Added proper wave-based progression
  - Each wave spawns a set number of enemies (5 + 2 per wave)
  - Clear all enemies to advance to next wave
  - Wave announcement displays when new wave starts
  - UI shows current wave, spawn progress, and enemy count
  - Difficulty multiplier increases 15% per wave
- **Enemy Type Unlocks**: Enemies unlock based on wave number (Wave 3: Fast, Wave 5: Tank)
- **Enhanced UI**: Added wave display, spawn progress, and wave cleared message
- **Refined Difficulty Scaling**: Spawn rate and difficulty tied to wave progression

### Initial Implementation
- Created complete OOP structure with Player, Enemy, Projectile, and Particle classes
- Implemented smooth movement physics with gravity and jumping
- Built three-state game manager (menu, playing, game over)
- Added visual feedback with particle effects and hit flashing
- Configured headless mode support for Replit environment

## How to Run

The game runs automatically when you click the **Run** button. 

If you need to run it manually:
```bash
python main.py
```

## Game Controls

### Movement
- **Move Left**: ← (Left Arrow) or A
- **Move Right**: → (Right Arrow) or D
- **Jump**: ↑ (Up Arrow) or W

### Combat
- **Attack**: SPACE (fires both melee slash and energy projectile)

### Menu Controls
- **Start Game**: SPACE (from main menu)
- **Restart**: R (from game over screen)

## Gameplay Guide

### Objective
Survive progressive waves of enemies! Each wave spawns a set number of enemies that you must defeat to advance. Waves get harder with more enemies, faster spawning, and stronger foes!

### Player Stats
- **Health**: 100 HP (displayed in top-left corner)
- **Melee Damage**: 50 per hit
- **Projectile Damage**: 25 per hit
- **Movement Speed**: Responsive horizontal movement with smooth jumping

### Wave System

The game uses a progressive wave-based system:

#### Wave Mechanics
- **Wave 1**: Starts with 5 enemies (all normal type)
- **Each New Wave**: Adds 2 more enemies (+2 per wave)
- **Wave Progression**: Clear all enemies to advance to the next wave
- **Wave States**: 
  - Spawning: Enemies are being spawned into the arena
  - Fighting: All wave enemies spawned, defeat them to continue
  - Cleared: Brief celebration, then auto-advance to next wave

#### Wave Progression
- Wave 1-2: Only Normal enemies
- Wave 3+: Fast enemies start appearing (50% chance)
- Wave 5+: Tank enemies join the fight (30% chance)
- Difficulty multiplier increases by 15% per wave
- Spawn rate increases with each wave (enemies appear faster)

### Enemy Types

#### Normal Enemies (Red)
- **Health**: 50 HP
- **Damage**: 20 per hit
- **Speed**: Medium
- **Score Value**: 10 points
- **Appears**: All waves

#### Fast Enemies (Orange)
- **Unlocks at**: Wave 3+
- **Health**: 30 HP
- **Damage**: 15 per hit
- **Speed**: Fast
- **Score Value**: 10 points

#### Tank Enemies (Purple)
- **Unlocks at**: Wave 5+
- **Health**: 100 HP
- **Damage**: 30 per hit
- **Speed**: Slow but powerful
- **Score Value**: 10 points

### Combat Tips
- Each attack fires both a melee slash and energy projectile
- Keep moving to avoid enemy collisions
- Use jumping to create space from enemies
- Watch your health bar - enemies damage you on contact
- Time your attacks - there's a cooldown between strikes

## Project Architecture

### Code Structure
```
main.py
├── Constants & Configuration
├── Particle Class (visual effects)
├── Projectile Class (energy blasts)
├── Player Class (hero character)
├── Enemy Class (AI opponents)
└── Game Class (main game manager)
```

### Key Features Implementation
- **Physics Engine**: Custom gravity, jumping, and ground collision
- **AI System**: Enemies track and move toward player position
- **Combat System**: Hit detection for both melee and ranged attacks
- **Particle System**: Dynamic visual effects for hits and attacks
- **State Management**: Clean separation of menu, gameplay, and game over states
- **Difficulty Scaling**: Mathematical progression based on score

### Design Decisions
- Used simple geometric shapes (rectangles and circles) for all visuals
- No external assets required - everything is procedurally drawn
- Headless mode support for Replit environment (no audio)
- 60 FPS target for smooth, responsive gameplay
- Object-oriented design for modularity and maintainability

## Technical Details

### Dependencies
- **Python 3.11**
- **pygame 2.6.1**

### Configuration
- Screen Resolution: 800x600
- Target FPS: 60
- Ground Level: 500px from top
- Gravity: 0.8 (consistent falling acceleration)

### Performance
The game is optimized for smooth performance:
- Efficient particle system with lifetime management
- Object pooling for enemies and projectiles
- Clean removal of inactive game objects
- Gradient background pre-calculated per frame

## Future Enhancement Ideas

### Planned Features
- Boss wave encounters every 10 kills
- Collectible power-ups (health, attack speed boost)
- Combo system with score multipliers
- Additional enemy types with unique behaviors
- Enhanced visual effects and animations
- Background music and sound effects (when audio is available)
- High score tracking and leaderboard

### Potential Improvements
- Persistent high score storage
- Multiple difficulty modes
- Character customization
- Weapon variety
- Environmental hazards
- Co-op multiplayer support

## Troubleshooting

### Game won't start
- Make sure pygame is installed: `pip install pygame`
- Check that Python 3.11 is active
- Verify no syntax errors in main.py

### Performance issues
- The game targets 60 FPS
- If running slowly, check system resources
- Ensure no other heavy processes are running

### Controls not responding
- Make sure the game window has focus
- Try clicking on the game window
- Restart the game with R key if in game over state

## User Preferences

- **Coding Style**: Clean, well-commented OOP design
- **No external assets**: All graphics procedurally generated
- **Replit-optimized**: Handles headless environment gracefully

---

**Have fun playing Hero's Destiny! See how high you can score!** 🎮⚔️
