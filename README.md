# Snake Game

A simple Snake Game implemented in Python. The game features a snake that grows longer as it consumes food, and the objective is to maximize the score without colliding with the game boundaries, enemies, or the snake's own body.

## Getting Started

1. Clone or download the repository to your local machine:

    ```bash
    git clone https://github.com/grantwilson38/basic-snake-game.git
    ```

2. Ensure you have Python and the required libraries installed. You can install the necessary libraries using:

    ```bash
    pip install pygame
    ```

3. Run the game by executing the Python script:

    ```bash
    python snake_game.py
    ```

## Game Controls

- Use the arrow keys (Up, Down, Left, Right) to control the snake's direction.

## Game Rules

1. The snake starts with a single segment.
2. Eating food (the small colored dots) increases the snake's length and score.
3. Golden powerups make you temporarily invincible. Blue powerups make you longer. White powerups increase your score.
4. You lose a life every time the snake collides with its own body, the game boundaries, or an enemy.
5. Enemies die when they collide with each other or with your body.

## Customization

You can customize certain aspects of the game by modifying the constants defined at the beginning of the script:

- `SCREEN_WIDTH` and `SCREEN_HEIGHT` define the dimensions of the game window.
- `SNAKE_SIZE` and `FOOD_SIZE` determine the size of the snake segments and food items.
- Color constants (`BLACK`, `WHITE`, `RED`, `GREEN`, `BLUE`) can be adjusted to change the appearance of the game elements.

Feel free to explore and modify the code to add new features or enhance existing ones.

## Dependencies

- Python 3.x
- Pygame library

## Acknowledgments

This game is inspired by classic Snake games and was created for educational purposes. It serves as a simple example of game development using Python.

## License

This Snake Game is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code for your projects.# basicSnakeGame
