import fitz
import json
import re

def clean_lines(text: str):
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]

def is_header_footer(line: str):
    keywords = [
        "2027考研英语红宝书",
        "共 6550 词",
        "扫码听单词",
        "纸上默写",
        "耳边复习",
        "不背单词 App",
        "单词不用背，融入语境自然会",
        "Word",
        "Meaning",
    ]
    if any(k in line for k in keywords):
        return True
    if re.search(r"\d+\s*/\s*\d+\s*页", line):
        return True
    return False

def preprocess_lines(text: str):
    lines = clean_lines(text)
    return [line for line in lines if not is_header_footer(line)]

def parse_page(text: str, page_num: int, debug=False):
    lines = preprocess_lines(text)

    word_line_pattern = re.compile(r"^(\d+)\s+([A-Za-z][A-Za-z'’\- ]*)$")
    pure_num_pattern = re.compile(r"^\d+$")

    words = []
    meanings = []

    i = 0
    in_meaning_section = False

    # -------- 第一阶段：扫单词区 --------
    while i < len(lines):
        line = lines[i]

        # 情况1：单词在同一行，例如 "1001 sensitive"
        m = word_line_pattern.match(line)
        if not in_meaning_section and m:
            words.append({
                "index": int(m.group(1)),
                "word": m.group(2).strip()
            })
            i += 1
            continue

        # 情况2：单词分两行，例如
        # 999
        # sensation
        if not in_meaning_section and pure_num_pattern.match(line):
            # 如果下一行是英文单词，则还是单词区
            if i + 1 < len(lines) and re.match(r"^[A-Za-z][A-Za-z'’\- ]*$", lines[i + 1]):
                words.append({
                    "index": int(line),
                    "word": lines[i + 1].strip()
                })
                i += 2
                continue
            else:
                # 纯数字行后面不是英文单词，说明进入释义区
                in_meaning_section = True

        if in_meaning_section:
            break

        i += 1

    # -------- 第二阶段：扫释义区 --------
    while i < len(lines):
        line = lines[i]
        if pure_num_pattern.match(line):
            idx = int(line)
            i += 1
            parts = []
            while i < len(lines) and not pure_num_pattern.match(lines[i]):
                parts.append(lines[i])
                i += 1
            meaning = " ".join(parts).strip()
            if meaning:
                meanings.append({
                    "index": idx,
                    "meaning": meaning
                })
        else:
            i += 1

    meaning_map = {m["index"]: m["meaning"] for m in meanings}

    result = []
    for w in words:
        idx = w["index"]
        if idx in meaning_map:
            result.append({
                "page": page_num,
                "index": idx,
                "word": w["word"],
                "meaning": meaning_map[idx]
            })

    if debug and (len(words) == 0 or len(result) == 0):
        with open(f"debug_page_{page_num}.txt", "w", encoding="utf-8") as f:
            f.write("===== lines =====\n")
            f.write("\n".join(lines))
            f.write("\n\n===== parsed_words =====\n")
            f.write(json.dumps(words, ensure_ascii=False, indent=2))
            f.write("\n\n===== parsed_meanings =====\n")
            f.write(json.dumps(meanings, ensure_ascii=False, indent=2))
            f.write("\n\n===== parsed_result =====\n")
            f.write(json.dumps(result, ensure_ascii=False, indent=2))

    return result

def extract_pdf(pdf_path: str, debug=False):
    doc = fitz.open(pdf_path)
    all_data = []

    for page_num in range(1, len(doc) + 1):
        text = doc[page_num - 1].get_text()
        page_data = parse_page(text, page_num, debug=debug)
        print(f"第 {page_num} 页提取 {len(page_data)} 条")
        all_data.extend(page_data)

    return all_data

if __name__ == "__main__":
    pdf_path = "2027考研英语红宝书-不背单词版.pdf"
    data = extract_pdf(pdf_path, debug=True)

    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"总共提取 {len(data)} 条")