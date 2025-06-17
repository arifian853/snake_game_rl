import pygame
import sys
import random

# --- Inisialisasi Pygame ---
pygame.init()

# --- Konfigurasi Jendela Game ---
screen_width = 720
screen_height = 480
# Ukuran satu blok/kotak di grid
grid_size = 20
# Pastikan ukuran jendela adalah kelipatan dari grid_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game Ular Klasik')

# --- Warna (format RGB) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# --- Konfigurasi Game ---
clock = pygame.time.Clock()
# Kecepatan gerak ular (frame per second)
snake_speed = 15

# Font untuk skor
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def show_score(score):
    """Menampilkan skor di layar"""
    value = score_font.render("Skor: " + str(score), True, WHITE)
    screen.blit(value, [10, 10])

def draw_snake(snake_body):
    """Menggambar semua segmen tubuh ular"""
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], grid_size, grid_size])

def game_loop():
    """Fungsi utama yang menjalankan game"""
    game_over = False
    game_close = False

    # Posisi awal ular di tengah layar
    x_pos = screen_width / 2
    y_pos = screen_height / 2

    # Perubahan posisi (kecepatan) awal
    x_change = 0
    y_change = 0

    # Tubuh ular (list dari koordinat [x, y])
    snake_body = []
    snake_length = 1

    # Posisi makanan pertama kali
    food_x = round(random.randrange(0, screen_width - grid_size) / grid_size) * grid_size
    food_y = round(random.randrange(0, screen_height - grid_size) / grid_size) * grid_size

    # Loop utama game
    while not game_over:

        # Loop untuk layar "Game Over"
        while game_close:
            screen.fill(BLUE)
            message = font_style.render("Anda Kalah! Tekan 'C' untuk Main Lagi atau 'Q' untuk Keluar", True, RED)
            screen.blit(message, [screen_width / 6, screen_height / 3])
            show_score(snake_length - 1)
            pygame.display.update()

            # Menunggu input pemain
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop() # Memulai game baru

        # Event handler (input dari keyboard)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -grid_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = grid_size
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -grid_size
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = grid_size
                    x_change = 0
        
        # Cek tabrakan dengan dinding
        if x_pos >= screen_width or x_pos < 0 or y_pos >= screen_height or y_pos < 0:
            game_close = True

        # Update posisi ular
        x_pos += x_change
        y_pos += y_change

        # Menggambar latar belakang
        screen.fill(BLACK)
        
        # Menggambar makanan
        pygame.draw.rect(screen, RED, [food_x, food_y, grid_size, grid_size])
        
        # Membuat kepala baru untuk ular
        snake_head = [x_pos, y_pos]
        snake_body.append(snake_head)

        # Logika pertumbuhan ular
        if len(snake_body) > snake_length:
            del snake_body[0]

        # Cek tabrakan dengan diri sendiri
        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_close = True
        
        # Menggambar ular
        draw_snake(snake_body)
        
        # Menampilkan skor
        show_score(snake_length - 1)

        # Memperbarui tampilan
        pygame.display.update()

        # Cek jika ular memakan makanan
        if x_pos == food_x and y_pos == food_y:
            # Memunculkan makanan baru di posisi acak
            food_x = round(random.randrange(0, screen_width - grid_size) / grid_size) * grid_size
            food_y = round(random.randrange(0, screen_height - grid_size) / grid_size) * grid_size
            snake_length += 1

        # Mengatur kecepatan game
        clock.tick(snake_speed)

    # Keluar dari Pygame dan program
    pygame.quit()
    sys.exit()

# Memulai game
if __name__ == "__main__":
    game_loop()