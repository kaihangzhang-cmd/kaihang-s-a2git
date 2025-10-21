# Poetry Button — Processing.py (final)
# English UI only; verses in Chinese + English translation; author only.
# Stable fonts, ASCII-only labels, prompt placed above the display card.

from datetime import datetime
import random

# 
poems = [
    {"text": u"床前明月光，疑是地上霜。", "en": "Moonlight before my bed, like frost upon the ground.", "author": u"Li Bai"},
    {"text": u"举头望明月，低头思故乡。", "en": "I raise my head to the bright moon, then bow and think of home.", "author": u"Li Bai"},
    {"text": u"春眠不觉晓，处处闻啼鸟。", "en": "In spring I sleep through dawn; birds sing everywhere.", "author": u"Meng Haoran"},
    {"text": u"野火烧不尽，春风吹又生。", "en": "Wildfire cannot burn it all; spring winds bring new life.", "author": u"Bai Juyi"},
    {"text": u"人面不知何处去，桃花依旧笑春风。", "en": "Her face is gone somewhere unknown; peach blossoms still smile in spring.", "author": u"Cui Hu"},
    {"text": u"会当凌绝顶，一览众山小。", "en": "I will stand at the summit where all other mountains seem small.", "author": u"Du Fu"},
    {"text": u"明月松间照，清泉石上流。", "en": "Moonlight through pines; clear springs run over stones.", "author": u"Wang Wei"},
    {"text": u"劝君更尽一杯酒，西出阳关无故人。", "en": "Please drink one more cup; west of the Pass there are no old friends.", "author": u"Wang Wei"},
    {"text": u"大风起兮云飞扬。", "en": "A great wind rises and the clouds soar high.", "author": u"Liu Bang"},
    {"text": u"但愿人长久，千里共婵娟。", "en": "May we live long, sharing the moon across a thousand miles.", "author": u"Su Shi"},
]

# 
used_indices = []
current_index = None
favs = []

# reveal animation
anim_alpha = 0
anim_y = 0
anim_active = False

# toast
toast_msg = ""
toast_timer = 0  # frames remaining

# fonts
uiFont = None
cjkFont = None

# buttons
buttons = {}

# layout constants
WIN_W, WIN_H = 720, 520
BTN_W, BTN_H = 220, 48
BTN_X = WIN_W/2 - BTN_W/2
BTN_Y = 40
BTN_AGAIN_W = 120
BTN_AGAIN_X = BTN_X + BTN_W + 12
BTN_AGAIN_Y = BTN_Y
PROMPT_Y = 95  # prompt sits here, above the card and below the buttons

CARD_MARGIN = 40
CARD_X = CARD_MARGIN
CARD_Y = 120
CARD_W = WIN_W - CARD_MARGIN*2
CARD_H = 250

FAV_LEFT_W, FAV_LEFT_H = 220, 44
FAV_LEFT_X = BTN_X - 232
FAV_LEFT_Y = 420
SAVE_W, SAVE_H = 300, 44
SAVE_X = BTN_X + 8
SAVE_Y = 420

# 
def pick_font_simple(name_list, size, fallback="Serif"):
    """Try names in order; if none load, fall back to 'fallback'."""
    for nm in name_list:
        try:
            f = createFont(nm, size, True)
            if f is not None:
                return f
        except:
            pass
    return createFont(fallback, size, True)

class Button(object):
    def __init__(self, label, x, y, w, h, primary=False):
        self.label = label
        self.x, self.y, self.w, self.h = x, y, w, h
        self.primary = primary
        self.hover = False
        self.down = False
        self.enabled = True
    
    def draw(self):
        self.hover = self.hit(mouseX, mouseY)
        noStroke()
        if not self.enabled:
            fill(200)
        else:
            if self.primary:
                if self.down and self.hover:  fill(70, 120, 255)
                elif self.hover:              fill(90, 140, 255)
                else:                         fill(80, 130, 255)
            else:
                if self.down and self.hover:  fill(220)
                elif self.hover:              fill(235)
                else:                         fill(245)
        rect(self.x, self.y, self.w, self.h, 12)
        
        fill(0 if not self.primary else 255)
        textAlign(CENTER, CENTER)
        textFont(uiFont)
        textSize(18)
        text(self.label, self.x + self.w/2, self.y + self.h/2)
    
    def hit(self, px, py):
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h
    
    def press(self):
        if self.enabled and self.hit(mouseX, mouseY):
            self.down = True
    
    def release(self):
        was_down = self.down
        self.down = False
        return self.enabled and was_down and self.hit(mouseX, mouseY)

def is_cjk(s):
    return any(ord(ch) > 127 for ch in s)

def wrap_text(txt, x, y, w, lh):
    """
    Safe wrapper:
    - For CJK lines, wraps per character.
    - For ASCII/English, wraps per word.
    Handles newlines in txt.
    Returns next y after the wrapped block.
    """
    paragraphs = unicode(txt).split(u"\n")
    cy = y
    for p in paragraphs:
        if is_cjk(p):
            line = u""
            for ch in p:
                test = line + ch
                if textWidth(test) > w and line:
                    text(line, x, cy)
                    cy += lh
                    line = ch
                else:
                    line = test
            if line:
                text(line, x, cy)
                cy += lh
        else:
            words = unicode(p).split(u" ")
            line = u""
            for wd in words:
                test = (line + u" " + wd).strip()
                if textWidth(test) > w and line:
                    text(line, x, cy)
                    cy += lh
                    line = wd
                else:
                    line = test
            if line:
                text(line, x, cy)
                cy += lh
    return cy

