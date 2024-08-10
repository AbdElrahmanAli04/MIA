import pygame

# Initialization
pygame.init()

# Constants
Window_x, Window_y = 700, 700
BlockWidth = BlockLength = 87.5
white_color = (255, 255, 255)
grey_color = (128, 128, 128)
green_color = (0, 255, 0)

# Setup screen
screen = pygame.display.set_mode((Window_x, Window_y))
pygame.display.set_caption("Batman Chess")
Icon = pygame.image.load('MIA-Python/WhatsApp Image 2024-07-30 at 20.00.53_7fe8770c.jpg')
pygame.display.set_icon(Icon)

# URLs for images
JusticeURLS = [
    ["MIA-Python/wr.png", "MIA-Python/JK.png", "MIA-Python/JP.png", "MIA-Python/JKing.png", "MIA-Python/JQueen.png", "MIA-Python/JP.png", "MIA-Python/JK.png", "MIA-Python/wr.png"],
    ["MIA-Python/J pawn.png", "MIA-Python/J pawn.png", "MIA-Python/J pawn.png", "MIA-Python/J pawn.png", "MIA-Python/J pawn.png", "MIA-Python/J pawn.png", "MIA-Python/J pawn.png", "MIA-Python/J pawn.png"]
]

VillansURLs = [
    ["MIA-Python/V paawn.png", "MIA-Python/V paawn.png", "MIA-Python/V paawn.png", "MIA-Python/V paawn.png", "MIA-Python/V paawn.png", "MIA-Python/V paawn.png", "MIA-Python/V paawn.png", "MIA-Python/V paawn.png"],
    ["MIA-Python/VR.png", "MIA-Python/VK.png", "MIA-Python/VP.png", "MIA-Python/V King.png", "MIA-Python/V Queen.png", "MIA-Python/VP.png", "MIA-Python/VK.png", "MIA-Python/VR.png"]
]

# Piece class
class Piece:
    def __init__(self, image_url, x, y):
        self.image_url = image_url
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_url)
        self.image = pygame.transform.scale(self.image, (int(BlockLength), int(BlockWidth)))
        self.rect = pygame.Rect(x, y, BlockLength, BlockWidth)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

# Initialize pieces
pieces = []
for i in range(2):
    for j in range(8):
        pieces.append(Piece(JusticeURLS[i][j], j * BlockLength, i * BlockWidth))
for i in range(6, 8):
    for j in range(8):
        pieces.append(Piece(VillansURLs[i - 6][j], j * BlockLength, i * BlockWidth))

JusticeTeam = pieces[0:16]
VillianTeam = pieces[16:32]

# Variables for mouse dragging and piece selection
dragging = False
dragged_piece = None
selected_piece = None
offset_x, offset_y = 0, 0
show_circles = False

def MakingBoard():
    for i in range(8):
        for j in range(8):
            Block_X_Location = BlockLength * i
            Block_Y_Location = BlockWidth * j
            color = white_color if (i + j) % 2 == 0 else grey_color
            pygame.draw.rect(screen, color, pygame.Rect(Block_X_Location, Block_Y_Location, BlockLength, BlockWidth))

def JusticeTeamAvailableMoves(selected_piece):
    if selected_piece in JusticeTeam[8:16]:  # Check if the selected piece is a pawn from JusticeTeam
        pygame.draw.circle(
            surface=screen, 
            color=green_color, 
            center=(selected_piece.x + BlockLength / 2, selected_piece.y + BlockWidth / 2 + BlockWidth), 
            radius=15
        )
        pygame.draw.circle(
            surface=screen, 
            color=green_color, 
            center=(selected_piece.x + BlockLength / 2, selected_piece.y + BlockWidth / 2 + 2 * BlockWidth), 
            radius=15
        )

def handle_mouse_events():
    global dragging, dragged_piece, offset_x, offset_y, selected_piece, show_circles
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()

    if mouse_buttons[0]:  # Left mouse button is pressed
        if not dragging:
            for piece in pieces:
                if piece.rect.collidepoint(mouse_x, mouse_y):
                    dragged_piece = piece
                    selected_piece = piece
                    offset_x = mouse_x - piece.x
                    offset_y = mouse_y - piece.y
                    for k in range (16,32) :
                        if show_circles.x == pieces[k].x :
                            show_circles = False
                        else : 
                            show_circles = True  # Set flag to show circles
                    dragging = True
                    break
        else:
            if dragged_piece:
                dragged_piece.update_position(mouse_x - offset_x, mouse_y - offset_y)
                show_circles = False  # Hide circles when dragging
    else:
        dragging = False
        dragged_piece = None
        show_circles = False  # Hide circles when mouse button is released

# Main game loop
while True:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    MakingBoard()
    handle_mouse_events()
    for piece in pieces:
        piece.draw(screen)
    if show_circles and selected_piece:
        JusticeTeamAvailableMoves(selected_piece)
    pygame.display.update()
