import pygame
from bleak import BleakScanner, BleakClient
import asyncio
import threading
import time

# Configuración de asyncio
asyncio_loop = asyncio.new_event_loop()
asyncio_thread = threading.Thread(target=asyncio_loop.run_forever, daemon=True)
asyncio_thread.start()

# Colores
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
WHITE = (240, 240, 240)
BLUE = (0, 122, 255)
DARK_BLUE = (0, 80, 160)
RED = (255, 59, 48)
DARK_RED = (200, 30, 30)
GREEN = (52, 199, 89)
DARK_GREEN = (28, 160, 66)
YELLOW = (255, 204, 0)
SHADOW = (150, 150, 150)

# Constantes
UUID_TX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
HIGHLIGHT_DURATION = 200  # ms
BUTTON_RADIUS = 15
ARROW_FONT_SIZE = 48

pygame.init()
screen = pygame.display.set_mode((450, 550))
pygame.display.set_caption("Control Otto - BLE")
font = pygame.font.SysFont('Arial', 32, bold=True)
arrow_font = pygame.font.SysFont('Arial', ARROW_FONT_SIZE, bold=True)

# Estados
connected = False
robot_client = None
last_pressed = None
status_message = None
status_time = 0

# Geometría de la interfaz
connect_button = pygame.Rect(125, 30, 200, 50)
directions = {
    "FORWARD": pygame.Rect(175, 150, 100, 80),
    "BACKWARD": pygame.Rect(175, 300, 100, 80),
    "LEFT": pygame.Rect(75, 225, 80, 80),
    "RIGHT": pygame.Rect(275, 225, 80, 80)
}
stop_button = pygame.Rect(175, 400, 100, 50)


async def connect_to_robot():
    global status_message, status_time
    devices = await BleakScanner.discover()
    for device in devices:
        if "Otto" in str(device.name):
            try:
                client = BleakClient(device.address)
                await client.connect()
                if client.is_connected:
                    return client
            except Exception as e:
                print(f"Error: {e}")
    return None


async def disconnect_robot(client):
    if client and client.is_connected:
        await client.disconnect()


async def send_command(client, command):
    if client and client.is_connected:
        await client.write_gatt_char(UUID_TX, command.encode())


def draw_button(surface, rect, text, bg_color, text_color, shadow=True):
    if shadow:
        pygame.draw.rect(surface, SHADOW, rect.move(3, 3), border_radius=BUTTON_RADIUS)
    pygame.draw.rect(surface, bg_color, rect, border_radius=BUTTON_RADIUS)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def draw_arrow_button(surface, rect, arrow, bg_color, shadow=True):
    if shadow:
        pygame.draw.rect(surface, SHADOW, rect.move(3, 3), border_radius=BUTTON_RADIUS)
    pygame.draw.rect(surface, bg_color, rect, border_radius=BUTTON_RADIUS)
    text_surf = arrow_font.render(arrow, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def status_led(surface):
    color = DARK_GREEN if connected else DARK_RED
    pygame.draw.circle(surface, color, (400, 55), 12)
    pygame.draw.circle(surface, WHITE, (400, 55), 12, 2)


running = True
while running:
    current_time = pygame.time.get_ticks()
    screen.fill(LIGHT_GRAY)

    # Dibujar sombras
    pygame.draw.rect(screen, SHADOW, (20, 20, 410, 510), border_radius=20)

    # Fondo principal
    main_panel = pygame.Rect(15, 15, 420, 520)
    pygame.draw.rect(screen, WHITE, main_panel, border_radius=20)

    # Botón de conexión
    btn_color = DARK_BLUE if connected else BLUE
    draw_button(screen, connect_button,
                "DESCONECTAR" if connected else "CONECTAR",
                btn_color, WHITE)

    # LED de estado
    status_led(screen)

    # Flechas direccionales
    arrows = {"FORWARD": "↑", "BACKWARD": "↓", "LEFT": "←", "RIGHT": "→"}
    for dir, rect in directions.items():
        color = DARK_BLUE if last_pressed == dir and (current_time - status_time < HIGHLIGHT_DURATION) else BLUE
        draw_arrow_button(screen, rect, arrows[dir], color)

    # Botón de stop
    stop_color = DARK_RED if last_pressed == "STOP" and (current_time - status_time < HIGHLIGHT_DURATION) else RED
    draw_button(screen, stop_button, "STOP", stop_color, WHITE)

    # Mensajes de estado
    if status_message and (current_time - status_time < 3000):
        text = font.render(status_message, True, DARK_GRAY)
        text_rect = text.get_rect(center=(225, 500))
        screen.blit(text, text_rect)

    pygame.display.flip()

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if connect_button.collidepoint(pos):
                if not connected:
                    def connect_callback(future):
                        global connected, robot_client, status_message, status_time
                        try:
                            robot_client = future.result()
                            connected = robot_client is not None
                            status_message = "Conectado!" if connected else "No encontrado"
                        except Exception as e:
                            status_message = f"Error: {str(e)}"
                            connected = False
                        status_time = pygame.time.get_ticks()


                    future = asyncio.run_coroutine_threadsafe(connect_to_robot(), asyncio_loop)
                    future.add_done_callback(connect_callback)
                    status_message = "Buscando robot..."
                    status_time = pygame.time.get_ticks()
                else:
                    asyncio.run_coroutine_threadsafe(disconnect_robot(robot_client), asyncio_loop)
                    robot_client = None
                    connected = False
                    status_message = "Desconectado"
                    status_time = pygame.time.get_ticks()

            elif connected:
                if stop_button.collidepoint(pos):
                    asyncio.run_coroutine_threadsafe(send_command(robot_client, "stop"), asyncio_loop)
                    last_pressed = "STOP"
                    status_time = current_time

                else:
                    for dir, rect in directions.items():
                        if rect.collidepoint(pos):
                            command = f"{dir.lower()} 3"
                            asyncio.run_coroutine_threadsafe(send_command(robot_client, command), asyncio_loop)
                            last_pressed = dir
                            status_time = current_time

pygame.quit()
if robot_client and robot_client.is_connected:
    asyncio.run_coroutine_threadsafe(robot_client.disconnect(), asyncio_loop)