import cv2
import os
import time

# Tạo thư mục lưu ảnh
os.makedirs("data/awake", exist_ok=True)
os.makedirs("data/drowsy", exist_ok=True)
os.makedirs("data/yawn", exist_ok=True)
# Đếm số ảnh hiện có để nối đuôi
def get_last_index(class_name):
    files = os.listdir(f"data/{class_name}")
    if not files:
        return 0
    indices = []
    for f in files:
        try:
            idx = int(f.split("_")[-1].split(".")[0])
            indices.append(idx)
        except:
            pass
    return max(indices) + 1 if indices else 0

cap = cv2.VideoCapture(1)

current_class = "awake"
count = {
    "awake": get_last_index("awake"),
    "drowsy": get_last_index("drowsy"),
    "yawn": get_last_index("yawn")
}
capture_interval = 0.2
last_capture = time.time()

print("=== THU THẬP DỮ LIỆU ===")
print("[A] = Chụp class AWAKE (tỉnh táo)")
print("[D] = Chụp class DROWSY (ngủ gật)")
print("[Y] = Chụp class YAWN (ngủ gật)")
print("[SPACE] = Bắt đầu/Dừng tự động chụp")
print("[Q] = Thoát")
print(f"\nClass hiện tại: {current_class.upper()}")
print(f"Awake hiện có: {count['awake']} ảnh")
print(f"Drowsy hiện có: {count['drowsy']} ảnh")
print(f"Yawn hiện có: {count['yawn']} ảnh")



auto_capture = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (227, 227))

    if auto_capture and (time.time() - last_capture) >= capture_interval:
        filename = f"data/{current_class}/Huy_{current_class}_{count[current_class]:04d}.jpg"
        cv2.imwrite(filename, resized)
        count[current_class] += 1
        last_capture = time.time()

    display = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
    color = (0, 255, 0) if current_class == "awake" else (0, 0, 255)
    status = "AUTO" if auto_capture else "MANUAL"

    cv2.putText(display, f"Class: {current_class.upper()}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(display, f"Awake: {count['awake']}  Drowsy: {count['drowsy']} Yawn: {count['yawn']}", (10, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(display, f"Mode: {status}", (10, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

    cv2.imshow("Thu thap du lieu", display)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('a'):
        current_class = "awake"
        print(f"Chuyển sang: AWAKE (đang có {count['awake']} ảnh)")
    elif key == ord('d'):
        current_class = "drowsy"
        print(f"Chuyển sang: DROWSY (đang có {count['drowsy']} ảnh)")
    elif key == ord('y'):
        current_class = "yawn"
        print(f"Chuyển sang: YAWN (đang có {count['yawn']} ảnh)")
    elif key == ord(' '):
        auto_capture = not auto_capture
        print(f"Auto capture: {'BẬT' if auto_capture else 'TẮT'}")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"\n=== KẾT QUÁ ===")
print(f"Awake:  {count['awake']} ảnh")
print(f"Drowsy: {count['drowsy']} ảnh")
print(f"Yawn:   {count['yawn']} ảnh")