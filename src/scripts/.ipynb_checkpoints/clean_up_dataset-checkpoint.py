import pandas as pd
import argparse
import os

# These are the columns we will keep in the results file.
cols = {'maker', 'model', 'mileage', 'manufacture_year', 'engine_displacement', 'engine_power', 'transmission', 'door_count', 'seat_count', 'fuel_type', 'price_eur'}

# Location of this script in the file system.
file_location = os.path.dirname(os.path.realpath(__file__))

# Handle the command line argument --dataset for passing the csv file.
parser = argparse.ArgumentParser(description='Cleanup the dataset.')
parser.add_argument('--dataset', help='Pass a .csv file, preferably stored in "datasets/" folder.')
args = parser.parse_args()

with open(args.dataset) as csv_file:

    # Get how many rows there are in the csv.
    row_count = sum(1 for row in csv_file)
    print(f"Lines in initial file: {row_count}")

    # Return back to the beginning of the file.
    csv_file.seek(0)

    # Read half of the file.
    df = pd.read_csv(csv_file, sep=',', nrows=int(row_count / 2), low_memory=False)

    # Clean the data by removing examples with empty values.
    df = df[pd.notnull(df['maker'])]
    df = df[pd.notnull(df['model'])]
    df = df[pd.notnull(df['price_eur'])]

    # Save the dataframe in result.csv
    try:
        df.to_csv(path_or_buf=f"{file_location}/../../datasets/result.csv", sep=",", columns=cols)
    except:
        print("Error with saving the result file.")
    else:
        print("Successfully cleaned up data, saving in datasets/result.csv")

    with open(f"{file_location}/../../datasets/result.csv") as result:
        row_count = sum(1 for row in result)
        print(f"Lines of the result file: {row_count}")

    df = pd.read_csv(csv_file, sep=',', skiprows=int(row_count / 2), low_memory=False)
    df.to_csv(path_or_buf=f"{file_location}/../../datasets/restdata.csv", sep=",")

    with open(f"{file_location}/../../datasets/restdata.csv") as result:
        row_count = sum(1 for row in result)
        print(f"Rest of the data used for admin validation etc: {row_count}")