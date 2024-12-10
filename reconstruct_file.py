from datetime import datetime

def reconstruct_file(file, start_time_str):
    """Reconstruct file from a certain time"""
    #converts the string time into a datetime object 
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")

    #dict for current lines
    lines = {}
    reconstructed_lines = []

    with open(file, 'r') as f:
        for line in f:
            parts = line.split(',')

            timestamp_str = parts[0]
            action = parts[1]
            line_no = parts[2].split(':')[0]
            content = parts[2].split(':')[1]

            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            # print(timestamp, action, line_no,content)
            if timestamp >= start_time:
                continue

            if action == '+':
                lines[line_no] = content.strip()
                reconstructed_lines.append(f"{str(timestamp)},{action},{line_no},{content}")

            elif action == '-':
                if line_no in lines:
                    del lines[line_no]
            # reconstructed_lines.append(f"{str(timestamp)},{action},{line_no},{content}")
                    
    
    return reconstructed_lines, lines
# print(reconstruct_file("journal_folder\j1_tracked1_txt_1733786317.DAT", "2024-12-09 18:19:24")[1])
test = reconstruct_file("journal_folder\j1_tracked1_txt_1733786317.DAT", "2024-12-09 18:19:24")[1]
print(type(test))
with open("./new_tracked1.txt", 'w') as f:
    for line in test.values():
        f.write(line + '\n')
        print(line)