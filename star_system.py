from resources import *

RTT = 500 # hauler round trip time in sec
DEMAND = {
  red_sci   : 4.0, 
  green_sci : 4.0, 
  gray_sci  : 4.0, 
  blue_sci  : 4.0, 
  purple_sci: 4.0, 
  golden_sci: 4.0, 
  white_sci : 4.0,
  em_sci    : 4.0,
  agri_sci  : 4.0,
  metal_sci : 4.0,
  cryo_sci  : 4.0, 
  prom_sci  : 4.0, 
}
ROCKET_PRODUCTIVITY = 1 + 0.6 * 4 # 4 x prod-2 modules

def forward(
  imported_rocket_mats: tp.Dict[Resource, float], 
):
  acc_import = {
    rocket_fuel: 0.0, 
    blue_circuit: 0.0, 
    low_dens: 0.0,
  }
  acc_rocket = 0.0

  def ship(
    resource: Resource, local_rocket_mats: tp.Tuple[Resource, ...] = (), 
  ):
    nonlocal acc_rocket
    assert resource.rocket_capacity is not None, resource
    n_per_sec = 0
    n_per_sec += imported_rocket_mats.get(resource, 0.0)
    if   resource is rocket_fuel:
      pass
    elif resource is blue_circuit:
      n_per_sec += DEMAND[prom_sci] * prom_sci.consumesThroughput()[blue_circuit]
    elif resource is low_dens:
      pass
    else:
      n_per_sec += sum([
        sps * sci.consumesThroughput().get(resource, 0.0) 
        # using throughput as inter-planetary throughput. this can break
        for sci, sps in DEMAND.items()
      ])
    this_resource_n_rockets_per_sec = n_per_sec / resource.rocket_capacity
    acc_rocket += this_resource_n_rockets_per_sec
    this_resource_n_rocket_parts_per_sec = this_resource_n_rockets_per_sec * 50 / ROCKET_PRODUCTIVITY
    for rocket_mat in acc_import.keys():
      if rocket_mat not in local_rocket_mats:
        acc_import[rocket_mat] += this_resource_n_rocket_parts_per_sec * rocket_part.ingredients[rocket_mat]
    return f'{n_per_sec:.2f} / s, {this_resource_n_rockets_per_sec * RTT:.1f} rockets / trip'

  def consumeOneRocketPerTrip():
    for rocket_mat in acc_import.keys():
      acc_import[rocket_mat] += 50 / RTT * rocket_part.ingredients[rocket_mat]
    return 'one rocket per trip'

  markdown = f'''
# star system
- Per second {DEMAND = }

## fulgora
- im
  - none
- ex
  - rocket_fuel: {ship(rocket_fuel, local_rocket_mats=(rocket_fuel, blue_circuit, low_dens))}
  - heavy oil barrels: {ship(lube, local_rocket_mats=(rocket_fuel, blue_circuit, low_dens))}
  - holmium plate: {ship(holmium_plate, local_rocket_mats=(rocket_fuel, blue_circuit, low_dens))}
  - superconductor: {ship(superconductor, local_rocket_mats=(rocket_fuel, blue_circuit, low_dens))}
  - sci: {ship(em_sci, local_rocket_mats=(rocket_fuel, blue_circuit, low_dens))}
  - eventually, plastic + grenade
- orbit drops carbon, ice, iron_ore, calcite

## nauvis
- use biolabs
- im
  - all sci
  - bioflux
- ex
  - supply fission fuel, for now
- orbit drops white sci

## gleba
- im
  - rocket parts
- ex
  - sci: {ship(agri_sci, local_rocket_mats=(rocket_fuel, ))}
  - bioflux: {consumeOneRocketPerTrip()}
  - fibre: {ship(fibre)} (to prom ship)
  - stack inserter: on-demand
- orbit drops carbon, but in the future

## vulcanus
- ex
  - red_sci: {ship(red_sci, local_rocket_mats=(blue_circuit, low_dens))}
  - green_sci: {ship(green_sci, local_rocket_mats=(blue_circuit, low_dens))}
  - gray_sci: {ship(gray_sci, local_rocket_mats=(blue_circuit, low_dens))}
  - blue_sci: {ship(blue_sci, local_rocket_mats=(blue_circuit, low_dens))}
  - purple_sci: {ship(purple_sci, local_rocket_mats=(blue_circuit, low_dens))}
  - golden_sci: {ship(golden_sci, local_rocket_mats=(blue_circuit, low_dens))}
  - metal_sci: {ship(metal_sci, local_rocket_mats=(blue_circuit, low_dens))}
  - blue circuits: {ship(blue_circuit, local_rocket_mats=(blue_circuit, low_dens))}
  - low_dens: {ship(low_dens, local_rocket_mats=(blue_circuit, low_dens))}
  - tungsten carbide: {ship(tungsten_carbide, local_rocket_mats=(blue_circuit, low_dens))} (to prom ship)
  - tungsten plate: on-demand
  - repair packs: on-demand
- im
  - heavy oil barrels (for lube)
  - rocket fuel
  - eventually, plastic (57/s) + grenade (16.7/s)
    - plastic 57/s
    - assume sulfur from space
    - petro 57 * 20 / 1.234 = 923.82 liquid / s
    - light/water = 923.82 / 2 * 3 / 1.234 = 1122.96 liquid /s
    - water = 1122.96 + 1122.96 / 1.234 = 2032.98 liquid / s
    - ice = 2032.98 / 20 / 1.234 = 82.37 / s
    - plastic water requirement (sulfur form space) is 57*30 = 1710/s
- orbit drops sulfur (4 droppers), carbon

## aquilo
- im
  - blue circuit, LDS (for rocket)
  - holmium plate
- ex
  - sci: {ship(cryo_sci)}
  - fluoroketon barrels: {ship(fluoroketone)}
  - lithium plate: {ship(lithium_plate)}
  - fusion cells: trace amount
  - maybe plastic + grenade!!! If this is the case, scratch fulgora

## stats
- {acc_rocket * RTT} rocket / {RTT} sec

## Issues
- inf plastic?
  - eventaully, aquilo route water + fulgora oil + space carbon
  - now, spend a lot of sulf acids
  - what if aquilo = inf plastic?

## todo
- fulgora
  - use logistics to solve the production    
'''

  return markdown, acc_import

def main():
  guess = {
    rocket_fuel: 1.0, 
    blue_circuit: 1.0,
    low_dens: 1.0,
  }
  while True:
    markdown, actual = forward(guess)
    print(*[format(x, '.2f') for x in actual.values()])
    loss = sum([
      abs(guess[resource] - actual[resource])
      for resource in guess.keys()
    ])
    if loss < 1e-8:
      break
    guess = actual
  input('Found solution. Enter...')
  print()
  print(markdown)

if __name__ == '__main__':
  main()
