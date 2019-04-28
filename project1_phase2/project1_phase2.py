import glob
import io
import os
import pdb
import sys
import re
import random
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk import ne_chunk
from collections import Counter
from string import punctuation
from sklearn.ensemble import RandomForestClassifier
nltk.download('stopwords')

def get_entity(text):
    """Prints the entity inside of the text."""
    names = []
    for sent in sent_tokenize(text):
        for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                #print(chunk.label(), ' '.join(c[0] for c in chunk.leaves()))
                #print(' '.join(c[0] for c in chunk.leaves()))
                names.append(' '.join(c[0] for c in chunk.leaves()))

    return names



def readFile(filename):

    # Load in a text file
    file = open(filename,'r')
    text_file = file.read()
    entity = get_entity(text_file)
    return entity,text_file


def read_textfiles_from_directory(directory, file_regexp, count_of_files_to_extract):

    files = sorted(os.listdir(directory))
    files1=files[-count_of_files_to_extract:] #500
    file_name = [f for f in files1 if re.search(file_regexp, f) ]

    # Construct a list of text from those that match the regexp
    list_of_textfiles = [readFile(directory + "/" + f)[1] for f in files1 if re.search(file_regexp, f) ]

    entities= [readFile(directory + "/" + f)[0] for f in files1 if re.search(file_regexp, f) ]

    return (file_name,entities,list_of_textfiles)



def redaction(file,lists):
    text=file
    #print("type :",type())
    j=0
    #Frequency_of_fields = [len(names(text)),len(getlocation(text)),len(date(text)),len(number(text)),len(genders(text)),len(address(text)),len(concepts(text,concept)])
    found=''
    for i in range(len(lists)):
        if(text.find(lists[i])>0):
            ## count of redaccted files
            j=j+1
        if(j==1):
            found = lists[i]
            lists1 = lists[i].split()
#            print("i:",lists1)
            if(len(lists1)>1):
                text = re.sub(lists[i],u'\u2588'*len(lists1[0])+' '+u'\u2588'*len(lists1[1]),text)

            else:
                #print("else")
                text = re.sub(lists[i],u'\u2588'*len(lists[i]),text)
            break;
    #print(text)
    return text,found


def Removing_uneccesary(files):

    Space = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    files = [Space.sub(" ", line) for line in files]
    return files


def Train_and_test_cases(filenames,entities,files,split,count_of_files_to_extract):
    #i recommend creating the solution as a list

    if(split<1):
        split=100*split;

    filenames_train=[]
    entities_train=[]
    files_train=[]
    train=[]

    filenames_test=[]
    entities_test=[]
    files_test=[]
    test=[]

    for i in range(0,count_of_files_to_extract):
        j = random.uniform(0,100)
        if j < split:

            filenames_train.append(filenames[i])
            entities_train.append(entities[i])
            files_train.append(files[i])

        else:

            filenames_test.append(filenames[i])
            entities_test.append(entities[i])
            files_test.append(files[i])

    train.append(filenames_train)
    train.append(entities_train)
    train.append(files_train)

    test.append(filenames_test)
    test.append(entities_test)
    test.append(files_test)

    return train, test


def cleaning_TrainingSet(filenames,entities,files):  
    ## Removing the files that donot have any names
    #entity_of_redated_files[0]
    labels=[None]*len(files)
    #labels=[]
    #print(len(labels),"Files",len(files),"Entities",len(entities))

    count=0
    for i in range(len(entities)): 
        if(count < len(entities)):
            if(len(entities[count])==0) :
                #print("i",count)
                filenames.pop(count)
                entities.pop(count)
                files.pop(count)
                
                labels.pop(count)
            count=count+1

    
    ## Labeling names as one name per document one that has most frequent assumption: the most frequent name will be on the one that is denoting the document
    for i in range(len(entities)):
        Counter1 = Counter(entities[i]) 
        most_occur = Counter1.most_common(1) 
        if len(most_occur) >0:
            if most_occur[0][1] > 1:
                labels[i]=most_occur[0][0] 

    ## considering the names that are most frequent in other documents

    collect_labels=[]            
    for i in range(len(entities)):
        #print("lable",len(labels))
        if labels[i] != None :
            collect_labels.append(labels[i])

    for i in range(len(entities)): 
       # print("lable",len(labels))
        if labels[i] == None :
            for j in range(len(collect_labels)):
                most_occur=Counter(entities[i]+[collect_labels[j]]).most_common(1)
                if len(most_occur) > 0:
                    if most_occur[0][1] > 1:
                        labels[i]=collect_labels[j]

    # Considering only the ones that have names in it after cleaning
    index_none=[]
    for i in range(len(labels)):
        if labels[i]==None:
            index_none.append(i)
    #print(len(index_none))

    count=0
    for i in range(len(labels)):
        if len(index_none)>count:
            if i==index_none[count]:
                filenames.pop(i-count)
                entities.pop(i-count)
                files.pop(i-count)
                #entity_of_redated_files.pop(i-count)
                labels.pop(i-count)
                count=count+1
    print("Final No. of Files : ",len(files))
    return filenames,entities,files,labels

