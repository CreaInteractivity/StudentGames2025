import pygame
import asyncio

# Simple Actor class - minimal changes from working version
class Actor:
    def __init__(self, color_or_image, size=(32, 32)):
        self.color = None
        self.image = None
        self.size = size
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self._pos = (0, 0)

        # If it's a string, try to load as image, otherwise use as color
        if isinstance(color_or_image, str):
            try:
                self.image = pygame.image.load(color_or_image).convert_alpha()
                print(f"Loaded: {color_or_image}")
            except:
                print(f"Failed to load: {color_or_image}, using magenta square")
                self.color = (255, 0, 255)  # Magenta if image fails
        else:
            self.color = color_or_image

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self.rect.center = value

    @property
    def x(self):
        return self.rect.centerx

    @x.setter
    def x(self, value):
        self.rect.centerx = value
        self._pos = (value, self._pos[1])

    @property
    def y(self):
        return self.rect.centery

    @y.setter
    def y(self, value):
        self.rect.centery = value
        self._pos = (self._pos[0], value)

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

    def colliderect(self, other):
        return self.rect.colliderect(other.rect)

# Global variables
screen = None
clock = None
igloo_wall = None
igloo_door = None
iglu_ahhh = None
alien2 = None
trees = []
tree = None

def tree_row(x_start, x_end, x_delta, y):
    for x in range(x_start, x_end, x_delta):
        new_tree = Actor("images/tree2_small.png", (40, 40))  # Fixed: "images" folder and "tree2_small.png"
        new_tree.pos = (x, y)
        trees.append(new_tree)

def tree_column(y_start, y_end, y_delta, x):
    for y in range(y_start, y_end, y_delta):
        new_tree = Actor("images/tree_small.png", (40, 40))  # Fixed: "images" folder
        new_tree.pos = (x, y)
        trees.append(new_tree)

def setup_trees():
    """Create all the trees for the maze"""
    global trees
    trees = []  # Clear existing trees

    #top
    tree_row(100, 700, 50, 100)
    #bottom enterence
    tree_column(350, 600, 50, 100)
    #top enterence
    tree_column(100, 250, 50, 100)
    #bottom line
    tree_row(140, 400, 50, 350)
    #top line
    tree_row(150, 550, 50, 200)
    #top side
    tree_column(250, 500, 50, 500)
    #bottom side
    tree_column(400, 570, 50, 390)
    #bottom
    tree_row(100, 720, 50, 570)
    #top bottom
    tree_row(550, 670, 50, 450)
    #side
    tree_column(100, 480, 50, 700)
    #fill in top
    tree_row(140, 700, 50, 140)
    #fill in right side 1
    tree_column(200, 420, 50, 540)
    #fill in right side 2
    tree_column(200, 420, 50, 580)
    #fill in right side 3
    tree_column(200, 420, 50, 620)
    #fill in right side 4
    tree_column(200, 420, 50, 660)
    #fill in left side 1
    tree_column(350, 600, 50, 140)
    #fill in left side 2
    tree_column(350, 600, 50, 180)
    #fill in left side 3
    tree_column(350, 600, 50, 220)
    #fill in left side 4
    tree_column(350, 600, 50, 260)
    #fill in left side 5
    tree_column(350, 600, 50, 300)
    #fill in left side 6
    tree_column(350, 600, 50, 340)

def draw():
    screen.fill((173, 216, 230))  # light blue

    # Draw single tree
    tree.draw(screen)

    # Draw all maze trees
    for tree_actor in trees:
        tree_actor.draw(screen)

    # Draw text using pygame's built-in font
    font = pygame.font.Font(None, 36)
    text = font.render("maze navigators by joe, bella, and amelia, 2025", True, (128, 0, 128))
    screen.blit(text, (50, 50))

    # Draw igloos as colored rectangles
    for position in [(100+150, 275), (200+150, 275), (300+100, 275)]:
        igloo_wall.pos = position
        igloo_wall.draw(screen)

    igloo_door.pos = 300, 270
    igloo_door.draw(screen)

    # Draw players
    iglu_ahhh.draw(screen)
    alien2.draw(screen)

def update():
    # Get current key states
    keys = pygame.key.get_pressed()

    # Store the players' current positions before attempting to move
    old_player_x = iglu_ahhh.x
    old_player_y = iglu_ahhh.y
    new_player_x = alien2.x
    new_player_y = alien2.y

    # Move the players based on keys
    if keys[pygame.K_LEFT]:
        iglu_ahhh.x -= 3
    if keys[pygame.K_RIGHT]:
        iglu_ahhh.x += 3
    if keys[pygame.K_UP]:
        iglu_ahhh.y -= 3
    if keys[pygame.K_DOWN]:
        iglu_ahhh.y += 3

    if keys[pygame.K_d]:
        alien2.x += 3
    if keys[pygame.K_a]:
        alien2.x -= 3
    if keys[pygame.K_w]:
        alien2.y -= 3
    if keys[pygame.K_s]:
        alien2.y += 3

    # Check for collision between players
    if iglu_ahhh.colliderect(alien2):
        print("Collision!")
        # If a collision occurred, revert both players to their positions before the move
        iglu_ahhh.x = old_player_x
        iglu_ahhh.y = old_player_y
        alien2.x = new_player_x
        alien2.y = new_player_y

    # Check for collision with trees
    for tree_actor in trees:
        if iglu_ahhh.colliderect(tree_actor):
            iglu_ahhh.x = old_player_x
            iglu_ahhh.y = old_player_y
            break

    for tree_actor in trees:
        if alien2.colliderect(tree_actor):
            alien2.x = new_player_x
            alien2.y = new_player_y
            break

async def main():
    global screen, clock, igloo_wall, igloo_door, iglu_ahhh, alien2, tree

    # Initialize pygame
    pygame.init()

    # Constants
    WIDTH = 800
    HEIGHT = 600

    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Navigators")
    clock = pygame.time.Clock()

    print("Pygame initialized")

    # Create actors - look in "images" folder for PNG files
    print("Trying to load images...")
    igloo_wall = Actor("images/iglooalt.png", (50, 50))
    igloo_door = Actor("images/igloodoor.png", (30, 40))
    iglu_ahhh = Actor("images/alien_small.png", (20, 20))
    alien2 = Actor("images/p1-duck_small.png", (20, 20))
    tree = Actor("images/tree_small.png", (40, 40))
    print("Image loading attempts complete")

    # Set initial positions (avoiding tree collisions)
    iglu_ahhh.pos = (755, 333)  # Original position from your script - should be clear
    alien2.pos = (20, 40)     # Safe position on the right side, away from maze
    tree.pos = (100, 100)

    print("Actors created")

    # Setup the maze
    setup_trees()

    print(f"Maze setup complete, {len(trees)} trees created")
    print("Starting game loop...")

    running = True
    frame_count = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        update()

        # Draw everything
        draw()

        # Update display
        pygame.display.flip()
        clock.tick(60)

        frame_count += 1
        if frame_count % 300 == 0:  # Print every 5 seconds
            print(f"Game running, frame {frame_count}")

        # Essential for pygbag
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
