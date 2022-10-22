def getNameAndSeq(e):
    name, seq = e.split("\n", 1)
    return (name.strip(), seq.replace("\n", "").strip())

def parseFasta(fasta):
    return [getNameAndSeq(e) for e in fasta.read().split(">")[1:]]

def parseFastq(fastq):
    lines = fastq.readlines()
    return [(name.replace("\n", "").replace("@", "", 1), seq.replace("\n", "")) for name, seq in zip(lines[0:len(lines):2], lines[1:len(lines):2])]
