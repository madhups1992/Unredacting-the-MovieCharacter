import argparse
import re

import project1_phase2


def main():
    filepath= '/project/cs5293sp19-project1-phase2/aclImdb/train/pos'
    file_regexp = ".txt"

    count_of_files_to_extract=800

    filenames,entities,files = project1_phase2.read_textfiles_from_directory(filepath, file_regexp,count_of_files_to_extract)

    # split is the probalility for how much percent of training data set is needed
    split = 0.85
    #count_of_files_to_extract=500
    train , test = project1_phase2.Train_and_test_cases(filenames,entities,files,split,count_of_files_to_extract)
    
    train_filename = train[0][:]
    train_entity = train[1][:]
    train_files = train[2][:]

    test_filename = test[0][:]
    test_entity = test[1][:]
    test_files = test[2][:]

    # Removing <BR> and some few unneccesary things by cleaning
    train_files = project1_phase2.Removing_uneccesary(train_files)
    test_files = project1_phase2.Removing_uneccesary(test_files)
    len(train_entity)

    train_filename,train_entity,train_files,train_labels = project1_phase2.cleaning_TrainingSet(train_filename,train_entity,train_files)
    redacted_file_test,test_labels = project1_phase2.redacted_of_files(test_files,train_labels)
    redacted_file_train,train_labels = project1_phase2.redacted_of_files(train_files,train_labels)

    total_correct,accuracy,y_pred = project1_phase2.ModelConstruction(redacted_file_train,redacted_file_test,train_labels,test_labels)

    print("Unredactor:")
    print("Total Words to unredact from test set : ",len(test_labels))
    print("Total Words Correctly unredacted : ", total_correct)
    print("Total Accuracy : ", accuracy)

    print()
    print()
    print("Ground truth\t","Prediction\t","positive")
    print("-----------------------------------------------")

    for i in range(len(y_pred)):

        if(test_labels[i]==y_pred[i]):
            print(test_labels[i],"\t\t",y_pred[i],'\t 1')
        else:
            print(test_labels[i],"\t\t",y_pred[i],'\t 0')

    unredacted_file_test = project1_phase2.unredactor(redacted_file_test,y_pred)
    print("original :")
    print(redacted_file_test[1])
    print("Unredaccted :")
    #print(re.sub(u"[\u2588]+ ?[\u2588]+",y_pred[0],unredacted_test_files[0]))
    print(unredacted_file_test[1])

main()
