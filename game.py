import pygame
import random
# Импортируем новую константу SQUARE_SPEED
from config import WINDOW_WIDTH, WINDOW_HEIGHT, SQUARE_SIZE, BLACK, RED, SQUARE_SPEED 

class SquareGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Случайный квадрат")
        
        # Создаем квадрат в случайном месте
        self.square_x = random.randint(0, WINDOW_WIDTH - SQUARE_SIZE)
        self.square_y = random.randint(0, WINDOW_HEIGHT - SQUARE_SIZE)
        
        # --- НОВЫЕ ПЕРЕМЕННЫЕ ДЛЯ ДВИЖЕНИЯ ---
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

    def handle_input(self, event):
        """Обрабатывает нажатия и отпускания клавиш WASD и ESC."""
        
        # Обработка выхода
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
            # Нажатие WASD
            if event.key == pygame.K_a:
                self.move_left = True
            elif event.key == pygame.K_d:
                self.move_right = True
            elif event.key == pygame.K_w:
                self.move_up = True
            elif event.key == pygame.K_s:
                self.move_down = True
        
        elif event.type == pygame.KEYUP:
            # Отпускание WASD
            if event.key == pygame.K_a:
                self.move_left = False
            elif event.key == pygame.K_d:
                self.move_right = False
            elif event.key == pygame.K_w:
                self.move_up = False
            elif event.key == pygame.K_s:
                self.move_down = False
                
        return True # Продолжать работу

    def update_position(self):
        """Обновляет координаты квадрата и ограничивает их границами экрана."""
        
        # Горизонтальное движение
        if self.move_left:
            self.square_x -= SQUARE_SPEED
        if self.move_right:
            self.square_x += SQUARE_SPEED
            
        # Вертикальное движение
        if self.move_up:
            self.square_y -= SQUARE_SPEED
        if self.move_down:
            self.square_y += SQUARE_SPEED
            
        # Ограничение движения
        self.square_x = max(0, min(self.square_x, WINDOW_WIDTH - SQUARE_SIZE))
        self.square_y = max(0, min(self.square_y, WINDOW_HEIGHT - SQUARE_SIZE))
    
    def run(self):
        running = True
        clock = pygame.time.Clock() # Добавляем часы для контроля FPS
        
        while running:
            # 1. Обработка событий
            for event in pygame.event.get(): 
                if not self.handle_input(event):
                    running = False
            
            # 2. Обновление позиции
            self.update_position()
            
            # 3. Отрисовка
            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, RED, (self.square_x, self.square_y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.display.flip()
            
            # Ограничиваем частоту кадров для стабильности
            clock.tick(60) 
        
        pygame.quit()