def redacted_of_files(test_files,train_labels):
    redacted_file=[]
    labels=[]

    for i in range(len(test_files)):
        redacted = redaction(test_files[i],train_labels)
        if(len(redacted[1])>0):
            redacted_file.append(redacted[0])
            labels.append(redacted[1])
            #print("count Of redated :",Count_of_redacted_words[len(Count_of_redacted_words)-1])
            #print("redacted",redacted[0])
    return redacted_file,labels


def Feature_selection(redacted_file_train,freqnt_words):
    ##Feature selection
    Feature_dict=[]
    #Feature-1:Total number of redacted words in the text
    #tot_redacted_words=len(train_labels)
    #print(tot_redacted_words)


    for i in range(len(redacted_file_train)):

        Each_Feature = []
        #Number of words in the document
        Number_of_words = len(re.findall("[a-zA-Z_]+", redacted_file_train[i]))
        Each_Feature.append(Number_of_words)

        #redacted word length
        redacted_word_len = len(re.search(u"[\u2588]+ ?[\u2588]+", redacted_file_train[i]).group())
        Each_Feature.append(redacted_word_len)

        #Number of redacted names in the file
        Number_of_redaction = len(re.findall(u"[\u2588]+ ?[\u2588]+", redacted_file_train[i]))
        Each_Feature.append(Number_of_redaction)

        #Number of total Names present in the document
        Names_per_file = len(get_entity(redacted_file_train[i]))
        Each_Feature.append(Names_per_file)

        #Space present between redacted words
        if(re.search(u"([\u2588]+)( )?([\u2588]+)", redacted_file_train[i]).group(2)!=None):
            Space_in_names = 1
            Each_Feature.append(Space_in_names)
            # first words length
            Each_Feature.append(len(re.search(u"([\u2588]+)( )?([\u2588]+)", redacted_file_train[i]).group(1)))
            #second words length
            Each_Feature.append(len(re.search(u"([\u2588]+)( )?([\u2588]+)", redacted_file_train[i]).group(3)))

        else:
            #if no space is present everything else is 0 as default
            Space_in_names = 0
            Each_Feature.append(Space_in_names)
            Each_Feature.append(0)
            Each_Feature.append(0)


#         for j in range(len(freqnt_words)):
#             #print("Frequent Words : ",j," : ",freqnt_words[j])
#             Number_reqWords = len(re.findall(freqnt_words[j], redacted_file_train[i]))
#             Each_Feature.append(Number_reqWords)

        #if it has opostopy s " 's "
        Names_having_optspy_s = len(re.findall(u"[\u2588]+\'s", redacted_file_train[i]))
        Each_Feature.append(Names_having_optspy_s)

        #append everything together as one feature
        Feature_dict.append(Each_Feature)

    return Feature_dict

def total_predicted_correct(y_pred,test_labels):
    count = 0
    for i in range(len(test_labels)):
        if(y_pred[i]==test_labels[i]):
            count=count+1
    return count


def ModelConstruction(redacted_file_train,redacted_file_test,train_labels,test_labels):

    freqnt_words = Frequent_words(redacted_file_train)
    freqnt_words = Removing_uneccesary_braces(freqnt_words)

    X_train = Feature_selection(redacted_file_train,freqnt_words)
    X_test = Feature_selection(redacted_file_test,freqnt_words)
    Y_train = train_labels
    Y_test = test_labels

    classifier = RandomForestClassifier(n_estimators = 200, criterion = 'entropy',max_features=8, max_leaf_nodes=20,min_samples_split=10 ,oob_score=True,random_state =2)
    classifier.fit(X_train, Y_train)

    y_pred = classifier.predict(X_test)

    total_correct = total_predicted_correct(y_pred,Y_test)

    accuracy=total_correct/len(test_labels)

    return total_correct,accuracy,y_pred


def Frequent_words(redacted_file_train):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    #without_stp = Counter()
    most_occur=[]
    without_stp=[]
    for i in range(len(redacted_file_train)):
        without_stp.append(Counter())
        spl=redacted_file_train[i].split()
        without_stp[i].update(w.lower().rstrip(punctuation)for w in spl if w not in stopwords)
        most_occur.append([y for y in without_stp[i].most_common(3)])
    strin=[]
    for i in range(len(most_occur)):
        for j in range(len(most_occur[i])):
            strin.append(most_occur[i][j][0])

    return (list(set(strin)))

def Removing_uneccesary_braces(string):
    for i in range(len(string)):
        Space = re.compile("[\(\),.]")
        if((re.search(Space, string[i]))!=None):
            #print("i",i)
            string[i] = Space.sub("", string[i])
    return string

def unredactor(redacted_file_test,y_pred):
    unredacted_test_files=[]
    for i in range(len(redacted_file_test)):
        unredacted_test_files.append(re.sub(u"[\u2588]+ ?[\u2588]+",y_pred[i],redacted_file_test[i]))
    return unredacted_test_files


