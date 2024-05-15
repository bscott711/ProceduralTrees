import pygame

brown0 = (133, 94, 41)
brown1 = (102, 68, 20)
trunk_outline = pygame.Color(79, 58, 28, 255)
trunk_width_power = 3 / 4

green0 = (100, 140, 50)
green1 = (90, 130, 40)
green2 = (80, 120, 30)
leaves_outline = pygame.Color(68, 94, 52, 255)
shadow_color = pygame.Color(0, 0, 0, 100)
leaves_shadow_ratio = 1.5
children_for_leaves = 6

leaf_surface_width = 64
leaf_surface_height = 64
tree_surface_width = 360
tree_surface_height = 460
tree_base_pos = (tree_surface_width / 2, tree_surface_height - 30)
shadow_base = tree_base_pos[1] - 30

start_branch_len = 30
start_branch_angle = 90
tree_max_nodes = 50
min_length = 12
max_length = 40
min_angle_left = 100
max_angle_left = 145
min_angle_right = 35
max_angle_right = 80

bend_age_change = -3
grow_age_change = 12
grow_length_change = 2

