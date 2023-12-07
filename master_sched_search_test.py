import datetime as datetime
import pandas as pd


def search_master_schedule(keyword: str) -> dict:
    """
    Searches the master schedule for any keyword and returns all of the information related to the matches
    @param keyword: The keyword to search for
    """
    print("Searching master schedule for keyword: " + keyword)
    try:
        df = pd.read_excel('Master Schedule.xlsx', sheet_name='Master Schedule')
    except Exception as e:
        print(f"Error reading the file: {e}")
        return {}

    result = df[df.apply(lambda row: row.astype(str).str.contains(keyword).any(), axis=1)]
    # print(result.to_dict(orient='list'))
    result = clean_data_structure(result.to_dict(orient='list'))
    return result

def clean_data_structure(data: dict) -> dict:
    cleaned_data = {}
    for key, value in data.items():
        # Skip keys that are 'Unnamed:'
        if isinstance(key, str) and "Unnamed:" in key:
            continue

        # Remove nan and None values from the list
        cleaned_values = [v for v in value if v is not None and not pd.isna(v)]

        # If the list is empty after removing nan/None, skip this key
        if not cleaned_values:
            continue

        # Convert datetime objects to strings for readability
        cleaned_values = [v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, datetime.datetime) else v for v in cleaned_values]

        # Convert single-item lists to just the item
        if len(cleaned_values) == 1:
            cleaned_data[key] = cleaned_values[0]
        else:
            cleaned_data[key] = cleaned_values

    return cleaned_data


# Usage
result = search_master_schedule('D87348-005')
print(result)
