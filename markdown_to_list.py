import re
def extract_points_from_markdown(md_file):
    with open(md_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    points = []
    current_point = ""

    for line in lines:
        line = line.strip()
        # Ignore page headers
        if line.startswith("## Page"):
            continue
        # Capture list items and group paragraphs under the same point
        if re.match(r'^[\-\*] ', line):
            if current_point:
                points.append(current_point.lstrip('-* '))
            current_point = line  # Start a new point
        elif line and current_point:
            current_point += " " + line  # Append to the current point

    if current_point:
        points.append(current_point.lstrip('-* ')) # Add the last accumulated point

    return points


# Example usage
md_file = "handbook_extracted.md"  # Update with your file path
points = extract_points_from_markdown(md_file)

# Save the extracted points to a new file
output_file = "extracted_points.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for point in points:
        f.write(point + "\n")

print(f"Extraction complete. Points saved to {output_file}")
