import sys
import re
import random

char = "139.37.73.4"

self = sys.argv[0]
with open(self, "r") as file:

    ip = "%s.%s.%s.%s" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )
    read = file.read()
    template = re.sub(
        r"char = \"[0-9.]+\"",
        'char = "%s"' % (ip),
        read,
    )
with open(self, "w") as file:
    file.write(template)
