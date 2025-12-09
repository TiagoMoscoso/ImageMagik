from typing import Dict
import numpy as np

from app.domain.filters.filterbrightness import Filter_brightness
from app.domain.filters.filtercontrast import Filter_contrast
from app.domain.filters.filterinvert import Filter_invert
from app.domain.filters.filterkernel import Filter_kernel
from app.domain.filters.filterthreshold import Filter_threshold
from app.domain.filters.filtermean import Filter_mean
from app.domain.filters.filtermedian import Filter_median
from app.domain.filters.filterlaplacian import Filter_laplacian
from app.domain.filters.filtermask import Filter_mask
from app.domain.filterspec import FilterSpec
from app.domain.filters.filterhistogram import Filter_histogram
from app.domain.filters.filterdifference import Filter_difference
from app.domain.imageconverter import parse_kernel
from app.domain.paramspec import ParamSpec

filter_invert = Filter_invert()
filter_brightness = Filter_brightness()
filter_contrast = Filter_contrast()
filter_kernel = Filter_kernel()
filter_threshold = Filter_threshold()
filter_mean = Filter_mean()
filter_median = Filter_median()
filter_laplacian = Filter_laplacian()
filter_mask = Filter_mask()
filter_histogram = Filter_histogram()
filter_difference = Filter_difference()
#REGRA CRIA UMA CLASSE FILTER_NOME_DO_FILTRO QUE HERDA OBRIGATORIAMENTE DE FILTER, adicionar nesse dicionario e ja vai direto pra ui

FILTERS: Dict[str, FilterSpec] = {
    "Inverter": FilterSpec("Inverter", [], filter_invert.apply),

    "Brilho": FilterSpec("Brilho", [
        ParamSpec("offset", "int", 0, -255, 255, 5)
    ], filter_brightness.apply),


    "Contraste": FilterSpec("Contraste", [
        ParamSpec("factor", "float", 1.2, 0.1, 5.0, 0.05)
    ], filter_contrast.apply),

    "Limiarização": FilterSpec("Limiarização", [
        ParamSpec("threshold", "int", 128, 0, 255, 1)
    ], filter_threshold.apply),

    "Média": FilterSpec("Média", [
        ParamSpec("size", "int", 3, 1, 15, 2)
    ], filter_mean.apply),

    "Mediana": FilterSpec("Mediana", [
        ParamSpec("size", "int", 3, 1, 15, 2),
        ParamSpec("border", "select", "replicate", options=["replicate", "zero"])
    ], filter_median.apply),

    "Laplaciano": FilterSpec("Laplaciano", [], filter_laplacian.apply),

    "Máscara": FilterSpec("Máscara", [
        ParamSpec("mask", "image", 0),
    ], filter_mask.apply),

    "Kernel customizado": FilterSpec("Custom Kernel", [
        ParamSpec("rows", "int", 3, 1, 15, 1),
        ParamSpec("cols", "int", 3, 1, 15, 1),
        ParamSpec("weights", "text", "0 -1 0\n-1 5 -1\n0 -1 0")
    ], lambda img, **kw: filter_kernel.apply(img, kernel=parse_kernel(kw))),

    "Histograma": FilterSpec("Histograma", [], filter_histogram.apply),

    "Diff": FilterSpec("Diff", [
        ParamSpec("other", "image", 0),
    ], filter_difference.apply)
}


