from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'work' / 'ig-carousel-assets'
OUT = ROOT / 'outputs' / 'ig-carousel-35-55'
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1350
IVORY = '#F6F1E8'
PAPER = '#FBF8F2'
INK = '#243237'
MUTED = '#6B7773'
SAGE = '#7D9A87'
SAGE_DARK = '#3E5E52'
TERRACOTTA = '#B9795E'
NAVY = '#203A4B'
GOLD = '#D6B66D'
LINE = '#D9D1C3'

FONT = 'C:/Windows/Fonts/NotoSansTC-VF.ttf'
FONT_BOLD = 'C:/Windows/Fonts/msjhbd.ttc'
FONT_SCALE = 1.12

def f(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, round(size * FONT_SCALE))

def fit_cover(img, box):
    x, y, w, h = box
    scale = max(w / img.width, h / img.height)
    resized = img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - w) // 2
    top = (resized.height - h) // 2
    return resized.crop((left, top, left + w, top + h))

def text(draw, xy, s, size, fill=INK, bold=False, anchor=None, spacing=12):
    draw.multiline_text(xy, s, font=f(size, bold), fill=fill, spacing=spacing, anchor=anchor)

def wrap(s, width, size):
    chars, lines, line = [], [], ''
    for ch in s:
        trial = line + ch
        if f(size).getlength(trial) > width and line:
            lines.append(line)
            line = ch
        else:
            line = trial
    if line: lines.append(line)
    return '\n'.join(lines)

def base():
    return Image.new('RGB', (W, H), IVORY)

def photo(dst, source, box, overlay=None):
    x, y, w, h = box
    dst.paste(fit_cover(source, box), (x, y))
    if overlay:
        layer = Image.new('RGBA', (w, h), overlay)
        dst.paste(layer, (x, y), layer)

