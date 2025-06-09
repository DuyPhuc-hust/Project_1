import os
import glob
import json
from datetime import datetime
import typer
from rich import print as rprint
import webbrowser

def main():
    # Tìm các file checkin_data_*.json trong checkin_src/user_data
    data_files = glob.glob(os.path.join("checkin_src", "user_data", "checkin_data_*.json"))   
    if not data_files:
        rprint("❌ Không tìm thấy file nào có định dạng checkin_data_*.json trong checkin_src/user_data")
        return    
    rprint("[bold]Danh sách file checkin_data_*.json:[/bold]")
    for i, file_path in enumerate(data_files, 1):
        try:
            creation_time = os.path.getctime(file_path)
            time_str = datetime.fromtimestamp(creation_time).strftime("%d/%m/%Y %H:%M:%S")
        except:
            time_str = "Không xác định"
        rprint(f"{i}. [bold]{file_path}[/bold] (tạo lúc {time_str})")
    
    choice = typer.prompt("Chọn số thứ tự file để xuất dữ liệu", type=int)
    
    if choice < 1 or choice > len(data_files):
        rprint("❌ Lựa chọn không hợp lệ")
        return
    
    selected_file = data_files[choice - 1]
    with open(selected_file, "r", encoding="utf-8") as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError:
            rprint("❌ File JSON bị lỗi hoặc không hợp lệ")
            return

    output_folder = os.path.join("checkin_src", "checkin_graph")
    os.makedirs(output_folder, exist_ok=True)
    
    output_file = os.path.join(output_folder, "checkin_data.js")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("const checkinData = ")
        json.dump(json_data, f, indent=2, ensure_ascii=False)
        f.write(";")
    rprint(f"✅ Dữ liệu đã được ghi vào: [bold]{output_file}[/bold]")
    
    html_file = os.path.join(output_folder, "checkin.html")
    if os.path.exists(html_file):
        webbrowser.open(f"file://{os.path.abspath(html_file)}")
        rprint(f"🌐 Đã mở [bold]{html_file}[/bold] trên trình duyệt mặc định")
    else:
        rprint(f"⚠️ Không tìm thấy file [bold]{html_file}[/bold] để mở")

if __name__ == "__main__":
    main()