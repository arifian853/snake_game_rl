# --- START OF FILE test_snake_rl.py ---

import pygame
from snake_rl import SnakeGameRL
from q_learning_agent import QLearningAgent

def test_agent():
    game = SnakeGameRL()
    agent = QLearningAgent()
    agent.epsilon = 0  # Tidak ada eksplorasi saat testing (selalu pilih aksi terbaik)
    agent.load_model('snake_q_table.pkl')
    
    running = True
    games_played = 0
    total_score = 0
    
    while running:
        state = game.reset()
        games_played += 1
        
        while not game.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            
            if not running:
                break
            
            # Dapatkan aksi dari state saat ini
            action = agent.get_action(state)
            
            # Lakukan langkah
            next_state, _, _ = game.step(action)
            state = next_state
            
            game.render()
        
        total_score += game.score
        avg_score = total_score / games_played
        print(f"Game {games_played}: Skor = {game.score}, Rata-rata Skor = {avg_score:.2f}")
    
    pygame.quit()

if __name__ == "__main__":
    test_agent()