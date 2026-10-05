import tkinter as tk
from tkinter import ttk, messagebox

from Weapons import COLUMNS
from WeaponsData import get_weapons, Stack, Queue
from MergeSort import MergeSorter, Searcher

# ---------------- ส่วนประกอบหน้าตา (สี / ปุ่มมุมเว้า / กล่องตาราง) ----------------
BG = "#1f1f1f"          # พื้นหลังมืด
BLUE = "#0572d6"        # น้ำเงินหลัก
BLUE_HOVER = "#1b88ee"  # เมื่อเอาเมาส์ชี้
BLUE_SEL = "#38a1ff"    # ปุ่มที่ถูกเลือก
BLUE_DARK = "#0a5bb0"   # หัวตาราง
FONT = "Leelawadee UI"  # ฟอนต์ไทย (ถ้าไม่มีจะใช้ฟอนต์สำรองของระบบ)


class NotchButton(tk.Canvas):
    """ปุ่มสี่เหลี่ยมมุมเว้า (สี่เหลี่ยม + วงกลมสีพื้นหลังที่มุมทั้ง 4)"""

    def __init__(self, master, text, command, width=180, height=68, r=12):
        super().__init__(master, width=width, height=height, bg=BG,
                         highlightthickness=0, cursor="hand2")
        self.command = command
        self.selected = False
        self.rect = self.create_rectangle(0, 0, width, height, fill=BLUE, outline=BLUE)
        for x, y in ((0, 0), (width, 0), (0, height), (width, height)):
            self.create_oval(x - r, y - r, x + r, y + r, fill=BG, outline=BG)
        self.create_text(width / 2, height / 2, text=text, fill="white",
                         font=("Segoe UI", 14))
        self.bind("<Enter>", lambda e: self._paint(BLUE_SEL if self.selected else BLUE_HOVER))
        self.bind("<Leave>", lambda e: self._paint(BLUE_SEL if self.selected else BLUE))
        self.bind("<Button-1>", lambda e: self.command())

    def _paint(self, color):
        self.itemconfig(self.rect, fill=color, outline=color)

    def set_selected(self, flag):
        self.selected = flag
        self._paint(BLUE_SEL if flag else BLUE)


class NotchBox(tk.Canvas):
    """กล่องสีน้ำเงินมุมเว้าขนาดใหญ่ สำหรับวางตารางแสดงผล"""

    def __init__(self, master, width, height, r=26):
        super().__init__(master, width=width, height=height, bg=BG, highlightthickness=0)
        self.create_rectangle(0, 0, width, height, fill=BLUE, outline=BLUE)
        for x, y in ((0, 0), (width, 0), (0, height), (width, height)):
            self.create_oval(x - r, y - r, x + r, y + r, fill=BG, outline=BG)
        self.inner = tk.Frame(self, bg=BLUE)
        self.create_window(width / 2, height / 2, window=self.inner,
                           width=width - 24, height=height - 60)


def dark_button(master, text, command):
    return tk.Button(master, text=text, command=command, bg="#2d2d2d", fg="white",
                     activebackground=BLUE, activeforeground="white", relief="flat",
                     bd=0, padx=10, pady=4, cursor="hand2", font=(FONT, 10))


# ---------------- หน้าจอหลัก ----------------
TOP_N = 10             # จำนวนอันดับที่แสดงเมื่อเลือกคุณสมบัติ (กด all = แสดงทั้งหมด)

PROPS = ["damage", "rate", "weight", "effective", "accuracy",
         "ammo", "recoil", "reload", "type", "all"]


