import pygame
import random
import os

class CatchGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 900, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Apple Catcher")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        
        self.state = "MENU"
        self.highscore = self.load_highscore()
        
        self.player_rect = pygame.Rect(self.width // 2 - 25, self.height - 60, 50, 50)
        self.item_rect = pygame.Rect(0, -30, 30, 30)
        
        try:
            self.img_idle = pygame.transform.scale(pygame.image.load("assets/images/player_idle.png").convert_alpha(), (50, 50))
            self.img_left = pygame.transform.scale(pygame.image.load("assets/images/player_l.png").convert_alpha(), (50, 50))
            self.img_right = pygame.transform.scale(pygame.image.load("assets/images/player_r.png").convert_alpha(), (50, 50))
            self.item_img = pygame.transform.scale(pygame.image.load("assets/images/stone.png").convert_alpha(), (30, 30))
            self.player_img = self.img_idle
            self.use_assets = True
        except:
            self.use_assets = False

        self.reset_game()

        self.last_tap_time = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0}
        self.double_tap_delay = 250
        self.dash_distance = 120

    def load_highscore(self):
        if os.path.exists("highscore.txt"):
            try:
                with open("highscore.txt", "r") as f:
                    content = f.read().strip()
                    return int(content) if content else 0
            except: return 0
        return 0

    def save_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))

    def reset_game(self):
        self.player_rect.x = self.width // 2 - 25
        self.score = 0
        self.item_speed = 5
        self.spawn_item()

    def spawn_item(self):
        self.item_rect.x = random.randint(0, self.width - 30)
        self.item_rect.y = -30

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: self.state = "PLAYING"
                    if event.key == pygame.K_2: self.running = False
            
            elif self.state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    now = pygame.time.get_ticks()
                    if event.key in self.last_tap_time:
                        if now - self.last_tap_time[event.key] < self.double_tap_delay:
                            if event.key == pygame.K_LEFT: self.player_rect.x -= self.dash_distance
                            if event.key == pygame.K_RIGHT: self.player_rect.x += self.dash_distance
                        self.last_tap_time[event.key] = now
            
            elif self.state == "GAMEOVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: 
                        self.reset_game()
                        self.state = "PLAYING"
                    if event.key == pygame.K_2: self.state = "MENU"

    def update(self):
        if self.state == "PLAYING":
            keys = pygame.key.get_pressed()
            
            if self.use_assets:
                self.player_img = self.img_idle
                if keys[pygame.K_LEFT]:
                    self.player_rect.x -= 7
                    self.player_img = self.img_left
                if keys[pygame.K_RIGHT]:
                    self.player_rect.x += 7
                    self.player_img = self.img_right
            else:
                if keys[pygame.K_LEFT]: self.player_rect.x -= 7
                if keys[pygame.K_RIGHT]: self.player_rect.x += 7

            self.player_rect.clamp_ip(self.screen.get_rect())
            self.item_rect.y += self.item_speed
            
            if self.item_rect.colliderect(self.player_rect):
                self.score += 1
                self.item_speed += 0.2
                self.spawn_item()
            elif self.item_rect.y > self.height:
                self.save_highscore()
                self.state = "GAMEOVER"

    def draw_text(self, text, y_offset, color=(0, 0, 0)):
        img = self.font.render(text, True, color)
        rect = img.get_rect(center=(self.width // 2, self.height // 2 + y_offset))
        self.screen.blit(img, rect)

    def draw(self):
        self.screen.fill((240, 240, 240))
        
        if self.state == "MENU":
            self.draw_text("APPLE CATCHER", -60, (0, 100, 255))
            self.draw_text(f"Рекорд: {self.highscore}", -10)
            self.draw_text("1. Играть", 50)
            self.draw_text("2. Выйти", 90)
            
        elif self.state == "PLAYING":
            if self.use_assets:
                self.screen.blit(self.player_img, self.player_rect)
                self.screen.blit(self.item_img, self.item_rect)
            else:
                pygame.draw.rect(self.screen, (0, 0, 255), self.player_rect)
                pygame.draw.rect(self.screen, (255, 0, 0), self.item_rect)
            
            score_txt = self.font.render(f"Счет: {self.score}", True, (0,0,0))
            self.screen.blit(score_txt, (10, 10))
            
        elif self.state == "GAMEOVER":
            self.draw_text("ИГРА ОКОНЧЕНА", -60, (255, 0, 0))
            self.draw_text(f"Ваш счет: {self.score}", -10)
            self.draw_text("1. Сначала", 50)
            self.draw_text("2. В меню", 90)
            
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    CatchGame().run()
