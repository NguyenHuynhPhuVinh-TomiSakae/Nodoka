def logic_game(text):
    names = []
    positions = []
    
    # Tách các dòng trong text
    lines = text.splitlines()
    
    for line in lines[1:]:
        if ":" in line and " at position " in line:
            try:
                # Tách lấy tên quân bài và loại bỏ "images\"
                name_part = line.split(":")[1].split(" at")[0].strip()
                name = name_part.replace("images\\", "").strip()
                
                # Lấy vị trí quân bài
                position = line.split(" at position ")[1].strip()
                
                names.append(name)
                positions.append(position)
            except IndexError:
                print(f"Lỗi khi xử lý dòng: {line}")
                continue

    def find_valid_sets_and_pairs(names, positions):
        valid_sets = []
        valid_pairs = []

        n = len(names)
        
        # Kiểm tra tất cả các bộ ba có thể
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    set_to_check = [names[i], names[j], names[k]]
                    positions_to_check = [positions[i], positions[j], positions[k]]
                    
                    current_values = [int(name.split("-")[-1]) if '-' in name else None for name in set_to_check]
                    
                    if len(set(set_to_check)) == 1:  # All the same
                        valid_sets.append((set_to_check, positions_to_check))
                    elif all(v is not None for v in current_values) and len(set([name.split("-")[0] for name in set_to_check])) == 1:
                        sorted_values = sorted(current_values)
                        if sorted_values == list(range(min(sorted_values), min(sorted_values) + 3)):
                            valid_sets.append((set_to_check, positions_to_check))
                    
        # Kiểm tra tất cả các bộ đôi có thể
        for i in range(n):
            for j in range(i + 1, n):
                pair_to_check = [names[i], names[j]]
                positions_to_check = [positions[i], positions[j]]
                
                if names[i] == names[j]:
                    valid_pairs.append((pair_to_check, positions_to_check))
                else:
                    current_value_i = int(names[i].split("-")[-1]) if '-' in names[i] else None
                    current_value_j = int(names[j].split("-")[-1]) if '-' in names[j] else None
                    
                    if current_value_i is not None and current_value_j is not None:
                        if names[i].split("-")[0] == names[j].split("-")[0] and abs(current_value_i - current_value_j) == 1:
                            valid_pairs.append((pair_to_check, positions_to_check))
        
        return valid_sets, valid_pairs

    valid_sets, valid_pairs = find_valid_sets_and_pairs(names, positions)
    
    if valid_sets:
        for valid_set, pos_set in valid_sets:
            print(f"Valid set of 3: {valid_set} at positions {pos_set}")
        return valid_sets
    elif valid_pairs:
        for valid_pair, pos_pair in valid_pairs:
            print(f"Valid pair of 2: {valid_pair} at positions {pos_pair}")
        return valid_pairs
    else:
        print("No valid sets or pairs found.")
        return None

# Đầu vào
text = """
Detected positions:
0: images\man-4 at position (17, 47)
1: images\man-5 at position (115, 52)
2: images\pin-4 at position (212, 52)
3: images\sou-2 at position (501, 47)
4: images\sou-2 at position (597, 48)
5: images\pin-7 at position (402, 49)
6: images\sou-9 at position (1079, 47)
7: images\sou-5 at position (1175, 47)
8: images\pin-6 at position (307, 50)
9: images\nan at position (1312, 48)
10: images\sou-4 at position (886, 51)
11: images\sou-4 at position (932, 51)
12: images\sou-3 at position (692, 49)
13: images\sou-3 at position (788, 49)
14: images\sou-5 at position (982, 52)
"""

logic_game(text)
