import subprocess
from time import time
import typer
from dotenv import load_dotenv
from rich import print as rprint
import os
import glob
import json
import networkx as nx
import matplotlib.pyplot as plt


from .facebook.account.account_friend import AccountFriend
from .facebook.login import FacebookLogIn
from .logs import Logs
from .repository import crawlerqueue_repository
from .scripts.urlid import get_account_id
from typing_extensions import Annotated
from .facebook.account.account_friend_layer import AccountFriendLayer
from .analytics.graph import create_relationship_graph
from selenium.webdriver.chrome.options import Options

load_dotenv()
logs = Logs()
app = typer.Typer(
    pretty_exceptions_enable=False,
)

""" Analytics """

def create_graph_from_friends_data(data_dir):
    """
    Create a graph of connections between users based on their friends data
    from a specific friends_data directory
    
    Args:
        data_dir (str): Path to the friends_data directory
    """
    G = nx.DiGraph()
    
    # Đọc file JSON chính trong thư mục
    json_files = glob.glob(os.path.join(data_dir, "*.json"))
    if not json_files:
        rprint(f"Không tìm thấy file dữ liệu nào trong thư mục {data_dir}")
        return None
    
    # Đọc dữ liệu từ file JSON
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                
                # Thêm node gốc
                root_user = data.get("root_user") or data.get("account_id")
                if not root_user:
                    continue
                
                # Xử lý dữ liệu chính
                main_data = data.get("data", data)
                if not main_data:
                    continue
                
                # Thêm node gốc vào đồ thị
                G.add_node(root_user, label=root_user)
                
                # Xử lý danh sách bạn bè
                process_friends_data(G, main_data, root_user)
                
            except json.JSONDecodeError:
                rprint(f"Không thể đọc file {json_file}")
                continue
    
    if len(G.nodes) == 0:
        rprint("Không có dữ liệu để vẽ đồ thị")
        return None
    
    # Vẽ đồ thị
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.3)
    labels = {node: G.nodes[node].get('label', node) for node in G.nodes()}
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=800, 
            node_color='skyblue', font_size=8, font_weight='bold',
            edge_color='gray', width=0.5, arrows=True)
    
    plt.title(f"Đồ thị quan hệ bạn bè từ {data_dir}")
    plt.show()
    
    return G

def process_friends_data(G, data, parent_id):
    """
    Đệ quy xử lý dữ liệu bạn bè và thêm vào đồ thị
    
    Args:
        G (nx.DiGraph): Đồ thị
        data (dict): Dữ liệu bạn bè
        parent_id (str): ID của node cha
    """
    friends = data.get("friends", [])
    if not friends:
        return
    
    for friend in friends:
        # Lấy ID của bạn bè
        friend_id = friend.get("username") or friend.get("uid") or friend.get("id")
        if not friend_id:
            continue
        
        # Tên hiển thị
        friend_name = friend.get("name", friend_id)
        
        # Thêm node bạn bè vào đồ thị
        G.add_node(friend_id, label=friend_name)
        
        # Thêm cạnh kết nối
        G.add_edge(parent_id, friend_id)
        
        # Xử lý dữ liệu bạn bè của bạn bè (nếu có)
        friends_data = friend.get("friends_data")
        if friends_data:
            process_friends_data(G, friends_data, friend_id)

@app.command()
def graph() -> None:
    """Create a graph of connections between Person objects based on their Friends"""
    create_relationship_graph()


