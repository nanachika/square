import pygame
import random
from config2 import (WINDOW_WIDTH, WINDOW_HEIGHT, SQUARE_SIZE, 
                   BLACK, RED, GREEN, WHITE, YELLOW, BLUE,
                   SQUARE_SPEED, START_SCORE, SCORE_INCREMENT)

class SquareGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Квадратная охота")
        
        # Создаем шрифт для отображения счета
        self.font = pygame.font.SysFont(None, 36)
        
        # Создаем игрока (зеленый квадрат) в центре экрана
        self.player_x = WINDOW_WIDTH // 2 - SQUARE_SIZE // 2
        self.player_y = WINDOW_HEIGHT // 2 - SQUARE_SIZE // 2
        
        # Создаем цель (красный квадрат) в случайном месте
        self.target_x = random.randint(0, WINDOW_WIDTH - SQUARE_SIZE)
        self.target_y = random.randint(0, WINDOW_HEIGHT - SQUARE_SIZE)
        
        # Счет игры
        self.score = START_SCORE
        
        # Переменные для движения игрока
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        
        # Переменная для анимации "съедения"
        self.eating_animation = 0

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
        """Обновляет координаты игрока и ограничивает их границами экрана."""
        
        # Горизонтальное движение
        if self.move_left:
            self.player_x -= SQUARE_SPEED
        if self.move_right:
            self.player_x += SQUARE_SPEED
            
        # Вертикальное движение
        if self.move_up:
            self.player_y -= SQUARE_SPEED
        if self.move_down:
            self.player_y += SQUARE_SPEED
            
        # Ограничение движения игрока
        self.player_x = max(0, min(self.player_x, WINDOW_WIDTH - SQUARE_SIZE))
        self.player_y = max(0, min(self.player_y, WINDOW_HEIGHT - SQUARE_SIZE))
        
        # Проверка столкновения игрока с целью
        player_rect = pygame.Rect(self.player_x, self.player_y, SQUARE_SIZE, SQUARE_SIZE)
        target_rect = pygame.Rect(self.target_x, self.target_y, SQUARE_SIZE, SQUARE_SIZE)
        
        if player_rect.colliderect(target_rect):
            # Увеличиваем счет
            self.score += SCORE_INCREMENT
            
            # Создаем новую цель в случайном месте
            self.target_x = random.randint(0, WINDOW_WIDTH - SQUARE_SIZE)
            self.target_y = random.randint(0, WINDOW_HEIGHT - SQUARE_SIZE)
            
            # Запускаем анимацию "съедения"
            self.eating_animation = 10
        
        # Обновляем анимацию
        if self.eating_animation > 0:
            self.eating_animation -= 1
    
    def run(self):
        running = True
        clock = pygame.time.Clock() # Добавляем часы для контроля FPS
        
        while running:
            # 1. Обработка событий
            for event in pygame.event.get(): 
                if not self.handle_input(event):
                    running = False
            
            # 2. Обновление позиции и проверка столкновений
            self.update_position()
            
            # 3. Отрисовка
            self.screen.fill(BLACK)
            
            # Рисуем инструкции
            instructions = [f"Счет: {self.score}"]
            
            for i, line in enumerate(instructions):
                text = self.font.render(line, True, YELLOW)
                self.screen.blit(text, (10, 10 + i * 30))
            
            # Рисуем анимацию "съедения", если она активна
            if self.eating_animation > 0:
                glow_size = SQUARE_SIZE + self.eating_animation * 2
                glow_x = self.target_x - (glow_size - SQUARE_SIZE) // 2
                glow_y = self.target_y - (glow_size - SQUARE_SIZE) // 2
                pygame.draw.rect(self.screen, BLUE, 
                               (glow_x, glow_y, glow_size, glow_size), 
                               border_radius=10)
            
            # Рисуем цель (красный квадрат) с закругленными углами
            pygame.draw.rect(self.screen, RED, 
                           (self.target_x, self.target_y, SQUARE_SIZE, SQUARE_SIZE),
                           border_radius=10)
            
            # Рисуем игрока (зеленый квадрат) с закругленными углами
            pygame.draw.rect(self.screen, GREEN, 
                           (self.player_x, self.player_y, SQUARE_SIZE, SQUARE_SIZE),
                           border_radius=10)
            
            # Рисуем обводку вокруг игрока
            pygame.draw.rect(self.screen, WHITE, 
                           (self.player_x, self.player_y, SQUARE_SIZE, SQUARE_SIZE),
                           3, border_radius=10)
            
            pygame.display.flip()
            
            # Ограничиваем частоту кадров для стабильности
            clock.tick(60) 
        
        pygame.quit()