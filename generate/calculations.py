import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, hypot, pi


def plot_star_polygon(n, step, ax):
    """
    Plot a regular star polygon on the given axes.
    """

    ratio = retrieve_ratio(n, step)

    deg = 180 - (360 / n)

    initial_rotation = -pi / 2 + pi / n

    points = generate_star_points(n, step)
    points = rotate_points(points, initial_rotation)

    if n % 2 == 0:
        path1_end = points.index(points[0], 1)
        path1 = points[: path1_end + 1]
        xs1, ys1 = zip(*path1)
        ax.plot(xs1, ys1, "b-")

        path2 = points[path1_end + 1 :]
        xs2, ys2 = zip(*path2)
        ax.plot(xs2, ys2, "b-")
    else:
        points.append(points[0])
        xs, ys = zip(*points)
        ax.plot(xs, ys, "b-")

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"\n{{{n}/2}}   {deg:.2f}°   {ratio:.4f}:1\n")


def plot_logarithmic_spiral(n, step, ax):
    """
    Plot a logarithmic spiral on the given axes.
    The spiral will go outward when the ratio > 1 and inward when ratio < 1.
    """
    ratio = retrieve_ratio(n, step)
    deg = 180 - (360 / n)
    theta_arc = np.radians(deg)

    E = np.array([0.0, 0.0])
    D = np.array([1.0, 0.0])

    R = 1.0

    all_x = []
    all_y = []

    for i in range(10):
        perp = np.array([-D[1], D[0]])
        perp = perp / np.linalg.norm(perp) * R
        C = E + perp

        start_vec = E - C
        start_angle = np.arctan2(start_vec[1], start_vec[0])

        n_points = 50
        sweep = np.linspace(0, theta_arc, n_points)
        angles = start_angle + sweep

        radius_scale = np.power(ratio, sweep / theta_arc)
        varying_R = R * radius_scale

        arc_x = C[0] + varying_R * np.cos(angles)
        arc_y = C[1] + varying_R * np.sin(angles)

        if i == 0:
            all_x.extend(arc_x)
            all_y.extend(arc_y)
        else:
            all_x.extend(arc_x[1:])
            all_y.extend(arc_y[1:])

        E = np.array([arc_x[-1], arc_y[-1]])

        end_vec = E - C
        end_vec_norm = end_vec / np.linalg.norm(end_vec)
        D = np.array([-end_vec_norm[1], end_vec_norm[0]])

        R = R * ratio

    xs = np.array(all_x)
    ys = np.array(all_y)
    ax.plot(xs, ys, "r-")

    ax.set_aspect("equal")
    ax.axis("equal")
    ax.set_title(f"{{{n}/2}}   {deg:.2f}°   {ratio:.4f}:1")


def generate_star_points(n, step, radius=1):
    """
    Generate points for a regular star polygon with n vertices and step size.
    """

    points = []
    for i in range(n):
        angle = 2 * pi * i / n
        x = radius * cos(angle)
        y = radius * sin(angle)
        points.append((x, y))

    if n % 2 == 0:
        star_points = []
        for i in range(0, n, 2):
            star_points.append(points[i])
        star_points.append(points[0])
        for i in range(1, n, 2):
            star_points.append(points[i])
        star_points.append(points[1])

        return star_points

    star_points = []
    current = 0
    for _ in range(n):
        star_points.append(points[current])
        current = (current + step) % n

    return star_points


def retrieve_ratio(n, step):
    """
    Retrieve the ratio (base)/(leg) of the isosceles triangle that forms a star's tip.
    For a star polygon the triangle is defined by:
      - the tip (a vertex on the circle)
      - the two intersection points of the extended star edges adjacent to that tip.
    This construction yields, for example, a ratio of ~0.618 for a pentagram (5/2)
    and 1 for a hexagram.
    """

    vertices = [(cos(2 * pi * i / n), sin(2 * pi * i / n)) for i in range(n)]

    V0 = vertices[0]

    p1 = V0
    p2 = vertices[step % n]
    p3 = vertices[n - 1]
    p4 = vertices[(n - 1 + step) % n]
    I1 = line_intersection(p1, p2, p3, p4)

    p1b = V0
    p2b = vertices[(n - step) % n]
    p3b = vertices[1]
    p4b = vertices[(1 - step) % n]
    I2 = line_intersection(p1b, p2b, p3b, p4b)

    if I1 is None or I2 is None:
        leg = 1.0
        base = 2 * sin(pi / n)
    else:
        leg = hypot(I1[0] - V0[0], I1[1] - V0[1])
        base = hypot(I1[0] - I2[0], I1[1] - I2[1])

    return base / leg


def line_intersection(p1, p2, p3, p4):
    """
    Return the intersection point of the lines (p1,p2) and (p3,p4).
    p1, p2, p3, p4 are tuples (x,y).
    """

    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if abs(denom) < 1e-9:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom

    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def rotate_points(points, angle):
    """Rotate points around origin by given angle in radians."""

    rotated = []

    for x, y in points:
        new_x = x * cos(angle) - y * sin(angle)
        new_y = x * sin(angle) + y * cos(angle)
        rotated.append((new_x, new_y))

    return rotated
