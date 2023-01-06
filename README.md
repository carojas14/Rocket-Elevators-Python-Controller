# Rocket Elevators Python Controller
This is the python residential controller program. The scenarios used to test the program is for a 10 story building served by 2 elevator cages.

The necessary file to run some tests is also included.

### Installation

make sure to install the Package Installer for Python (PIP) if needed:

https://pip.pypa.io/en/stable/installing/

Next, install Pytest:

https://docs.pytest.org/en/6.2.x/getting-started.html

Running the tests
To launch the tests:

`pytest`

You can also get more details about each test by adding the -v flag:

`pytest -v`


### This controller is capable of supporting two main events:

1. A person presses a call button to request an elevator, the controller selects an available cage and it is routed to that person based on two parameters provided by pressing the button:
a. The floor where the person is
b. The direction in which he wants to go (Up or Down)
It should be noted that an elevator already in motion (or stopped but still having other requests to be completed) should be prioritized versus an "Idle" elevator.
2. A person enters an elevator, selects a floor of the control panel and it moves to the floor requested. The parameter provided is the requested floor.


### Test Scenarios

Scenario 1:
Elevator A is Idle at floor 2
Elevator B is Idle at floor 6
Someone is on floor 3 and wants to go to the 7th floor.
Elevator A is expected to be sent.

Scenario 2:
Elevator A is Idle at floor 10
Elevator B is idle at floor 3
Someone is on the 1st floor and requests the 6th floor.
Elevator B should be sent.

2 minutes later, someone else is on the 3rd floor and requests the 5th floor. Elevator B should be sent.

Finally, a third person is at floor 9 and wants to go down to the 2nd floor.
Elevator A should be sent.

Scenario 3:
Elevator A is Idle at floor 10
Elevator B is Moving from floor 3 to floor 6
Someone is on floor 3 and requests the 2nd floor.
Elevator A should be sent.

5 minutes later, someone else is on the 10th floor and wants to go to the 3rd. Elevator B should be sent.

