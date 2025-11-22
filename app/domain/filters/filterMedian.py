import numpy as np

#o peso do kernel não é aplicado em mediana
def apply_kernel_median(k_length, k_offset, matrix, x, y):
    neighbors = []
    for ky in range(0, k_length):
        for kx in range(0, k_length):
            try:
                neighbors.append(matrix[y+ky-k_offset][x+kx-k_offset])
            except Exception: #caso pegue um valor fora do range da matriz de pixels
                neighbors.append(0) #estratégia de utilizar zero padding
                
    neighbors.sort()
    mid_term = len(neighbors) // 2
    median_value = neighbors[mid_term]
    return max(0, min(255, int(median_value)))#valor normalizado entre 0 e 255
            

class Filter_Median():
    def apply(self, img, kernel):

        output_img = np.copy(img)
        
        height = len(img)
        width = len(img[0])

        kernel_length = len(kernel)

        #aplica offset do kernel, para saber até onde irá os filtros do kernel
        kernel_offset = kernel_length // 2 

        for y in range(0, height):
            for x in range(0, width):
                output_img[y][x] = apply_kernel_median(kernel_length, kernel_offset, img, x, y)

        return output_img


                        

        