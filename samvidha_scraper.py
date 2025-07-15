from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_attendance_summary(username: str, password: str) -> str:
    """Logs in, scrapes attendance and returns a formatted summary string."""
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # opts.add_argument("--headless")  # enable in production

    driver = webdriver.Chrome(options=opts)
    try:
        driver.get("https://samvidha.iare.ac.in/")
        time.sleep(2)

        driver.find_element(By.ID, "txt_uname").send_keys(username)
        driver.find_element(By.ID, "txt_pwd").send_keys(password)
        driver.find_element(By.ID, "but_submit").click()
        time.sleep(3)

        driver.get("https://samvidha.iare.ac.in/home?action=course_content")
        time.sleep(5)

        page = driver.find_element(By.TAG_NAME, "body").text.upper()
        p = page.count("PRESENT")
        a = page.count("ABSENT")
        total = p + a

        if total:
            pct = round(p / total * 100, 2)
            return (f"✅ Present: {p}\n❌ Absent: {a}\n"
                    f"📈 Attendance %: {pct}")
        return "⚠️ No attendance rows found."
    except Exception as e:
        return f"❌ Error while scraping:\n{e}"
    finally:
        driver.quit()
