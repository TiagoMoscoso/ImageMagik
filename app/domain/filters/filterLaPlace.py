import numpy as np

def generate_laplacian_kernel(size: int):
    if size % 2 == 0:
        raise ValueError("O tamanho do kernel deve ser ímpar.")

    kernel = np.full((size, size), -1, dtype=float)
    center = size // 2
    kernel[center, center] = (size * size) - 1
    return kernel

def apply_kernel_laplacian(matrix, x, y, kernel, k_offset):
    height = len(matrix)
    width = len(matrix[0])
    k_size = len(kernel)

    value = 0

    for ky in range(k_size):
        for kx in range(k_size):
            ny = y + ky - k_offset
            nx = x + kx - k_offset

            # zero padding
            if 0 <= ny < height and 0 <= nx < width:
                pixel = matrix[ny][nx]
            else:
                pixel = 0

            value += kernel[ky][kx] * pixel

    # normaliza para 0–255
    return max(0, min(255, int(value)))


class Filter_Laplacian:
    def apply(self, img, kernel_size):
        # kernel Laplaciano (N conexões conexões)
        kernel = generate_laplacian_kernel(kernel_size)

        k_size = len(kernel)
        k_offset = k_size // 2

        height = len(img)
        width = len(img[0])

        output_img = np.zeros_like(img)

        for y in range(height):
            for x in range(width):
                output_img[y][x] = apply_kernel_laplacian(
                    img, x, y, kernel, k_offset
                )

        return output_img


