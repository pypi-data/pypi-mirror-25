import vcf

class vcfparser( object ):
	def __init__( self , **kwargs ):
		filename = kwargs.get( 'filename' , "" )
		header = kwargs.get( 'header' , [] )
		info = kwargs.get( 'info' , {} )

	def open( self , rw = "r" ):
        inFile = None
        if ( re.match( "\.gz" , self.filename ) ):
            inFile = vcf.Reader( open( self.filename , 'r' ) , compressed=True )
        else:
            inFile = vcf.Reader( open( inputFile , 'r' ) )
		return inFile

	def read( self , **kwargs ):
        """ read & parse input .vcf
            Look for VEP CSQ info field & extract all information possible
            Can get allele frequency & clinical annotations after VEP v81 (or so)
            http://useast.ensembl.org/info/docs/tools/vep/vep_formats.html#output
        """
		inFile = self.open( rw = "r" )
        appendTo = kwargs.get( "appendTo" , "user" )
        thresholdAF = kwargs.get( "thresholdAF" , 1 )
        anyFilter = kwargs.get( "anyFilter" , False )
        preVEP = []
        vepDone = False
        exacDone = False
        clinvarDone = False
        vepInfo = OD()
        self.vcfHeaderInfo = []
        metadata = inFile.metadata
        #print( str( metadata ) )
        failedFilter = 0
        failedAF = 0
        [ vepDone , exacDone , clinvarDone ] = self.readMetaData( metadata , inFile.infos , vepInfo )
        for record in inFile:
            chrom = record.CHROM
            reference = record.REF
            alternates = record.ALT
            if anyFilter and record.FILTER != "PASS":
                failedFilter += 1
                continue
            start = record.start + 1 #1-base beginning of ref
            stop = record.end #0-base ending of ref
            info = record.INFO
            alti = -1
            for alternate in alternates:
                alti += 1
                alt = str( alternate )
                if alt == "None":
                    alt = None
                if record.is_indel and not record.is_deletion: #insertion
                    reference = "-"
                    alt = alt[1:len(alt)]
                    stop = stop + 1
                elif record.is_deletion:
                    reference = reference[1:len(reference)] #assumes only one base overlap
                    alt = "-"
                    start = start + 1
                    stop = stop

                parentVar = mafvariant( \
                    chromosome = chrom , \
                    start = start , \
                    stop = stop , \
                    dbsnp = record.ID , \
                    reference = reference , \
                    alternate = alt , \
                )

                var = chargervariant( \
                    parentVariant=parentVar
                )

                #hasAF = False
                #[ hasAF , skip ] = self.getAF( info , var , thresholdAF , alti )
                #print( str( var.alleleFrequency ) )
                #if skip:
                #   continue
#               hasClinVar = False
#               ClinVarElsewhere = info.get( 'clinvar_measureset_id' , 0 )
#               var.clinvarVariant.clinical["description"] = info.get( 'clinvar_measureset_id' , "noClinVar" )
#               var.clinvarVariant.uid = info.get( 'clinvar_measureset_id' , "noClinVar" )
#               if ClinVarElsewhere != 0:
                hasAF = False
                self.getVEPConsequences( info , var , preVEP , hasAF )
                if self.skipIfHighAF( var , thresholdAF ):
                    failedAF += 1
                    continue

                self.appendToList( appendTo , var )
        totalVars = len( self.userVariants ) + failedFilter + failedAF
        print(  "Skipping: " + str( failedFilter ) + \
                " for filters and " + str( failedAF ) + " for AF of " + \
                str( totalVars ) )
        return [ vepDone , preVEP , exacDone , clinvarDone ]

