from SimpleCV import Blob

# SimpleCV classifies blobs on a per blob basis
# This is a simple function that takes a list of blobs and classifies them all
# Returning a dictionary with the index of the blob with the value as the classification
# To use the return type, you would do:
# Blob #3
# data[2] returns say, 'Rectangle'
# Then you would go back to the blobs list you put into this function and call the respective index
# blobs[2] = Blob Object, data[2] = 'Rectangle'

def classify(blobs, tolerance):

    data = {}

    for index, blob in enumerate(blobs):

        if blob.isRectangle(tolerance):
            data[index] = 'Rectangle'

        elif blob.isCircle(tolerance):
            data[index] = 'Circle'

        # If blob cannot be classified as either with specified tolerance
        else:
            data[index] = None

    return data