# Overrun Oubliette

## To Run

Install files to a single directory and enter `python3 runner.py` in the command line.

The game will parse standard commands in a few basic formats. Enter "help" at any time (past the intro) to see the list of available commands.

## Known Issues
- [ ] Damage/defense is not well scaled; most encounters end in one interchange. Better linking to hero levels by individual stat (rather than overall level as currently handled) will likely improve this.
- [ ] Item impact on stats occasionally goes rogue, adding or subtracting large and seemingly random nombers. This is difficult to replicate, so the cause is unknown. Typically this is not a breaking issue if it happens at all.

## Future Features

- [ ] Add a map; the directions are difficult to keep track of, making returning  to prior locations particularly challenging.
- [ ] Add disadvantages based on affinity, potentially including:
  - [ ] Disadvantage when facing an enemy or weapon with opposing affinity
  - [ ] Disadvantage when attempting to use an item with opposing affinity