def toast(msg):
    global toast_msg, toast_timer
    toast_msg = msg
    toast_timer = 120  # ~2s at 60fps

def draw_toast():
    tw = textWidth(toast_msg) + 32
    th = 36
    x = WIN_W/2 - tw/2
    y = WIN_H - 70
    noStroke()
    fill(0, 170)
    rect(x, y, tw, th, 18)
    fill(255)
    textAlign(CENTER, CENTER)
    textFont(uiFont)
    text(toast_msg, WIN_W/2, y + th/2)

# 
def setup():
    global uiFont, cjkFont, buttons
    size(WIN_W, WIN_H)
    frameRate(60)
    background(245)
    textMode(SHAPE)  # better glyph handling
    
    # UI font (ASCII)
    uiFont  = pick_font_simple(["Segoe UI", "Helvetica", "Arial", "SansSerif"], 18)
    # CJK-capable font (try common names; falling back is OK but may show tofu if no CJK on system)
    cjkFont = pick_font_simple(
        ["Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", "PingFang SC", "MS Mincho", "Arial Unicode MS"],
        22
    )
    
    # Buttons
    buttons["show"]  = Button("Show a Poem", BTN_X, BTN_Y, BTN_W, BTN_H, primary=True)
    buttons["again"] = Button("Again", BTN_AGAIN_X, BTN_AGAIN_Y, BTN_AGAIN_W, BTN_H, primary=False)
    buttons["fav"]   = Button("Favourite", FAV_LEFT_X, FAV_LEFT_Y, FAV_LEFT_W, FAV_LEFT_H, primary=False)
    buttons["save"]  = Button("Save Favourites (TXT)", SAVE_X, SAVE_Y, SAVE_W, SAVE_H, primary=False)

def draw():
    global anim_alpha, anim_y, anim_active, toast_timer
    background(245)
    
    # Title
    textAlign(CENTER, TOP)
    textFont(uiFont); fill(0); textSize(22)
    text("Poetry Button", WIN_W/2, 8)
    textSize(14); fill(80)
    text("Click to reveal a random non-repeating verse", WIN_W/2, 36)
    
    # Buttons row
    for b in buttons.values():
        b.draw()
    
    # Prompt ABOVE the card (only when no poem yet)
    if current_index is None:
        fill(120)
        textAlign(CENTER, CENTER)
        textFont(uiFont); textSize(16)
        text("Press 'Show a Poem'", WIN_W/2, PROMPT_Y)
    
    # Card
    noStroke(); fill(255); rect(CARD_X, CARD_Y, CARD_W, CARD_H, 16)
    stroke(0, 20); noFill(); rect(CARD_X, CARD_Y, CARD_W, CARD_H, 16)
    
    # Content within card
    if current_index is not None:
        poem = poems[current_index]
        if anim_active:
            anim_alpha = min(255, anim_alpha + 22)
            anim_y *= 0.8
            if anim_alpha >= 254 and abs(anim_y) < 0.5:
                anim_active = False
        
        tx = CARD_X + 24
        ty = CARD_Y + 24 + anim_y
        tw = CARD_W - 48
        
        # Chinese verse
        fill(0, anim_alpha)
        textAlign(LEFT, TOP)
        textFont(cjkFont); textSize(22)
        next_y = wrap_text(poem["text"], tx, ty, tw, 32)
        
        # English translation
        fill(40, anim_alpha)
        textFont(uiFont); textSize(16)
        next_y = wrap_text(poem["en"], tx, next_y + 8, tw, 22)
        
        # Author only
        fill(60, anim_alpha)
        textFont(uiFont); textSize(16)
        text("- " + poem.get("author", ""), tx, CARD_Y + CARD_H - 36)
    
    # Favourites count
    fill(80); textAlign(LEFT, BOTTOM); textFont(uiFont); textSize(14)
    text("Favourites: %d" % len(favs), 12, WIN_H - 10)
    
    # Toast
    if toast_timer > 0:
        draw_toast()
        toast_timer -= 1

def mousePressed():
    for b in buttons.values():
        b.press()

def mouseReleased():
    if buttons["show"].release():
        show_new_poem()
    elif buttons["again"].release():
        show_new_poem()
    elif buttons["fav"].release():
        add_favourite()
    elif buttons["save"].release():
        save_favourites()

def show_new_poem():
    global current_index, used_indices, anim_alpha, anim_y, anim_active
    n = len(poems)
    if n == 0:
        toast("No poems available")
        return
    available = [i for i in range(n) if i not in used_indices]
    if not available:
        used_indices = []
        available = list(range(n))
    idx = random.choice(available)
    used_indices.append(idx)
    current_index = idx
    anim_alpha = 0
    anim_y = 10
    anim_active = True

def add_favourite():
    if current_index is None:
        toast("Show a poem first")
        return
    p = poems[current_index]
    if p not in favs:
        favs.append(p)
        toast("Added to favourites")
    else:
        toast("Already in favourites")

def save_favourites():
    if not favs:
        toast("No favourites to save")
        return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = "favourites_%s.txt" % ts
    lines = [u"%s  -  %s  -  %s" % (p["text"], p.get("en",""), p.get("author","")) for p in favs]
    saveStrings(fname, lines)
    toast("Saved as %s" % fname)
