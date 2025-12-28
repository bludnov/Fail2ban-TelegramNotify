import aiohttp
import asyncio
import aiofiles
import re
import json
import dotenv
import os
import time

dotenv.load_dotenv()

API = os.environ.get("TelegramAPI")
CHAT_ID = "вставьте свой юзер айди"

recent_bans = {}

async def sender(session, data):
    ip = data.get("query")
    country = data.get("country", "Неизвестно")
    city = data.get("city", "Неизвестно")
    isp = data.get("isp", "Неизвестно")
    org = data.get("as", "Неизвестно") # возможно не будет работать
    lat = data.get("lat")
    lon = data.get("lon")
    maps_url = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "Координат нет"

    text = (
        f"🛡 **Fail2ban-TelegramNotify**\n"
        f"!!! попытка взлома вдски\n\n"
        f"🌐 **IP:** `{ip}`\n"
        f"🌍 **Место:** {country}, {city}\n"
        f"🏢 **Провайдер:** {isp}\n"
        f"📑 **Сеть:** {org}\n\n"
        f"📍 [Посмотреть на карте]({maps_url})"
    )

    url = f"https://api.telegram.org/bot{API}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }

    try:
        async with session.post(url, json=payload) as r:
            if r.status != 200:
                print(f"TG ERR: {r.status}")
    except Exception as e:
        print(f"EXCEPTION IN SENDER: {e}")

async def checkip(line, session):
    try:
        line = line.strip()
        if not line or "Ban" not in line:
            return
        
        match = re.search(r"Ban\s+([\d\.]+)", line)
        if match:
            ip = match.group(1)
            
            current_time = time.time()
            if ip in recent_bans and current_time - recent_bans[ip] < 30:
                return
            recent_bans[ip] = current_time

            fields = "status,message,country,city,lat,lon,isp,as,query"
            async with session.get(f'http://ip-api.com/json/{ip}?fields={fields}') as r:
                if r.status == 200:
                    jsonned = await r.json()
                    await sender(session, jsonned)
                else:
                    print(f"IP-API ERR: {r.status}")
                    
    except Exception as e:
        print(f"EXCEPTION IN CHECKIP: {e}")

async def reader(session):
    log_path = '/var/log/fail2ban.log'
    print(f"[$] Fail2ban-TelegramNotify запущен: {log_path}...")
    
    async with aiofiles.open(log_path, mode='r') as f:
        await f.seek(0, 2)
        while True:
            line = await f.readline()
            if not line:
                await asyncio.sleep(0.5)
                continue
            await checkip(line, session)

async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(reader(session))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[$] Fail2ban-TelegramNotify отключён")
