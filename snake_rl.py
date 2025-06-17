# --- START OF FILE snake_rl.py ---

import pygame
import sys
import random
from collections import namedtuple

# Helper untuk posisi dan arah
Point = namedtuple('Point', 'x y')
Direction = {
    "UP": Point(0, -1),
    "DOWN": Point(0, 1),
    "LEFT": Point(-1, 0),
    "RIGHT": Point(1, 0)
}

class SnakeGameRL:
    def __init__(self, width=640, height=480, grid_size=20):
        pygame.init()
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Snake RL - Smart Agent')
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (213, 50, 80)
        self.GREEN = (0, 200, 0)
        
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        """Reset game ke kondisi awal"""
        self.direction = Direction["RIGHT"]
        
        self.head = Point(self.width // 2, self.height // 2)
        self.snake_body = [self.head, 
                           Point(self.head.x - self.grid_size, self.head.y),
                           Point(self.head.x - (2 * self.grid_size), self.head.y)]
        
        self.score = 0
        self.game_over = False
        self._place_food()
        self.steps = 0 # Lacak langkah untuk mencegah loop tak terbatas
        return self.get_state()
    
    def _place_food(self):
        """Tempatkan makanan di posisi acak yang tidak di tubuh ular."""
        while True:
            x = random.randint(0, (self.width - self.grid_size) // self.grid_size) * self.grid_size
            y = random.randint(0, (self.height - self.grid_size) // self.grid_size) * self.grid_size
            self.food = Point(x, y)
            if self.food not in self.snake_body:
                break
    
    def get_state(self):
        """
        Dapatkan state yang sederhana dan efektif.
        State adalah tuple 11-bit:
        [danger_straight, danger_right, danger_left,
         dir_left, dir_right, dir_up, dir_down,
         food_left, food_right, food_up, food_down]
        """
        head = self.head
        
        # Tentukan titik di sekitar kepala ular
        point_l = Point(head.x - self.grid_size, head.y)
        point_r = Point(head.x + self.grid_size, head.y)
        point_u = Point(head.x, head.y - self.grid_size)
        point_d = Point(head.x, head.y + self.grid_size)
        
        dir_l = self.direction == Direction["LEFT"]
        dir_r = self.direction == Direction["RIGHT"]
        dir_u = self.direction == Direction["UP"]
        dir_d = self.direction == Direction["DOWN"]
        
        # Tentukan bahaya relatif terhadap arah gerak
        danger_straight = (dir_r and self._is_collision(point_r)) or \
                          (dir_l and self._is_collision(point_l)) or \
                          (dir_u and self._is_collision(point_u)) or \
                          (dir_d and self._is_collision(point_d))
        
        danger_right = (dir_u and self._is_collision(point_r)) or \
                       (dir_d and self._is_collision(point_l)) or \
                       (dir_l and self._is_collision(point_u)) or \
                       (dir_r and self._is_collision(point_d))
                       
        danger_left = (dir_d and self._is_collision(point_r)) or \
                      (dir_u and self._is_collision(point_l)) or \
                      (dir_r and self._is_collision(point_u)) or \
                      (dir_l and self._is_collision(point_d))

        state = (
            int(danger_straight),
            int(danger_right),
            int(danger_left),
            
            int(dir_l),
            int(dir_r),
            int(dir_u),
            int(dir_d),
            
            int(self.food.x < self.head.x),  # Makanan di kiri
            int(self.food.x > self.head.x),  # Makanan di kanan
            int(self.food.y < self.head.y),  # Makanan di atas
            int(self.food.y > self.head.y)   # Makanan di bawah
        )
        return state

    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Tabrakan dengan dinding
        if pt.x < 0 or pt.x >= self.width or pt.y < 0 or pt.y >= self.height:
            return True
        # Tabrakan dengan tubuh sendiri
        if pt in self.snake_body[1:]:
            return True
        return False
    
    def step(self, action):
        """
        Lakukan satu langkah game berdasarkan aksi.
        Aksi: [Lurus, Belok Kanan, Belok Kiri]
        """
        self.steps += 1
        reward = 0
        
        # Arah baru berdasarkan aksi [straight, right, left]
        clock_wise = [Direction["RIGHT"], Direction["DOWN"], Direction["LEFT"], Direction["UP"]]
        idx = clock_wise.index(self.direction)

        if action == 1: # Belok kanan
            new_idx = (idx + 1) % 4
            self.direction = clock_wise[new_idx]
        elif action == 2: # Belok kiri
            new_idx = (idx - 1 + 4) % 4
            self.direction = clock_wise[new_idx]
        # Jika action == 0, tidak ada perubahan arah (lurus)

        # Update posisi kepala
        self.head = Point(self.head.x + self.direction.x * self.grid_size, self.head.y + self.direction.y * self.grid_size)
        self.snake_body.insert(0, self.head)
        
        # Cek tabrakan
        if self._is_collision() or self.steps > 100 * len(self.snake_body): # Hukuman jika terlalu lama tanpa makan
            self.game_over = True
            reward = -10 # Hukuman besar untuk mati / loop
            return self.get_state(), reward, self.game_over

        # Cek apakah memakan makanan
        if self.head == self.food:
            self.score += 1
            reward = 10 # Hadiah besar untuk makan
            self._place_food()
            self.steps = 0 # Reset step counter
        else:
            # Hapus ekor jika tidak makan
            self.snake_body.pop()
            
        return self.get_state(), reward, self.game_over
    
    def render(self):
        """Render game ke layar"""
        self.screen.fill(self.BLACK)
        
        # Gambar makanan
        pygame.draw.rect(self.screen, self.RED, [self.food.x, self.food.y, self.grid_size, self.grid_size])
        
        # Gambar ular
        for segment in self.snake_body:
            pygame.draw.rect(self.screen, self.GREEN, [segment.x, segment.y, self.grid_size, self.grid_size])
            pygame.draw.rect(self.screen, self.WHITE, [segment.x, segment.y, self.grid_size, self.grid_size], 1)

        # Tampilkan skor
        font = pygame.font.SysFont("arial", 25)
        value = font.render("Skor: " + str(self.score), True, self.WHITE)
        self.screen.blit(value, [10, 10])
        
        pygame.display.update()
        self.clock.tick(30)