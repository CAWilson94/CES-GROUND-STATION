
def test(passes):
    first_pass = passes.first().riseTime
    end_pass = passes.last().setTime
    duration = end_pass - first_pass
    print("DURATION: ----------------" + str(duration))

    total_contact_time = 0
    for item in passes:
        total_contact_time += item.duration.seconds

    total_non_contact_time = duration.seconds - total_contact_time

    print("TOTAL CONTACT TIME ======" + str(total_contact_time) + " IN SECONDS")

    print("TOTAL NON CONTACT TIME ======" + str(total_non_contact_time) + " IN SECONDS")
