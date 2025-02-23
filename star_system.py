from resources import *

RTT = 500 # hauler round trip time in sec
DEMAND = {
  red_sci   : 4.0, 
  green_sci : 4.0, 
  gray_sci  : 2.0, 
  blue_sci  : 4.0, 
  purple_sci: 3.0, 
  golden_sci: 4.0, 
  white_sci : 4.0,
  em_sci    : 4.0,
  agri_sci  : 1.0,
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
  - eventually, plastic + coal + sulfur
- orbit drops carbon, ice, iron_ore, calcite

## nauvis
- use biolabs
- im
  - all sci
  - bioflux
  - blue_circuit
  - tungsten carbide
  - superconductor
  - fibre
  - lithium plate
  - fluoroketone
- ex
  - supply fission fuel, for now
  - eventually, none.
- harvestor drops prom chunks; orbit drops white sci

## gleba
- im
  - rocket parts
- ex
  - sci: {consumeOneRocketPerTrip()}
  - bioflux: {consumeOneRocketPerTrip()}
  - fibre: {ship(fibre)}
  - stack inserter: future
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
  - tungsten carbide: {ship(tungsten_carbide, local_rocket_mats=(blue_circuit, low_dens))}
  - tungsten plate: on-demand
- im
  - heavy oil barrels (for lube)
  - rocket fuel
  - eventually, plastic + coal + sulfur
- drop ice, carbon

## aquilo
- im
  - rocket parts
  - holmium plate
  - 
  - concrete
  - iron
  - copper
  - steel
  - engine
  - plastic
  - heat pipes
  - 
  - silo
  - landing pad
- ex
  - sci: {ship(cryo_sci)}
  - fluoroketon barrels: {ship(fluoroketone)}
  - lithium plate: {ship(lithium_plate)}
  - fusion cells: trace amount
  - maybe plastic + coal + sulfur!!! If this is the case, scratch fulgora

## stats
- {acc_rocket * RTT} rocket / {RTT} sec

## Issues
- inf plastic?
  - eventaully, aquilo route water + fulgora oil + space carbon
  - now, spend a lot of sulf acids
  - what if aquilo = inf plastic?
- scale gleba sci?
  - just don't do it
    - or duplicate the base. but that's 0 fun isn't it

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
      (guess[resource] - actual[resource]) ** 2 
      for resource in guess.keys()
    ])
    if loss < 1e-6:
      break
    guess = actual
  input('Found solution. Enter...')
  print()
  print(markdown)

if __name__ == '__main__':
  main()
