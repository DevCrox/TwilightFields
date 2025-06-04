import pygame
from config import *

# Module-level font cache
_FONT_CACHE = {}

def _get_cached_font(path, size):
    key = (path, size)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = pygame.font.Font(path, size)
    return _FONT_CACHE[key]

class DialogBox:
    def __init__(self, game):
        self.game = game
        # Dialog box dimensions and position
        self.width = WIN_WIDTH - 100  # Slightly smaller than window width
        self.height = 150
        self.x = 50  # Centered horizontally
        self.y = WIN_HEIGHT - self.height - 20  # Near bottom of screen
        
        # Create the dialog box surface with brown background
        self.surface = pygame.Surface((self.width, self.height))
        self.brown_color = (139, 69, 19)  # Dark brown
        self.border_color = (101, 67, 33)  # Darker brown for border
        self.inner_border_color = (205, 133, 63)  # Peru brown for inner border
        
        # Text properties - separate fonts for NPC text and choices (using cached fonts)
        self.npc_font = _get_cached_font("Writing_Police\\arial.ttf", 20)  # NPC text
        self.choice_font = _get_cached_font("Writing_Police\\arial.ttf", 16)  # Player choices
        self.name_font = _get_cached_font("Writing_Police\\SuperCaramel.ttf", 24)  # Name font
        self.text_color = WHITE
        self.choice_color = (255, 255, 200)  # Light yellow for choices
        self.name_color = (255, 223, 186)  # Light peach for name
        
        # Dialog state
        self.active = False
        self.current_text = ""
        self.current_npc_name = ""
        self.choices = []
        self.selected_choice = 0
        self.callback = None

        # Text wrapping properties
        self.max_line_width = 350  # Maximum width for text lines
        self.line_spacing = 25  # Space between lines
        
        # Performance optimization caches
        self._text_cache = {}
        self._wrapped_text_cache = {}
        self._needs_redraw = True
        self._last_selected_choice = -1
        
    def _render_text_cached(self, text, font, color):
        """Cache rendered text surfaces to avoid re-rendering same text"""
        cache_key = (text, id(font), color)
        if cache_key not in self._text_cache:
            self._text_cache[cache_key] = font.render(text, True, color)
        return self._text_cache[cache_key]
        
    def wrap_text(self, text, font, max_width):
        # Cache wrapped text results to avoid recalculating
        cache_key = (text, id(font), max_width)
        if cache_key in self._wrapped_text_cache:
            return self._wrapped_text_cache[cache_key]
            
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word + " ", True, self.text_color)
            word_width = word_surface.get_width()

            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(" ".join(current_line))
            
        # Cache the result for future use
        self._wrapped_text_cache[cache_key] = lines
        return lines
        
    def start_dialog(self, text, npc_name="", choices=None, callback=None):
        self.active = True
        self.current_text = text
        self.current_npc_name = npc_name
        # Always add "Goodbye" as the last choice if not already present
        if choices is None:
            choices = []
        if "Goodbye" not in choices:
            choices.append("Goodbye")
        self.choices = choices
        self.selected_choice = 0
        self.callback = callback
        self._needs_redraw = True  # Force redraw on new dialog
        
    def end_dialog(self):
        self.active = False
        self.current_text = ""
        self.current_npc_name = ""
        self.choices = []
        self.callback = None
        
    def handle_input(self, event):
        if not self.active or not self.choices:
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_choice = (self.selected_choice - 1) % len(self.choices)
                self._needs_redraw = True  # Mark for redraw when selection changes
            elif event.key == pygame.K_DOWN:
                self.selected_choice = (self.selected_choice + 1) % len(self.choices)
                self._needs_redraw = True  # Mark for redraw when selection changes
            elif event.key == pygame.K_RETURN:
                if self.callback:
                    self.callback(self.selected_choice)
                
    def draw(self, screen):
        if not self.active:
            return
        
        # Performance optimization: Only redraw if something actually changed
        if not self._needs_redraw and self._last_selected_choice == self.selected_choice:
            screen.blit(self.surface, (self.x, self.y))
            return
            
        # Draw brown background
        pygame.draw.rect(self.surface, self.brown_color, (0, 0, self.width, self.height))
        
        # Draw stylish border - outer thick border
        border_width = 6
        pygame.draw.rect(self.surface, self.border_color, (0, 0, self.width, self.height), border_width)
        
        # Draw inner border with lighter color
        inner_border = 2
        pygame.draw.rect(self.surface, self.inner_border_color, 
                        (border_width, border_width, 
                         self.width - 2*border_width, 
                         self.height - 2*border_width), inner_border)
        
        # Add corner decorations
        corner_size = 12
        for x, y in [(0, 0), (self.width - corner_size, 0), 
                     (0, self.height - corner_size), 
                     (self.width - corner_size, self.height - corner_size)]:
            pygame.draw.rect(self.surface, self.inner_border_color, 
                           (x, y, corner_size, corner_size), 2)
        
        # Draw name plate at the top
        if self.current_npc_name:
            # Create a polygon for the name plate (trapezoid shape)
            name_height = 35
            name_surface = self._render_text_cached(self.current_npc_name, self.name_font, self.name_color)
            name_width = name_surface.get_width() + 40  # Add padding
            
            # Define the trapezoid points for a stylized name plate
            points = [
                (0, 0),  # Top left
                (10 + name_width - 10, 0),  # Top right
                (10 + name_width, name_height),  # Bottom right
                (10, name_height)  # Bottom left with indent
            ]
            
            # Draw the dark name plate background
            pygame.draw.polygon(self.surface, (40, 40, 40), points)  # Very dark gray
            
            # Add highlight effect
            highlight_points = [
                (points[0][0], points[0][1]),
                (points[1][0], points[1][1]),
                (points[1][0] + 10, points[1][1] + 2)
            ]
            pygame.draw.polygon(self.surface, (60, 60, 60), highlight_points)  # Slightly lighter gray
            
            # Draw name text
            name_x = 20  # Padding from left
            name_y = (name_height - name_surface.get_height()) // 2  # Center vertically
            self.surface.blit(name_surface, (name_x, name_y))
        
        # Calculate the width for NPC text and choices
        npc_text_width = self.width * 0.6  # 60% of the width for NPC text
        choice_text_width = self.width * 0.35  # 35% of the width for choices
        
        # Draw wrapped main text using cached rendering
        lines = self.wrap_text(self.current_text, self.npc_font, npc_text_width)
        for i, line in enumerate(lines):
            text_surface = self._render_text_cached(line, self.npc_font, self.text_color)
            self.surface.blit(text_surface, (20 + border_width, 45 + i * self.line_spacing))
        
        # Draw choices on the right side if any
        if self.choices:
            choice_x = self.width - choice_text_width - 20
            current_y = 45  # Start below name plate
            
            for i, choice in enumerate(self.choices):
                # Wrap each choice text
                choice_lines = self.wrap_text(choice, self.choice_font, choice_text_width)
                
                # Draw selection arrow for the current choice
                if i == self.selected_choice:
                    arrow = "→"
                    arrow_surface = self._render_text_cached(arrow, self.choice_font, self.choice_color)
                    self.surface.blit(arrow_surface, (choice_x - 20, current_y))
                
                # Draw each line of the wrapped choice text using cached rendering
                color = self.choice_color if i == self.selected_choice else self.text_color
                for line in choice_lines:
                    choice_surface = self._render_text_cached(line, self.choice_font, color)
                    self.surface.blit(choice_surface, (choice_x, current_y))
                    current_y += 20  # Smaller spacing for choice lines
                
                current_y += 5  # Add some space between different choices
        
        # Draw the dialog box on screen
        screen.blit(self.surface, (self.x, self.y))
        
        # Mark as drawn and update tracking variables
        self._needs_redraw = False
        self._last_selected_choice = self.selected_choice
