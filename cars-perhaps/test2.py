import pygame
import sys
import math

# Initialize Pygame engine
pygame.init()

# Setup screen for full-screen borderless windowed mode
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("White Color Ripple Hexagon Grid")
clock = pygame.time.Clock()

# Geometric configurations
SIDE_LENGTH = 45
GAP = 4  
COL_SPACING = SIDE_LENGTH * 1.5
ROW_SPACING = math.sqrt(3) * SIDE_LENGTH

# Color definitions (Changed to clean white styles)
BASE_TILE_COLOR = (24, 25, 38)     # Off-state dark charcoal core
BASE_RIM_COLOR = (70, 75, 100)     # Off-state dim slate rim
WHITE_GLOW_COLOR = (255, 255, 255) # Pure white for hover highlights and shockwave cores

def get_hexagon_points(center_x, center_y, side):
    """Calculates coordinates for 6 hexagon vertices."""
    points = []
    for i in range(6):
        angle_rad = math.radians(60 * i)
        x = center_x + side * math.cos(angle_rad)
        y = center_y + side * math.sin(angle_rad)
        points.append((x, y))
    return points

def is_point_in_hex(px, py, cx, cy, side):
    """Checks if a point is inside a hexagon using Ray-Casting."""
    if math.hypot(px - cx, py - cy) > side:
        return False
    vertices = get_hexagon_points(cx, cy, side)
    n = len(vertices)
    inside = False
    
    p1x, p1y = vertices[n - 1] 
    
    for i in range(n):
        p2x, p2y = vertices[i]
        if py > min(p1y, p2y):
            if py <= max(p1y, p2y):
                if px <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or px <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# --- PRE-GENERATE THE GRID STATE ---
hex_grid = []
max_cols = int(SCREEN_WIDTH / COL_SPACING) + 2
max_rows = int(SCREEN_HEIGHT / ROW_SPACING) + 2

for col in range(-1, max_cols):
    for row in range(-1, max_rows):
        x_pos = col * COL_SPACING
        y_pos = row * ROW_SPACING
        if col % 2 == 1:
            y_pos += ROW_SPACING / 2
            
        hex_grid.append({
            'x': x_pos,
            'y': y_pos,
            'glow': 0.0,
            'color': WHITE_GLOW_COLOR  # Default to pure white
        })

# Active expansion trackers
ripple_effects = []
DIM_SPEED = 0.015     # Pace at which glow vanishes from screens
RIPPLE_SPEED = 12.0    # Pixel radius speed expanding out each frame
RIPPLE_WIDTH = 60.0    # Thickness layer of the shockwave ring
MAX_RIPPLE_DIST = 500  # Distance cutoff for ripple dispersion

# Drag tracking variables
last_ripple_pos = None
MIN_DRAG_DIST = 35    # Minimum distance mouse must move to spawn another drag ripple

# Main program loop
running = True

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    spawn_ripple = False
    
    # --- EVENT PROCESSING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                spawn_ripple = True
                last_ripple_pos = (mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                last_ripple_pos = None

    # --- DRAG LOGIC ---
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Index 0 is Left Click
        if last_ripple_pos is None:
            spawn_ripple = True
            last_ripple_pos = (mouse_x, mouse_y)
        else:
            dist_moved = math.hypot(mouse_x - last_ripple_pos[0], mouse_y - last_ripple_pos[1])
            if dist_moved > MIN_DRAG_DIST:
                spawn_ripple = True
                last_ripple_pos = (mouse_x, mouse_y)

    # Spawn the ripple if triggered by a click or drag movement
    if spawn_ripple:
        ripple_effects.append({
            'cx': mouse_x,
            'cy': mouse_y,
            'radius': 0.0,
            'color': WHITE_GLOW_COLOR  # Overrode random generator to static white
        })

    # --- UPDATE ACTIVE RIPPLES ---
    for rip in ripple_effects[:]:
        rip['radius'] += RIPPLE_SPEED
        if rip['radius'] > MAX_RIPPLE_DIST:
            ripple_effects.remove(rip)

    # --- RENDERING AND CORE GRID UPDATE LOGIC ---
    screen.fill((10, 10, 18))  
    
    for tile in hex_grid:
        is_hovered = is_point_in_hex(mouse_x, mouse_y, tile['x'], tile['y'], SIDE_LENGTH - GAP)
        
        # Check if the tile falls inside any running shockwave envelopes
        for rip in ripple_effects:
            distance = math.hypot(tile['x'] - rip['cx'], tile['y'] - rip['cy'])
            
            if rip['radius'] - RIPPLE_WIDTH <= distance <= rip['radius']:
                falloff = 1.0 - (abs(distance - (rip['radius'] - RIPPLE_WIDTH / 2)) / (RIPPLE_WIDTH / 2))
                falloff = max(0.0, min(1.0, falloff))
                
                if falloff > tile['glow']:
                    tile['glow'] = falloff
                    tile['color'] = rip['color']

        # Natural slow decay fade-out loops
        if tile['glow'] > 0:
            tile['glow'] -= DIM_SPEED
            if tile['glow'] < 0:
                tile['glow'] = 0.0

        # Structural response properties
        if is_hovered:
            shadow_offset = 5
            current_side = (SIDE_LENGTH - GAP) + 3
            
            # Hover rim matches active white glowing state seamlessly 
            rim_color = WHITE_GLOW_COLOR
            
            shadow_points = get_hexagon_points(tile['x'] + shadow_offset, tile['y'] + shadow_offset, current_side)
            pygame.draw.polygon(screen, (5, 5, 10), shadow_points)
        else:
            current_side = SIDE_LENGTH - GAP
            
            # Linearly interpolate the border/rim color too so it fades along with the face core!
            r_rim = int(BASE_RIM_COLOR[0] + (WHITE_GLOW_COLOR[0] - BASE_RIM_COLOR[0]) * tile['glow'])
            g_rim = int(BASE_RIM_COLOR[1] + (WHITE_GLOW_COLOR[1] - BASE_RIM_COLOR[1]) * tile['glow'])
            b_rim = int(BASE_RIM_COLOR[2] + (WHITE_GLOW_COLOR[2] - BASE_RIM_COLOR[2]) * tile['glow'])
            rim_color = (r_rim, g_rim, b_rim)

        # Calculate linear interpolation matrix for core face filling
        r_face = int(BASE_TILE_COLOR[0] + (tile['color'][0] - BASE_TILE_COLOR[0]) * tile['glow'])
        g_face = int(BASE_TILE_COLOR[1] + (tile['color'][1] - BASE_TILE_COLOR[1]) * tile['glow'])
        b_face = int(BASE_TILE_COLOR[2] + (tile['color'][2] - BASE_TILE_COLOR[2]) * tile['glow'])
        interpolated_fill_color = (r_face, g_face, b_face)

        # Construct final canvas vector profiles
        hex_vertices = get_hexagon_points(tile['x'], tile['y'], current_side)
        pygame.draw.polygon(screen, interpolated_fill_color, hex_vertices)
        pygame.draw.polygon(screen, rim_color, hex_vertices, width=2)
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
