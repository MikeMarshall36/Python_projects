class Creature:
    Hp = 100
    def __init__(self,Health):
        self.Hp = Health

class Player(Creature):
    lvl = 0
    skills = []
    M_DMG = 0
    s_DMG = 0
    ammunition = 0
    xp = 0
    Weapon = ''
    def __init__(self,level, skills, m_damage, s_damage, ammo, experience, firearm):
        self.lvl = level
        self.skills = skills
        self.M_DMGDMG = m_damage
        self.s_DMG = s_damage
        self.ammunition = ammo
        self.xp = experience
        self.Weapon = firearm
    def Shooting(self,times):
        if self.ammunition - times <= 0:
            while self.ammunition > 0:
                self.ammunition -= 1
                times -= 1
            print('\033[32m\n*click*\n \033[0m'*times)

    def getting_hit(self, e_dmg):
        if self.Hp != 0:
            self.Hp -= e_dmg
        else:
            print('Game over(character is dead)')

    def Healing(self):
        if self.Hp != 100:
            h_need = 100 - self.Hp
            self.Hp += h_need
        else:
            print('Your health is full\nStatus: OK')

    def Gun_switching(self):
        if self.Weapon == 'primary':
            self.Weapon = 'backup'
            self.M_DMG, self.s_DMG = self.s_DMG, self.M_DMG

        elif self.Weapon == 'backup':
            self.Weapon = 'primary'
            self.M_DMG, self.s_DMG = self.s_DMG, self.M_DMG
    def LVL_up(self):
        if self.lvl <10:
            while self.xp > 400:
                self.xp -= 400
                self.lvl += 1
        else:
            print('Max level reached!')

    def Total_Output(self):
        print(self.lvl,self.skills, self.M_DMG, self.s_DMG,self.ammunition, self.xp, self.Weapon, self.Hp)

n = [11,22,43,15]
Valera = Player(0,n,20,5,10,1024,'primary')
Valera.Total_Output()
Valera.Shooting(15)
Valera.getting_hit(29)
Valera.LVL_up()
Valera.Gun_switching()
Valera.Total_Output()
print(Valera.M_DMG)