import pandas
from geopy.geocoders import Nominatim
nom=Nominatim(scheme="http")
#csv_file_orig=pandas.read_csv("2017-05-08-10-44-25-734809.csv")

def address_check(data_frame):
    """function checks whether address is present in input"""
    global check
    global address_index
    headers=list(data_frame.columns.values)
    if 'address' in headers:
        check=True
        address_index=headers.index('address')
    elif 'Address' in headers:
        check=True
        address_index=headers.index('Address')
    else:
        check=False
    return check

def result_df_generate(my_file):
    """function returns original dataframe with coordinates - if in input df adress exists else returns message"""
    csv_file_orig=pandas.read_csv(my_file)
    address_check(csv_file_orig)
    if check==True:
        try:
            work_df=csv_file_orig[['address']].rename(columns={'address': 'ADDRESS'})
        except:
            work_df=csv_file_orig[['Address']].rename(columns={'Address': 'ADDRESS'})

        work_df["Coordinates"]=work_df["ADDRESS"].apply(nom.geocode)
        work_df["Latitude"]=work_df["Coordinates"].apply(lambda x: x.latitude if x!= None else None)
        work_df["Longitude"]=work_df["Coordinates"].apply(lambda x: x.longitude if x!= None else None)
        result_df=csv_file_orig.merge(work_df[['Latitude','Longitude','ADDRESS']],how='left',on=None,
                                      left_on=list(csv_file_orig.columns.values)[address_index],
                                      right_on='ADDRESS').drop(columns='ADDRESS')
        return(result_df)
    else:
        return("There is no address/Address column in your dataframe")
