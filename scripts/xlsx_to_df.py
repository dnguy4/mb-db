import pandas as pd
import sqlite3 as sq


def excel_to_json(excel_path, sheet_name):
    """
    Convert an Excel sheet to JSON format.

    Args:
        excel_path (str): Path to the Excel file
        sheet_name (str): Name of the sheet to convert

    Returns:
        str: JSON representation of the Excel sheet
    """
    try:
        # Read the Excel file
        headers = [
            "Source",
            "Card Type",
            "Cost",
            "Qty",
            "Set",
            "Divider",
            "Star",
            "Element",
            "Type",
            "Card Name",
            "References",
            "Comments and Errata",
            "Card Text",
            "Source Symbol",
            "Copyright",
            "Count",
        ]
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        df = df[headers]
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        table_name = "card_list"
        conn = sq.connect(f"{table_name}.sqlite")
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()

        # Convert to JSON with pretty formatting
        json_output = df.to_json(orient="records", indent=2)
        return json_output

    except FileNotFoundError:
        print(f"Error: File '{excel_path}' not found")
        return None
    except ValueError as e:
        print(f"Error reading Excel file: {str(e)}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# Example usage
excel_path = "mb.xlsx"
sheet_name = "Master List"

json_data = excel_to_json(excel_path, sheet_name)
if json_data:
    with open("card_list.json", "w") as f:
        f.write(json_data)
        # json.dump(json_data, fp=f)
