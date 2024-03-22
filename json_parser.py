import json

def print_unique_json_structure(data, indentation="", printed_keys=set()):
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{indentation}{key}:")
            if key not in printed_keys:
                printed_keys.add(key)
                print_unique_json_structure(value, indentation + "  ", printed_keys)
            else:
                print(f"{indentation}  (Repeating key, skipping content)")
    elif isinstance(data, list):
        for index, item in enumerate(data):
            print(f"{indentation}[{index}]:")
            print_unique_json_structure(item, indentation + "  ", printed_keys)
    else:
        print(f"{indentation}{type(data).__name__}")

if __name__ == "__main__":
    json_file_path = "nearby.json"  # Replace with your actual JSON file path
    
    try:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
            print_unique_json_structure(json_data)
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
