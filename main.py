import cv2
import numpy as np
import pyautogui
import os
import time
import keyboard  # Thư viện để lắng nghe phím

def find_images(image_path, region, threshold=0.8):
    # Đọc ảnh mẫu cần tìm
    template = cv2.imread(image_path, 0)
    if template is None:
        print(f"Could not read image: {image_path}")
        return []

    # Chụp màn hình hiện tại trong vùng kiểm tra
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Tìm kiếm ảnh trên màn hình
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    # Nếu tìm thấy vị trí khớp, trả về danh sách các vị trí và kích thước
    positions = []
    for pt in zip(*loc[::-1]):
        # Lưu vị trí góc trên cùng bên trái và kích thước của mẫu
        positions.append(pt)
    
    return positions

def group_positions(positions, x_distance=30):
    """Nhóm các vị trí có giá trị x giao động lớn hơn hoặc bằng x_distance vào cùng một nhóm."""
    if not positions:
        return []
    
    # Sắp xếp các vị trí theo giá trị x
    positions_sorted = sorted(positions, key=lambda p: p[0])
    groups = []
    current_group = []
    
    for pos in positions_sorted:
        if not current_group:
            current_group.append(pos)
        else:
            last_x = current_group[-1][0]
            if abs(pos[0] - last_x) >= x_distance:
                groups.append(current_group)
                current_group = [pos]
            else:
                current_group.append(pos)
    
    if current_group:
        groups.append(current_group)
    
    # Chỉ lấy vị trí đầu tiên của mỗi nhóm
    return [group[0] for group in groups]

def process_single_image(image_path, region):
    """Chỉ xử lý một ảnh cụ thể."""
    print(f"Processing image: {image_path}")
    positions = find_images(image_path, region)
    if positions:
        print(f"Image found at positions: {positions}")
        grouped_positions = group_positions(positions)
        return grouped_positions  # Trả về danh sách các nhóm vị trí
    else:
        print(f"Image not found: {image_path}")
        return []

def custom_sort_key(filename):
    order = {
        "man": 1,
        "pin": 2,
        "sou": 3,
        "haku": 4,
        "hatsu": 5,
        "chun": 6,
        "Ton": 7,
        "Nan": 8,
        "Sha": 9,
        "Pei": 10
    }
    
    # Tách phần tên và số từ tên tệp
    parts = filename.split('-')
    tile_type = parts[0]
    tile_number = parts[1].split('.')[0] if len(parts) > 1 else ""
    
    # Trả về giá trị sắp xếp dựa trên loại và số
    return (order.get(tile_type, 100), int(tile_number) if tile_number.isdigit() else 0)

def sort_images(image_list):
    # Sắp xếp danh sách ảnh sử dụng khóa tùy chỉnh
    return sorted(image_list, key=custom_sort_key)

def collect_positions(image_file, positions, image_size):
    """Lưu vị trí và tên quân bài vào mảng."""
    image_name = os.path.splitext(image_file)[0]
    return [(image_name, pos) for pos in positions]

