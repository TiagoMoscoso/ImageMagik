import numpy as np


def apply_kernel_mean(k_length, k_offset, kernel, matrix, x, y):
    sum = 0
    for ky in range(0, k_length):
        for kx in range(0, k_length):
            try:
                kernel_weight = kernel[ky][kx]
                sum += (matrix[y+ky-k_offset][x+kx-k_offset] * kernel_weight)
            except Exception: #caso pegue um valor fora do range da matriz de pixels
                sum += 0 #estratégia de utilizar zero padding
                
            #ex em uma matrix 3x3
            # 1 it:
            #soma += matrix[y-1][x-1] + matrix[y-1][x] + matrix[y-1][x+1]

            # 2 it:
            # soma += matrix[y][x-1] + matrix[y][x] + matrix[y][x+1]

            #3 it:
            # soma += matrix[y+1][x-1] + matrix[y+1][x] + matrix[y+1][x+1]
    avarage_value = int (sum / (k_length * k_length))
    return max(0, min(255, int(avarage_value)))#valor normalizado entre 0 e 255
            

class Filter_Avarage():
    def apply(self, img, kernel):

        output_img = np.copy(img)
        
        height = len(img)
        width = len(img[0])

        kernel_length = len(kernel)

        #aplica offset do kernel, para saber até onde irá os filtros do kernel
        kernel_offset = kernel_length // 2 

        for y in range(0, height):
            for x in range(0, width):
                output_img[y][x] = apply_kernel_mean(kernel_length, kernel_offset, kernel, img, x, y)

        return output_img


                        

        