from math import sin, cos
import arcade as arc


class Timings:
    interval_primary = 0.7
    interval_secondary = 1.4


def update_fire(
    dt: float = 1 / 60,
) -> None:
    """Called in Alien.on_update"""
    return


def pattern_primary(timer: float, bullet: arc.Sprite) -> None:
    bullet.change_x = 10
    bullet.change_y = 10


def fire(
    bullet_texture: arc.Texture,
    bullet_scale: float,
    pattern="star8",
) -> list[arc.Sprite]:
    """Called in Alien._fire"""
    bullets = []
    if pattern == "star8":
        base_angle = 360 // 8
        angles = [base_angle * a for a in range(8)]
        for angle in angles:
            bullet = arc.Sprite(
                texture=bullet_texture,
                scale=bullet_scale,
            )
            bullet.change_x = sin(angle)
            bullet.change_y = cos(angle)
            bullets.append(bullet)

    return bullets
