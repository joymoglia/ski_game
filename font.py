import pygame

pygame.init()

print(pygame.font.get_fonts())


# white = (255,255,255)
# black = (0,0,0)
# red = (255,0,0)
# green = (0,155,0)
# smallfont = pygame.font.SysFont(("berlinsansfbdemi"), 10)
# medfont = pygame.font.SysFont(("segoeuiblack"), 20)
# largefont = pygame.font.SysFont(("berlinsansfbdemi"), 30)

# def render_font(msg, color, size):
#     """ Renders font into a surface and rect"""
#     if size == "small":
#         msg_surface = smallfont.render(msg, True, color)
#     elif size == "medium":
#         msg_surface = medfont.render(msg, True, color)
#     elif size == 'large':
#         msg_surface = largefont.render(msg, True, color)
    
#     return msg_surface, msg_surface.get_rect()
    
# def draw_message(msg, color, size="small"):
#     msg_surface, msg_rect = render_font(msg, color, size)
#     msg_rect.midtop = (X_DIM/2, 0)
#     SCREEN.blit(msg_surface, msg_rect)