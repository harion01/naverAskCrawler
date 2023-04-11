

def convert_text_to_json_format(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write("[\n")
        first = True

        while True:
            title = infile.readline().strip().replace('"', '\\"')
            if not title:
                break
            content = infile.readline().strip().replace('"', '\\"')

            # Skip the empty line between entries
            infile.readline()

            if not first:
                outfile.write(",\n")
            else:
                first = False

            formatted_entry = f'    {{\n        "prompt": "{title}",\n        "completion": "\'{content}"\n    }}'
            outfile.write(formatted_entry)

        outfile.write("\n]")

# Usage example
input_file_path = "result/mediGate/medigate.txt"
output_file_path = "result/mediGate/medigate_convert.txt"
convert_text_to_json_format(input_file_path, output_file_path)
print("Job Done!")
