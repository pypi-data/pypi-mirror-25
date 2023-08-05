def doOverlap(rectangle1, rectangle2):
    if (
        rectangle1['x'] + rectangle1['w'] <= rectangle2['x'] or
        rectangle1['y'] + rectangle1['h'] <= rectangle2['y'] or
        rectangle2['x'] + rectangle2['w'] <= rectangle1['x'] or
        rectangle2['y'] + rectangle2['h'] <= rectangle1['y']
    ):
        return False

    return True

def getOverlapRectangles(basicRectangle, rectangles):
    overlaps = list(map(lambda rectangle: doOverlap(basicRectangle, rectangle), rectangles))
    return [index for index, overlap in enumerate(overlaps) if overlap]

def findAllOverlaps(rectangles):
    allOverlaps = []
    for index, rectangle in enumerate(rectangles):
        if ((index + 1) != len(rectangles)):
            overlaps = [x + index + 1 for x in getOverlapRectangles(rectangle, rectangles[index + 1:])]
            if(len(overlaps) > 0):
                allOverlaps.extend([index] + overlaps)

    return list(set(allOverlaps))
