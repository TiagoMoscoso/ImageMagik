from .Filter import (
    Filter, GrayFilter, BlurFilter,
    InvertFilter, BrightnessFilter, ContrastFilter,
    SepiaFilter, ThresholdFilter, PixelateFilter, EdgeFilter
)

FILTERS = {cls.key: cls() for cls in (
    GrayFilter, BlurFilter, InvertFilter,
    BrightnessFilter, ContrastFilter,
    SepiaFilter, ThresholdFilter, PixelateFilter, EdgeFilter
)}

FILTERS_LIST = [{"key": f.key, "name": f.name} for f in FILTERS.values()]
