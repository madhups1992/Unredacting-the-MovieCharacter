import pytest
import project1_phase2
from project1_phase2 import unredactor

def tests_trainTestSplit():
    
    filepath = '/project/cs5293sp19-project1-phase2/aclImdb/train/pos'
    
    count_of_files_to_extract=10

    filenames,entities,files = unredactor.read_textfiles_from_directory(filepath, '.txt',count_of_files_to_extract)
    
    train , test = unredactor.Train_and_test_cases(filenames,entities,files,0.6,count_of_files_to_extract)
    
    assert len(train[0]) > 0 and len(test[0])>0
