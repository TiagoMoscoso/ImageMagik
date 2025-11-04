from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any
from PIL import Image

Coords = Tuple[int, int, int, int]

class Filter(ABC):
    key: str = "base"
    name: str = "Base"

    @abstractmethod
    def apply(self, image: Image.Image, coordinates: Coords, arguments: Dict[str, Any]) -> Image.Image:
        raise NotImplementedError

class GrayFilter(Filter):
    key = "gray"
    name = "Escala de Cinza"

    def apply(self, image, coordinates, arguments):
        x0, y0, x1, y1 = coordinates
        left, top, right, bottom = min(x0,x1), min(y0,y1), max(x0,x1), max(y0,y1)
        out = image.copy()
        px = out.load()
        for y in range(top, bottom):
            for x in range(left, right):
                r, g, b, a = px[x, y]
                gray = int((r + g + b) / 3)
                px[x, y] = (gray, gray, gray, a)
        return out


class BlurFilter(Filter):
    key = "blur"
    name = "Desfoque Simples"

    def apply(self, image, coordinates, arguments):
        radius = int(arguments.get("radius", 1))
        x0, y0, x1, y1 = coordinates
        left, top, right, bottom = min(x0,x1), min(y0,y1), max(x0,x1), max(y0,y1)
        out = image.copy()
        px = image.load()
        new_px = out.load()

        for y in range(top + radius, bottom - radius):
            for x in range(left + radius, right - radius):
                r_sum = g_sum = b_sum = a_sum = 0
                count = 0
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        r, g, b, a = px[x + dx, y + dy]
                        r_sum += r; g_sum += g; b_sum += b; a_sum += a
                        count += 1
                new_px[x, y] = (
                    int(r_sum / count),
                    int(g_sum / count),
                    int(b_sum / count),
                    int(a_sum / count)
                )
        return out


class InvertFilter(Filter):
    key = "invert"
    name = "Inverter Cores"

    def apply(self, image, coordinates, arguments):
        left, top, right, bottom = min(coordinates[0], coordinates[2]), min(coordinates[1], coordinates[3]), max(coordinates[0], coordinates[2]), max(coordinates[1], coordinates[3])
        out = image.copy()
        px = out.load()
        for y in range(top, bottom):
            for x in range(left, right):
                r, g, b, a = px[x, y]
                px[x, y] = (255 - r, 255 - g, 255 - b, a)
        return out


class BrightnessFilter(Filter):
    key = "brightness"
    name = "Ajustar Brilho"

    def apply(self, image, coordinates, arguments):
        factor = float(arguments.get("factor", 1.2))
        left, top, right, bottom = min(coordinates[0], coordinates[2]), min(coordinates[1], coordinates[3]), max(coordinates[0], coordinates[2]), max(coordinates[1], coordinates[3])
        out = image.copy()
        px = out.load()
        for y in range(top, bottom):
            for x in range(left, right):
                r, g, b, a = px[x, y]
                r = min(int(r * factor), 255)
                g = min(int(g * factor), 255)
                b = min(int(b * factor), 255)
                px[x, y] = (r, g, b, a)
        return out


class ContrastFilter(Filter):
    key = "contrast"
    name = "Ajustar Contraste"

    def apply(self, image, coordinates, arguments):
        factor = float(arguments.get("factor", 1.3))
        left, top, right, bottom = min(coordinates[0], coordinates[2]), min(coordinates[1], coordinates[3]), max(coordinates[0], coordinates[2]), max(coordinates[1], coordinates[3])
        out = image.copy()
        px = out.load()
        def adj(v): return min(max(int((v - 128) * factor + 128), 0), 255)
        for y in range(top, bottom):
            for x in range(left, right):
                r, g, b, a = px[x, y]
                px[x, y] = (adj(r), adj(g), adj(b), a)
        return out


class SepiaFilter(Filter):
    key = "sepia"
    name = "Tons Sépia"

    def apply(self, image, coordinates, arguments):
        left, top, right, bottom = min(coordinates[0], coordinates[2]), min(coordinates[1], coordinates[3]), max(coordinates[0], coordinates[2]), max(coordinates[1], coordinates[3])
        out = image.copy()
        px = out.load()
        for y in range(top, bottom):
            for x in range(left, right):
                r, g, b, a = px[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                px[x, y] = (min(tr,255), min(tg,255), min(tb,255), a)
        return out


class ThresholdFilter(Filter):
    key = "threshold"
    name = "Limiar (Preto e Branco)"

    def apply(self, image, coordinates, arguments):
        limit = int(arguments.get("limit", 128))
        left, top, right, bottom = min(coordinates[0], coordinates[2]), min(coordinates[1], coordinates[3]), max(coordinates[0], coordinates[2]), max(coordinates[1], coordinates[3])
        out = image.copy()
        px = out.load()
        for y in range(top, bottom):
            for x in range(left, right):
                r, g, b, a = px[x, y]
                avg = (r + g + b) // 3
                v = 255 if avg > limit else 0
                px[x, y] = (v, v, v, a)
        return out


class PixelateFilter(Filter):
    key = "pixelate"
    name = "Pixelizar"

    def apply(self, image, coordinates, arguments):
        size = int(arguments.get("size", 8))
        left, top, right, bottom = min(coordinates[0], coordinates[2]), min(coordinates[1], coordinates[3]), max(coordinates[0], coordinates[2]), max(coordinates[1], coordinates[3])
        out = image.copy()
        px = out.load()
        for y in range(top, bottom, size):
            for x in range(left, right, size):
                r_sum = g_sum = b_sum = a_sum = count = 0
                for dy in range(size):
                    for dx in range(size):
                        if x + dx < right and y + dy < bottom:
                            r, g, b, a = px[x + dx, y + dy]
                            r_sum += r; g_sum += g; b_sum += b; a_sum += a
                            count += 1
                if count == 0: continue
                r, g, b, a = r_sum//count, g_sum//count, b_sum//count, a_sum//count
                for dy in range(size):
                    for dx in range(size):
                        if x + dx < right and y + dy < bottom:
                            px[x + dx, y + dy] = (r, g, b, a)
        return out


class EdgeFilter(Filter):
    key = "edges"
    name = "Detecção de Bordas"

    def apply(self, image, coordinates, arguments):
        left, top, right, bottom = min(coordinates[0], coordinates[2]), min(coordinates[1], coordinates[3]), max(coordinates[0], coordinates[2]), max(coordinates[1], coordinates[3])
        out = image.copy()
        px = image.load()
        new_px = out.load()
        for y in range(top + 1, bottom - 1):
            for x in range(left + 1, right - 1):
                r1, g1, b1, a1 = px[x, y]
                r2, g2, b2, a2 = px[x + 1, y]
                r3, g3, b3, a3 = px[x, y + 1]
                diff = abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
                diff += abs(r1 - r3) + abs(g1 - g3) + abs(b1 - b3)
                val = 255 if diff > 120 else 0
                new_px[x, y] = (val, val, val, 255)
        return out
