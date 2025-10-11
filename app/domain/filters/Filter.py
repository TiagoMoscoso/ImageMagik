class Filter:
    def apply(self, image, coordinates, arguments):
        raise NotImplementedError("Subclasses must implement the apply method")