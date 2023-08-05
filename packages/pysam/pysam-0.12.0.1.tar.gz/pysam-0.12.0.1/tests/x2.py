

import pysam, multiprocessing, sys

def p(pipeR):
    c = pysam.AlignmentFile(pipeR.fileno(), duplicate_filehandle=False)
    print(c.fileno())
    print(pipeR.fileno())
    d = pysam.AlignmentFile(sys.stdout, 'w', template=c, duplicate_filehandle=False)
    print(d.fileno())
    for r in c.fetch(until_eof=True): d.write(r)
    c.close()
    d.close()

a = pysam.AlignmentFile('ex3.bam')
pipeR, pipeW = multiprocessing.Pipe(False)
print("pipeR", pipeR.fileno())
print("pipeW", pipeW.fileno())
b = pysam.AlignmentFile(pipeW.fileno(), 'wbu', template=a)
print("b", b.fileno())

proc = multiprocessing.Process(target=p, args=(pipeR,))
proc.start()

for r in a: b.write(r)
a.close()
b.close()
pipeW.close()

#proc = multiprocessing.Process(target=p, args=(pipeR,))
#proc.start()
proc.join()