@app.command()
def graph_friends_data() -> None:
    """Vẽ đồ thị quan hệ từ dữ liệu trong thư mục friends_data"""
    # Tìm tất cả các thư mục có dạng friends_data_*
    data_dirs = glob.glob("friends_data_*")
    
    if not data_dirs:
        rprint("❌ Không tìm thấy thư mục dữ liệu nào có dạng friends_data_*")
        return
    
    rprint("[bold]Danh sách thư mục dữ liệu:[/bold]")
    for i, dir_name in enumerate(data_dirs, 1):
        # Hiển thị thông tin về thư mục
        json_files = glob.glob(os.path.join(dir_name, "*.json"))
        num_files = len(json_files)
        
        # Lấy thông tin về thời gian tạo thư mục
        try:
            creation_time = os.path.getctime(dir_name)
            from datetime import datetime
            time_str = datetime.fromtimestamp(creation_time).strftime("%d/%m/%Y %H:%M:%S")
        except:
            time_str = "Không xác định"
            
        rprint(f"{i}. [bold]{dir_name}[/bold] - {num_files} file - Tạo lúc: {time_str}")
    
    # Cho phép người dùng chọn thư mục
    choice = typer.prompt(
        "Chọn số thứ tự thư mục để vẽ đồ thị",
        type=int
    )
    
    # Kiểm tra lựa chọn hợp lệ
    if choice < 1 or choice > len(data_dirs):
        rprint("❌ Lựa chọn không hợp lệ")
        return
    
    selected_dir = data_dirs[choice - 1]
    rprint(f"Đang vẽ đồ thị từ dữ liệu trong thư mục [bold]{selected_dir}[/bold]...")
    
    # Vẽ đồ thị
    time_start = time()
    graph = create_graph_from_friends_data(selected_dir)
    time_end = time()
    
    if graph:
        rprint(f"✅ Vẽ đồ thị thành công sau {time_end - time_start:.2f} giây")
        rprint(f"   - Số node: {len(graph.nodes())}")
        rprint(f"   - Số cạnh: {len(graph.edges())}")
    else:
        rprint("❌ Không thể vẽ đồ thị từ dữ liệu trong thư mục này")