def process_clicks(positions, image_size, region):
    """In ra danh sách các vị trí và chờ người dùng nhập để nhấn vào vị trí đó."""
    text = "Detected positions:\n"
    for i, (name, pos) in enumerate(positions):
        text += f"{i}: {name} at position {pos}\n"
    
    # In ra toàn bộ thông tin đã lưu
    print(text)
    
    while True:
        try:
            choice = int(input("Enter the number of the position to click (or -1 to exit): "))
            if 0 <= choice < len(positions):
                name, pos = positions[choice]
                x, y = pos
                center_x = x + image_size[0] // 2
                center_y = y + image_size[1] // 2
                screen_x = center_x + region[0]
                screen_y = center_y + region[1]
                print(f"Clicking at position: ({screen_x}, {screen_y})")
                pyautogui.click(screen_x, screen_y)
                time.sleep(0.5)  # Tạm dừng giữa các lần nhấp chuột
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def detect_and_click_pass(pass_image_path, pass_region, riichi_image_path, tsumo_image_path, ron_image_path):
    """Kiểm tra liên tục và nhấn vào ảnh pass nếu phát hiện, ưu tiên các ảnh khác."""
    while True:
        # Kiểm tra ảnh riichi, tsumo, ron
        for image_path, action_name in [(riichi_image_path, 'riichi'), (tsumo_image_path, 'tsumo'), (ron_image_path, 'ron')]:
            positions = find_images(image_path, pass_region)
            if positions:
                for position in positions:
                    x, y = position
                    print(f"Clicking {action_name} image at: ({x + pass_region[0]}, {y + pass_region[1]})")
                pyautogui.click(x + pass_region[0], y + pass_region[1])
                break  # Ngừng kiểm tra nếu tìm thấy ảnh khác

        # Kiểm tra ảnh pass nếu không có ảnh riichi, tsumo, ron
        positions = find_images(pass_image_path, pass_region)
        if positions:
            for position in positions:
                x, y = position
                print(f"Clicking pass image at: ({x + pass_region[0]}, {y + pass_region[1]})")
            pyautogui.click(x + pass_region[0], y + pass_region[1])

        time.sleep(3)  # Thời gian chờ trước khi kiểm tra lại

def main():
    # Xác định vùng kiểm tra cho ảnh pass (x, y, width, height)
    pass_region = (473, 764, 1588 - 473, 865 - 764)  # Vùng kiểm tra từ (473, 764) với kích thước 1115x101
    pass_image_path = 'images/pass.png'  # Thay đổi đường dẫn đến ảnh pass
    riichi_image_path = 'images/riichi.png'
    tsumo_image_path = 'images/tsumo.png'
    ron_image_path ='images/ron.png'
    # Xác định vùng kiểm tra cho các ảnh khác (x, y, width, height)
    region = (289, 840, 1422, 170)  # Vùng kiểm tra từ (289, 840) với kích thước 1422x170

    # Đường dẫn đến thư mục chứa ảnh cần kiểm tra
    images_folder = 'images'

    # Giả sử kích thước quân bài là cố định
    image_size = (100, 150)  # Ví dụ: chiều rộng 100px, chiều cao 150px

    # Khởi động kiểm tra liên tục ảnh pass
    import threading
    pass_thread = threading.Thread(target=detect_and_click_pass, args=(pass_image_path, pass_region, riichi_image_path, tsumo_image_path, ron_image_path))
    pass_thread.daemon = True
    pass_thread.start()

    while True:
        detected_positions = []  # Mảng lưu các vị trí phát hiện
        image_files = os.listdir(images_folder)  # Lấy danh sách các tệp ảnh trong thư mục
        image_files = [f for f in image_files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]  # Lọc các tệp ảnh
        sorted_files = sort_images(image_files)  # Sắp xếp các tệp ảnh

        # Duyệt qua toàn bộ các tệp đã sắp xếp
        for image_file in sorted_files:
            image_path = os.path.join(images_folder, image_file)
            grouped_positions = process_single_image(image_path, region)
            if grouped_positions:  # Nếu có các nhóm vị trí khớp
                # Thêm các vị trí vào mảng
                detected_positions.extend(collect_positions(image_file, grouped_positions, image_size))

        # In ra các ảnh đã phát hiện cùng số nhóm
        if detected_positions:
            print("Detected images and their positions:")
            for name, pos in detected_positions:
                print(f"{name} at position {pos}")
            process_clicks(detected_positions, image_size, region)
        else:
            print("No images detected.")
        
        # Chờ 3 giây trước khi kiểm tra lại sau khi đã chọn và nhấn vào các vị trí
        print("Finished processing all images. Checking again in 3 seconds...")
        if keyboard.is_pressed('q'):
            print("Exit key pressed. Exiting the program.")
            break
        
        time.sleep(3)

if __name__ == "__main__":
    main()
