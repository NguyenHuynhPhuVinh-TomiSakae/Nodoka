import random
import re

def is_consecutive_numbers3(name1, name2, name3):
    match1 = re.match(r'(\D+)(\d+)', name1)
    match2 = re.match(r'(\D+)(\d+)', name2)
    match3 = re.match(r'(\D+)(\d+)', name3)
    
    if not (match1 and match2 and match3):
        return False
    
    prefix1, num1 = match1.groups()
    prefix2, num2 = match2.groups()
    prefix3, num3 = match3.groups()
    
    return (prefix1 == prefix2 == prefix3) and (int(num2) == int(num1) + 1) and (int(num3) == int(num2) + 1)

def is_consecutive_numbers2(name1, name2):
    match1 = re.match(r'(\D+)(\d+)', name1)
    match2 = re.match(r'(\D+)(\d+)', name2)
    
    if not (match1 and match2):
        return False
    
    prefix1, num1 = match1.groups()
    prefix2, num2 = match2.groups()
    
    return (prefix1 == prefix2) and (int(num2) == int(num1) + 1)

def logic_game(text):
    names = []
    positions = []
    
    lines = text.splitlines()
    
    for line in lines[1:]:
        name = line.split(":")[1].split(" at")[0].strip()
        position = line.split(" at position ")[1].strip()
        names.append(name)
        positions.append(position)
    
    valid_groups3 = []
    
    i = 0
    while i < len(names) - 2:
        if is_consecutive_numbers3(names[i], names[i + 1], names[i + 2]):
            valid_groups3.append((i, i + 1, i + 2))
            i += 3
        else:
            i += 1
    
    i = 0
    while i < len(names) - 2:
        if names[i] == names[i + 1] == names[i + 2]:
            valid_groups3.append((i, i + 1, i + 2))
            i += 3
        else:
            i += 1
    
    all_indices3 = {index for group in valid_groups3 for index in group}
    sorted_indices3 = sorted(all_indices3)
    
    if valid_groups3:
        print(f"Valid group3 indices: {sorted_indices3}")
    else:
        print("No valid groups found.")
    
    grouped_indices3 = all_indices3
    remaining_names3 = [name for i, name in enumerate(names) if i not in grouped_indices3]
    remaining_positions3 = [position for i, position in enumerate(positions) if i not in grouped_indices3]
    
    remaining_indices3 = [i for i in range(len(names)) if i not in grouped_indices3]

    print("\nRemaining indices after removal:")
    print(remaining_names3)
    print(remaining_positions3)
    
    valid_groups2 = []
    
    i = 0
    while i < len(remaining_names3) - 1:
        if is_consecutive_numbers2(remaining_names3[i], remaining_names3[i + 1]):
            valid_groups2.append((i, i + 1))
            i += 2
        else:
            i += 1
    
    i = 0
    while i < len(remaining_names3) - 1:
        if remaining_names3[i] == remaining_names3[i + 1]:
            valid_groups2.append((i, i + 1))
            i += 2
        else:
            i += 1
    
    all_indices2 = {index for group in valid_groups2 for index in group}
    sorted_indices2 = sorted(all_indices2)
    
    if valid_groups2:
        print(f"Valid group2 indices: {sorted_indices2}")
    else:
        print("No valid groups found.")
    
    grouped_indices2 = all_indices2
    remaining_names2 = [name for i, name in enumerate(remaining_names3) if i not in grouped_indices2]
    remaining_positions2 = [position for i, position in enumerate(remaining_positions3) if i not in grouped_indices2]
    
    remaining_indices2 = [i for i in range(len(remaining_names3)) if i not in grouped_indices2]

    print("\nRemaining indices after removal:")
    print(remaining_names2)
    print(remaining_positions2)
    
    # Chọn ngẫu nhiên giá trị từ remaining_indices2 hoặc remaining_indices3
    if remaining_positions2:
        output = random.choice(remaining_positions2)
    elif remaining_positions3:
        output = random.choice(remaining_positions3)
    else:
        output = None

    print("\nRandomly selected index:")
    print(output)

# Ví dụ sử dụng
text = """Detected positions:
0: man-4 at position (17, 47)
1: man-4 at position (114, 46)
2: man-5 at position (213, 51)
3: pin-4 at position (309, 51)
4: pin-4 at position (405, 52)
5: pin-4 at position (1316, 51)
6: pin-5 at position (501, 52)
7: pin-8 at position (597, 50)
8: sou-5 at position (692, 52)
9: sou-7 at position (788, 52)
10: sou-8 at position (885, 50)
11: chun at position (1173, 50)
12: nan at position (979, 49)
13: nan at position (1076, 48)"""

logic_game(text)
