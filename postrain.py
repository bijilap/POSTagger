import sys
import subprocess

class postrain:
    feature_set={}
    features_fname='pos.in'
    model_fname="pos.model"
    
    def __init__(self,mname):
        self.model_fname=mname
        
        
    def read_training_file(self,fname):
        f=open(fname,'r')
        fout=open(self.features_fname,'w')
        for line in f:
            #print line
            pword='BOS' #previous word
	    ppword='BNULL' #previous previous word
	    ptag='BOS' #previous tag
	    pptag='BNULL' #previous of previous tag
            nword='EOS' #next word
	    nnword='ENULL' #next next word
	    sufpw=None #suffix of previous word
	    sufnw=None #suffix of next word
            words_tags=line.split()
            for i in range(len(words_tags)):
                (word,tag)=words_tags[i].split('/')
                #print word+" "+tag
                if i+1>=len(words_tags):
                    nword='EOS'
		    sufnw=None
		    nnword='ENULL'
		    
                else:
		    if i+2>=len(words_tags):
			nnword='EOS'
		    else:
			nnword=words_tags[i+2].split('/')[0]
                    nword=words_tags[i+1].split('/')[0]
		    sufnw=nword[-3:]
		sufw=word[-3:]
		ssufw=word[-2:] #two character suffix
		prefix=word[0]
                feature=tag+" "+"pw:"+str(pword)+" w:"+str(word)+" nw:"+str(nword)+" sufpw:"+str(sufpw)+" sufnw:"+str(sufnw)+" sufw:"+str(sufw)+" prefix:"+str(prefix)+" ptag:"+str(ptag)+" pptag:"+str(pptag)+" ssufw:"+str(ssufw)+'\n'
		ppword=pword                
		pword=word
		sufpw=pword[-3:]
		pptag=ptag
		ptag=tag
                fout.write(feature)
                #print feature
        f.close()
        fout.close
        
    def plearn(self):
        subprocess.call('python ./perceplearn.py '+self.features_fname+' '+self.model_fname,shell=True)

fname=sys.argv[1]
mname=sys.argv[2]
pobj=postrain(mname)
pobj.read_training_file(fname)
pobj.plearn()
pobj.read_training_file(fname)
