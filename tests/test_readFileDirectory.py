import pytest
import project1_phase2
from project1_phase2 import unredactor

def tests_readFileDirectory():
    
    filepath = '/project/cs5293sp19-project1-phase2/aclImdb/train/pos'
    
    count_of_files_to_extract=2

    filenames,entities,files = unredactor.read_textfiles_from_directory(filepath, '.txt',count_of_files_to_extract)
    
    assert len(filenames)==2
