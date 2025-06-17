# Snake Reinforcement Learning Project

A reinforcement learning implementation of the classic Snake game using Q-Learning algorithm. The AI agent learns to play Snake through trial and error, gradually improving its performance over thousands of training episodes.

## 🎮 Project Overview

This project demonstrates how an AI agent can learn to play the Snake game using Q-Learning, a model-free reinforcement learning algorithm. The agent starts with no knowledge of the game and learns optimal strategies through exploration and exploitation.

## 🚀 Features

- **Q-Learning Implementation**: Custom Q-Learning agent with configurable hyperparameters
- **Smart State Representation**: 11-dimensional state space capturing danger detection and food direction
- **Visual Training**: Watch the agent learn in real-time with pygame visualization
- **Performance Tracking**: Real-time plotting of training progress and average scores
- **Model Persistence**: Save and load trained models for continued training or testing
- **Collision Detection**: Comprehensive collision system for walls and self-collision
- **Adaptive Exploration**: Epsilon-greedy strategy with decay for balanced exploration/exploitation

## 📁 Project Structure

```
reinforcement_learning/
├── snake.py              # Original Snake game implementation
├── snake_rl.py           # RL-optimized Snake environment
├── q_learning_agent.py   # Q-Learning agent implementation
├── train_snake_rl.py     # Training script with visualization
├── test_snake_rl.py      # Testing script for trained agent
├── snake_q_table.pkl     # Saved Q-table (generated after training)
└── README.md             # README
```

## 🧠 How It Works

### State Representation
The agent perceives the game through an 11-dimensional state vector:
- **Danger Detection** (3 bits): Immediate collision threats (straight, right, left)
- **Current Direction** (4 bits): Snake's current movement direction
- **Food Location** (4 bits): Relative position of food (left, right, up, down)

### Action Space
The agent can choose from 3 actions:
- `0`: Continue straight
- `1`: Turn right
- `2`: Turn left

### Reward System
- **+10**: Eating food
- **-10**: Collision (game over)
- **0**: Normal movement
- **-10**: Taking too long without eating (prevents infinite loops)

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone https://github.com/arifian853/snake_game_rl.git
cd snake_game_rl
```

2. **Create Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install required dependencies**:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Training the Agent

Run the training script to start teaching the AI:

```bash
python train_snake_rl.py
```

**Training Features**:
- Trains for 25,000 episodes by default
- Renders gameplay every 2,000 episodes
- Saves model every 1,000 episodes
- Displays progress plots after training
- Press 'X' to stop training early

### Testing the Trained Agent

Watch your trained agent play:

```bash
python test_snake_rl.py
```

**Testing Features**:
- Loads the saved Q-table
- No exploration (epsilon = 0)
- Displays real-time performance statistics
- Continuous gameplay until manually stopped

### Playing the Original Game

Try the human-playable version:

```bash
python snake.py
```

## ⚙️ Configuration

### Hyperparameters (in `q_learning_agent.py`):
- **Learning Rate**: `0.001` - How quickly the agent updates its knowledge
- **Discount Factor**: `0.9` - Importance of future rewards
- **Epsilon Decay**: `0.9995` - Rate of exploration reduction
- **Epsilon Min**: `0.01` - Minimum exploration rate

### Game Settings (in `snake_rl.py`):
- **Grid Size**: `20px` - Size of each game cell
- **Window Size**: `640x480` - Game window dimensions
- **Max Steps**: `100 * snake_length` - Prevents infinite loops

## 📊 Training Progress

The training script generates real-time plots showing:
- Score per episode
- Rolling average over 100 episodes
- Training progress visualization

**Expected Performance**:
- **Episodes 0-5,000**: Random exploration, low scores
- **Episodes 5,000-15,000**: Learning basic survival
- **Episodes 15,000+**: Optimized food-seeking behavior

## 🔧 Customization

### Modify Training Parameters

Edit `train_snake_rl.py`:

```python
def train_agent(episodes=25000, render_every=2000):
    agent = QLearningAgent(
        learning_rate=0.001,    # Adjust learning speed
        discount_factor=0.9,    # Future reward importance
        epsilon_decay=0.9995    # Exploration decay rate
    )
```

### Change Game Environment

Modify `snake_rl.py` constructor:

```python
game = SnakeGameRL(width=800, height=600, grid_size=25)
```

## 🎓 Learning Outcomes

This project demonstrates:
- **Reinforcement Learning Fundamentals**: Q-Learning algorithm implementation
- **State Space Design**: Effective feature engineering for RL
- **Exploration vs Exploitation**: Epsilon-greedy strategy
- **Neural Network Alternative**: Tabular Q-Learning approach
- **Game AI Development**: Applying RL to classic games

## 🚧 Future Improvements

- **Deep Q-Network (DQN)**: Replace tabular Q-learning with neural networks
- **Experience Replay**: Add memory buffer for more stable learning
- **Double DQN**: Reduce overestimation bias
- **Prioritized Experience Replay**: Focus on important experiences
- **Multi-Agent Training**: Train multiple agents simultaneously

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Performance optimizations
- Additional RL algorithms (SARSA, Actor-Critic)
- Enhanced visualization
- Hyperparameter tuning
- Documentation improvements

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Inspired by classic reinforcement learning tutorials
- Built with Python, Pygame, and NumPy
- Q-Learning algorithm based on Sutton & Barto's "Reinforcement Learning: An Introduction"

---

**Happy Learning! 🐍🤖**
        