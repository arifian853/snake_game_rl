# --- START OF FILE q_learning_agent.py ---

import random
import numpy as np
from collections import defaultdict
import pickle

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, epsilon=1.0, epsilon_decay=0.999, epsilon_min=0.01):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        # Aksi: [0: Lurus, 1: Kanan, 2: Kiri]
        self.q_table = defaultdict(lambda: [0, 0, 0])
    
    def get_action(self, state):
        """
        Pilih aksi: eksplorasi (acak) atau eksploitasi (terbaik).
        Aksi akan berupa integer [0, 1, 2].
        """
        if random.random() < self.epsilon:
            # Eksplorasi: pilih aksi acak
            return random.randint(0, 2)
        else:
            # Eksploitasi: pilih aksi dengan Q-value tertinggi
            return np.argmax(self.q_table[state])
    
    def update_q_table(self, state, action, reward, next_state):
        """Update Q-table menggunakan formula Q-learning."""
        current_q = self.q_table[state][action]
        
        # Q-value masa depan terbaik dari state berikutnya
        max_future_q = np.max(self.q_table[next_state])
        
        # Formula Q-learning
        new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (reward + self.discount_factor * max_future_q)
        
        self.q_table[state][action] = new_q
    
    def decay_epsilon(self):
        """Kurangi epsilon untuk mengurangi eksplorasi seiring waktu."""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save_model(self, filename="snake_q_table.pkl"):
        """Simpan Q-table ke file."""
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)
        print(f"Model berhasil disimpan ke {filename}")
    
    def load_model(self, filename="snake_q_table.pkl"):
        """Muat Q-table dari file."""
        try:
            with open(filename, 'rb') as f:
                q_dict = pickle.load(f)
                self.q_table = defaultdict(lambda: [0, 0, 0], q_dict)
            print(f"Model berhasil dimuat dari {filename}")
        except FileNotFoundError:
            print(f"File {filename} tidak ditemukan. Memulai dengan Q-table kosong.")