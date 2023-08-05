def doOverlap(rectangle1, rectangle2):
    if (
        rectangle1['x'] + rectangle1['w'] <= rectangle2['x'] or
        rectangle1['y'] + rectangle1['h'] <= rectangle2['y'] or
        rectangle2['x'] + rectangle2['w'] <= rectangle1['x'] or
        rectangle2['y'] + rectangle2['h'] <= rectangle1['y']
    ):
        return False

    return True

def getAllOverlaps(basicRectangle, rectangles):
    overlaps = list(map(lambda rectangle: doOverlap(basicRectangle, rectangle), rectangles))
    return [index for index, overlap in enumerate(overlaps) if overlap]
