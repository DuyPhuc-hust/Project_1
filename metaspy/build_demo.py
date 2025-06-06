import subprocess
import os
import sys

def show_main_menu():
    """Hiển thị menu chính và xử lý lựa chọn của người dùng."""
    
    while True:
        print("\n=== Công cụ thu thập thông tin người dùng trên Facebook ===")
        print("1. Thu thập danh sách bạn bè người dùng")
        print("2. Thu thập dữ liệu hồ sơ người dùng")
        print("3. Tạo biểu đồ quan hệ (kết nối, vị trí))")
        print("4. Dừng chương trình")
        choice = input("Nhập lựa chọn (1-4): ")

        if choice == "1":
            user_id = input("Nhập ID người dùng để thu thập danh sách bạn bè: ")
            # Gọi lệnh python main.py friend-layer-crawler <user_id> trực tiếp
            subprocess.run(["python3", "main.py", "friend-layer-crawler", user_id])
        
        elif choice == "2":
            # Gọi lệnh python -m src.facebook.account.crawl_profile_data trực tiếp
            subprocess.run(["python3", "-m", "src.facebook.account.crawl_profile_data"])
        
        elif choice == "3":
            # Gọi lệnh python run_graph.py trực tiếp
            subprocess.run(["python3", "run_graph.py"])
        
        elif choice == "4":
            print("Thoát chương trình.")
            break
        
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    show_main_menu()