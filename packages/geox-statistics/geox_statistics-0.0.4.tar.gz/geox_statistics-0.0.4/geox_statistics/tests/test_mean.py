from geox_statistics import mean

def test_mean_of_three_values():
    value = mean.mean([2, 4, 6])
    assert value == 6
