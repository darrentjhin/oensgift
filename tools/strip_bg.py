#!/usr/bin/env python3
"""Remove the flat background from official-style artwork and trim to the subject.

Only clears near-white pixels that are CONNECTED to the image border, so white
parts of the subject (Mewtwo's body, Charizard's belly) are kept. Outputs a
tightly-cropped RGBA PNG with a transparent background.

Usage: python3 tools/strip_bg.py <in.png> <out.png> [white_threshold]
"""
import sys
from collections import deque
import numpy as np
from PIL import Image


def strip(inp, outp, thresh=232, fill_holes=False):
    im = Image.open(inp).convert("RGBA")
    arr = np.array(im)
    h, w = arr.shape[:2]
    rgb = arr[:, :, :3].astype(np.int16)
    # "background-ish": bright and near-grey (low channel spread) so coloured
    # subject pixels are never mistaken for background
    bright = (rgb.min(axis=2) >= thresh)
    flat = (rgb.max(axis=2) - rgb.min(axis=2) <= 18)
    whiteish = bright & flat

    visited = np.zeros((h, w), bool)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if whiteish[y, x] and not visited[y, x]:
                visited[y, x] = True
                dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if whiteish[y, x] and not visited[y, x]:
                visited[y, x] = True
                dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        if y > 0 and whiteish[y - 1, x] and not visited[y - 1, x]:
            visited[y - 1, x] = True; dq.append((y - 1, x))
        if y < h - 1 and whiteish[y + 1, x] and not visited[y + 1, x]:
            visited[y + 1, x] = True; dq.append((y + 1, x))
        if x > 0 and whiteish[y, x - 1] and not visited[y, x - 1]:
            visited[y, x - 1] = True; dq.append((y, x - 1))
        if x < w - 1 and whiteish[y, x + 1] and not visited[y, x + 1]:
            visited[y, x + 1] = True; dq.append((y, x + 1))

    cleared = visited.copy()
    if fill_holes:
        # also clear LARGE pure-white pockets trapped inside the subject (e.g.
        # background gaps enclosed by Rayquaza's coils or a Flareon tail curl).
        # Strict purity + a min-size threshold keep the subject's own shaded
        # light areas AND tiny white details (eye glints) intact.
        pure = (rgb.min(axis=2) >= 244) & (rgb.max(axis=2) - rgb.min(axis=2) <= 10) & ~visited
        min_hole = max(2500, int(h * w * 0.003))
        pv = np.zeros((h, w), bool)
        pys, pxs = np.where(pure)
        for sy, sx in zip(pys.tolist(), pxs.tolist()):
            if pv[sy, sx]:
                continue
            stack = [(sy, sx)]; pv[sy, sx] = True; comp = []
            while stack:
                y, x = stack.pop(); comp.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and pure[ny, nx] and not pv[ny, nx]:
                        pv[ny, nx] = True; stack.append((ny, nx))
            if len(comp) >= min_hole:
                for (y, x) in comp:
                    cleared[y, x] = True

    arr[:, :, 3] = np.where(cleared, 0, arr[:, :, 3])
    visited = cleared

    # soften the 1px halo: any opaque pixel touching the cleared region and still
    # near-white gets partial alpha so edges don't show a white fringe
    op = arr[:, :, 3] > 0
    nb_bg = np.zeros((h, w), bool)
    nb_bg[1:, :] |= visited[:-1, :]
    nb_bg[:-1, :] |= visited[1:, :]
    nb_bg[:, 1:] |= visited[:, :-1]
    nb_bg[:, :-1] |= visited[:, 1:]
    halo = op & nb_bg & (rgb.min(axis=2) >= thresh - 24)
    arr[:, :, 3][halo] = (arr[:, :, 3][halo] * 0.45).astype(np.uint8)

    # tight crop to the subject (with a small margin)
    ys, xs = np.where(arr[:, :, 3] > 8)
    if len(xs):
        m = 6
        y0, y1 = max(0, ys.min() - m), min(h, ys.max() + 1 + m)
        x0, x1 = max(0, xs.min() - m), min(w, xs.max() + 1 + m)
        arr = arr[y0:y1, x0:x1]

    Image.fromarray(arr).save(outp)
    print(f"{inp} -> {outp}  ({arr.shape[1]}x{arr.shape[0]}, transparent)")


if __name__ == "__main__":
    thr = int(sys.argv[3]) if len(sys.argv) > 3 else 232
    holes = len(sys.argv) > 4 and sys.argv[4] == "holes"
    strip(sys.argv[1], sys.argv[2], thr, holes)