class WeaponsGUI:
    def __init__(self, root, weapons):
        self.root = root
        self.weapons = weapons              # ข้อมูลทั้งหมดจาก WeaponsData

        self.root.title("Weapons Manager")
        self.root.configure(bg=BG)
        self.root.geometry("1140x740")
        self.root.resizable(False, False)

        self.current = list(self.weapons)   # รายการที่กำลังแสดง
        self.key = "damage"
        self.asc = False
        self.history = Stack()              # Stack : ประวัติสำหรับ Undo
        self.queue = Queue()                # Queue : คิวอาวุธที่เลือก
        self.buttons = {}

        self.setup_style()
        self.setup_ui()
        self.choose("damage", record=False)

    # ---------- สร้างหน้าจอ ----------
    def setup_style(self):
        st = ttk.Style()
        st.theme_use("clam")
        st.configure("Blue.Treeview", background=BLUE, fieldbackground=BLUE,
                     foreground="white", rowheight=26, borderwidth=0, font=(FONT, 11))
        st.configure("Blue.Treeview.Heading", background=BLUE_DARK, foreground="white",
                     relief="flat", font=(FONT, 11, "bold"))
        st.map("Blue.Treeview", background=[("selected", "white")],
               foreground=[("selected", BLUE)])
        st.map("Blue.Treeview.Heading", background=[("active", BLUE_DARK)])
        st.configure("Blue.Vertical.TScrollbar", background=BLUE_DARK, troughcolor=BLUE,
                     bordercolor=BLUE, arrowcolor="white")

    def setup_ui(self):
        tk.Label(self.root, text="เลือกคุณสมบัติของ Weapons", bg=BG, fg="white",
                 font=(FONT, 34, "bold")).pack(pady=(14, 4))

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=60)

        # ซ้าย: ปุ่มเลือกคุณสมบัติ 2 คอลัมน์ x 5 แถว
        left = tk.Frame(body, bg=BG)
        left.pack(side="left", anchor="n", pady=(16, 0))
        for i, p in enumerate(PROPS):
            b = NotchButton(left, p, lambda k=p: self.choose(k))
            b.grid(row=i // 2, column=i % 2, padx=14, pady=10)
            self.buttons[p] = b

        # ขวา: ชื่อคุณสมบัติ + กล่องตาราง + แผงควบคุม
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", anchor="n", padx=(40, 0))

        self.title_lbl = tk.Label(right, text="", bg=BG, fg="white", font=(FONT, 22, "bold"))
        self.title_lbl.pack(pady=(6, 6))

        box = NotchBox(right, 620, 370)
        box.pack()
        self.tree = ttk.Treeview(box.inner, style="Blue.Treeview", show="headings",
                                 selectmode="browse")
        sb = ttk.Scrollbar(box.inner, orient="vertical", command=self.tree.yview,
                           style="Blue.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", lambda e: self.do_enqueue())

        # แผงควบคุม (เรียง / Undo / Queue)
        row1 = tk.Frame(right, bg=BG)
        row1.pack(fill="x", pady=(10, 4))
        self.order_btn = dark_button(row1, "", self.toggle_order)
        self.order_btn.pack(side="left", padx=(0, 6))
        dark_button(row1, "ย้อนกลับ (Undo)", self.do_undo).pack(side="left", padx=6)
        dark_button(row1, "Enqueue", self.do_enqueue).pack(side="left", padx=6)
        dark_button(row1, "Dequeue", self.do_dequeue).pack(side="left", padx=6)
        self.stack_lbl = tk.Label(row1, text="", bg=BG, fg="#aaaaaa", font=(FONT, 10))
        self.stack_lbl.pack(side="right")

        # แผงค้นหา
        row2 = tk.Frame(right, bg=BG)
        row2.pack(fill="x", pady=4)
        tk.Label(row2, text="ค้นหา:", bg=BG, fg="white", font=(FONT, 10)).pack(side="left")
        self.search_var = tk.StringVar()
        e = tk.Entry(row2, textvariable=self.search_var, width=16, bg="#2d2d2d", fg="white",
                     insertbackground="white", relief="flat", font=(FONT, 11))
        e.pack(side="left", padx=6, ipady=3)
        e.bind("<Return>", lambda ev: self.do_linear())
        dark_button(row2, "Linear Search", self.do_linear).pack(side="left", padx=4)
        dark_button(row2, "Binary Search", self.do_binary).pack(side="left", padx=4)
        dark_button(row2, "แสดงทั้งหมด", lambda: self.choose(self.key)).pack(side="left", padx=4)

        self.queue_lbl = tk.Label(right, text="", bg=BG, fg="white", font=(FONT, 10), anchor="w")
        self.queue_lbl.pack(fill="x", pady=(6, 0))
        self.status = tk.Label(right, text="", bg=BG, fg="#aaaaaa", font=(FONT, 10), anchor="w")
        self.status.pack(fill="x")

    # ---------- แสดงผลในตาราง ----------
    def display_weapons(self, msg=""):
        if self.key == "all":
            cols = [a for _, a in COLUMNS]
            rows = self.current                      # all -> แสดงทั้งหมด (เลื่อนดูได้)
        else:
            cols = ["rank", "name", self.key]
            rows = self.current[:TOP_N]              # แสดงเฉพาะ 10 อันดับแรก

        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text="อันดับ" if c == "rank" else c.capitalize())
            if self.key == "all":
                w = 70 if c == "name" else 110 if c == "type" else 58
                self.tree.column(c, width=w, minwidth=w, anchor="center", stretch=False)
            elif c == "rank":
                self.tree.column(c, width=80, minwidth=80, anchor="center", stretch=False)
            else:
                self.tree.column(c, width=230, minwidth=100, anchor="center", stretch=True)
        self.tree.delete(*self.tree.get_children())
        for i, w in enumerate(rows, 1):
            if self.key == "all":
                self.tree.insert("", "end", values=[getattr(w, c) for c in cols])
            else:
                self.tree.insert("", "end", values=[i, w.name, getattr(w, self.key)])

        if self.key != "all" and len(self.current) > TOP_N:
            msg += f"  |  แสดง {TOP_N} อันดับแรกจาก {len(self.current)} รายการ"

        self.title_lbl.config(text=self.key)
        for k, b in self.buttons.items():
            b.set_selected(k == self.key)
        self.order_btn.config(text="เรียง: น้อย → มาก" if self.asc else "เรียง: มาก → น้อย")
        self.stack_lbl.config(text=f"Stack (ประวัติ): {len(self.history)}")
        names = " → ".join(w.name for w in self.queue.items()) or "(ว่าง)"
        self.queue_lbl.config(text=f"คิว (FIFO): {names}")
        self.status.config(text=msg)

    def snapshot(self):
        self.history.push((list(self.current), self.key, self.asc))     # push ลง Stack

    def search_attr(self):
        return "name" if self.key == "all" else self.key

    # ---------- การทำงานของปุ่ม ----------
    def choose(self, key, record=True):
        if record:
            self.snapshot()
        self.key = key
        if key == "all":
            self.current = list(self.weapons)
            msg = f"แสดงข้อมูลทั้งหมด {len(self.weapons)} รายการ"
        else:
            self.current = MergeSorter.sort(self.weapons, key, self.asc)
            msg = f"เรียงตาม {key} ด้วย Merge Sort"
        self.display_weapons(msg)

    def toggle_order(self):
        if self.key == "all":
            self.status.config(text="เลือกคุณสมบัติด้านซ้ายก่อน จึงจะเรียงลำดับได้")
            return
        self.snapshot()
        self.asc = not self.asc
        self.current = MergeSorter.sort(self.current, self.key, self.asc)
        self.display_weapons(f"เรียงตาม {self.key} ({'น้อย→มาก' if self.asc else 'มาก→น้อย'})")

    def do_undo(self):
        if self.history.is_empty():
            self.status.config(text="ไม่มีประวัติให้ย้อนกลับ")
            return
        self.current, self.key, self.asc = self.history.pop()          # pop จาก Stack
        self.display_weapons("ย้อนกลับ 1 ขั้น (pop จาก Stack)")

    def do_linear(self):
        text = self.search_var.get().strip()
        if not text:
            return self.choose(self.key)
        self.snapshot()
        attr = self.search_attr()
        self.current = Searcher.linear_search(self.weapons, attr, text)
        self.display_weapons(f"Linear Search: พบ {len(self.current)} รายการที่ {attr} มีคำว่า '{text}'")

    def do_binary(self):
        text = self.search_var.get().strip()
        if not text:
            return self.choose(self.key)
        attr = self.search_attr()
        try:
            target = Searcher.parse_value(self.weapons, attr, text)
        except ValueError:
            return messagebox.showwarning("ข้อมูลไม่ถูกต้อง", "ช่องนี้ต้องกรอกเป็นตัวเลข")
        self.snapshot()
        data = MergeSorter.sort(self.weapons, attr, True)    # Binary Search ต้องเรียงก่อนเสมอ
        self.current = Searcher.binary_search(data, attr, target)
        self.display_weapons(f"Binary Search: ค้น {attr} = {target} พบ {len(self.current)} รายการ")

    def selected_weapon(self):
        sel = self.tree.selection()
        if not sel:
            return None
        name = str(self.tree.set(sel[0], "name"))
        return next(w for w in self.weapons if w.name == name)

    def do_enqueue(self):
        w = self.selected_weapon()
        if w is None:
            self.status.config(text="คลิกเลือกอาวุธในตารางก่อน แล้วกด Enqueue (หรือดับเบิลคลิก)")
            return
        self.queue.enqueue(w)
        self.display_weapons(f"Enqueue: เพิ่ม {w.name} ต่อท้ายคิว")

    def do_dequeue(self):
        if self.queue.is_empty():
            self.status.config(text="คิวว่างอยู่")
            return
        w = self.queue.dequeue()
        self.display_weapons(f"Dequeue: นำ {w.name} ออกจากหัวคิว")
        messagebox.showinfo(f"ข้อมูล {w.name}", w.info_text())


if __name__ == "__main__":
    root = tk.Tk()
    weapons_data = get_weapons()
    app = WeaponsGUI(root, weapons_data)
    root.mainloop()
