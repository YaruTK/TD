import field_calc as fp
import image_transformation as tr
import os

class Tower(object):
    _reg = []

    def __init__(self, name, shoots_min, pn):
        self._reg.append(self)
        self.hint = "SIMGASLDG"
        self.name = name
        if not os.path.exists('resources/towers/' + self.name + '/'):
            os.makedirs('resources/towers/' + self.name + '/')
        self.folder = 'resources/towers/' + self.name + '/'
        self.attack_speed = shoots_min
        self.projectile_name = pn
        self.AT = []


class Projectile(object):
    _reg = []

    def __init__(self, name, dmg, vel, pt):
        self.name = name
        self.velocity = vel
        self.projectile_type = pt
        if not os.path.exists('resources/projectiles/' + self.name + '/'):
            os.makedirs('resources/projectiles/' + self.name + '/')
        self.folder = 'resources/projectiles/' + self.name + '/'
        self.dmg = dmg


#class Path(object):


arch_1 = Tower('archer_level_one', 100, 'arrow')
arch_1.AT = ['00100',
            '01110',
            '01110',
            '11T11']


arrow = Projectile('arrow', 60, 120, 'physical')


#class Creep(object):


#class Wave(object):


class OnBoard(object):
        _reg = []

        def __init__(self, pos):
            self._reg.append(self)
            self.position = pos
