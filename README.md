# xml-converters

This repository contains Python scripts to convert various formats to the [XML format used in OPUS](http://opus.nlpl.eu/).

## Generic

### treetagger2opus.py

Converts tab-separated output from [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) to the OPUS format.

### opus2conll.py

Converts the OPUS format to CONLL. 

### conll2opus.py

Converts CONLL to the OPUS format. 

### swda2opus.py

Converts SWDA to the OPUS format.

## Language specific

### br.py (Breton)

Converts output from [a morphological analyzer of Breton by Francis Tyers](http://xixona.dlsi.ua.es/~fran/breton/) to the OPUS format.

### he.py (Hebrew)

Converts output from [the MILA Tagging Request Service](http://yeda.cs.technion.ac.il:8088/fileuploader/)  to the OPUS format.

### pl.py (Polish)

Converts output from [the Morpheusz tagger](http://ws.clarin-pl.eu/tager.shtml?en) to the OPUS format.

### zh.py (Mandarin Chinese)

Converts output from the [Stanford CoreNLP Log-linear Part-of-Speech tagger](https://nlp.stanford.edu/software/tagger.shtml) to the OPUS format.

## Other scripts

The repository also contains some other scripts.

### remove_enters.py

Strips new lines from a file.
