from glyphNameFormatter import GlyphName, __version__

from glyphNameFormatter.unicodeRangeNames import getAllRangeNames, getRangeByName, rangeNameToModuleName

import importlib
import time

import subprocess
import pkg_resources



def getExportVersionNumber():
    commitNumber = subprocess.check_output(["git", "rev-list", "HEAD", "--count"])
    __version__
    return "%s - git commit: %s" % (__version__, commitNumber)


def generateFlat(path, onlySupported=True):
    data = [
        "# glyph name formatted unicode list aka GNFUL",
        "# GlyphNameFormatter version %s" % getExportVersionNumber(),
        "# generated on %s" % time.strftime("%Y %m %d %H:%M:%S"),
        "# format",
        "# <glyphName> <hex unicode>"
    ]
    for rangeName in getAllRangeNames():
        if onlySupported:
            moduleName = rangeNameToModuleName(rangeName)
            try:
                module = importlib.import_module('glyphNameFormatter.rangeProcessors.%s' % moduleName)
            except:
                continue
        data.append("# %s" % rangeName)
        for u in range(*getRangeByName(rangeName)):
            g = GlyphName(uniNumber=u)
            name = g.getName(extension=True)
            if name is None:
                continue
            data.append("%s %04X" % (name, u))

    f = open(path, "w")
    f.write("\n".join(data))
    f.close()

if __name__ == "__main__":
    generateFlat(path="./../names/glyphNamesToUnicode.txt")
