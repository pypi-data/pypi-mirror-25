import pysam, multiprocessing, sys

def p(pipeR, pipeW):
    pipeW.close()
    c = pysam.AlignmentFile(pipeR.fileno(),
                            duplicate_filehandle=False)
    for r in c.fetch(until_eof=True):
        print(str(r))
    c.close()
    
pipeR, pipeW = multiprocessing.Pipe(False)
a = pysam.AlignmentFile('ex3.bam')
b = pysam.AlignmentFile(pipeW.fileno(), 'wbu', template=a, duplicate_filehandle=False)

proc = multiprocessing.Process(target=p, args=(pipeR, pipeW))
proc.start()
for r in a:
    b.write(r)

a.close()
b.close()
proc.join()

