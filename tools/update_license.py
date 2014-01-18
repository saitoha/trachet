#!/usr/bin/env python

import sys
import re

template_file = 'tools/licenseblock.txt'
pattern = re.compile('\n?(.*)(\\*\\*\\*\\*\\* BEGIN LICENSE BLOCK \\*\\*\\*\\*\\*)(?:.*\n)*\\1(\\*\\*\\*\\*\\* END LICENSE BLOCK \\*\\*\\*\\*\\*)', re.MULTILINE)

for filename in sys.argv[1:]:
    f = open(filename)
    try:
        content = f.read()
        m = re.search(pattern, content)
        if m:
            sep = m.group(1)
            copying = sep + sep.join(open(template_file).readlines())
            content = re.sub(pattern, "\n\\1\\2\n%s\\1\\3" % copying, content, re.MULTILINE)
            out = open(filename, "w")
            try:
                out.write(content)
            finally:
                out.close()
    finally:
        f.close()
