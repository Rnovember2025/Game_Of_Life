import pytest
from main import make_random_state,step_simulation,Conways_Rules,parse_rfe

def test_mk_rndm_st():
    assert len(make_random_state(0,(0,0),50)) == 0, \
           "State specified with 0 area returned cells"
    assert len(make_random_state(10,(0,0),50)) == 50, \
           "State specified as 50% full is greater or less than half full"
    assert len(make_random_state(10,(0,0),0)) == 0, \
           "State specified as 0% full has a non zero length"

    state = make_random_state(5,(2,2),100)
    assert len(state) == 25, "State specified as 100% full is less than 100% full"
    low_x = 2
    low_y = 2
    high_x = 2
    high_y = 2

    for cell in state:
        test_x = cell[0]
        test_y = cell[1]

        low_x = min(low_x,test_x)
        low_y = min(low_y,test_y)
        high_x = max(high_x,test_x)
        high_y = max(high_y,test_y)

    assert 0 <= low_x <= 2, "State containes cells outside specified area"
    assert 0 <= low_y <= 2, "State containes cells outside specified area"
    assert 2 <= high_x <= 5, "State containes cells outside specified area"
    assert 2 <= high_y <= 5, "State containes cells outside specified area"

def test_step_simulation():
    state = [(1,1),(2,1),(3,1),(2,1),(3,2)]
    step_simulation(state, Conways_Rules)
    assert state == [(2, 1), (3, 1), (3, 2), (2, 0)], \
           "Simulation did not follow Conways Rules of the Game of Life"

    state = []
    step_simulation(state,Conways_Rules)
    assert state == [], "Simulation of blank state yielded alive cells somehow..."

def test_Conways_Rules():
    assert Conways_Rules([1,0,0,0,1,0,0,0,0]) == False, \
           "Class Conways_Rules did not follow Conways_Rules"
    assert Conways_Rules([1,1,0,0,1,0,0,0,0]) == True, \
           "Class Conways_Rules did not follow Conways_Rules"
    assert Conways_Rules([1,1,0,0,1,0,0,1,0]) == True, \
           "Class Conways_Rules did not follow Conways_Rules"
    assert Conways_Rules([1,1,0,0,1,0,0,1,1]) == False, \
           "Class Conways_Rules did not follow Conways_Rules"

    assert Conways_Rules([1,1,0,0,0,0,0,0,0]) == False, \
           "Class Conways_Rules did not follow Conways_Rules"
    assert Conways_Rules([0,0,1,0,0,1,1,0,0]) == True, \
           "Class Conways_Rules did not follow Conways_Rules"
    assert Conways_Rules([0,0,1,1,0,1,1,0,0]) == False, \
           "Class Conways_Rules did not follow Conways_Rules"

def test_parse_rfe():
    assert parse_rfe("bob$2bo$ooo!") == [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    assert parse_rfe("junk_o!") == [(0,0)]

pytest.main(["-v", "--tb=line", "-rN", __file__])
