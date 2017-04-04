
def test(passes):
    first_pass = passes.first().riseTime
    end_pass = passes.last().setTime
    duration = end_pass - first_pass
    print("DURATION: ----------------" + str(duration))
