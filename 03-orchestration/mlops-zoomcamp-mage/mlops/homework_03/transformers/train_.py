from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    categorical_variables = ['PULocationID', 'DOLocationID']
    train_dicts = df[categorical_variables].to_dict(orient = 'records')

    # Vectorizer the training variables 
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)

    # Setup the Prediction_Variables 
    predictor = 'duration'
    y_train = df[predictor].values

    # Train the model 
    lr = LinearRegression() 
    lr.fit(X_train, y_train) 

    # Print the intercept
    print(lr.intercept_)  
    
    return dv, lr


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'