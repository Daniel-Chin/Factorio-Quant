# from pprint import pprint

from resources import *

def main():
    ONE_PER_HOUR = 1.0 / 60 / 60
    d = {
        red_sci   : 4.0, 
        green_sci : 4.0, 
        gray_sci  : 2.0, 
        blue_sci  : 4.0, 
        purple_sci: 3.0, 
        golden_sci: 4.0, 
        metal_sci : 4.0,

        blue_circuit: 0.31,
        low_dens: 0.31,

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
        heat_pipe: ONE_PER_HOUR * 8, 
        heat_exchanger: ONE_PER_HOUR * 4,
        turbine: ONE_PER_HOUR * 8,
        drill: 0.01, 
        elec_furnance: 0.02, 
        assem_2: 0.02, 
        chemical_plant: 0.005, 
    }
    items = Resource.dictConsumesThroughput(d, ignore_top=True).items()
    for k, v in sorted(items, key=lambda x: x[1], reverse=True):
        if v == 0.0:
            continue
        print(k, f'{v:6.1f}', sep='\t')
    
    print('\n\nBreakdown\n\n')
    for res, qty in d.items():
        print(res, qty)
        for k, v in res.consumesThroughput().items():
            print(k, f'{v * qty:6.1f}', sep='\t')
        print()

if __name__ == '__main__':
    main()
