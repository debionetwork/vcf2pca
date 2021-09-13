import ipyrad
import ipyrad.analysis as ipa

vcffile = "anolis.vcf"
# Create the pca object
# `quiet=True` indicates we don't care about the details, at this point
pca = ipa.pca(data=vcffile)
pca.run()
img = pca.draw()
# print(img)

import toyplot.png
toyplot.png.render(img[0], "anolis.png")