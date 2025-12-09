import numpy as np
from app.domain.filter import Filter


class Filter_median(Filter):
    def apply(self, img: np.ndarray, size: int = 3, **kwargs) -> np.ndarray:
        gray = self.ensure_gray(img)
        height, width = gray.shape
        output = np.zeros((height, width), dtype=np.uint8)

        # pega modo de borda (border) dos parametros
        border_mode = str(kwargs.get("border", "replicate")).lower()

        # ajusta tamanho da mascara
        if size < 1:
            size = 1
        if size % 2 == 0:
            size += 1

        radius = size // 2  # raio da mascara

        for y in range(height):      # linha
            for x in range(width):   # coluna

                neighbors: list[int] = []

                # percorre vizinhanca
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        neighbor_y = y + dy
                        neighbor_x = x + dx

                        # dentro da imagem
                        if 0 <= neighbor_y < height and 0 <= neighbor_x < width:
                            neighbors.append(int(gray[neighbor_y, neighbor_x]))
                        else:
                            # tratamento de borda
                            if border_mode == "zero":
                                # contribui como 0
                                neighbors.append(0)
                            else:
                                # replicate (padrao)
                                clamped_y = min(max(neighbor_y, 0), height - 1)
                                clamped_x = min(max(neighbor_x, 0), width - 1)
                                neighbors.append(int(gray[clamped_y, clamped_x]))

                # ordena e pega mediana
                neighbors.sort()
                mid_index = len(neighbors) // 2
                output[y, x] = neighbors[mid_index]

        return output
