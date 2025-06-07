import os
import glob
import json
from datetime import datetime
import typer
from rich import print as rprint
import webbrowser

def main():
    data_dirs = glob.glob(os.path.join("user_data", "data_*"))
    
    if not data_dirs:
        rprint("❌ Không tìm thấy thư mục dữ liệu nào có dạng data_*")
        return
    
    rprint("[bold]Danh sách thư mục dữ liệu:[/bold]")
    for i, dir_name in enumerate(data_dirs, 1):
        json_files = glob.glob(os.path.join(dir_name, "*.json"))
        num_files = len(json_files)
        
        try:
            creation_time = os.path.getctime(dir_name)
            time_str = datetime.fromtimestamp(creation_time).strftime("%d/%m/%Y %H:%M:%S")
        except:
            time_str = "Không xác định"
            
        rprint(f"{i}. [bold]{dir_name}[/bold]")
    
    choice = typer.prompt("Chọn số thứ tự thư mục để xuất dữ liệu", type=int)
    
    if choice < 1 or choice > len(data_dirs):
        rprint("❌ Lựa chọn không hợp lệ")
        return
    
    selected_dir = data_dirs[choice - 1]
    json_files = glob.glob(os.path.join(selected_dir, "*.json"))
    
    if not json_files:
        rprint(f"❌ Không có file data_*.json nào trong thư mục {selected_dir}")
        return

    rprint("\n[bold]Chọn chức năng:[/bold]")
    rprint("1. Tạo biểu đồ kết nối bạn bè")
    rprint("2. Tạo biểu đồ vị trí địa lý")
    
    sub_choice = typer.prompt("Nhập số thứ tự chức năng", type=int)
    
    first_json_file = json_files[0]
    with open(first_json_file, "r", encoding="utf-8") as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError:
            rprint("❌ File JSON bị lỗi hoặc không hợp lệ")
            return

    output_folder = "graph-create"
    os.makedirs(output_folder, exist_ok=True)
    
    if sub_choice == 1:
        output_file = os.path.join(output_folder, "friends_data.js")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("const jsonData = ")
            json.dump(json_data, f, indent=2, ensure_ascii=False)
            f.write(";")
        rprint(f"✅ Dữ liệu đã được ghi vào: [bold]{output_file}[/bold]")
        
        html_file = os.path.join(output_folder, "connection.html")
        if os.path.exists(html_file):
            webbrowser.open(f"file://{os.path.abspath(html_file)}")
            rprint(f"🌐 Đã mở [bold]{html_file}[/bold] trên trình duyệt mặc định")
        else:
            rprint(f"⚠️ Không tìm thấy file [bold]{html_file}[/bold] để mở")
            
    elif sub_choice == 2:
        output_file = os.path.join(output_folder, "location_data.js")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("const jsonData = ")
            json.dump(json_data, f, indent=2, ensure_ascii=False)
            f.write(";")
        rprint(f"✅ Dữ liệu đã được ghi vào: [bold]{output_file}[/bold]")
        
        html_file = os.path.join(output_folder, "location.html")
        if os.path.exists(html_file):
            webbrowser.open(f"file://{os.path.abspath(html_file)}")
            rprint(f"🌐 Đã mở [bold]{html_file}[/bold] trên trình duyệt mặc định")
        else:
            rprint(f"⚠️ Không tìm thấy file [bold]{html_file}[/bold] để mở")
    else:
        rprint("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()