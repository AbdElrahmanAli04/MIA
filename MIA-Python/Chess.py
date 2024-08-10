import pygame

#Notes 
#1-The valid moves for now are for castle in y dirictions and pawns only
#2-also its valid to capture using only the white pawns 
#3-To capture a piece use the Right click , and moving is indeed with left click
#4-Sorry for the non completed game , But it was the best I could :(


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
    def move(self, x_offset, y_offset):
        self.rect = self.rect.move(x_offset, y_offset)
        self.x, self.y = self.rect.topleft  # Update the position attributes
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
CaptringList = pieces.copy()
# Variables for mouse dragging and piece selection
dragging = False
dragged_piece = None
selected_piece = None
offset_x, offset_y = 0, 0

def MakingBoard():
    for i in range(8):
        for j in range(8):
            Block_X_Location = BlockLength * i
            Block_Y_Location = BlockWidth * j
            color = white_color if (i + j) % 2 == 0 else grey_color
            pygame.draw.rect(screen, color, pygame.Rect(Block_X_Location, Block_Y_Location, BlockLength, BlockWidth))

#Defining moves fn for all pices White And Black

def is_position_occupied_WP(x, y):
    for piece in VillianTeam:
        if piece.rect.collidepoint((x, y)):
            return piece
    return None


def WPawns(piece):
    if piece in pieces[8:16]:  
        Wtarget_y = piece.y + 87.5
        if is_position_occupied_WP(piece.x, Wtarget_y) is None:
            Piece.move(piece, 0, 87.5) 

def WpawnsCapturing(piece):
    if piece in pieces[8:16]:  
        Wtarget_y = piece.y + 87.5*2
        Xtarget = piece.x + 87.5
        captured_piece = is_position_occupied_WP(Xtarget, Wtarget_y)
        if captured_piece is not None and captured_piece in CaptringList[16:31]:
            piece.move(87.5, 87.5)
            pieces.remove(captured_piece)

def is_position_occupied_BP(x, y):
    for piece in JusticeTeam:
        if piece.rect.collidepoint((x, y)):
            return piece
    return None

def BPawns(piece):
    if piece in pieces[16:24]:  
        Btarget_y = piece.y -87.5
        if is_position_occupied_BP(piece.x, Btarget_y) is None:
            Piece.move(piece, 0, -87.5)  

def is_position_occupied_WR(x, y):
    for piece in pieces:
        if piece.rect.collidepoint((x, y+87.5)) or  piece.rect.collidepoint((x, y-87.5)) :
            return piece
    return None


def WRock(piece):
    if piece == pieces[0] or pieces == pieces[7]: 
        if is_position_occupied_WR(piece.x, piece.y) is None:
            Piece.move(piece, 0, 87.5) 

def is_position_occupied_BR(x, y):
    for piece in pieces:
        if piece.rect.collidepoint((x, y+87.5)) or  piece.rect.collidepoint((x, y-87)) :
            return piece
    return None


def BRock(piece):
    if piece == pieces[24] or piece == pieces[31]: 
        if is_position_occupied_BR(piece.x, piece.y) is None:
            Piece.move(piece, 0, -87.5) 

def PicesMovings (piece) :
    WPawns (piece)
    BPawns(piece)
    WRock(piece)            
    BRock(piece)

def PicesCapturing(piece) :
    WpawnsCapturing(piece)


def handle_mouse_events():
    global dragging, dragged_piece, offset_x, offset_y, selected_piece
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
                    PicesMovings(selected_piece)
                    dragging = True
                    break
    elif mouse_buttons [2] :
        if not dragging:
            for piece in pieces:
                if piece.rect.collidepoint(mouse_x, mouse_y):
                    dragged_piece = piece
                    selected_piece = piece
                    offset_x = mouse_x - piece.x
                    offset_y = mouse_y - piece.y
                    WpawnsCapturing(selected_piece)
                    dragging = True
                    break 
        #else:
            #if dragged_piece:
                #dragged_piece.update_position(mouse_x - offset_x, mouse_y - offset_y)
    else:
        dragging = False
        dragged_piece = None


#pieces.remove(pieces[0])

#pawn = Piece.move(pieces[0],87.5*5,87.5*5) 

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
    pygame.display.update()


#I want when i choose a piece the avilable moves is shown to me , but if there is a piece located in a position of the avilable moves the circle of this avilable move should be erased


#then I want to click on the piece so the avilable moves are shown to me until I choose another piece , or i move it in one of the avilable postions 
#when I move a piece the justice pices will not be avilable to select until I move a piece from the other team 
#when a pwan have a picec thats postion is the pawn postion.x +87.5 and postion.y +87 or postion.x-87.5 and postion.y+87.5 , it can capture it 
#when a piece is captured , there will be a colored block in a layer on it so it will be removed , and it should be removed from the pieces list , and the clored block should be the same color as the pice= was on
#when the queen have no avilabel moves the game will end and there should be a CheckMate message , I will try to insert a play again button also 


"""Notes : 
white rocks are pieces[0] and pieces[7]
white Knights are pieces[1] and pieces[6]
white Bishop are pieces[2] and pieces[5]
white King is pieces[3] 
white Queen is pieces[4]
white pawns are pieces[8:16]

Black rocks are pieces[24] and pieces[31]
Black Knights are pieces[25] and pieces[30]
Black Bishop are pieces[26] and pieces[29]
Black King is pieces[27] 
Black Queen is pieces[28]
Black pawns are pieces[16:24]



def AvailableMoves(selected_piece):
    if selected_piece in JusticeTeam[8:16]:  # Check if the selected piece is a pawn from JusticeTeam
        fisrt_circle = pygame.draw.circle(surface=screen, color=green_color, center=(selected_piece.x + BlockLength / 2, selected_piece.y + BlockWidth / 2 + BlockWidth), radius=15)
        second_circle = pygame.draw.circle(surface=screen, color=green_color, center=(selected_piece.x + BlockLength / 2, selected_piece.y + BlockWidth / 2 + 2 * BlockWidth), radius=15)

                else : 
            pygame.draw.circle(surface=screen,color=green_color,center=(piece.x+131.25,piece.y+131.25),radius=15) 

"""

