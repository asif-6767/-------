#!/usr/bin/env python3

import os
import sys
import time
import json
import random
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

# ==================== COLORS ====================
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
C = '\033[96m'
M = '\033[95m'
W = '\033[97m'
N = '\033[0m'

# ==================== FUNCTIONS ====================
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def loading(text, sec=1.5):
    frames = ['⣾','⣽','⣻','⢿','⡿','⣟','⣯','⣷']
    end = time.time() + sec
    i = 0
    while time.time() < end:
        sys.stdout.write(f'\r{C}{frames[i%8]} {text}...{N}')
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write('\r' + ' '*50 + '\r')

def matrix(sec=1.2):
    chars = "⣿⣶⣤⣀⣠⣴⣶⣿"
    end = time.time() + sec
    while time.time() < end:
        line = ''.join(random.choice(chars) for _ in range(40))
        sys.stdout.write(f'\r{G}{line}{N}')
        sys.stdout.flush()
        time.sleep(0.04)
    sys.stdout.write('\r' + ' '*50 + '\r')

def box(txt, col=G):
    w = 50
    print(f"{col}┌{'─'*(w-2)}┐{N}")
    print(f"{col}│ {txt[:48]:<48} │{N}")
    print(f"{col}└{'─'*(w-2)}┘{N}")

# ==================== BANNER ====================
def banner():
    clear()
    matrix()
    print(f"""
{C}╔══════════════════════════════════════════════════════════════╗
{C}║{W}  ████████╗██╗  ██╗██╗  ████████╗ ██████╗ ██╗  ██╗{C} ║
{C}║{W}  ╚══██╔══╝██║  ██║██║  ╚══██╔══╝██╔═══██╗██║ ██╔╝{C} ║
{C}║{W}     ██║   ███████║██║     ██║   ██║   ██║█████╔╝ {C} ║
{C}║{W}     ██║   ██╔══██║██║     ██║   ██║   ██║██╔═██╗ {C} ║
{C}║{W}     ██║   ██║  ██║██║     ██║   ╚██████╔╝██║  ██╗{C} ║
{C}║{W}     ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝    ╚═════╝ ╚═╝  ╚═╝{C} ║
{C}╠══════════════════════════════════════════════════════════════╣
{C}║{Y}        TikTok Data Toolkit v3.0{C}                         ║
{C}║{M}     ⚡ by ᴀꜱɪꜰ ɪꜱʟᴀᴍ ⚡{C}                           ║
{C}╚══════════════════════════════════════════════════════════════╝{N}
""")

def menu():
    print(f"""
{G}┌────────────────────────────────────────────────────────┐
{G}│{W}  ┌──────────────────────────────────────────┐  {G}│
{G}│{W}  │{C}  1{W}  ›  {Y}User Lookup{W}              {C}👤{W}  │  {G}│
{G}│{W}  │{C}  2{W}  ›  {Y}Bulk Scraper{W}              {C}📊{W}  │  {G}│
{G}│{W}  │{C}  3{W}  ›  {Y}Exit{W}                       {C}🚪{W}  │  {G}│
{G}│{W}  └──────────────────────────────────────────┘  {G}│
{G}└────────────────────────────────────────────────────────┘{N}
""")

