import os
import pickle
import re
import json
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich import print as rprint

# Định nghĩa các biến thư mục
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
project_root = os.path.dirname(src_dir)

class FacebookCheckinScraper:
    def __init__(self, user_id: str, post_limit: int = 100):
        self.user_id = user_id
        self.profile_url = f"https://www.facebook.com/{user_id}" if not user_id.isdigit() else f"https://www.facebook.com/profile.php?id={user_id}"
        self.post_limit = post_limit
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        self._driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self._driver, 10)

    def _find_cookie_file(self) -> str:
        possible_paths = [
            os.path.join(project_root, "cookies.json"),
            os.path.join(src_dir, "cookies.json"),
            os.path.join(current_dir, "cookies.json"),
            os.path.join(os.path.dirname(current_dir), "cookies.json"),
        ]
        for path in possible_paths:
            rprint(f"- {path}")
            if os.path.exists(path):
                rprint(f"[green]Tìm thấy file cookie tại: {path}[/green]")
                return path
        raise FileNotFoundError(f"Không tìm thấy file cookie ở các vị trí:\n" + "\n".join(f"- {p}" for p in possible_paths))

    def _load_cookies(self) -> None:
        try:
            self._driver.get("https://www.facebook.com")
            sleep(2)
            self._driver.delete_all_cookies()
            cookie_path = self._find_cookie_file()
            with open(cookie_path, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    try:
                        self._driver.add_cookie(cookie)
                    except Exception as e:
                        rprint(f"[red]Lỗi khi thêm cookie: {e}[/red]")
            rprint("[green]Đã load cookies thành công[/green]")
            self._driver.refresh()
            sleep(2)
        except Exception as e:
            rprint(f"[red]Lỗi khi load cookies: {e}[/red]")
            raise

    def _load_cookies_and_refresh_driver(self) -> None:
        self._load_cookies()

    def get_checkin_posts(self):
        self._load_cookies_and_refresh_driver()
        self._driver.get(self.profile_url)
        sleep(5)
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='main']")))
        except Exception as e:
            rprint(f"[red]Lỗi: Không tìm thấy container bài viết: {e}[/red]")
            return []

        posts_data = []
        processed_posts = set()
        index = 1

        while len(posts_data) < self.post_limit:
            posts = self._driver.find_elements(By.XPATH, "//div[@role='article']//span[contains(text(), 'đã có mặt ở') or contains(text(), 'đã có mặt tại')]")
            new_posts_found = False

            for post in posts:
                try:
                    article = post.find_element(By.XPATH, "./ancestor::div[@role='article']")
                    post_id = article.get_attribute("id") or hash(article.text[:100])
                    if post_id in processed_posts:
                        continue

                    self._driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", article)
                    sleep(1)

                    post_text = article.text
                    location = article.find_element(By.XPATH, ".//strong/span/a[contains(@href, 'facebook.com')]").text
                    time_element = article.find_elements(By.XPATH, ".//span[contains(@class, 'timestampContent')]")
                    post_time = time_element[0].text if time_element else ""
                    if not post_time:
                        date_match = re.search(r"(\d+\s+[Tt]háng\s+\d+,\s+\d+)", post_text)
                        post_time = date_match.group(1) if date_match else "Không rõ thời gian"

                    posts_data.append({
                        "index": index,
                        "time": post_time,
                        "location": location
                    })
                    index += 1
                    rprint(f"[cyan]Đã xử lý bài viết check-in tại: {location} (Thời gian: {post_time})[/cyan]")

                    processed_posts.add(post_id)
                    new_posts_found = True
                    if len(posts_data) >= self.post_limit:
                        break
                except Exception as e:
                    rprint(f"[yellow]Lỗi khi xử lý bài viết: {e}[/yellow]")

            if not new_posts_found:
                self._driver.execute_script("window.scrollBy(0, 1000);")
                sleep(5)
                new_posts = self._driver.find_elements(By.XPATH, "//div[@role='article']")
                if len(new_posts) <= len(processed_posts):
                    rprint("[yellow]Không còn bài viết mới để tải[/yellow]")
                    break

        return posts_data

    def crawl(self):
        try:
            rprint(f"[cyan]Đang crawl check-in từ profile: {self.profile_url}[/cyan]")
            data = self.get_checkin_posts()
            rprint(f"[green]Đã tìm thấy {len(data)} bài viết check-in[/green]")

            # Lưu kết quả vào file
            now = datetime.now()
            timestamp = now.strftime("%Hh_%M_%d_%m_%Y")
            output_dir = os.path.join(current_dir, "..", "data")
            os.makedirs(output_dir, exist_ok=True)
            file_name = f"check_in_data_{timestamp}.json"
            output_path = os.path.join(output_dir, file_name)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            rprint(f"[green]Đã lưu dữ liệu vào: {output_path}[/green]")

            for idx, post in enumerate(data, 1):
                rprint(f"\n[bold]Bài viết {idx}:[/bold]")
                rprint(f"Thời gian: {post['time']}")
                rprint(f"Địa điểm: {post['location']}")
            return data
        finally:
            cookies = self._driver.get_cookies()
            cookies_path = os.path.join(current_dir, "..", "data", "cookies.json")
            os.makedirs(os.path.dirname(cookies_path), exist_ok=True)
            with open(cookies_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            self._driver.quit()

if __name__ == "__main__":
    user_id = "phuc.duy.980944"  # Thay bằng ID hoặc username
    scraper = FacebookCheckinScraper(user_id, post_limit=100)
    scraper.crawl()