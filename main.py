import pygame
from sprites import *
from config import *
from dialog import DialogBox
import sys
from database import GameDatabase


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Twilight Fields")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Writing_Police\\arial.ttf", 32)
        self.caramel_font = pygame.font.Font("Writing_Police\\SuperCaramel.ttf", 75)
        self.db = GameDatabase()
        self.running = True
        self.won = False

        # Camera zoom properties
        self.camera_scale = 1.0
        self.target_scale = 1.0
        self.zoom_speed = 0.05
        self.zoom_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        
        # Load essential spritesheets
        self.character_spritesheet = Spritesheet("img/character.png")  # Player character
        self.terrain_spritesheet = Spritesheet("img/terrain.png")      # World tiles
        self.enemy_spritesheet = Spritesheet("img/enemy.png")         # Enemy sprites
        self.attack_spritesheet = Spritesheet("img/attack.png")       # Attack animations
        
        # Load NPC spritesheets
        self.male_npc_spritesheet = Spritesheet("img/PIPOYA/Male/Male 01-1.png")
        self.female_npc_spritesheet = Spritesheet("img/PIPOYA/Female/Female 01-1.png")
        
        # Load backgrounds
        self.intro_background = pygame.image.load("./img/introbackground.png")
        self.go_background = pygame.image.load("./img/gameover.png")

        self.sword_sound = pygame.mixer.Sound("sounds\\sword.mp3")
        self.enemies_counter = 5
        
        # Initialize dialog system
        self.dialog_box = DialogBox(self)

    def play_music(self, mp3File):
        pygame.mixer.stop()
        self.medieval_sound.play(-1)

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Terrain_Creator_Collide(self, j, i, 960, 576)               
                elif column == "G":
                    Grass(self, j, i)
                elif column == "H":
                    Terrain_Creator_Collide(self, j, i, 960, 448)         
                elif column == "E":
                    Enemy(self, j, i)
                elif column == "N":
                    # Create a male NPC by default
                    NPC(self, j, i, NPCType.MALE)
                elif column == "M":
                    # Female NPC
                    NPC(self, j, i, NPCType.FEMALE)
                elif column == "F":
                    Terrain_Creator_Pass(self, j, i, 128, 352)
                elif column == "W":
                    Water(self, j, i)
                elif column == "C":
                    Water(self, j, i)
                    Terrain_Creator_Pass(self, j, i, 20, 680)
                elif column == "X":
                    Terrain_Creator_Pass(self, j, i, 900, 164)
                elif column == "P":
                    self.player = Player(self, j, i)
                
    
    def new(self):
        
        # A new game starts
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.blocks = pygame.sprite.LayeredUpdates()
        self.understroyable = pygame.sprite.LayeredUpdates()
        self.grass = pygame.sprite.LayeredUpdates()

        self.players = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.villagers = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

        self.medieval_sound = pygame.mixer.Sound("sounds\\Medieval.mp3")
        self.play_music(self.medieval_sound)
    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            # Handle dialog input
            self.dialog_box.handle_input(event)

            # Only handle game input if not in dialog
            if not self.dialog_box.active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if mouse_buttons[0]:
                        self.sword_sound.play(0)
                        if self.player.facing == "up":
                            Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                        elif self.player.facing == "down":
                            Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                        elif self.player.facing == "left":
                            Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                        elif self.player.facing == "right":
                            Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
    def update(self):
        self.all_sprites.update()

    def start_camera_zoom(self):
        self.target_scale = 1.5  # Zoom in 1.5x
        
    def reset_camera_zoom(self):
        self.target_scale = 1.0  # Reset to normal zoom
        
    def update_camera_zoom(self):
        # Smoothly interpolate between current and target scale
        if self.camera_scale != self.target_scale:
            diff = self.target_scale - self.camera_scale
            if abs(diff) < self.zoom_speed:
                self.camera_scale = self.target_scale
            else:
                self.camera_scale += self.zoom_speed if diff > 0 else -self.zoom_speed

    def draw(self):
        SKY_BLUE = (135, 206, 235)  # Light sky blue color
        self.zoom_surface.fill(SKY_BLUE)
        
        # Draw all sprites to the zoom surface
        self.all_sprites.draw(self.zoom_surface)
        
        # Update camera zoom
        self.update_camera_zoom()
        
        # Apply zoom effect
        if self.camera_scale != 1.0:
            # Calculate zoom center (player position)
            center_x = self.player.rect.centerx
            center_y = self.player.rect.centery
            
            # Calculate scaled dimensions
            scaled_width = int(WIN_WIDTH * self.camera_scale)
            scaled_height = int(WIN_HEIGHT * self.camera_scale)
            
            # Scale the surface
            scaled_surface = pygame.transform.scale(self.zoom_surface, (scaled_width, scaled_height))
            
            # Calculate offset to keep player centered
            offset_x = int((scaled_width - WIN_WIDTH) / 2)
            offset_y = int((scaled_height - WIN_HEIGHT) / 2)
            
            # Draw the scaled portion centered on the player
            self.screen.blit(scaled_surface, (-offset_x, -offset_y))
        else:
            # No zoom, just draw normally
            self.screen.blit(self.zoom_surface, (0, 0))
        
        # Draw dialog box if active (always draw on top, unaffected by zoom)
        self.dialog_box.draw(self.screen)
        
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # Game loop
        while self.playing:
            self.events()
            self.update()
            self.check_win_condition()
            self.enemies_checker()
            self.draw()

    def check_win_condition(self):
        if len(self.enemies) == 0 and not self.won:
            self.won = True
            self.playing = False
            self.win_screen()

    def win_screen(self):
        # Increment win counter in database
        self.db.add_win()
        total_wins = self.db.get_wins()
        
        # Your existing win text
        text = self.caramel_font.render("You Won!", True, BLACK)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 - 80))
        
        # Add win counter with trophy icon
        win_counter_font = pygame.font.Font("Writing_Police\\SuperCaramel.ttf", 55)
        trophy_text = "🏆 " if total_wins > 0 else ""
        wins_text = win_counter_font.render(f"{trophy_text}Total Victories: {total_wins}", True, (139, 69, 19))
        wins_rect = wins_text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 - 20))
        # Add milestone message if applicable
        milestones = {
            1: "First Victory!",
            5: "5 Wins Achieved!",
            10: "Veteran Player!",
            25: "Champion Status!",
            50: "Legendary Hero!",
            100: "Master of All!"
        }
        milestone_text = milestones.get(total_wins)

        
        # Your existing buttons
        replay_button = Button(WIN_WIDTH/2 - 200, WIN_HEIGHT/2 + 80, 150, 50, WHITE, BLACK, "Replay", 32)
        leave_button = Button(WIN_WIDTH/2 + 50, WIN_HEIGHT/2 + 80, 150, 50, WHITE, BLACK, "Leave", 32)
        
        # Animation variables
        counter = 0
        win_display = 0
        
        while self.running:
            counter += 1  # Simple frame counter for animations
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if replay_button.is_pressed(mouse_pos, mouse_pressed):
                # Reset game state
                self.won = False
                pygame.mixer.stop()
                self.new()
                self.main()
                return

            if leave_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False
                return
            
            # Animate win counter
            if win_display < total_wins and counter % 5 == 0:  # Increment every 5 frames
                win_display += 1
            
            # Draw win screen
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(text, text_rect)
            
            # Draw animated win counter
            animated_wins_text = win_counter_font.render(f"{trophy_text}Total Victories: {win_display}", True, (139, 69, 19))
            self.screen.blit(animated_wins_text, wins_rect)
            
            # Draw milestone message if applicable
            if milestone_text:
                # Pulsing effect for milestone text
                pulse = abs(math.sin(counter/20)) * 10  # Pulsing size between 0-10
                milestone_font_size = 28 + int(pulse)
                milestone_font = pygame.font.Font(None, milestone_font_size)
                
                milestone_surface = milestone_font.render(milestone_text, True, (255, 215, 0))  # Gold color
                milestone_rect = milestone_surface.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 + 30))
                self.screen.blit(milestone_surface, milestone_rect)
            
            self.screen.blit(replay_button.image, replay_button.rect)
            self.screen.blit(leave_button.image, leave_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def enemies_checker(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            print(self.enemies_counter)

    def game_over(self):
        text = self.font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, "Restart", 32)

        for sprite in self.all_sprites:
            sprite.kill()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            keys = pygame.key.get_pressed()
            if restart_button.is_pressed(mouse_pos, mouse_pressed) or keys[pygame.K_RETURN]:
                pygame.mixer.stop()
                self.new()
                self.main()
                return
            
            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = self.caramel_font.render('Twilight Fields', True, BLACK)
        title_rect = title.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 - 100))

        play_button = Button(WIN_WIDTH/2-115, WIN_HEIGHT/2, 250, 50, WHITE, BLACK, 'Play', 32)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            keys = pygame.key.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed) or keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                intro = False
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    if not g.won:  # Only show game over screen if player hasn't won
        g.game_over()

pygame.quit()
sys.exit()