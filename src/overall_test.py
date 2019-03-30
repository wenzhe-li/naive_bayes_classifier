from prepare_dataset import prepare_dataset
from extract_feature import extract_features
from cross_validate import validate

if __name__ == '__main__':
    print('preparing for the dataset')
    prepare_dataset()
    print('extracting features')
    extract_features()
    print('initializing for validation')
    validate()