genomefile="data/Ptr_genome.fasta"
align="data/Gremlin_TIR_aln.fasta"
outDir="test_outdir"
tempDir="temp_test"
modelName = "Gremlin_hmm"

genome = importFasta(genomefile)

stckhlmFile = convertAlign(alnFile=align,inFormat='fasta',tempDir=tempDir)


cmds = list()
hmmbuildCmd,modelPath = _hmmbuild_command(modelname=modelName,cores=4,inAlign=stckhlmFile,outdir=tempDir)
hmmPressCmd = _hmmpress_command(exePath="hmmpress", hmmfile=modelPath)
#Note: use genome file
nhmmerCmd,resultDir = _nhmmer_command(exePath="nhmmer",nobias=False,matrix=None,modelPath=modelPath,genome=genomefile,evalue=0.001,cores=4,outdir=tempDir)
cmds.append(hmmbuildCmd)
cmds.append(hmmPressCmd)
cmds.append(nhmmerCmd)
run_cmd(cmds,verbose=True)

nhmmer_result_dir = os.path.join(os.path.abspath(resultDir),'*.tab')

hitTable = None
for resultfile in glob.glob(nhmmer_result_dir):
	hitTable = import_nhmmer(infile=resultfile,hitTable=hitTable)

###
hitsDict,hitIndex = table2dict(hitTable)

hitIndex = parseHits(hitsDict=hitsDict, hitIndex=hitIndex, maxDist=16000)

hitIndex,paired,unpaired = iterateGetPairs(hitIndex, stableReps=1)


writeTIRs(outDir=outDir, hitTable=hitTable, mineval=0.001, genome=genome)


TIRelements = fetchElements(paired=paired, hitIndex=hitIndex, genome=genome)

writeElements(outDir, eleDict=TIRelements)

orphans = fetchUnpaired(hitIndex=hitIndex)


gffWrite(featureList=TIRelements, writeTIRs=True, unpaired=orphans)





