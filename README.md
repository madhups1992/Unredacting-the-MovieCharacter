# Project-Phase_2

## UnRedactor:

This project uses IMDB dataset from "http://ai.stanford.edu/~amaas/data/sentiment/" this website. 
It is the lagest movie review available for sentiment analysis.
We are going to use this for doing redaction and unredaction.

## Redactor : 

Hiding the important information to the public is a important task such as credic card details are redacted for security.
In this project we are going to redact names present in the reviews.

## UnRedactor:

We have to divide our available dataset for training and testing and redact both the datasets.
Finally test it on the test data and unredact the information.

  
## Procedure Followed :

        1. We have to take all the names from the document in the training data set and label the document with names belong to that document.
           For labeling there were lots of confusions that is solved as shown below.
           The location of the dataBase "/project/cs5293sp19-project1-phase2/aclImdb/train/pos".
           For training and testing the function was developed to divide it to % split we need (Modifiable).

        2. File cleaining the files that were read need to be cleaned to remove "<BR>,/,<str>" etc.,

        3. There will be many entity present in the single file. We have to construct a training set.
            1.Labeling names based on the most Frequent names in that document.
            2.There may be multiple names and may not have any repetitions. 
            That can be replaced with the names present in our previous labels list if those lables are present in the current file.
            3.Remaining can be ignored.

        4. These labels are then passed to the redactor along with the labels list and it will redact all the names that are present for both training and test dataset

        5. We have to extract features to do training. 
            1.No. of names in the given document.
            2.No. of names redacted names per document.
            3.No. of words? 
            4.No. Sentence in document.
            5.Top 4 most common words in the document other than stopwords.
            6.Is there a space between the redaction?
            7.If there is a space what is the length of each words?
            8.Is there an " ***'s " with the redcted name where *** is redacted name?

        6. From the previous steps we have converted the given document into multi-class classifier problem.
           Build model with training data and labels as the output variable.
           In this project various models like naive bayes, logistic and random forest were tried but random forest seems to work well
           That is provided in python file.

        7. After testing the model on the test set provided the statistics of the number of entities correctly found and which were not.
           The accuracy about the prediction and comparition between which original labels vs predicted and which one is correct. 

        8. Finally using the model it was easy to unredact the redacted files and displayed both the results.
           sometimes result will not show the real name since it might be the wrongly predicted results.

## Test Cases:
	
	1. test_readFileDirectory : The module was tested against extracting .txt files from the given directory.
	2. test_getentity : The module was able to extract entities from the text file
	3. test_redacted : The module was tested on proper redation perfomace of given list.
	4. test_cleaningData : Tested this module whether it is able to clean and label the given set of files properly.
	5. test_feature : Tested on the features are extracted properly and have all the features
	6. test_trainTestSplit : Tested on how the split is done whether it is able to handle decimal as well as % wise.
	7. test_unredactor : This module is tested on whether it is able to unredact properly all the names. 


## Run the code :

	Program : " python /project/cs5293sp19-project1-phase2/project1_phase2/main.py "
	(This is the location where main.py is present, It might take atleast 10 mins to run)
	pytest code : " pipenv run python -m pytest " 
	
	
## sample output :

	Unredactor:
	Total Words to unredact from test set :  79
	Total Words Correctly unredacted :  29
	Total Accuracy :  0.3670886075949367

	Ground truth     Prediction      positive
	-----------------------------------------------
	Wayne            Wayne   	1
	Dreyfuss         Verneuil        0
	Mad Dog          Mad Dog         1
	Scrooge          Scrooge         1
	Ryan             John    	0
	Starck           Beatty          0
	John             John    	1
	John             John    	1
	Sandler          Scrooge         0
   

        original :
        I originally saw this very dark comedy around 2000 or so on cable TV. What a surprise and delight! Everyone is covert
        ly armed in this movie! ████████ plays the "mental" don (remember the New York don who was supposed to be schizophren
        ic? Art imitates life or vice versa?). Diane Lane and Ellen Barkin are at their most beautiful and NOT to be toyed wi
        th! Thus proving that beauty and toughness DO go together! Then there is the great "bullshit" scene between Barkin an
        d Jeff Goldblum (Rita and Mickey) where they verbally play off the world "bullshit." This film is both subtle and bal
        d. For all the shooting, it can be a very quiet film. And, you have the opportunity to see several actors in their fi
        nal or near final roles. Joey Bishop. Richard Pryor. Henry Silva. It is not a film for everyone. But, if you like a f
        ilm that has a lot of word play and keeps moving without blowing up everything in sight, this is the film for you. Ro
        ger Ebert dumps on this film. He's flat wrong. THIS is a fine, fine film! Maybe just not one for Ebert. I consider it
         as a 10 because of how well it is done and how funny the script can be, while not really being a straight comedy kin
        d of film. I like it so well that I bought it on DVD because it just doesn't get shown very much on cable TV. Now, it
        's all mine!
        Unredaccted :
        I originally saw this very dark comedy around 2000 or so on cable TV. What a surprise and delight! Everyone is covert
        ly armed in this movie! Verneuil plays the "mental" don (remember the New York don who was supposed to be schizophren
        ic? Art imitates life or vice versa?). Diane Lane and Ellen Barkin are at their most beautiful and NOT to be toyed wi
        th! Thus proving that beauty and toughness DO go together! Then there is the great "bullshit" scene between Barkin an
        d Jeff Goldblum (Rita and Mickey) where they verbally play off the world "bullshit." This film is both subtle and bal
        d. For all the shooting, it can be a very quiet film. And, you have the opportunity to see several actors in their fi
        nal or near final roles. Joey Bishop. Richard Pryor. Henry Silva. It is not a film for everyone. But, if you like a f
        ilm that has a lot of word play and keeps moving without blowing up everything in sight, this is the film for you. Ro
        ger Ebert dumps on this film. He's flat wrong. THIS is a fine, fine film! Maybe just not one for Ebert. I consider it
         as a 10 because of how well it is done and how funny the script can be, while not really being a straight comedy kin
        d of film. I like it so well that I bought it on DVD because it just doesn't get shown very much on cable TV. Now, it
        's all mine!   

   
## Reference:

    "https://docs.python.org" - Used the website for python usage.
    Used project1's test modules to construct testcases.

