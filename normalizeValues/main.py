import os
import sys
import unicodedata

#################################################
#Accents are not shown correctly in Pajek
#################################################
def strip_accents(str):
    return ''.join(c for c in unicodedata.normalize('NFD', str)
                   if unicodedata.category(c) != 'Mn')

if len(sys.argv) != 2:
    print("Usage: python Main.py <file_name>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    with open(file_path, 'r', encoding='utf-8') as reader:
        #################################################
        # Temporary file where original info will be copies, then transferred back to the original file with changes
        #################################################
        temp_file_path = "temp.txt"
        with open(temp_file_path, 'w', encoding='utf-8') as writer:
            is_vertices_section = False
            min_x = float('inf')
            min_y = float('inf')
            max_x = float('-inf')
            max_y = float('-inf')

            for line in reader:
                #################################################
                # Start obtaining values when reaching vertices section
                #################################################
                if line.startswith("*Vertices"):
                    is_vertices_section = True
                    writer.write(line)
                    continue
                #################################################
                # Stop obtaining values when reaching edges section
                #################################################
                if line.startswith("*Edges"):
                    is_vertices_section = False

                if is_vertices_section:
                    p = line.split("\"")
                    parts = p[2].split(" ")
                    if len(parts) > 3:
                        #################################################
                        # Obtain min and max x and y values
                        #################################################
                        x = float(parts[1])
                        y = float(parts[2])

                        min_x = min(min_x, x)
                        min_y = min(min_y, y)
                        max_x = max(max_x, x)
                        max_y = max(max_y, y)

                writer.write(line)

            #################################################
            # Obtain x and y ranges applying 10% margin
            #################################################
            margin = 0.1
            range_x = max_x - min_x
            range_y = max_y - min_y
            margin_x = margin * range_x
            margin_y = margin * range_y
            min_x -= margin_x
            min_y -= margin_y
            max_x += margin_x
            max_y += margin_y
            range_x = max_x - min_x
            range_y = max_y - min_y

    with open(temp_file_path, 'r', encoding='utf-8') as reader, open(file_path, 'w', encoding='utf-8') as writer:
        for line in reader:
            #################################################
            # Start applying changes when reaching vertices section
            #################################################
            if line.startswith("*Vertices"):
                is_vertices_section = True
                writer.write(line)
                continue
            #################################################
            # Stop applying changes when reaching edges section
            #################################################
            if line.startswith("*Edges"):
                is_vertices_section = False
            if is_vertices_section:
                p = line.split("\"")
                p[1] = strip_accents(p[1])
                parts = p[2].split(" ")
                if len(parts) > 3:
                    x = float(parts[1])
                    y = float(parts[2])

                    #################################################
                    # Normalize values to a range between 0 and 1
                    #################################################
                    normalized_x = (x - min_x) / range_x
                    normalized_y = 1 - ((y - min_y) / range_y)

                    writer.write(p[0] + "\"" + p[1] + "\" " + str(normalized_x) + " " + str(normalized_y) + " 0.0\n")
                else:
                    writer.write(line)
            else:
                writer.write(line)

    os.remove(temp_file_path)
    print("Coordinates have been normalized and file has been successfully.")
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print("Error:", e)