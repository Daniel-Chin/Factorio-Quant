ROCKET_PART = 0.34  # 3.4 rockets / 500s
SPS =  4.0
FIBER = 0.4

PRODUCTIVITY = 1.78
SPEED = 2.0 * (1 - 0.1 * 4)

FRUIT_PER_TREE = 50.0 / 5 / 60

def forward(need_nutrient_as_fuel: float, p):
    acc_fuel = 0.0
    nutrient = need_nutrient_as_fuel

    p('fiber', format(FIBER, '.2f'))
    productivity = 1.5 * (1 - 0.188)
    speed = 1.6
    n_chambers = FIBER * 5 / speed / productivity
    p(f'{n_chambers = }')
    acc_fuel += n_chambers * 0.5
    p('carbon', FIBER * 1 / productivity)
    y_mash = FIBER * 10 / productivity
    del productivity, speed
    p()

    p('sci', format(SPS, '.2f'))
    n_chambers = SPS * 4 / SPEED / PRODUCTIVITY
    p(f'{n_chambers = }')
    acc_fuel += n_chambers * 1.7
    egg = SPS * 1 / PRODUCTIVITY
    bioflux = SPS * 1 / PRODUCTIVITY
    p()

    p('egg', format(egg, '.2f'))
    n_chambers = egg * 15 / SPEED / PRODUCTIVITY
    p(f'{n_chambers = }')
    acc_fuel += n_chambers * 1.7
    nutrient += egg * 30 / PRODUCTIVITY
    p()

    rocket_fuel = ROCKET_PART / 1.1
    p('rocket fuel', format(rocket_fuel, '.2f'))
    n_chambers = rocket_fuel * 10 / SPEED / PRODUCTIVITY
    p(f'{n_chambers = }')
    acc_fuel += n_chambers * 1.7
    bioflux += rocket_fuel * 2 / PRODUCTIVITY
    jelly = rocket_fuel * 30 / PRODUCTIVITY
    p()

    p('nutrient', format(nutrient, '.2f'))
    n_chambers = nutrient * (2 / 40) / SPEED / PRODUCTIVITY
    p(f'{n_chambers = }')
    acc_fuel += n_chambers * 1.7
    bioflux += nutrient / 8 / PRODUCTIVITY
    p()

    p('bioflux', format(bioflux, '.2f'))
    speed = SPEED * 1.3 # quality-2 biochamber
    n_chambers = bioflux * (6 / 4) / speed / PRODUCTIVITY
    p(f'{n_chambers = }')
    acc_fuel += n_chambers * 1.7
    y_mash += bioflux * 15 / 4 / PRODUCTIVITY
    jelly += bioflux * 12 / 4 / PRODUCTIVITY
    del speed
    p()

    p('jelly', format(jelly, '.2f'))
    n_chambers = jelly / 4 / SPEED / PRODUCTIVITY
    p(f'{n_chambers = }')
    acc_fuel += n_chambers * 1.7
    brain = jelly / 4 / PRODUCTIVITY
    p()

    p('y_mash', format(y_mash, '.2f'))
    n_chambers = y_mash / 2 / SPEED / PRODUCTIVITY
    p(f'{n_chambers = }')
    acc_fuel += n_chambers * 1.7
    yumako = y_mash / 2 / PRODUCTIVITY
    p()

    p('brain', format(brain, '.2f'))
    p('trees', brain / FRUIT_PER_TREE)
    p()

    p('yumako', format(yumako, '.2f'))
    p('trees', yumako / FRUIT_PER_TREE)
    p()

    p('Total chambers ~=', acc_fuel / 1.7)

    return acc_fuel / 2.0

def nop(*_, **__):
    pass

def main():
    guess = 1.0
    while True:
        actual = forward(guess, nop)
        loss = abs(actual - guess)
        # print(f'{loss = }')
        if loss < 1e-6:
            break
        guess = actual
    # input('Found solution. Enter...')
    forward(actual, print)

if __name__ == '__main__':
    main()
