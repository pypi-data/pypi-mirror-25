## install
```python
python setup.py install
```

## Run
```python
camel_race
```

## Requirements
This game was developed and tested on Fedora 25 with python 2.7

## Design in a glance
Launcher objects receives CLiGame instance 
    manages the full life cycle of the game
    responsible for printing
    
CamelRace is instance of CLiGame and receives CamelRaceGameConfig object
    internal state represented by self.camels = dict(camel_name, camel)
    next_turn() method controlled by launcher, executes periodically each round, manipulates internal state and relation between camel
    race is composed of:
        InputProcessor: processes user input according to game rules (local), also simulates cpu players
        commenter : static methods to create comments (imports messages from constants due to multilanguage support, comment related messages could go here instead)
    
CamelRaceGameConfig consists of global config and camels info:
    loads configs and serves as camels factory
    also prompt user for config
    
Three camel classes are instance of Camel abstract class
    each camel has special proporties
    each camel has a weapon, weapon instance has all the info needed to make attack 
    
   
## Tests 
implemented some examples:

* for some interactive methods, doctest is enough and improves code readability
example: python -m doctest -v games/cli_game_launcher.py

* unittests: few unittests are implemented
example: python tests/test_race.py

* blackbox tests:
example: python tests/run_black_box_test.py  (uses files under tests/black_tests)
this will start a race of all cpu managed camels, and will save all the random inputs produced by cpu in results.pkl file
and save all internal states of the game in state.pkl file in the same directory
now (input config file + results file should produce same state file ) can be used as inputs for black box test
create as much as you want to increase coverage, can be extended to allow manual input from user
