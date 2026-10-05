# หัวคอลัมน์ที่ใช้แสดงผล (ชื่อที่แสดง, ชื่อ attribute ในคลาส)
COLUMNS = [
    ("Name", "name"), ("Damage", "damage"), ("Rate", "rate"),
    ("Effective", "effective"), ("Ammo", "ammo"), ("Reload", "reload"),
    ("Weight", "weight"), ("Accuracy", "accuracy"), ("Recoil", "recoil"),
    ("Type", "type"),
]


class Weapons:
    """คลาสต้นแบบของข้อมูลอาวุธ (10 คุณสมบัติ)"""

    def __init__(self, name, damage, rate, effective, ammo, reload, weight, accuracy, recoil, type):
        self.name = name
        self.damage = damage
        self.rate = rate
        self.effective = effective
        self.ammo = ammo
        self.reload = reload
        self.weight = weight
        self.accuracy = accuracy
        self.recoil = recoil
        self.type = type

    def show_info(self):
        print("Name:", self.name)
        print("Damage:", self.damage)
        print("Rate:", self.rate)
        print("Effective:", self.effective)
        print("Ammo:", self.ammo)
        print("Reload:", self.reload)
        print("Weight:", self.weight)
        print("Accuracy:", self.accuracy)
        print("Recoil:", self.recoil)
        print("Type:", self.type)

    def as_row(self):
        return (self.name, self.damage, self.rate, self.effective, self.ammo,
                self.reload, self.weight, self.accuracy, self.recoil, self.type)

    def info_text(self):
        return "\n".join(f"{title}: {getattr(self, attr)}" for title, attr in COLUMNS)