@app.command()
def friend_crawler(
    user_id: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
    max_friends_input = typer.prompt(
        "Nhập số lượng bạn bè cần thu thập (nhấn Enter để thu thập tất cả)",
        default="",
        type=str,
        show_default=False
    )
    max_friends = None
    if max_friends_input.strip():
        try:
            max_friends = int(max_friends_input)
            if max_friends <= 0:
                typer.echo("Số lượng bạn bè phải lớn hơn 0. Sẽ thu thập tất cả bạn bè.")
                max_friends = None
        except ValueError:
            typer.echo("Đầu vào không hợp lệ. Sẽ thu thập tất cả bạn bè.")
            max_friends = None

    rprint(f"Bắt đầu thu thập dữ liệu từ {user_id}")
    scraper = AccountFriend(user_id=user_id, max_friends=max_friends, crawler=True)
    
    time_start = time()
    scraper.pipeline()
    time_end = time()
    
    if scraper.is_pipeline_successful:
        rprint(f"✅ Thu thập thành công sau {time_end - time_start} giây ✅")
        
        users = crawlerqueue_repository.get_crawler_queues_status_false()
        while len(users) > 0:
            for user in users:
                user_id = get_account_id(user.url)
                rprint(f"Đang thu thập dữ liệu từ {user_id}")
                scraper = AccountFriend(user_id=user_id, max_friends=max_friends, crawler=True)
                scraper.pipeline()

                if scraper.is_pipeline_successful:
                    crawlerqueue_repository.delete_crawler_queue(user.id)
            
            users = crawlerqueue_repository.get_crawler_queues_status_false()
    else:
        rprint(f"❌ Không thể thu thập dữ liệu từ người dùng chính ❌")

@app.command()
def display_queue() -> None:
    queue_data = crawlerqueue_repository.get_crawler_queues_status_false()
    if len(queue_data) == 0:
        rprint("[bold] Queue is empty. [/bold]")
    else:
        rprint(
            f"[bold] Found {len(queue_data)} queue objects with status False: [/bold]"
        )
        for queue in queue_data:
            rprint(f"- [bold] ID: {queue.id} [/bold] {queue.url}")

@app.command()
def delete_queue_object(
    id: Annotated[int, typer.Argument(help="CrawlerQueue id")]
) -> None:
    if crawlerqueue_repository.delete_crawler_queue(id):
        rprint("✅ Queue object deleted ✅")
    else:
        rprint("❌Failed to delete Queue object from database. Please try again.❌")

@app.command()
def clear_queue() -> None:
    delete = crawlerqueue_repository.delete_all()
    if delete:
        rprint("✅ Queue cleared ✅")
    else:
        rprint("❌Queue not cleared, please try again❌")

@app.command()
def login_2_step() -> None:
    # Tạo ChromeOptions luôn non-headless
    options = Options()
    options.add_argument("--start-maximized")  # Phóng to cửa sổ
    options.add_argument("--disable-notifications")  # Tắt thông báo
    options.add_argument("--disable-extensions")  # Tương tự Scraper
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-web-security")
    options.add_argument(
        "--disable-features=IsolateOrigins,site-per-process"
    )
    options.add_argument(
        "--enable-features=NetworkService,NetworkServiceInProcess"
    )
    options.add_argument("--profile-directory=Default")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # Không thêm --headless để luôn hiển thị giao diện

    # Khởi tạo FacebookLogIn với custom_options
    facebook = FacebookLogIn(custom_options=options)

    time_start = time()
    facebook.login_2_step_pipeline()
    time_end = time()

    if facebook.is_pipeline_successful:
        rprint(f"✅Logging successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Logging failed after {time_end - time_start} seconds ❌")

@app.command()
def login() -> None:
    facebook = FacebookLogIn()

    time_start = time()
    facebook.login_no_verification_pipeline()
    time_end = time()

    if facebook.is_pipeline_successful:
        rprint(f"✅Logging successful after {time_end - time_start} seconds ✅")
    else:
        rprint(f"❌Logging failed after {time_end - time_start} seconds ❌")

@app.command()
def friend_layer_crawler(
    user_id: Annotated[str, typer.Argument(help="Facebook user id")]
) -> None:
    max_layers = typer.prompt(
        "Nhập số tầng cần crawl (0 = chỉ lấy bạn bè trực tiếp)",
        type=int
    )
    
    if max_layers < 0:
        typer.echo("Số tầng phải lớn hơn hoặc bằng 0")
        return
    
    # Yêu cầu nhập số bạn bè cần thu thập cho mỗi node ở từng tầng
    friends_per_node_per_layer = []
    typer.echo(f"\nNhập số bạn bè cần thu thập cho mỗi node ở từng tầng:")
    
    for layer in range(max_layers + 1):
        while True:
            friends = typer.prompt(
                f"Tầng {layer}{' (bạn bè trực tiếp)' if layer == 0 else ''}: "
                f"Số bạn bè cần thu thập cho mỗi node",
                type=int
            )
            if friends > 0:
                friends_per_node_per_layer.append(friends)
                break
            typer.echo("Số lượng bạn bè phải lớn hơn 0. Vui lòng nhập lại.")
    
    # Hiển thị thông tin cấu hình và dự đoán số lượng tài khoản
    total_accounts = 0
    num_nodes = []  # Số node ở mỗi tầng
    typer.echo(f"\nThông tin crawl:")
    typer.echo(f"- Số tầng: {max_layers}")
    typer.echo(f"\nSố node và bạn bè cần thu thập ở từng tầng:")
    
    for layer in range(max_layers + 1):
        friends = friends_per_node_per_layer[layer]
        if layer == 0:
            nodes_in_layer = friends  # Tầng 0: Số node = số bạn bè trực tiếp
            typer.echo(
                f"- Tầng 0 (bạn bè trực tiếp): {nodes_in_layer} node "
                f"(mỗi node gốc thu thập {friends} bạn bè)"
            )
        else:
            nodes_in_layer = num_nodes[layer - 1] * friends_per_node_per_layer[layer]  # Sử dụng số bạn bè của tầng hiện tại
            typer.echo(
                f"- Tầng {layer}: {nodes_in_layer} node "
                f"(mỗi node thu thập {friends} bạn bè)"
            )
        num_nodes.append(nodes_in_layer)
        total_accounts += nodes_in_layer
    
    typer.echo(f"\n- Tổng số tài khoản dự kiến: {total_accounts}")
    
    if not typer.confirm("Bạn có muốn tiếp tục không?"):
        return
    
    rprint(f"Bắt đầu crawl dữ liệu từ {user_id} với {max_layers} tầng")
    crawler = AccountFriendLayer(user_id, max_layers, friends_per_node_per_layer)
    crawler.crawl()
