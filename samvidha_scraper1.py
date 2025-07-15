from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_attendance_summary(username, password):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless')  # Optional after testing

    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: Login
        driver.get("https://samvidha.iare.ac.in/")
        time.sleep(2)

        driver.find_element(By.ID, "txt_uname").send_keys(username)
        driver.find_element(By.ID, "txt_pwd").send_keys(password)
        driver.find_element(By.ID, "but_submit").click()
        time.sleep(3)

        print("✅ Logged in successfully")

        # Step 2: Navigate to attendance page
        driver.get("https://samvidha.iare.ac.in/home?action=course_content")
        time.sleep(5)

        # Step 3: Get full visible page text
        full_text = driver.find_element(By.TAG_NAME, "body").text

        # Step 4: Count occurrences of PRESENT and ABSENT
        present_count = full_text.upper().count("PRESENT")
        absent_count = full_text.upper().count("ABSENT")
        total = present_count + absent_count

        print("\n📄 Extracted Page Text (trimmed):")
        print("\n".join(full_text.splitlines()[:15]) + "\n...")  # Show first 15 lines

        print("\n📊 Attendance Summary:")
        print(f"✅ Present: {present_count}")
        print(f"❌ Absent: {absent_count}")

        if total > 0:
            percentage = round((present_count / total) * 100, 2)
            print(f"📈 Attendance Percentage: {percentage}%")
        else:
            print("⚠️ No attendance data found (0 present & absent combined).")

        driver.quit()

    except Exception as e:
        print("❌ Error:", e)
        driver.quit()

if __name__ == "__main__":
    username = "23951a67d8"
    password = "sanjay89191"
    get_attendance_summary(username, password)

