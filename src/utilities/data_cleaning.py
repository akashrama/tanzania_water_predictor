def import_pump_data():
    #import training data 
    df_train = pd.read_csv('../../../data/raw/train_set_values.csv')
    df_labels = pd.read_csv('../../../data/raw/train_set_labels.csv')
    

    #merge labels and features:
    df_train= pd.merge(df_train, df_labels, on='id')
    
    return df_train

def values_to_keep(df, column, number_of_values_to_keep, verbose = False):
    """
    This function takes in a pandas dataframe, the column of concern, and a number of categories to reduce the number 
    of unique values to. It prints the number of unique values in the column and the top value counts of each. It also
    returns a list of categorical values to retain. 
    """
    number_of_values_to_keep = number_of_values_to_keep-1
    
    if verbose == True:
        print(len(df[column].value_counts()))
        print(df[column].value_counts())
        
        list_of_values = df[column].value_counts()
        list_of_values_to_keep = list(list_of_values[0:number_of_values_to_keep].index)
    else:
        
        list_of_values = df[column].value_counts()
        list_of_values_to_keep = list(list_of_values[0:number_of_values_to_keep].index)
        
    return list_of_values_to_keep


def reduce_categorical_values(df, column_name, number_of_values_to_keep):
    
    """
    This function reduces the number of unique categorical values in a specific dataframe's column. It keeps the top 
    'number_of_values_to_keep' values, and casts the other remaining categorical values as "Other". This function 
    returns a Dataframe with the altered categorical values. Using this function can reduce the amount of dummy columns
    needed whilst maintaining the information contained in the column.
    """
    #use helper function to create a list of cat. values to keep
    list_of_classes_to_keep = values_to_keep(df, column_name, number_of_values_to_keep)
    
    #use subsetting to test if cat. value is in list, if not cast it to 'Other'    "~" means isNOTin 
    df[column_name].loc[~df[column_name].isin(list_of_classes_to_keep)]='Other'
    
    return df
    

def cols_to_drop():
    """
    This small helper function creates a list of columns to be dropped by future functions.
    
    The columns selected to drop have logic behind the decision. Please see the jupyter notebook:
    ../../notebooks/Exploratory/Brent/Eda_cleaning/ for the detailed logic behind the feature selection. 
    
    """
    cols_to_drop = ['scheme_name','subvillage','id','wpt_name','recorded_by','extraction_type_group',
                    'extraction_type','management_group','payment','water_quality','quantity','source','source_type',
                   'waterpoint_type', 'lga', 'ward', 'district_code','region_code','latitude', 'longitude']
    return cols_to_drop


def drop_features(df, list_of_columns):
    """
    This function drops columns included in list_of_columns
    """
    
    df = df.drop(list_of_columns, axis =1)
    return df

def simplify_categorical_features(df):
    """
    This function simplifies all of the features that have many categorical values in preperation for OneHotEncoding,
    and in the process also cleans up some NaN values.
    
    Each feature's simplification has logic behind it. Please see the jupyter notebook:
    ../../notebooks/Exploratory/Brent/Eda_cleaning/ for the detailed logic behind the simplification.
    """
    
    df = reduce_categorical_values(df, 'funder', 10)
    df = reduce_categorical_values(df, 'installer', 10)
    df = reduce_categorical_values(df, 'scheme_management', 12)
    return df

def construction_binner(row):
    """
    This function's main purpose is to address the '0' values in construction_year. 0 is am impossible value for 
    year of construction, so it casts '0' as 'unknown'. Because 'unknown' is not a continuous value, this function
    then bins the years into decades. So, the resulting column is categorical data with decade values. 
    
    This function is meant to be used apart of a df.apply(lambda row:) function as follows
    
    df_train['construction_year'] = df_train.apply(lambda row: construction_binner(row), axis=1)

    """
    
    if row['construction_year'] >= 1960 and row['construction_year'] < 1970:
        return '60'
    elif row['construction_year'] >= 1970 and row['construction_year'] < 1980:
        return '70'
    elif row['construction_year'] >= 1980 and row['construction_year'] < 1990:
        return '80'
    elif row['construction_year'] >= 1990 and row['construction_year'] < 2000:
        return '90'
    elif row['construction_year'] >= 2000 and row['construction_year'] < 2010:
        return '00'
    elif row['construction_year'] >= 2010:
        return '10'
    else:
        return 'unknown'

def fill_nans(df):
    """
    This function cleans up NaN values that still remain, and adjusts impossible values, and categorizes the private 
    well feature. 
    
    Each feature's NaN value imputation has logic behind it. Please see the jupyter notebook:
    ../../notebooks/Exploratory/Brent/Eda_cleaning/ for the detailed logic behind the imputation.
    """
    df.public_meeting.fillna(value='Unknown', inplace=True)
    df.permit.fillna(value='Unknown', inplace=True)
    df.installer.replace(to_replace = '0', value = 'Other', inplace = True)
                  
    #account for the impossible year of construction values using contruction_binner function
    df['construction_year'] = df.apply(lambda i: construction_binner(i), axis=1)

    #categorize private wells as private, or public:
    df['num_private'].loc[df['num_private']>0]=1
     
    #remove impossible values from gps_height
    df_train['gps_height'].loc[df_train['gps_height']<0]=0

    return df

def date_time_transform(df):
    """
    This function transforms the date time features in preperation for modeling.
       
    Please see the jupyter notebook: ../../notebooks/Exploratory/Brent/Eda_cleaning/ 
    for the detailed logic behind the handling of date features.
    """

    df.date_recorded = pd.to_datetime(df.date_recorded)
    df['days_since']=df.date_recorded-df.date_recorded.min()
    df['days_since']=df['days_since'].astype(int)/(8.64e+13)
    df = df.drop('date_recorded', axis=1)
    return df

def clean_all_data(df):
    """
    This function utilizes the helper functions to complete all of the cleaning.
    """
    
    list_of_columns = cols_to_drop()
    df = drop_features(df, list_of_columns)
    df = simplify_categorical_features(df)
    df = fill_nans(df)
    cleaned_df = date_time_transform(df)
    return cleaned_df
                  
def encode_data(df):
    """
    Use pd.getdummies to onehot encode categorical data. Returns two dataframes : dummy_df and target. 
    """
    target = df.status_group
    df_train = df.drop('status_group', axis=1)

    cat_feats = ['funder','installer', 'num_private',
           'region','public_meeting', 'scheme_management', 'permit',
           'construction_year', 'extraction_type_class', 'management',
           'payment_type', 'quality_group', 'quantity_group', 'source_class',
           'waterpoint_type_group', 'basin']

    dum_df = pd.get_dummies(df, columns = cat_feats)
    return dum_df, target