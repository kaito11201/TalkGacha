from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests

FILE_NAME = "トークテーマガチャ.txt"
URL = "https://talkgacha.com/"

# お題系
REFRESH_INTERVAL = 60 * 1 # お題を出す間隔(単位は秒)
REFRESH_NUM = 100 # お題を出す回数
SPLIT_NUM = 15 # お題の文字を何文字で改行するか

# 棒読み系(棒読みちゃんの設定を見てね)
VOICE = 0
VOLUME = -1
SPEED = -1
TONE = -1

def setting_driver():
  options = webdriver.ChromeOptions()
  options.add_argument("--headless")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--no-sandbox")

  driver = webdriver.Chrome(
      ChromeDriverManager().install(),
      options=options
  )
  
  driver.get(URL)
  
  return driver

def get_text(driver):
  driver.implicitly_wait(5)
  element = driver.find_element(By.CLASS_NAME, "talk-theme-text")
  return element.text

def output_file(driver, text):
  split_texts = [text[x:x+SPLIT_NUM] for x in range(0, len(text), SPLIT_NUM)]

  f = open(FILE_NAME, "w", encoding='utf-8')
  
  print("【トークテーマ】", file=f)
  for split_text in split_texts:
    print(split_text, file=f)

  f.close()

def speak_bouyomi(text, voice=0, volume=20, speed=-1, tone=-1):
  
  try:
    res = requests.get(
        'http://localhost:50080/Talk',
        params={
            'text': text,
            'voice': voice,
            'volume': volume,
            'speed': speed,
            'tone': tone})
    return res.status_code
  except requests.exceptions.ConnectionError:
    print("棒読みちゃんが起動されていない可能性があります。")

if __name__ == "__main__":
  
  driver = setting_driver()
  
  for num in range(REFRESH_NUM):
    text = get_text(driver)
    output_file(driver, text)
    speak_bouyomi(text, VOICE, VOLUME, SPEED, TONE)
    if num == REFRESH_NUM - 1:
      speak_bouyomi("これが最後のお題になります。", VOICE, VOLUME, SPEED, TONE)
      
    time.sleep(REFRESH_INTERVAL)
    driver.refresh()
    
  driver.close()