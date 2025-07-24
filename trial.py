import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gradient Rect with Border Radius")

# Colors for the gradient
colors = [(15, 12, 41), (48, 43, 99), (36, 36, 62)]

def draw_gradient_rect(surface, rect, colors, border_radius=0):
    # Create a temporary surface with per-pixel alpha (for transparency)
    gradient_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Draw horizontal gradient
    for x in range(rect.width):
        rel = x / rect.width
        if rel < 0.5:
            start_color = colors[0]
            end_color = colors[1]
            local_rel = rel / 0.5
        else:
            start_color = colors[1]
            end_color = colors[2]
            local_rel = (rel - 0.5) / 0.5

        r = int(start_color[0] + (end_color[0] - start_color[0]) * local_rel)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * local_rel)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * local_rel)

        pygame.draw.line(gradient_surf, (r, g, b), (x, 0), (x, rect.height))

    # Create a mask for rounded corners
    mask_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask_surf, (255, 255, 255), mask_surf.get_rect(), border_radius=border_radius)

    # Use mask_surf as an alpha mask
    gradient_surf.blit(mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Blit the final gradient onto the main surface
    surface.blit(gradient_surf, rect.topleft)

# Main loop
while True:
    screen.fill((30, 30, 30))  # Background

    # Draw a gradient rectangle with rounded corners
    rect = pygame.Rect(150, 200, 500, 150)
    draw_gradient_rect(screen, rect, colors, border_radius=30)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
