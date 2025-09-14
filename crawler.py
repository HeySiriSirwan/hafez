import requests
from bs4 import BeautifulSoup
import json
import re
import time
from tqdm import tqdm

base_url = "https://ganjoor.net/hafez/ghazal/sh"
total_ghazals = 495
ghazals_data = {}

for i in tqdm(range(1, total_ghazals + 1), desc="Crawling Ghazals"):
    url = f"{base_url}{i}"
    if i % 3 == 0:
        time.sleep(2)
    if i % 7 == 0:
        time.sleep(3)
    if i % 11 == 0:
        time.sleep(4)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        baits = {}
        bait_divs = soup.find_all('div', class_='b')
        for div in bait_divs:
            bn_id = div.get('id', '')
            if bn_id and bn_id.startswith('bn'):
                try:
                    num = int(bn_id[2:])
                except ValueError:
                    print(f"Warning: Invalid bait ID {bn_id} in ghazal {i}")
                    continue
                m1 = div.find('div', class_='m1')
                m2 = div.find('div', class_='m2')
                m1_text = m1.find('p').text.strip() if m1 and m1.find('p') else ''
                m2_text = m2.find('p').text.strip() if m2 and m2.find('p') else ''
                content = f"{m1_text}\n{m2_text}".strip()
                if content:
                    baits[str(num)] = {"content": content, "meaning": ""}
        summaries_div = soup.find('div', id='summaries')
        if summaries_div:
            summary_divs = summaries_div.find_all('div', class_='coupletsummary')
            for sdiv in summary_divs:
                blockquote = sdiv.find('blockquote')
                if blockquote:
                    a_tag = blockquote.find('a', href=re.compile(r'#bn\d+'))
                    if a_tag and a_tag.get('href'):
                        href = a_tag['href']
                        match = re.search(r'#bn(\d+)', href)
                        if match:
                            num = int(match.group(1))
                            notice = sdiv.find('div', class_='notice')
                            meaning = notice.find('p').text.strip() if notice and notice.find('p') else ''
                            if str(num) in baits:
                                baits[str(num)]["meaning"] = meaning
                            else:
                                print(f"meaning found for non-existent bait {num} in ghazal {i}")
                        else:
                            print(f"invalid summary link format {href} in ghazal {i}")
                    else:
                        print(f"no valid <a> tag found in summary for ghazal {i}")
        else:
            print(f"no summaries div found for ghazal {i}")
        vazn = ""
        bahr = ""
        ghaleb = ""
        tedad_abiat = len(baits)
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                tds = row.find_all('td')
                if len(tds) >= 2:
                    label = tds[0].text.strip()
                    value = tds[1].text.strip()
                    if 'وزن:' in label:
                        match = re.match(r'(.+?)\s*\((.+)\)', value)
                        if match:
                            vazn = match.group(1).strip()
                            bahr = match.group(2).strip()
                        else:
                            vazn = value
                    elif 'قالب شعری:' in label:
                        ghaleb = value
                    elif 'تعداد ابیات:' in label:
                        try:
                            tedad_abiat = int(value) if value and value.isdigit() else len(baits)
                        except ValueError:
                            print(f"invalid tedad_abiat '{value}' in ghazal {i}")
                            tedad_abiat = len(baits)

        tedad_comments = 0
        comments_section = soup.find('div', id='comments-section')
        if comments_section:
            p_tag = comments_section.find('p')
            if p_tag:
                text = p_tag.text
                match = re.search(r'تا به حال (\d+) حاشیه', text)
                if match:
                    tedad_comments = int(match.group(1))
                else:
                    print(f"could not extract comment count from '{text}' in ghazal {i}")
        if baits:
            ghazals_data[str(i)] = {
                "baits": baits,
                "vazn": vazn,
                "bahr": bahr,
                "ghaleb": ghaleb,
                "tedad_abiat": tedad_abiat,
                "tedad_comments": tedad_comments
            }
        else:
            print(f"no baits found for ghazal {i}")
        time.sleep(2)
        print(baits['1']['content'])

    except requests.RequestException as e:
        print(f"error fetching ghazal {i}: {e}")
        continue
    except Exception as e:
        print(f"unexpected error in ghazal {i}: {e}")
        continue

with open('hafez_ghazals.json', 'w', encoding='utf-8') as f:
    json.dump(ghazals_data, f, ensure_ascii=False, indent=4)