def label(draw, x, y, s, fill=SAGE_DARK):
    width = max(164, int(f(19, True).getlength(s) + 38))
    draw.rounded_rectangle((x, y, x + width, y + 40), 20, fill=fill)
    text(draw, (x + width // 2, y + 20), s, 19, fill='#FFFFFF', bold=True, anchor='mm')

def page_no(draw, n):
    text(draw, (W - 70, H - 58), f'{n:02d} / 08', 20, fill=MUTED, bold=True, anchor='rm')

def arrow(draw, a, b, fill=TERRACOTTA, width=5):
    draw.line((a, b), fill=fill, width=width)
    ang = math.atan2(b[1]-a[1], b[0]-a[0])
    p1 = (b[0] - 20*math.cos(ang-0.5), b[1] - 20*math.sin(ang-0.5))
    p2 = (b[0] - 20*math.cos(ang+0.5), b[1] - 20*math.sin(ang+0.5))
    draw.polygon([b, p1, p2], fill=fill)

overloaded = Image.open(ASSET / 'scene-overloaded.png').convert('RGB')
focused = Image.open(ASSET / 'scene-focused.png').convert('RGB')
zones = Image.open(ASSET / 'scene-four-zones.png').convert('RGB')
happy = Image.open(ASSET / 'scene-happy-coffee.png').convert('RGB')
desk_close = Image.open(ASSET / 'scene-desk-close.png').convert('RGB')
desk_window = Image.open(ASSET / 'scene-window-desk.png').convert('RGB')
back_work = Image.open(ASSET / 'scene-back-work.png').convert('RGB')

# 1 cover
im = base(); d = ImageDraw.Draw(im)
photo(im, overloaded, (0, 0, W, H), (20, 35, 30, 100))
label(d, 70, 78, '給 35–55 歲職場女性')
text(d, (70, 250), '你不是懶，\n只是還沒找出\n真正耗能的地方', 66, fill='#FFFFFF', bold=True, spacing=16)
text(d, (74, 590), '卡關自查包｜30 分鐘先理出頭緒', 27, fill='#F9E8C7', bold=True)
d.rounded_rectangle((70, 1090, 1010, 1230), 26, fill=(251, 248, 242, 235))
text(d, (108, 1130), '從自查 → 分類 → 排序 → 開始 7 天行動', 28, fill=SAGE_DARK, bold=True)
page_no(d, 1); im.save(OUT / '01-cover.png')

# 2 situation
im = base(); d = ImageDraw.Draw(im); photo(im, focused, (0, 0, W, 720), (246, 241, 232, 10))
d.rectangle((0, 720, W, H), fill=PAPER)
text(d, (70, 790), '每一件事，\n都像要先處理', 57, fill=INK, bold=True, spacing=12)
text(d, (72, 970), wrap('工作還沒做完，家裡又有事情等著你。想休息時，腦中卻還在排下一件事。', 880, 28), 28, fill=MUTED, spacing=12)
arrow(d, (130, 1165), (380, 1115)); text(d, (400, 1090), '不是不努力，是同時被太多事拉住', 23, fill=TERRACOTTA, bold=True)
page_no(d, 2); im.save(OUT / '02-situation.png')

# 3 four pressures
im = base(); d = ImageDraw.Draw(im)
text(d, (70, 72), '你以為自己只是累，', 42, fill=INK, bold=True)
text(d, (70, 135), '其實可能是四種壓力疊在一起', 42, fill=INK, bold=True)
photo(im, desk_close, (70, 250, 940, 560), (255, 255, 255, 20))
cards = [('工作負荷', '事情一直加量', 90, 880, NAVY), ('家庭分工', '責任反覆回到你身上', 570, 880, SAGE_DARK), ('自我能量', '沒有真正休息', 90, 1060, TERRACOTTA), ('界線與拒絕', '想拒絕卻開不了口', 570, 1060, GOLD)]
for title, sub, x, y, c in cards:
    d.rounded_rectangle((x, y, x + 420, y + 132), 22, fill='#FFFFFF', outline=LINE, width=2)
    d.ellipse((x+22, y+30, x+72, y+80), fill=c)
    text(d, (x+92, y+25), title, 26, fill=INK, bold=True)
    text(d, (x+92, y+70), sub, 19, fill=MUTED)
page_no(d, 3); im.save(OUT / '03-four-pressures.png')

# 4 reframe
im = base(); d = ImageDraw.Draw(im); photo(im, focused, (0, 0, W, 820), (248, 241, 229, 20))
d.rectangle((0, 820, W, H), fill=IVORY)
text(d, (70, 890), '你不一定需要更多方法，', 42, fill=INK, bold=True)
text(d, (70, 950), '可能要先知道哪一塊最耗能', 42, fill=INK, bold=True)
text(d, (72, 1070), wrap('當所有問題混在一起，再好的方法也很難持續。先分清楚來源，才有機會排出先後。', 900, 26), 26, fill=MUTED)
label(d, 72, 1205, '先分清楚，再開始')
page_no(d, 4); im.save(OUT / '04-reframe.png')

# 5 self check
im = base(); d = ImageDraw.Draw(im); photo(im, desk_window, (0, 0, W, 700), (245, 238, 223, 20))
d.rectangle((0, 700, W, H), fill=PAPER)
label(d, 70, 755, '01｜自查')
text(d, (70, 835), '第一步：先做 12 題自查', 46, fill=INK, bold=True)
text(d, (72, 930), wrap('每題都可以複選，選出最符合你目前狀態的選項。不用寫長篇心得，先把反覆出現的卡住訊號找出來。', 900, 26), 26, fill=MUTED)
for i, s in enumerate(['工作／家庭／能量／界線', '每題可複選', '先選最符合現在的狀態']):
    y = 1080 + i*55
    d.ellipse((82, y+10, 94, y+22), fill=SAGE_DARK)
    text(d, (120, y), s, 23, fill=INK)
page_no(d, 5); im.save(OUT / '05-self-check.png')

# 6 radar result
im = base(); d = ImageDraw.Draw(im)
label(d, 70, 70, '02｜分類結果')
text(d, (70, 150), '第二步：看見你的壓力分布', 43, fill=INK, bold=True)
cx, cy, r = 340, 660, 245
pts = []
vals = [0.86, 0.62, 0.48, 0.72]
names = ['工作', '能量', '界線', '家庭']
for ring in [1, .66, .33]:
    p=[]
    for i in range(4):
        ang=-math.pi/2+i*math.pi/2
        p.append((cx+math.cos(ang)*r*ring, cy+math.sin(ang)*r*ring))
    d.polygon(p, outline=LINE, fill=None)
for i in range(4):
    ang=-math.pi/2+i*math.pi/2
    end=(cx+math.cos(ang)*r, cy+math.sin(ang)*r)
    d.line((cx,cy,end[0],end[1]), fill=LINE, width=3)
    tx=cx+math.cos(ang)*(r+54); ty=cy+math.sin(ang)*(r+54)
    text(d, (tx,ty), names[i], 22, fill=INK, bold=True, anchor='mm')
poly=[]
for i,v in enumerate(vals):
    ang=-math.pi/2+i*math.pi/2
    poly.append((cx+math.cos(ang)*r*v, cy+math.sin(ang)*r*v))
d.polygon(poly, fill=(126, 160, 139, 120), outline=SAGE_DARK)
for p in poly: d.ellipse((p[0]-8,p[1]-8,p[0]+8,p[1]+8), fill=TERRACOTTA)
text(d, (650, 365), '把「很累」放回\n可以理解的面向', 37, fill=INK, bold=True, spacing=14)
text(d, (650, 535), wrap('透過過勞輪／雷達圖，看見目前哪一塊最需要被注意。', 330, 23), 23, fill=MUTED)
for i,(n,v,c) in enumerate(zip(['工作負荷','家庭分工','界線與拒絕','自我能量'], [86,72,62,48], [NAVY,SAGE_DARK,TERRACOTTA,GOLD])):
    y=780+i*85; text(d,(650,y),n,21,fill=INK,bold=True); d.rounded_rectangle((650,y+35,955,y+49),7,fill='#E7E1D5'); d.rounded_rectangle((650,y+35,650+3.05*v,y+49),7,fill=c); text(d,(980,y+28),f'{v}%',19,fill=MUTED,bold=True,anchor='rm')
page_no(d, 6); im.save(OUT / '06-radar-result.png')

# 7 order and action
im = base(); d = ImageDraw.Draw(im); photo(im, back_work, (0, 0, W, 650), (246, 241, 232, 10))
d.rectangle((0,650,W,H), fill=IVORY)
label(d, 70, 715, '03 → 04｜排序與行動')
text(d, (70, 805), '排順序，\n再開始 7 天行動', 48, fill=INK, bold=True, spacing=12)
text(d, (72, 990), wrap('依分類分數排出優先處理順序，再把第一順位轉成接下來 7 天可以開始的小行動。', 900, 26), 26, fill=MUTED)
steps=[('1','先找出最高分面向'),('2','選一個最值得先處理的項目'),('3','每天完成一個小步驟')]
for i,(n,s) in enumerate(steps):
    x=78+i*315; y=1130; d.ellipse((x,y,x+52,y+52),fill=SAGE_DARK); text(d,(x+26,y+26),n,23,fill='#FFFFFF',bold=True,anchor='mm'); text(d,(x+70,y+5),s,20,fill=INK,bold=True)
page_no(d, 7); im.save(OUT / '07-order-action.png')

# 8 CTA
im = base(); d = ImageDraw.Draw(im); photo(im, happy, (0, 0, W, H), (33, 51, 47, 75))
text(d, (70, 140), '不用一次解決\n全部問題', 66, fill='#FFFFFF', bold=True, spacing=14)
text(d, (74, 365), '先找出你現在最該處理的那一塊，\n再從一個小行動開始。', 28, fill='#F8E8C8', bold=True, spacing=12)
d.rounded_rectangle((70, 650, 1010, 1040), 28, fill=(251,248,242,238))
text(d, (112, 715), '35–55 歲職場女性卡關自查包', 32, fill=INK, bold=True)
for i,s in enumerate(['12 題複選自查','分類與過勞輪／雷達圖','優先順序排序表','7 天啟動行動表']):
    y=805+i*52; d.ellipse((123,y+10,135,y+22),fill=SAGE_DARK); text(d,(165,y),s,24,fill=INK)
d.rounded_rectangle((70, 1105, 1010, 1215), 22, fill=GOLD)
text(d, (540, 1158), '點個人檔案連結購買', 30, fill=INK, bold=True, anchor='mm')
page_no(d, 8); im.save(OUT / '08-cta.png')

print(f'created {len(list(OUT.glob("*.png")))} pages in {OUT}')
thumbs = []
for p in sorted(OUT.glob('0*.png')):
    src = Image.open(p).convert('RGB')
    src.thumbnail((270, 338), Image.Resampling.LANCZOS)
    card = Image.new('RGB', (270, 370), '#FFFFFF')
    card.paste(src, ((270-src.width)//2, 0))
    ImageDraw.Draw(card).text((18, 345), p.stem, font=f(16, True), fill=INK)
    thumbs.append(card)
sheet = Image.new('RGB', (270*4, 370*2), IVORY)
for i, card in enumerate(thumbs): sheet.paste(card, ((i%4)*270, (i//4)*370))
sheet.save(OUT / 'contact-sheet.png')
