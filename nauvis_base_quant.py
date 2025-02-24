'''
pre bus productions
    smelting

    oil processing
    sulfur
    sulf_acid
    battery
    explosive

    plastic
    (green_circuit) (22 assems)
    red_circuit     (needs 7.6 green circuits) (22 assems)
    blue_circuit    (needs 36 green circuits, 3.6 red circuits) (18 assems)
    low_dens        (needs 40 copper) (30 assems)

pre bus
    copper  (74.6)
    copper
    steel   ( 4.0)  (shared with main bus, so 12.4; ore = 62)
    iron    (45.0) - green_circuit  (43.6)

    (petro) ( 5.8 barrels) (70 petro per refinery)
    plastic (24.9)
    coal
    sulfur - sulf_acid

main bus
    iron
    copper
    steel
    stone
'''

# from pprint import pprint

from resources import *

def main():
    ONE_PER_HOUR = 1.0 / 60 / 60
    d = {
        rocket_part: 0.15, 
        belt: 1.0, 
        red_belt: 0.3,
        blue_belt: 0.1, 
        ug_belt: 0.1, 
        red_ug_belt: 0.05, 
        blue_ug_belt: 0.01, 
        splitter: 0.1, 
        red_splitter: 0.03,
        blue_splitter: 0.01,
        iron_chest: 0.1,
        inserter: 0.1, 
        blue_inserter: 0.1, 
        elec_pole: 0.1, 
        big_pole: 0.05, 
        substation: 0.02, 
        pipe_to_ground: 0.1, 
        rail: 0.3, 
        signal: 0.1, 
        logi_robot: 0.1, 
        cons_robot: 0.1,
        storage_chest: 0.01,
        roboport: 0.01,
        combinator: 0.03,
        selector: 0.01,
        reactor: ONE_PER_HOUR,
        heat_pipe: ONE_PER_HOUR * 8, 
        heat_exchanger: ONE_PER_HOUR * 4,
        centrifuge: ONE_PER_HOUR, 
        turbine: ONE_PER_HOUR * 8,
        drill: 0.01, 
        elec_furnance: 0.02, 
        assem_2: 0.02, 
        chemical_plant: 0.005, 
        lab: ONE_PER_HOUR, 
        wall: 0.1, 
        laser_turret: 0.01, 
        flamer_turret: 0.01, 
        red_sci   : .5, 
        green_sci : .5,
        gray_sci  : .5,
        blue_sci  : .5,
        purple_sci: .5,
        golden_sci: .5,
    }
    items = Resource.dictConsumesThroughput(d, ignore_top=True).items()
    for k, v in sorted(items, key=lambda x: x[1], reverse=True):
        if v == 0.0:
            continue
        print(k, f'{v:6.1f}', sep='\t')
    
    # print('\n\nBreakdown\n\n')
    # for res, qty in d.items():
    #     print(res, qty)
    #     for k, v in res.consumesThroughput().items():
    #         print(k, f'{v * qty:6.1f}', sep='\t')
    #     print()

if __name__ == '__main__':
    main()