# ==================== MAIN SCRAPER ====================
def get_info(user):
    if user.startswith('@'):
        user = user[1:]
    
    url = f"https://www.tiktok.com/@{user}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
    except:
        return None
    
    if r.status_code != 200:
        return None
    
    html = r.text
    
    patterns = {
        'id': r'"id":"(\d+)"',
        'user': r'"uniqueId":"(.*?)"',
        'name': r'"nickname":"(.*?)"',
        'followers': r'"followerCount":(\d+)',
        'following': r'"followingCount":(\d+)',
        'likes': r'"heartCount":(\d+)',
        'videos': r'"videoCount":(\d+)',
        'bio': r'"signature":"(.*?)"',
        'verified': r'"verified":(true|false)',
        'private': r'"privateAccount":(true|false)',
        'region': r'"region":"([^"]*)"',
        'pic': r'"avatarLarger":"(.*?)"'
    }
    
    info = {}
    for k, p in patterns.items():
        m = re.search(p, html)
        info[k] = m.group(1) if m else None
    
    if info.get('pic'):
        info['pic'] = info['pic'].replace('\\u002F', '/')
    
    # Social links
    links = []
    bio = info.get('bio') or ''
    
    # Bio links
    for link in re.findall(r'"bioLink":{"link":"([^"]+)"', html):
        clean = link.replace('\\u002F', '/')
        if clean not in links:
            links.append(clean)
    
    # Span links
    for span in re.findall(r'<span[^>]*class="[^"]*SpanLink[^"]*">([^<]+)</span>', html):
        if '.' in span and ' ' not in span and span not in links:
            links.append(span)
    
    # Instagram
    ig = re.search(r'[iI][gG]:\s*@?([a-zA-Z0-9._]+)', bio)
    if ig:
        links.append(f"📸 IG: @{ig.group(1)}")
    
    # YouTube
    yt = re.search(r'([yY][tT]|[yY]outube):\s*@?([a-zA-Z0-9._]+)', bio)
    if yt:
        links.append(f"▶️ YT: @{yt.group(2)}")
    
    # Twitter/X
    tw = re.search(r'([tT]witter|[xX]):\s*@?([a-zA-Z0-9._]+)', bio)
    if tw:
        links.append(f"🐦 X: @{tw.group(2)}")
    
    # Email
    em = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', bio)
    if em:
        links.append(f"✉️ {em.group(0)}")
    
    info['links'] = links
    return info

# ==================== DISPLAY ====================
def show_info(info):
    if not info:
        box("✗ No data found", R)
        return
    
    print(f"\n{G}╔{'═'*48}╗{N}")
    print(f"{G}║{W}  📊 PROFILE DATA{G}{' '*34}║{N}")
    print(f"{G}╚{'═'*48}╝{N}\n")
    
    print(f"{C}┌{'─'*48}┐{N}")
    print(f"{C}│{Y}  BASIC INFO{C}{' '*36}│{N}")
    print(f"{C}├{'─'*48}┤{N}")
    
    fields = [
        ('ID', info.get('id')),
        ('User', f"@{info.get('user')}"),
        ('Name', info.get('name')),
        ('Verified', '✅' if info.get('verified')=='true' else '❌'),
        ('Private', '🔒' if info.get('private')=='true' else '🔓'),
        ('Region', info.get('region'))
    ]
    
    for label, val in fields:
        if val:
            v = str(val)[:30]
            print(f"{C}│ {W}{label:<6}{C}: {G}{v:<40}{C}│{N}")
    
    print(f"{C}└{'─'*48}┘{N}\n")
    
    print(f"{C}┌{'─'*48}┐{N}")
    print(f"{C}│{Y}  STATS{C}{' '*40}│{N}")
    print(f"{C}├{'─'*48}┤{N}")
    
    stats = [
        ('👥 Followers', info.get('followers')),
        ('👤 Following', info.get('following')),
        ('❤️ Likes', info.get('likes')),
        ('🎬 Videos', info.get('videos'))
    ]
    
    for label, val in stats:
        if val:
            print(f"{C}│ {W}{label:<12}{C}: {G}{str(val):>10}{C}  │{N}")
    
    print(f"{C}└{'─'*48}┘{N}\n")
    
    bio = info.get('bio')
    if bio and bio != 'No signature found':
        print(f"{C}┌{'─'*48}┐{N}")
        print(f"{C}│{Y}  BIO{C}{' '*44}│{N}")
        print(f"{C}├{'─'*48}┤{N}")
        b = bio.replace('\\n',' ').replace('\\r','')
        if len(b) > 42:
            b = b[:39] + '...'
        print(f"{C}│ {W}{b:<46} │{N}")
        print(f"{C}└{'─'*48}┘{N}\n")
    
    links = info.get('links', [])
    if links:
        print(f"{C}┌{'─'*48}┐{N}")
        print(f"{C}│{Y}  SOCIAL{C}{' '*40}│{N}")
        print(f"{C}├{'─'*48}┤{N}")
        for link in links[:4]:
            if len(link) > 42:
                link = link[:39] + '...'
            print(f"{C}│ {G}•{W} {link:<44} │{N}")
        print(f"{C}└{'─'*48}┘{N}")
    
    user = info.get('user')
    if user:
        print(f"\n{C}🔗 {W}https://www.tiktok.com/@{user}{N}")

