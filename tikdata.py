#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import random
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

# ============= COLOR SYSTEM =============
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

# ============= TERMINAL UTILITIES =============
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def center_text(text, width=None):
    if width is None:
        width = get_terminal_width()
    padding = max(0, (width - len(text)) // 2)
    return ' ' * padding + text

def hr(char='═', width=None):
    if width is None:
        width = get_terminal_width()
    return char * min(width, 80)

# ============= ANIMATIONS =============
def loading(text="Processing", duration=1.5):
    frames = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f'\r{Colors.CYAN}{frames[i % len(frames)]} {text}...{Colors.RESET}')
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()

def matrix_effect(duration=1.5):
    chars = "⣿⣶⣤⣀⣠⣴⣶⣿"
    end = time.time() + duration
    while time.time() < end:
        line = ''.join(random.choice(chars) for _ in range(40))
        sys.stdout.write(f'\r{Colors.GREEN}{line}{Colors.RESET}')
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()

def progress_bar(percent, width=30):
    filled = int(width * percent / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{Colors.CYAN}{bar}{Colors.RESET}] {percent}%"

# ============= BANNER =============
def show_banner():
    clear()
    matrix_effect(0.8)
    
    banner = f"""
{Colors.BG_BLACK}{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
{Colors.BG_BLACK}{Colors.CYAN}║{Colors.WHITE}  ████████╗██╗  ██╗██╗  ████████╗ ██████╗ ██╗  ██╗{Colors.CYAN} ║
{Colors.BG_BLACK}{Colors.CYAN}║{Colors.WHITE}  ╚══██╔══╝██║  ██║██║  ╚══██╔══╝██╔═══██╗██║ ██╔╝{Colors.CYAN} ║
{Colors.BG_BLACK}{Colors.CYAN}║{Colors.WHITE}     ██║   ███████║██║     ██║   ██║   ██║█████╔╝ {Colors.CYAN} ║
{Colors.BG_BLACK}{Colors.CYAN}║{Colors.WHITE}     ██║   ██╔══██║██║     ██║   ██║   ██║██╔═██╗ {Colors.CYAN} ║
{Colors.BG_BLACK}{Colors.CYAN}║{Colors.WHITE}     ██║   ██║  ██║██║     ██║   ╚██████╔╝██║  ██╗{Colors.CYAN} ║
{Colors.BG_BLACK}{Colors.CYAN}║{Colors.WHITE}     ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝    ╚═════╝ ╚═╝  ╚═╝{Colors.CYAN} ║
{Colors.BG_BLACK}{Colors.CYAN}╠══════════════════════════════════════════════════════════════╣
{Colors.BG_BLACK}{Colors.CYAN}║{Colors.YELLOW}        Public Data Toolkit v3.0{Colors.CYAN}                         ║
{Colors.BG_BLACK}{Colors.CYAN}║{Colors.MAGENTA}     ⚡ by ᴀꜱɪꜰ ɪꜱʟᴀᴍ ⚡{Colors.CYAN}                           ║
{Colors.BG_BLACK}{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

# ============= MENU =============
def show_menu():
    menu = f"""
{Colors.BG_BLACK}{Colors.GREEN}┌────────────────────────────────────────────────────────┐
{Colors.BG_BLACK}{Colors.GREEN}│{Colors.WHITE}  ╭──────────────────────────────────────────╮  {Colors.GREEN}│
{Colors.BG_BLACK}{Colors.GREEN}│{Colors.WHITE}  │{Colors.CYAN}  1{Colors.WHITE}  ›  {Colors.YELLOW}User Lookup{Colors.WHITE}              {Colors.CYAN}👤{Colors.WHITE}  │  {Colors.GREEN}│
{Colors.BG_BLACK}{Colors.GREEN}│{Colors.WHITE}  │{Colors.CYAN}  2{Colors.WHITE}  ›  {Colors.YELLOW}Bulk Scraper{Colors.WHITE}              {Colors.CYAN}📊{Colors.WHITE}  │  {Colors.GREEN}│
{Colors.BG_BLACK}{Colors.GREEN}│{Colors.WHITE}  │{Colors.CYAN}  3{Colors.WHITE}  ›  {Colors.YELLOW}Exit{Colors.WHITE}                       {Colors.CYAN}🚪{Colors.WHITE}  │  {Colors.GREEN}│
{Colors.BG_BLACK}{Colors.GREEN}│{Colors.WHITE}  ╰──────────────────────────────────────────╯  {Colors.GREEN}│
{Colors.BG_BLACK}{Colors.GREEN}└────────────────────────────────────────────────────────┘{Colors.RESET}
"""
    print(menu)

# ============= YOUR ORIGINAL FUNCTION (100% WORKING) =============
def get_user_info(identifier, by_id=False):
    if by_id:
        url = f"https://www.tiktok.com/@{identifier}"
    else:
        if identifier.startswith('@'):
            identifier = identifier[1:]
        url = f"https://www.tiktok.com/@{identifier}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
    except:
        return None

    if response.status_code == 200:
        html_content = response.text
        
        try:
            soup = BeautifulSoup(html_content, 'lxml')
        except:
            soup = BeautifulSoup(html_content, 'html.parser')
        
        patterns = {
            'user_id': r'"webapp.user-detail":{"userInfo":{"user":{"id":"(\d+)"',
            'unique_id': r'"uniqueId":"(.*?)"',
            'nickname': r'"nickname":"(.*?)"',
            'followers': r'"followerCount":(\d+)',
            'following': r'"followingCount":(\d+)',
            'likes': r'"heartCount":(\d+)',
            'videos': r'"videoCount":(\d+)',
            'signature': r'"signature":"(.*?)"',
            'verified': r'"verified":(true|false)',
            'secUid': r'"secUid":"(.*?)"',
            'commentSetting': r'"commentSetting":(\d+)',
            'privateAccount': r'"privateAccount":(true|false)',
            'region': r'"ttSeller":false,"region":"([^"]*)"',
            'heart': r'"heart":(\d+)',
            'diggCount': r'"diggCount":(\d+)',
            'friendCount': r'"friendCount":(\d+)',
            'profile_pic': r'"avatarLarger":"(.*?)"'
        }
        
        info = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, html_content)
            info[key] = match.group(1) if match else None
        
        if "profile_pic" in info and info['profile_pic']:
            info['profile_pic'] = info['profile_pic'].replace('\\u002F', '/')
        
        # Extract social links
        social_links = []
        bio = info.get('signature') or ""
        
        # Bio links
        bio_link_pattern = r'"bioLink":{"link":"([^"]+)","risk":(\d+)}'
        for link, risk in re.findall(bio_link_pattern, html_content):
            clean = link.replace('\\u002F', '/')
            if clean not in social_links:
                social_links.append(clean)
        
        # Span links
        for span in re.findall(r'<span[^>]*class="[^"]*SpanLink[^"]*">([^<]+)</span>', html_content):
            if '.' in span and ' ' not in span and span not in social_links:
                social_links.append(span)
        
        # Instagram
        ig = re.search(r'[iI][gG]:\s*@?([a-zA-Z0-9._]+)', bio)
        if ig:
            social_links.append(f"📸 IG: @{ig.group(1)}")
        
        # YouTube
        yt = re.search(r'([yY][tT]|[yY]outube):\s*@?([a-zA-Z0-9._]+)', bio)
        if yt:
            social_links.append(f"▶️ YT: @{yt.group(2)}")
        
        # Twitter/X
        tw = re.search(r'([tT]witter|[xX]):\s*@?([a-zA-Z0-9._]+)', bio)
        if tw:
            social_links.append(f"🐦 X: @{tw.group(2)}")
        
        # Email
        email = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', bio)
        if email:
            social_links.append(f"✉️ {email.group(0)}")
        
        info['social_links'] = social_links
        return info
    else:
        return None

# ============= DISPLAY FUNCTIONS =============
def box(text, color=Colors.CYAN, width=None):
    if width is None:
        width = get_terminal_width()
    width = min(width, 60)
    text = text[:width-4]
    print(f"{color}┌{'─' * (width-2)}┐{Colors.RESET}")
    print(f"{color}│ {text:<{width-4}} │{Colors.RESET}")
    print(f"{color}└{'─' * (width-2)}┘{Colors.RESET}")

def display_user(info):
    if not info:
        box("✗ No data found", Colors.RED)
        return
    
    width = min(get_terminal_width(), 60)
    
    # Header
    print(f"\n{Colors.GREEN}╔{'═' * (width-2)}╗{Colors.RESET}")
    print(f"{Colors.GREEN}║{Colors.WHITE}  📊 PROFILE DATA{Colors.GREEN}{' ' * (width-18)}║{Colors.RESET}")
    print(f"{Colors.GREEN}╚{'═' * (width-2)}╝{Colors.RESET}\n")
    
    # Basic Info
    print(f"{Colors.CYAN}┌{'─' * (width-2)}┐{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.YELLOW}  BASIC INFO{Colors.CYAN}{' ' * (width-15)}│{Colors.RESET}")
    print(f"{Colors.CYAN}├{'─' * (width-2)}┤{Colors.RESET}")
    
    fields = [
        ('ID', info.get('user_id')),
        ('User', f"@{info.get('unique_id')}"),
        ('Name', info.get('nickname')),
        ('Verified', '✅' if info.get('verified') == 'true' else '❌'),
        ('Private', '🔒' if info.get('privateAccount') == 'true' else '🔓'),
        ('Region', info.get('region'))
    ]
    
    for label, value in fields:
        if value:
            val = str(value)[:30]
            print(f"{Colors.CYAN}│ {Colors.WHITE}{label:<6}{Colors.CYAN}: {Colors.GREEN}{val:<{width-12}}{Colors.CYAN}│{Colors.RESET}")
    
    print(f"{Colors.CYAN}└{'─' * (width-2)}┘{Colors.RESET}\n")
    
    # Stats
    print(f"{Colors.CYAN}┌{'─' * (width-2)}┐{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.YELLOW}  STATS{Colors.CYAN}{' ' * (width-11)}│{Colors.RESET}")
    print(f"{Colors.CYAN}├{'─' * (width-2)}┤{Colors.RESET}")
    
    stats = [
        ('👥 Followers', info.get('followers')),
        ('👤 Following', info.get('following')),
        ('❤️ Likes', info.get('likes')),
        ('🎬 Videos', info.get('videos')),
        ('🤝 Friends', info.get('friendCount'))
    ]
    
    for label, value in stats:
        if value:
            print(f"{Colors.CYAN}│ {Colors.WHITE}{label:<12}{Colors.CYAN}: {Colors.GREEN}{value:>10}{Colors.CYAN}  │{Colors.RESET}")
    
    print(f"{Colors.CYAN}└{'─' * (width-2)}┘{Colors.RESET}\n")
    
    # Bio
    bio = info.get('signature')
    if bio and bio != 'No signature found':
        print(f"{Colors.CYAN}┌{'─' * (width-2)}┐{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.YELLOW}  BIO{Colors.CYAN}{' ' * (width-9)}│{Colors.RESET}")
        print(f"{Colors.CYAN}├{'─' * (width-2)}┤{Colors.RESET}")
        bio_clean = bio.replace('\\n', ' ').replace('\\r', '')
        if len(bio_clean) > width-6:
            bio_clean = bio_clean[:width-9] + '...'
        print(f"{Colors.CYAN}│ {Colors.WHITE}{bio_clean:<{width-4}} │{Colors.RESET}")
        print(f"{Colors.CYAN}└{'─' * (width-2)}┘{Colors.RESET}\n")
    
    # Social Links
    links = info.get('social_links', [])
    if links:
        print(f"{Colors.CYAN}┌{'─' * (width-2)}┐{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.YELLOW}  SOCIAL{Colors.CYAN}{' ' * (width-11)}│{Colors.RESET}")
        print(f"{Colors.CYAN}├{'─' * (width-2)}┤{Colors.RESET}")
        for link in links[:4]:
            if len(link) > width-6:
                link = link[:width-9] + '...'
            print(f"{Colors.CYAN}│ {Colors.GREEN}•{Colors.WHITE} {link:<{width-6}} │{Colors.RESET}")
        print(f"{Colors.CYAN}└{'─' * (width-2)}┘{Colors.RESET}")
    
    # Profile URL
    username = info.get('unique_id')
    if username:
        print(f"\n{Colors.CYAN}🔗 {Colors.WHITE}https://www.tiktok.com/@{username}{Colors.RESET}")

def download_pp(url, username):
    if not url or not url.startswith('http'):
        box("No profile picture URL", Colors.YELLOW)
        return
    
    try:
        if not os.path.exists('pp_images'):
            os.makedirs('pp_images')
        
        loading("Downloading picture", 1.5)
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            fname = f"pp_images/{username}.jpg"
            with open(fname, 'wb') as f:
                f.write(resp.content)
            size = len(resp.content) / 1024
            box(f"✓ Saved: {fname} ({size:.1f}KB)", Colors.GREEN)
        else:
            box("✗ Download failed", Colors.RED)
    except Exception as e:
        box(f"✗ Error: {str(e)[:30]}", Colors.RED)

# ============= BULK SCRAPER =============
def bulk_scraper():
    width = min(get_terminal_width(), 60)
    
    print(f"\n{Colors.CYAN}╔{'═' * (width-2)}╗{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.YELLOW}  📊 BULK SCRAPER{Colors.CYAN}{' ' * (width-18)}║{Colors.RESET}")
    print(f"{Colors.CYAN}╚{'═' * (width-2)}╝{Colors.RESET}")
    
    print(f"\n{Colors.WHITE}Enter usernames (blank line to finish):{Colors.RESET}")
    
    users = []
    while True:
        line = input(f"{Colors.CYAN}> {Colors.WHITE}")
        if not line and users:
            break
        if line:
            users.append(line.strip())
    
    if not users:
        box("No usernames entered", Colors.YELLOW)
        return
    
    print(f"\n{Colors.WHITE}Processing {len(users)} users...{Colors.RESET}\n")
    
    results = []
    for i, user in enumerate(users, 1):
        print(f"{Colors.CYAN}[{i}/{len(users)}]{Colors.WHITE} @{user}{Colors.RESET}")
        info = get_user_info(user)
        if info:
            results.append(info)
            print(f"{Colors.GREEN}  ✓ Success{Colors.RESET}")
        else:
            print(f"{Colors.RED}  ✗ Failed{Colors.RESET}")
        time.sleep(0.3)
    
    if results:
        fname = f"bulk_{int(time.time())}.json"
        with open(fname, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n{Colors.GREEN}✓ Saved: {fname}{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}✓ {len(results)}/{len(users)} successful{Colors.RESET}")

# ============= MAIN =============
def main():
    while True:
        try:
            show_banner()
            show_menu()
            
            choice = input(f"\n{Colors.CYAN}┌─{Colors.WHITE}[{Colors.GREEN}Select{Colors.WHITE}]{Colors.CYAN}\n└──╼ {Colors.WHITE}")
            
            if choice == '1':
                show_banner()
                
                print(f"\n{Colors.CYAN}┌{'─' * 40}┐{Colors.RESET}")
                print(f"{Colors.CYAN}│{Colors.YELLOW}  USER LOOKUP{Colors.CYAN}{' ' * 27}│{Colors.RESET}")
                print(f"{Colors.CYAN}└{'─' * 40}┘{Colors.RESET}")
                
                user = input(f"\n{Colors.WHITE}Username: {Colors.CYAN}").strip()
                
                if user:
                    loading(f"Fetching @{user}", 2)
                    info = get_user_info(user)
                    
                    if info:
                        display_user(info)
                        
                        print(f"\n{Colors.YELLOW}Download profile pic? (y/n): {Colors.WHITE}")
                        if input().lower() == 'y':
                            download_pp(info.get('profile_pic'), info.get('unique_id') or user)
                        
                        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
                    else:
                        box("✗ No data found", Colors.RED)
                        input(f"\n{Colors.DIM}Press Enter...{Colors.RESET}")
                else:
                    box("✗ No username", Colors.YELLOW)
                    input(f"\n{Colors.DIM}Press Enter...{Colors.RESET}")
            
            elif choice == '2':
                show_banner()
                bulk_scraper()
                input(f"\n{Colors.DIM}Press Enter...{Colors.RESET}")
            
            elif choice == '3':
                print(f"\n{Colors.CYAN}╔{'═' * 40}╗{Colors.RESET}")
                print(f"{Colors.CYAN}║{Colors.YELLOW}  👋 Goodbye!{Colors.CYAN}{' ' * 28}║{Colors.RESET}")
                print(f"{Colors.CYAN}║{Colors.MAGENTA}  by ᴀꜱɪꜰ ɪꜱʟᴀᴍ{Colors.CYAN}{' ' * 23}║{Colors.RESET}")
                print(f"{Colors.CYAN}╚{'═' * 40}╝{Colors.RESET}")
                loading("Exiting", 1)
                sys.exit(0)
            
            else:
                box("✗ Invalid option", Colors.RED)
                input(f"\n{Colors.DIM}Press Enter...{Colors.RESET}")
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}⚠ Interrupted{Colors.RESET}")
            sys.exit(0)
        except Exception as e:
            box(f"✗ Error: {str(e)[:30]}", Colors.RED)
            input(f"\n{Colors.DIM}Press Enter...{Colors.RESET}")

if __name__ == "__main__":
    main()
