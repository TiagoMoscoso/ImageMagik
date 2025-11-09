from typing import Dict

import numpy as np

from app.domain.filters.filterbrightness import Filter_brightness
from app.domain.filters.filtercontrast import Filter_contrast
from app.domain.filters.filtergrayscale import Filter_grayscale
from app.domain.filters.filterinvert import Filter_invert
from app.domain.filters.filterkernel import Filter_kernel
from app.domain.filterspec import FilterSpec
from app.domain.imageconverter import parse_kernel
from app.domain.paramspec import ParamSpec


filter_invert = Filter_invert()
filter_grayscale = Filter_grayscale()
filter_brightness = Filter_brightness()
filter_contrast = Filter_contrast()
filter_kernel = Filter_kernel()
#REGRA CRIA UMA CLASSE FILTER_NOME_DO_FILTRO QUE HERDA OBRIGATORIAMENTE DE FILTER, adicionar nesse dicionario e ja vai direto pra ui

FILTERS: Dict[str, FilterSpec] = {
    "Invert": FilterSpec("Invert", [], filter_invert.apply),
    "Grayscale": FilterSpec("Grayscale", [], filter_grayscale.apply),
    "Brightness": FilterSpec("Brightness", [
        ParamSpec("factor", "float", 1.2, 0.1, 5.0, 0.05)
    ], filter_brightness.apply),
    "Contrast": FilterSpec("Contrast", [
        ParamSpec("factor", "float", 1.2, 0.1, 5.0, 0.05)
    ], filter_contrast.apply),
    "Custom Kernel": FilterSpec("Custom Kernel", [
        ParamSpec("rows", "int", 3, 1, 15, 1),
        ParamSpec("cols", "int", 3, 1, 15, 1),
        ParamSpec("weights", "text", "0 -1 0\n-1 5 -1\n0 -1 0")
    ], lambda img, **kw: filter_kernel.apply(img, kernel=parse_kernel(kw)))
}

