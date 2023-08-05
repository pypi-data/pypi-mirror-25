
from io import BytesIO
from PIL import Image
import numpy as np
import base64

def raw_base64_to_np_array(raw):
    return np.asarray(Image.open(BytesIO(base64.b64decode(raw))))
