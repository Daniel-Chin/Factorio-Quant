n_rockets_acc = 0

def oneMoreRocket():
    global n_rockets_acc
    n_rockets_acc += 1

s = f'''
# star system
- SPS = {(SPS := 4)}
- {(n_rockets := 6)} rocket / {(RTT := 500)} sec

## fulgora
- im
  - none
- ex
  - rocket_fuel
  - heavy oil barrels
  - holmium plate (1.5/s)
  - superconductor ()
  - sci
- drop carbon, ice, iron_ore, calcite

## nauvis
- biolabs
- fission supply, for the short term

## gleba
- im
  - rocket parts
- ex
  - sci
  - bioflux
  - fibre
  <!-- - stack inserter -->
<!-- - drop carbon -->

## vulcanus
- ex
  - all sci
  - empty barrels
  - blue circuits
  - low_dens
- im
  - lube barrels
  <!-- - plastic -->
  - rocket fuel
  - fibre
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
  - sci
  - fusion cells
  <!-- - plastic -->

## Issues
- inf plastic?
  - eventaully, aquilo route water + fulgora oil + space carbon
  - now, spend a lot of sulf acids
- conductors need oil?
- scale gleba sci?
  - just don't do it
    - or duplicate the base. but that's 0 fun isn't it

## todo
- fulgora
  - use logistics to solve the production    
'''

print(s)

assert n_rockets_acc == n_rockets, (n_rockets_acc, n_rockets)
