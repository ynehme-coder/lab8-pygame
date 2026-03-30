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
SQUARE_SIZE = 30
SQUARE_COUNT = 10
MAX_SPEED = 4

BACKGROUND_COLOR = (20, 24, 34)


@dataclass
class Square:
	"""Stores square position, velocity, and color."""

	x: float
	y: float
	vx: float
	vy: float
	color: tuple[int, int, int]


def create_random_square() -> Square:
	"""Create one square at a random position with random speed and color."""
	x = random.uniform(0, WINDOW_WIDTH - SQUARE_SIZE)
	y = random.uniform(0, WINDOW_HEIGHT - SQUARE_SIZE)
	vx = random.choice([-1, 1]) * random.uniform(1, MAX_SPEED)
	vy = random.choice([-1, 1]) * random.uniform(1, MAX_SPEED)
	color = (
		random.randint(70, 255),
		random.randint(70, 255),
		random.randint(70, 255),
	)
	return Square(x=x, y=y, vx=vx, vy=vy, color=color)


def random_nudge(square: Square) -> None:
	"""Slightly change direction to create a random-walk feeling."""
	square.vx += random.uniform(-0.2, 0.2)
	square.vy += random.uniform(-0.2, 0.2)

	# Keep speed in a sensible range so movement remains visible and stable.
	square.vx = max(-MAX_SPEED, min(MAX_SPEED, square.vx))
	square.vy = max(-MAX_SPEED, min(MAX_SPEED, square.vy))


def update_square(square: Square) -> None:
	"""Move square and bounce it on the window borders."""
	random_nudge(square)

	square.x += square.vx
	square.y += square.vy

	if square.x <= 0:
		square.x = 0
		square.vx *= -1
	elif square.x + SQUARE_SIZE >= WINDOW_WIDTH:
		square.x = WINDOW_WIDTH - SQUARE_SIZE
		square.vx *= -1

	if square.y <= 0:
		square.y = 0
		square.vy *= -1
	elif square.y + SQUARE_SIZE >= WINDOW_HEIGHT:
		square.y = WINDOW_HEIGHT - SQUARE_SIZE
		square.vy *= -1


def draw_square(surface: pygame.Surface, square: Square) -> None:
	"""Draw one square."""
	rect = pygame.Rect(int(square.x), int(square.y), SQUARE_SIZE, SQUARE_SIZE)
	pygame.draw.rect(surface, square.color, rect)


def handle_input(event: pygame.event.Event) -> bool:
	"""Stub: central place for input handling.

	Returns True when the app should stop running.
	"""
	if event.type == pygame.QUIT:
		return True

	# TODO: Add keyboard controls (pause with SPACE, reset with R, etc.).
	return False


def draw_overlay(surface: pygame.Surface) -> None:
	"""Stub: draw text or UI overlays.

	TODO: Show FPS and instructions in this function.
	"""
	_ = surface


def main() -> None:
	"""Run the animation loop."""
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Random Moving Squares")
	clock = pygame.time.Clock()

	squares = [create_random_square() for _ in range(SQUARE_COUNT)]

	running = True
	while running:
		for event in pygame.event.get():
			if handle_input(event):
				running = False

		screen.fill(BACKGROUND_COLOR)

		for square in squares:
			update_square(square)
			draw_square(screen, square)

		draw_overlay(screen)
		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()


if __name__ == "__main__":
	main()
