"""
Interactive Pygame Visualizer for FABRIK IK
Real-time visualization with mouse control
"""
import pygame
import sys
from solver import FabrikSolver2D


class FabrikVisualizer:
    """
    Interactive visualizer for FABRIK inverse kinematics.
    Click anywhere to move the arm to that position.
    """
    
    def __init__(self, width=1000, height=700):
        """
        Initialize the visualizer.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
        """
        pygame.init()
        
        # Window setup
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("FABRIK Interactive Visualizer - Click to Move Arm")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (50, 150, 255)
        self.RED = (255, 80, 80)
        self.GREEN = (80, 255, 80)
        self.GRAY = (150, 150, 150)
        self.YELLOW = (255, 255, 100)
        
        # Create arm at center of screen
        center_x = width // 2
        center_y = height // 2
        self.solver = FabrikSolver2D(center_x, center_y, marginOfError=0.01)
        
        # Add segments (3 segments - like shoulder-elbow-wrist)
        self.solver.addSegment(150, 0)   # Upper arm
        self.solver.addSegment(120, 0)   # Forearm
        self.solver.addSegment(100, 0)   # Hand
        
        # Target
        self.target = None
        self.target_reachable = True
        
        # Animation
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Font
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 36)
        
    def handle_events(self):
        """
        Handle user input events.
        
        Returns:
            Boolean indicating if program should continue running
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Set new target on mouse click
                self.target = pygame.mouse.get_pos()
                self.target_reachable = self.solver.compute(self.target[0], self.target[1])
        
        return True
    
    def draw_grid(self):
        """Draw a subtle grid in the background."""
        for x in range(0, self.width, 50):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, self.height), 1)
        for y in range(0, self.height, 50):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (self.width, y), 1)
    
    def draw_arm(self):
        """Draw the robotic arm."""
        positions = self.solver.get_joint_positions()
        
        # Draw segments as lines
        for i in range(len(positions) - 1):
            start_pos = (int(positions[i][0]), int(positions[i][1]))
            end_pos = (int(positions[i+1][0]), int(positions[i+1][1]))
            pygame.draw.line(self.screen, self.BLUE, start_pos, end_pos, 8)
        
        # Draw joints
        for i, pos in enumerate(positions):
            if i == 0:
                # Base point (larger, different color)
                pygame.draw.circle(self.screen, self.YELLOW, 
                                 (int(pos[0]), int(pos[1])), 12)
                pygame.draw.circle(self.screen, self.BLACK, 
                                 (int(pos[0]), int(pos[1])), 12, 2)
            elif i == len(positions) - 1:
                # End effector (green)
                pygame.draw.circle(self.screen, self.GREEN, 
                                 (int(pos[0]), int(pos[1])), 10)
                pygame.draw.circle(self.screen, self.BLACK, 
                                 (int(pos[0]), int(pos[1])), 10, 2)
            else:
                # Regular joints
                pygame.draw.circle(self.screen, self.RED, 
                                 (int(pos[0]), int(pos[1])), 8)
                pygame.draw.circle(self.screen, self.BLACK, 
                                 (int(pos[0]), int(pos[1])), 8, 2)
    
    def draw_target(self):
        """Draw the target point."""
        if self.target:
            color = self.GREEN if self.target_reachable else self.RED
            # Draw crosshair
            size = 15
            pygame.draw.line(self.screen, color, 
                           (self.target[0] - size, self.target[1]), 
                           (self.target[0] + size, self.target[1]), 3)
            pygame.draw.line(self.screen, color, 
                           (self.target[0], self.target[1] - size), 
                           (self.target[0], self.target[1] + size), 3)
            # Draw circle
            pygame.draw.circle(self.screen, color, self.target, 20, 3)
    
    def draw_info(self):
        """Draw information text on screen."""
        # Title
        title = self.title_font.render("FABRIK Interactive Visualizer", True, self.WHITE)
        self.screen.blit(title, (20, 20))
        
        # Instructions
        instruction = self.font.render("Click anywhere to move the arm", True, self.GRAY)
        self.screen.blit(instruction, (20, 60))
        
        # Target info
        if self.target:
            target_text = f"Target: ({self.target[0]}, {self.target[1]})"
            status_text = "Status: ✓ Reachable" if self.target_reachable else "Status: ✗ Out of Reach"
            
            target_surface = self.font.render(target_text, True, self.WHITE)
            status_color = self.GREEN if self.target_reachable else self.RED
            status_surface = self.font.render(status_text, True, status_color)
            
            self.screen.blit(target_surface, (20, self.height - 80))
            self.screen.blit(status_surface, (20, self.height - 50))
        
        # Arm info
        positions = self.solver.get_joint_positions()
        end_effector = positions[-1]
        ee_text = f"End Effector: ({int(end_effector[0])}, {int(end_effector[1])})"
        ee_surface = self.font.render(ee_text, True, self.WHITE)
        self.screen.blit(ee_surface, (self.width - 300, self.height - 50))
        
        # FPS
        fps_text = f"FPS: {int(self.clock.get_fps())}"
        fps_surface = self.font.render(fps_text, True, self.GRAY)
        self.screen.blit(fps_surface, (self.width - 100, 20))
        
        # Legend
        legend_y = 100
        pygame.draw.circle(self.screen, self.YELLOW, (self.width - 180, legend_y), 8)
        legend_text = self.font.render("Base (Fixed)", True, self.WHITE)
        self.screen.blit(legend_text, (self.width - 160, legend_y - 12))
        
        pygame.draw.circle(self.screen, self.RED, (self.width - 180, legend_y + 35), 6)
        legend_text = self.font.render("Joints", True, self.WHITE)
        self.screen.blit(legend_text, (self.width - 160, legend_y + 23))
        
        pygame.draw.circle(self.screen, self.GREEN, (self.width - 180, legend_y + 70), 8)
        legend_text = self.font.render("End Effector", True, self.WHITE)
        self.screen.blit(legend_text, (self.width - 160, legend_y + 58))
    
    def run(self):
        """Main application loop."""
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Clear screen
            self.screen.fill(self.BLACK)
            
            # Draw everything
            self.draw_grid()
            self.draw_target()
            self.draw_arm()
            self.draw_info()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    visualizer = FabrikVisualizer()
    visualizer.run()
