from __future__ import annotations

import typing as tp
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Resource:
    name: str
    ingredients: tp.Dict[Resource, float]
    direct_supply_target: tp.List[Resource] = field(default_factory=list)

    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
    
    def consumesThroughput(self, ignore_top: bool = False):
        a = {}
        if not ignore_top:
            a[self] = 1.0
        b = __class__.dictConsumesThroughput(self.ingredients)
        return __class__.sumTwoDicts(a, b)

    @staticmethod
    def dictConsumesThroughput(d: tp.Dict[Resource, float], ignore_top: bool = False):
        s = {}
        for res, qty in d.items():
            s = __class__.sumTwoDicts(s, __class__.scaleDict(
                res.consumesThroughput(ignore_top), qty, 
            ))
        return s

    @staticmethod
    def scaleDict(d: tp.Dict[Resource, float], factor: float, /):
        return {res: qty * factor for res, qty in d.items()}
    
    @staticmethod
    def sumTwoDicts(
        a: tp.Dict[Resource, float], 
        b: tp.Dict[Resource, float], /
    ):
        c: tp.Dict[Resource, float] = {}
        for t in (a, b):
            for res, qty in t.items():
                c[res] = c.get(res, 0.0) + qty
        return c
    
    def beforeMainBus(self):
        self.ingredients.clear()
        return self
    
    def localDirectSupply(self, res: Resource):
        return self.localIntermediate(res)
    
    def localIntermediate(self, intermediate: Resource):
        inter_qty = self.ingredients.pop(intermediate)
        for raw, qty in intermediate.ingredients.items():
            if raw not in self.ingredients:
                self.ingredients[raw] = 0.0
            self.ingredients[raw] += qty * inter_qty
        return self

iron_ore = Resource('iron_ore', {}).beforeMainBus()

stone = Resource('stone', {}).beforeMainBus()
iron = Resource('iron', {}).beforeMainBus()
copper = Resource('copper', {}).beforeMainBus()
coal = Resource('coal', {}).beforeMainBus()
water = Resource('water', {}).beforeMainBus()
petro = Resource('petro', {}).beforeMainBus()
sulfur = Resource('sulfur', {water: 15.0 / 50, petro: 15.0 / 50}).beforeMainBus()
sulf_acid = Resource('sulf_acid', {iron: 1.0, sulfur: 5.0, water: 100.0 / 50}).beforeMainBus()

steel = Resource('steel', {iron: 5.0}).beforeMainBus()
plastic = Resource('plastic', {coal: 0.5, petro: 10.0 / 50}).beforeMainBus()
gear = Resource('gear', {iron: 2.0})
cable = Resource('cable', {copper: 0.5})
green_circuit = Resource('green_circuit', {iron: 1.0, cable: 3.0}).localIntermediate(cable)
red_circuit = Resource('red_circuit', {green_circuit: 2.0, plastic: 2.0, cable: 4.0}).beforeMainBus()
blue_circuit = Resource('blue_circuit', {red_circuit: 2.0, green_circuit: 20.0, sulf_acid: 5.0 / 50}).localDirectSupply(red_circuit).beforeMainBus()
low_dens = Resource('low_dens', {copper: 20.0, steel: 2.0, plastic: 5.0}).beforeMainBus()

battery = Resource('battery', {iron: 1.0, copper: 1.0, sulf_acid: 20.0 / 50})
explosives = Resource('explosives', {sulfur: 0.5, coal: 0.5, water: 5.0 / 50})
stick = Resource('stick', {iron: 0.5})
pipe = Resource('pipe', {iron: 1.0})
engine = Resource('engine', {gear: 1.0, pipe: 2.0, steel: 1.0}).localDirectSupply(pipe).localIntermediate(gear)
motor = Resource('motor', {engine: 1.0, green_circuit: 2.0})
fly_robo = Resource('fly_robo', {steel: 1.0, battery: 2.0, green_circuit: 3.0, motor: 1.0})
rocket_part = Resource('rocket_part', {low_dens: 10.0, blue_circuit: 10.0})

