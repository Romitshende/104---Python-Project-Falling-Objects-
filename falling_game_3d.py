from ursina import *
import random

app = Ursina()

# Player
player = Entity(model='cube', color=color.azure, scale=(1.5, 0.5, 1.5), position=(0, -4, 0))

# Score and lives
score = 0
lives = 3
score_text = Text(text=f'Score: {score}', position=(-0.85, 0.45), scale=2, color=color.white)
lives_text = Text(text=f'Lives: {lives}', position=(0.6, 0.45), scale=2, color=color.white)

# Falling objects list
falling_objects = []

# Create a falling object
def spawn_object():
    obj_type = random.choice(['enemy', 'powerup'])
    color_type = color.red if obj_type == 'enemy' else color.green
    obj = Entity(model='cube', color=color_type, scale=1, position=(random.uniform(-5,5), 6, 0))
    obj.obj_type = obj_type
    falling_objects.append(obj)

# Spawn multiple at start
for _ in range(5):
    spawn_object()

def update():
    global score, lives

    # Player movement
    if held_keys['a']:
        player.x -= 5 * time.dt
    if held_keys['d']:
        player.x += 5 * time.dt

    for obj in falling_objects:
        obj.y -= 4 * time.dt

        # Collision
        if obj.intersects(player).hit:
            if obj.obj_type == 'enemy':
                lives -= 1
            else:
                score += 5
            obj.y = 6
            obj.x = random.uniform(-5,5)

        # If object goes off-screen
        if obj.y < -6:
            obj.y = 6
            obj.x = random.uniform(-5,5)
            if obj.obj_type == 'enemy':
                score += 1

    # Update text
    score_text.text = f"Score: {score}"
    lives_text.text = f"Lives: {lives}"

    # Game over check
    if lives <= 0:
        destroy(player)
        Text(text='GAME OVER', origin=(0,0), scale=3, color=color.red)
        application.pause()

Sky()
camera.orthographic = True
camera.fov = 10

app.run()