def download_pic(url, user):
    if not url or not url.startswith('http'):
        box("No profile picture", Y)
        return
    
    try:
        if not os.path.exists('pp_images'):
            os.makedirs('pp_images')
        
        loading("Downloading", 1.5)
        r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        
        if r.status_code == 200:
            fname = f"pp_images/{user}.jpg"
            with open(fname, 'wb') as f:
                f.write(r.content)
            size = len(r.content)/1024
            box(f"✓ Saved: {fname} ({size:.1f}KB)", G)
        else:
            box("✗ Download failed", R)
    except Exception as e:
        box(f"✗ Error: {str(e)[:30]}", R)

# ==================== BULK ====================
def bulk():
    print(f"\n{C}╔{'═'*48}╗{N}")
    print(f"{C}║{Y}  📊 BULK SCRAPER{C}{' '*34}║{N}")
    print(f"{C}╚{'═'*48}╝{N}")
    
    print(f"\n{W}Enter usernames (blank line to finish):{N}")
    users = []
    while True:
        line = input(f"{C}> {W}")
        if not line and users:
            break
        if line:
            users.append(line.strip())
    
    if not users:
        box("No usernames", Y)
        return
    
    print(f"\n{W}Processing {len(users)} users...{N}\n")
    results = []
    
    for i, user in enumerate(users, 1):
        print(f"{C}[{i}/{len(users)}]{W} @{user}{N}")
        info = get_info(user)
        if info:
            results.append(info)
            print(f"{G}  ✓ Success{N}")
        else:
            print(f"{R}  ✗ Failed{N}")
        time.sleep(0.3)
    
    if results:
        fname = f"bulk_{int(time.time())}.json"
        with open(fname, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n{G}✓ Saved: {fname}{N}")
    
    print(f"\n{C}✓ {len(results)}/{len(users)} successful{N}")

# ==================== MAIN ====================
def main():
    while True:
        try:
            banner()
            menu()
            choice = input(f"\n{C}┌─{W}[{G}Select{W}]{C}\n└──╼ {W}")
            
            if choice == '1':
                banner()
                print(f"\n{C}┌{'─'*40}┐{N}")
                print(f"{C}│{Y}  USER LOOKUP{C}{' '*27}│{N}")
                print(f"{C}└{'─'*40}┘{N}")
                
                user = input(f"\n{W}Username: {C}").strip()
                if user:
                    loading(f"Fetching @{user}", 2)
                    info = get_info(user)
                    if info:
                        show_info(info)
                        print(f"\n{Y}Download profile pic? (y/n): {W}")
                        if input().lower() == 'y':
                            download_pic(info.get('pic'), info.get('user') or user)
                        input(f"\n{DIM}Press Enter...{N}")
                    else:
                        box("✗ No data found", R)
                        input(f"\n{DIM}Press Enter...{N}")
                else:
                    box("✗ No username", Y)
                    input(f"\n{DIM}Press Enter...{N}")
            
            elif choice == '2':
                banner()
                bulk()
                input(f"\n{DIM}Press Enter...{N}")
            
            elif choice == '3':
                print(f"\n{C}╔{'═'*40}╗{N}")
                print(f"{C}║{Y}  👋 Goodbye!{C}{' '*28}║{N}")
                print(f"{C}║{M}  by ᴀꜱɪꜰ ɪꜱʟᴀᴍ{C}{' '*23}║{N}")
                print(f"{C}╚{'═'*40}╝{N}")
                loading("Exiting", 1)
                sys.exit(0)
            
            else:
                box("✗ Invalid option", R)
                input(f"\n{DIM}Press Enter...{N}")
        
        except KeyboardInterrupt:
            print(f"\n\n{Y}⚠ Interrupted{N}")
            sys.exit(0)
        except Exception as e:
            box(f"✗ Error: {str(e)[:30]}", R)
            input(f"\n{DIM}Press Enter...{N}")

if __name__ == "__main__":
    main()
