# HIT137_A3_T2
a complete, fully functional 2D side-scrolling game
# 2D Side-Scrolling Game

A complete 2D side-scrolling adventure game built with Python and Pygame, featuring multiple levels, enemies, collectibles, and boss battles.

## Features

### Core Gameplay
- **Player Character**: Blue hero with movement, jumping, and shooting abilities
- **3 Progressive Levels**: Increasing difficulty with different enemy types
- **Boss Battle**: Epic final boss fight in Level 3
- **Scoring System**: Points for defeating enemies and collecting items
- **Health & Lives**: Health bar, lives system, and invulnerability frames

### Enemy Types
- **Basic Enemy** (Red): Standard enemy with moderate stats
- **Fast Enemy** (Orange): Quick but fragile
- **Tank Enemy** (Dark Red): Slow but heavily armored
- **Boss Enemy** (Purple): Large boss with special attacks and movement patterns

### Collectibles
- **Health Packs** (Green): Restore 30 HP
- **Extra Lives** (Blue): Gain additional life
- **Point Bonuses** (Yellow): Bonus score points

### Game Mechanics
- Physics-based jumping with gravity
- Collision detection system
- Progressive level difficulty
- Game over and victory screens
- Restart functionality

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move left/right |
| Space / Up Arrow / W | Jump |
| F | Shoot projectiles |
| R | Restart (on game over) |
| ESC | Quit game |

## Requirements

```bash
pip install pygame
```

## How to Run

1. Ensure Python 3.7+ is installed
2. Install Pygame: `pip install pygame`
3. Run the game: `python side_scrolling_game.py`

## Game Progression

### Level 1
- 15 Basic enemies
- Introduction to game mechanics
- Basic collectibles

### Level 2
- 25 Mixed enemies (Basic + Fast)
- Increased spawn rate
- More collectible variety

### Level 3
- 20 Mixed enemies + Boss fight
- All enemy types present
- Epic boss battle with shooting mechanics

## Scoring

| Target | Points |
|--------|--------|
| Basic Enemy | 10 |
| Fast Enemy | 15 |
| Tank Enemy | 25 |
| Boss Enemy | 100 |
| Health Pack | 5 |
| Extra Life | 20 |
| Point Bonus | 50 |

## Technical Implementation

### Object-Oriented Design
- **Player Class**: Movement, health, lives, shooting
- **Enemy Classes**: Different types with unique behaviors
- **Boss Class**: Advanced AI with shooting patterns
- **Projectile Classes**: Player and enemy projectiles
- **Collectible Class**: Various item types
- **Game Class**: Level management and game state

### Key Features
- Sprite-based collision detection
- Real-time health bars
- Progressive difficulty scaling
- Professional game state management
- Clean code architecture with proper OOP principles

## File Structure

```
side_scrolling_game.py    # Main game file
README.md                 # This file
```

## Development Notes

This game demonstrates:
- Advanced Python OOP concepts
- Game development with Pygame
- Collision detection algorithms
- Game state management
- User interface design
- Real-time graphics rendering

## License

Educational project - free to use and modify.
