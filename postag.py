import sys
import operator


class pclassify:
    weights={}
    labels={}

    def __init__(self,fname):
        f=open(fname,'r')
        lline=f.readline().rstrip().split(' ')
	#print lline
        for l in lline:
            val=l.split('\t')
            self.labels[val[0]]=int(val[1])
            self.weights[val[0]]={}
        for l in f:
            param=l.split()
            self.weights[param[0]][param[1]]=float(param[2])
        f.close()
        #print self.labels

    def predict(self,features,fx):
        wi={}
        for l in self.labels:
            wi[l]=0.0
        for feature in fx:
            for l in self.labels:
                if self.weights[l].has_key(feature)==False:
                    continue
                wi[l]+=self.weights[l][feature]*fx[feature]
        zlabel=max(wi.iteritems(), key=operator.itemgetter(1))[0]
        return zlabel
    
    def classify(self,tfile):
        fl=open(tfile,'r')
        for line in fl:
            features=line.split()
            fx={}
            for feature in features:
                if fx.has_key(feature)==False:
                    fx[feature]=1
                else:
                    fx[feature]+=1
            zlabel=self.predict(features,fx)
            print zlabel
        fl.close()
        
    def classify_line(self,line):
        features=line.split()
        fx={}
        for feature in features:
            if fx.has_key(feature)==False:
                fx[feature]=1
            else:
                fx[feature]+=1
        zlabel=self.predict(features,fx)
        return zlabel


class postag:
    pc=object 
    def __init__(self,fname):
	self.pc=pclassify(fname)

    def classify(self):
        
        f=sys.stdin
        for line in f:
            words=line.split()
            pword='BOS' #previous word
	    ppword='BNULL' #previous previous word
	    ptag='BOS' #previous tag
	    pptag='BNULL' #previous of previous tag
            nword='EOS' #next word
	    nnword='ENULL' #next next word
	    sufpw=None #suffix of previous word
	    sufnw=None #suffix of next word
            outline=''
            for i in range(len(words)):
                word=words[i]
                #print word+" "+tag
                if i+1>=len(words):
                    nword='EOS'
		    sufnw=None
		    nnword='ENULL'
                else:
		    if i+2>=len(words):
			nnword='EOS'
		    else:
			nnword=words[i+2].split('/')[0]
                    nword=words[i+1].split('/')[0]
		    sufnw=nword[-3:]
		sufw=word[-3:]
		ssufw=word[-2:] #two character suffix
		prefix=word[0]
                feature="pw:"+str(pword)+" w:"+str(word)+" nw:"+str(nword)+" sufpw:"+str(sufpw)+" sufnw:"+str(sufnw)+" sufw:"+str(sufw)+" prefix:"+str(prefix)+" ptag:"+str(ptag)+" pptag:"+str(pptag)+" ssufw:"+str(ssufw)
                label=self.pc.classify_line(feature)
		ppword=pword
                pword=word
		sufpw=pword[-3:]
		pptag=ptag
		ptag=label
                outline=outline+word+'/'+label+' '
	    print outline
            #sys.stdout.write(outline+'\n') 
        f.close()
        
mod_file=sys.argv[1]
pt=postag(mod_file)
pt.classify()