iron_chest = Resource('iron_chest', {iron: 8.0})
belt = Resource('belt', {iron: 1.0, gear: 1.0}).localIntermediate(gear)
red_belt = Resource('red_belt', {belt: 1.0, gear: 5.0}).localDirectSupply(belt).localIntermediate(gear)
blue_belt = Resource('blue_belt', {red_belt: 1.0, gear: 10.0}).localDirectSupply(red_belt).localIntermediate(gear)
ug_belt = Resource('ug_belt', {iron: 5.0, belt: 2.5}).localDirectSupply(belt)
red_ug_belt = Resource('red_ug_belt', {ug_belt: 1.0, gear: 20.0}).localDirectSupply(ug_belt).localIntermediate(gear)
blue_ug_belt = Resource('blue_ug_belt', {red_ug_belt: 1.0, gear: 40.0}).localDirectSupply(red_ug_belt).localIntermediate(gear)
splitter = Resource('splitter', {iron: 5.0, belt: 4.0, green_circuit: 5.0}).localDirectSupply(belt)
red_splitter = Resource('red_splitter', {splitter: 1.0, gear: 10.0, green_circuit: 10.0}).localDirectSupply(splitter).localIntermediate(gear)
blue_splitter = Resource('blue_splitter', {red_splitter: 1.0, gear: 10.0, red_circuit: 10.0}).localDirectSupply(red_splitter).localIntermediate(gear)
inserter = Resource('inserter', {iron: 1.0, gear: 1.0, green_circuit: 1.0}).localIntermediate(gear).localDirectSupply(green_circuit)
red_inserter = Resource('red_inserter', {inserter: 1.0, gear: 1.0, iron: 1.0}).localIntermediate(gear).localDirectSupply(inserter)
blue_inserter = Resource('blue_inserter', {inserter: 1.0, iron: 2.0, green_circuit: 2.0}).localDirectSupply(inserter)
green_inserter = Resource('green_inserter', {blue_inserter: 1.0, gear: 15.0, green_circuit: 15.0, red_circuit: 1.0}).localIntermediate(gear).localDirectSupply(blue_inserter)
elec_pole = Resource('elec_pole', {steel: 2.0, stick: 4.0, cable: 2.0}).localIntermediate(cable).localIntermediate(stick)
big_pole = Resource('big_pole', {steel: 5.0, stick: 8.0, cable: 4.0}).localIntermediate(cable).localIntermediate(stick)
substation = Resource('substation', {steel: 10.0, cable: 6.0, red_circuit: 5.0}).localIntermediate(cable)
pipe_to_ground = Resource('pipe_to_ground', {pipe: 10.0, iron: 5.0}).localDirectSupply(pipe)
rail = Resource('rail', {stone: 0.5, steel: 0.5, stick: 0.5}).localIntermediate(stick)
signal = Resource('signal', {iron: 5.0, green_circuit: 1.0})
logi_robot = Resource('logi_robot', {fly_robo: 1.0, red_circuit: 2.0})
cons_robot = Resource('cons_robot', {fly_robo: 1.0, green_circuit: 2.0})
steel_chest = Resource('steel_chest', {steel: 8.0})
storage_chest = Resource('storage_chest', {steel_chest: 1.0, green_circuit: 3.0, red_circuit: 1.0})
roboport = Resource('roboport', {steel: 45.0, green_circuit: 45.0, red_circuit: 45.0})
combinator = Resource('combinator', {green_circuit: 5.0, cable: 5.0})
selector = Resource('selector', {combinator: 5.0, red_circuit: 2.0})
stone_brick = Resource('stone_brick', {stone: 2.0})
concrete = Resource('concrete', {stone_brick: 0.5, iron_ore: 0.1, water: 10.0 / 50}).localIntermediate(stone_brick)

reactor = Resource('reactor', {concrete: 500.0, steel: 500.0, red_circuit: 500.0, copper: 500.0})
heat_pipe = Resource('heat_pipe', {steel: 10.0, copper: 20.0})
heat_exchanger = Resource('heat_exchanger', {steel: 10.0, pipe: 10.0, copper: 100.0})
turbine = Resource('turbine', {pipe: 20.0, copper: 50.0, gear: 50.0}).localIntermediate(gear)
drill = Resource('drill', {gear: 5.0, green_circuit: 3.0, iron: 10.0}).localIntermediate(gear)
elec_furnance = Resource('elec_furnance', {steel: 10.0, red_circuit: 5.0, stone_brick: 10.0}).localIntermediate(stone_brick)
assem_1 = Resource('assem_1', {iron: 9.0, gear: 5.0, green_circuit: 3.0}).localIntermediate(gear)
assem_2 = Resource('assem_2', {assem_1: 1.0, gear: 5.0, green_circuit: 3.0, steel: 2.0}).localIntermediate(assem_1).localIntermediate(gear)
chemical_plant = Resource('chemical_plant', {steel: 5.0, green_circuit: 5.0, pipe: 5.0, gear: 5.0}).localIntermediate(gear)
centrifuge = Resource('centrifuge', {steel: 50.0, gear: 100.0, red_circuit: 100.0, concrete: 100.0}).localIntermediate(gear)
lab = Resource('lab', {green_circuit: 10.0, belt: 4.0, gear: 10.0}).localIntermediate(gear)

mag = Resource('mag', {iron: 4.0})
pierce_mag = Resource('pierce_mag', {mag: 1.0, copper: 5.0, steel: 1.0}).localIntermediate(mag)
wall = Resource('wall', {stone_brick: 5.0}).localIntermediate(stone_brick)
grenade = Resource('grenade', {iron: 5.0, coal: 10.0})
laser_turret = Resource('laser_turret', {steel: 20.0, green_circuit: 20.0, battery: 12.0})
flamer_turret = Resource('flamer_turret', {steel: 30.0, pipe: 10.0, gear: 15.0, engine: 5.0}).localIntermediate(gear)

prod_mod = Resource('prod_mod', {red_circuit: 5.0, green_circuit: 5.0})

red_sci = Resource('red_sci', {copper: 1.0, gear: 1.0}).localIntermediate(gear)
green_sci = Resource('green_sci', {belt: 1.0, inserter: 1.0}).localDirectSupply(inserter)
gray_sci = Resource('gray_sci', {pierce_mag: 0.5, wall: 1.0, grenade: 0.5}).localDirectSupply(wall)
blue_sci = Resource('blue_sci', {sulfur: 0.5, red_circuit: 1.5, engine: 1.0})
purple_sci = Resource('purple_sci', {rail: 10.0, elec_furnance: 1/3.0, prod_mod: 1/3.0}).localDirectSupply(rail)
golden_sci = Resource('golden_sci', {blue_circuit: 2/3.0, fly_robo: 1/3.0, low_dens: 1.0})
