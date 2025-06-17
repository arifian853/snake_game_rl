# --- START OF FILE train_snake_rl.py ---

import pygame
from snake_rl import SnakeGameRL
from q_learning_agent import QLearningAgent
import matplotlib.pyplot as plt
from collections import deque
import numpy as np

def plot_scores(scores, avg_scores):
    """Fungsi untuk menampilkan plot skor."""
    plt.figure(figsize=(10, 5))
    plt.plot(scores, label='Skor per Episode')
    plt.plot(avg_scores, label='Rata-rata 100 Episode', linewidth=2)
    plt.title('Progres Latihan Agen Ular')
    plt.xlabel('Episode')
    plt.ylabel('Skor')
    plt.legend()
    plt.grid(True)
    plt.show()

def train_agent(episodes=25000, render_every=2000):
    game = SnakeGameRL()
    agent = QLearningAgent(
        learning_rate=0.001,  # Learning rate lebih kecil untuk stabilitas
        discount_factor=0.9,
        epsilon_decay=0.9995 # Decay lebih lambat untuk eksplorasi lebih lama
    )
    # Coba muat model yang ada jika tersedia
    agent.load_model('snake_q_table.pkl')

    scores = []
    avg_scores = []
    recent_scores = deque(maxlen=100) # Untuk menghitung rata-rata skor

    for episode in range(1, episodes + 1):
        state = game.reset()
        
        while not game.game_over:
            # 1. Dapatkan aksi dari agen
            action = agent.get_action(state)
            
            # 2. Lakukan aksi dan dapatkan state baru, reward, dan status 'done'
            next_state, reward, done = game.step(action)
            
            # 3. Update Q-table
            agent.update_q_table(state, action, reward, next_state)
            
            state = next_state
            
            # Render game sesekali untuk melihat progres
            if episode % render_every == 0:
                game.render()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Pelatihan dihentikan oleh pengguna.")
                        agent.save_model('snake_q_table.pkl')
                        pygame.quit()
                        plot_scores(scores, avg_scores)
                        return
        
        # Simpan skor dan update epsilon
        scores.append(game.score)
        recent_scores.append(game.score)
        agent.decay_epsilon()
        
        # Print progress
        if episode % 100 == 0:
            avg_score = np.mean(recent_scores)
            avg_scores.append(avg_score)
            print(f"Episode {episode}, Rata-rata Skor (100 ep): {avg_score:.2f}, Epsilon: {agent.epsilon:.4f}")
            # Simpan model secara berkala
            if episode % 1000 == 0:
                agent.save_model('snake_q_table.pkl')

    # Simpan model final dan tampilkan plot
    print("Pelatihan selesai.")
    agent.save_model('snake_q_table.pkl')
    pygame.quit()
    plot_scores(scores, avg_scores)

if __name__ == "__main__":
    train_agent()