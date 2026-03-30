"""Simple pygame demo: 10 squares moving randomly on a canvas.

This file intentionally includes TODO notes and small extension stubs so it can
be used as a learning exercise.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

import pygame


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
FPS = 60
MIN_SQUARE_SIZE = 10
MAX_SQUARE_SIZE = 100
SQUARE_COUNT = 30
MAX_SPEED = 4

BACKGROUND_COLOR = (20, 24, 34)

# Color scale: dark cherry (small squares) to light cherry (large squares)
# Both endpoints are lighter than background for visibility
DARK_CHERRY = (110, 35, 50)      # Darker cherry for small squares
LIGHT_CHERRY = (255, 120, 140)   # Lighter cherry for large squares


def get_color_for_size(size: int) -> tuple[int, int, int]:
	"""Return a color based on square size: darker for small, lighter for large."""
	# Normalize size to 0-1 range
	normalized = (size - MIN_SQUARE_SIZE) / (MAX_SQUARE_SIZE - MIN_SQUARE_SIZE)
	# Interpolate RGB values
	r = int(DARK_CHERRY[0] + (LIGHT_CHERRY[0] - DARK_CHERRY[0]) * normalized)
	g = int(DARK_CHERRY[1] + (LIGHT_CHERRY[1] - DARK_CHERRY[1]) * normalized)
	b = int(DARK_CHERRY[2] + (LIGHT_CHERRY[2] - DARK_CHERRY[2]) * normalized)
	return (r, g, b)


@dataclass
class Square:
	"""Stores square position, velocity, color, size, and max speed."""

	x: float
	y: float
	vx: float
	vy: float
	color: tuple[int, int, int]
	size: int
	max_speed: float


def create_random_square() -> Square:
	"""Create one square at a random position with random speed, color, and size.
	
	Speed scales inversely with size: size 10 -> speed 190, size 100 -> speed 10.
	"""
	size = random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)
	# Map size to max_speed inversely: small squares are fast, large squares are slow
	max_speed = 50 - (size - MIN_SQUARE_SIZE) * (50 - 5) / (MAX_SQUARE_SIZE - MIN_SQUARE_SIZE)
	x = random.uniform(0, WINDOW_WIDTH - size)
	y = random.uniform(0, WINDOW_HEIGHT - size)
	vx = random.choice([-1, 1]) * random.uniform(1, max_speed)
	vy = random.choice([-1, 1]) * random.uniform(1, max_speed)
	color = get_color_for_size(size)
	return Square(x=x, y=y, vx=vx, vy=vy, color=color, size=size, max_speed=max_speed)


def random_nudge(square: Square) -> None:
	"""Slightly change direction to create a random-walk feeling."""
	square.vx += random.uniform(-0.2, 0.2)
	square.vy += random.uniform(-0.2, 0.2)

	# Keep speed in a sensible range so movement remains visible and stable.
	square.vx = max(-square.max_speed, min(square.max_speed, square.vx))
	square.vy = max(-square.max_speed, min(square.max_speed, square.vy))


def update_square(square: Square) -> None:
	"""Move square and bounce it on the window borders."""
	random_nudge(square)

	square.x += square.vx
	square.y += square.vy

	if square.x <= 0:
		square.x = 0
		square.vx *= -1
	elif square.x + square.size >= WINDOW_WIDTH:
		square.x = WINDOW_WIDTH - square.size
		square.vx *= -1

	if square.y <= 0:
		square.y = 0
		square.vy *= -1
	elif square.y + square.size >= WINDOW_HEIGHT:
		square.y = WINDOW_HEIGHT - square.size
		square.vy *= -1


def draw_square(surface: pygame.Surface, square: Square) -> None:
	"""Draw one square."""
	rect = pygame.Rect(int(square.x), int(square.y), square.size, square.size)
	pygame.draw.rect(surface, square.color, rect)


def handle_input(
	event: pygame.event.Event,
	paused: bool,
	target_fps: int,
	squares: list[Square],
) -> tuple[bool, bool, int, list[Square]]:
	"""Handle one event and return updated app state.

	Returns (should_quit, paused, target_fps, squares).
	"""
	if event.type == pygame.QUIT:
		return True, paused, target_fps, squares

	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_ESCAPE:
			return True, paused, target_fps, squares
		if event.key == pygame.K_SPACE:
			paused = not paused
		elif event.key == pygame.K_r:
			squares = [create_random_square() for _ in range(SQUARE_COUNT)]
		# elif event.key == pygame.K_UP:
		# 	# Higher FPS means smoother/faster updates.
		# 	target_fps = min(300, target_fps + 10)
		# elif event.key == pygame.K_DOWN:
		# 	target_fps = max(10, target_fps - 10)

	# TODO: Add more controls (e.g., C to randomize colors only).
	return False, paused, target_fps, squares


def draw_overlay(surface: pygame.Surface, paused: bool, target_fps: int) -> None:
	"""Draw simple status and control hints."""
	font = pygame.font.SysFont(None, 24)
	text_color = (235, 235, 235)

	status_text = "Status: Paused" if paused else "Status: Running"
	fps_text = f"Target FPS: {target_fps}"
	controls_text = "SPACE pause/resume | R reset | UP/DOWN speed | ESC quit"

	status_surface = font.render(status_text, True, text_color)
	fps_surface = font.render(fps_text, True, text_color)
	controls_surface = font.render(controls_text, True, text_color)

	surface.blit(status_surface, (10, 10))
	surface.blit(fps_surface, (10, 34))
	surface.blit(controls_surface, (10, 58))


def main() -> None:
	"""Run the animation loop."""
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Random Moving Squares")
	clock = pygame.time.Clock()

	squares = [create_random_square() for _ in range(SQUARE_COUNT)]
	paused = False
	target_fps = FPS

	running = True
	while running:
		for event in pygame.event.get():
			should_quit, paused, target_fps, squares = handle_input(
				event,
				paused,
				target_fps,
				squares,
			)
			if should_quit:
				running = False

		screen.fill(BACKGROUND_COLOR)

		for square in squares:
			if not paused:
				update_square(square)
			draw_square(screen, square)

		draw_overlay(screen, paused, target_fps)
		pygame.display.flip()
		clock.tick(target_fps)

	pygame.quit()


if __name__ == "__main__":
	main()
