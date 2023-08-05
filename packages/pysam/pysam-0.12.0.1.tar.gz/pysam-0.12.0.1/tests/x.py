import pysam

inf = pysam.AlignmentFile("-", "rb")
outf = pysam.AlignmentFile("-", "wb")

for read in inf:
    outf.write(read)

inf.close()
outf.close()
