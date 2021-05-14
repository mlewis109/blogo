from blogo import *

test_num = 0

tests_taken = 0
tests_passed = 0
tests_failed = 0
failed_list = []
tests_should_fail = 1

def do_test(name, test, expected_result):
    global test_num, result, failed_list
    global tests_taken, tests_passed, tests_failed
    tests_taken += 1
    print("Test "+str(test_num))
    print("    "+name)
    crash = False
    result = None
    turtle = Blogo("regression-test")
    full_test = """
turtle = Blogo("regression-test-"""+str(test_num)+"""")
global result
"""
    full_test += test
    
    try:
        exec(full_test)
    except Exception as e:
        crash = True
        result = str(e)
        
    print("Result = '"+str(result)+"'")
    def equal_enough(a, b):
        EPS = 0.00001
        if (a == b):
            return True
        try:
            if (len(a) != len(b)):
                return False
            for ai, bi in zip(a, b):
                try:
                    if (abs(ai - bi) > EPS):
                        return False
                except:
                    #if (a != b):
                    if (not equal_enough(ai, bi)):
                        return False
            return True
        except:
            pass   # Not iterable
        try:
            if (abs(a - b) < EPS):
                return True
        except:
            pass   # Can not do subtraction on them
        return False
    if (equal_enough(expected_result, result)):
        print("======")
        print("PASSED")
        print("======")
        tests_passed += 1
    else:
        print("Expected result = '"+str(expected_result)+"'")
        print("FAILED")
        tests_failed += 1
        if (test_num > 0):
            failed_list.append(test_num)
    print("")
    print("")
    test_num += 1
    
def show_results():
    global tests_taken, tests_passed, tests_failed
    global failed_list, tests_should_fail
    print("")
    print("Tests taken  = "+str(tests_taken))
    print("Tests passed = "+str(tests_passed))
    if (tests_failed != tests_should_fail or (tests_taken - tests_passed) != tests_should_fail):
        happy = False
        fail_str = " --> " + str(failed_list)
    else:
        happy = True
        fail_str = ""
    print("Tests failed = "+str(tests_failed) + fail_str)
    print("Tests that should fail = "+str(tests_should_fail))
    if (happy):
        print("YAY")
    else:
        print("ARGH!")

do_test("Simple test fail", """
turtle.fd(100)
result = turtle.get_pos()
""", (100, 100, 100))

do_test("Simple forward", """
turtle.fd(100)
result = turtle.get_pos()
""", (0, 100, 0))

do_test("Simple forward/left/forward", """
turtle.fd(100)
turtle.lt(90)
turtle.fd(100)
result = turtle.get_pos()
""", (-100, 100, 0))

do_test("Simple forward/right/forward", """
turtle.fd(100)
turtle.rt(90)
turtle.fd(100)
result = turtle.get_pos()
""", (100, 100, 0))

do_test("Simple forward/up/forward", """
turtle.fd(100)
turtle.up(90)
turtle.fd(100)
result = turtle.get_pos()
""", (0, 100, 100))

do_test("Simple forward/down/forward/left/forward", """
turtle.fd(100)
turtle.down(90)
turtle.fd(100)
turtle.lt(90)
turtle.fd(100)
result = turtle.get_pos()
""", (-100, 100, -100))

do_test("Get heading", """
result = []
result.append(turtle.get_heading())
turtle.lt(45)
result.append(turtle.get_heading())
turtle.fd(10)
turtle.lt(90)
result.append(turtle.get_heading())
turtle.fd(10)
turtle.lt(45)
result.append(turtle.get_heading())
turtle.rt(180)
result.append(turtle.get_heading())
turtle.rt(90)
result.append(turtle.get_heading())
turtle.lt(90)
result.append(turtle.get_heading())
""", [90, 135, 225, 270, 90, 0, 90])

do_test("Set heading", """
result = []
result.append(turtle.get_heading())
turtle.set_heading(45)
result.append(turtle.get_heading())
turtle.fd(10)
turtle.set_heading(135)
result.append(turtle.get_heading())
turtle.fd(10)
turtle.set_heading(180)
result.append(turtle.get_heading())
turtle.set_heading(0)
result.append(turtle.get_heading())
turtle.set_heading(-90)
result.append(turtle.get_heading())
turtle.set_heading(360)
result.append(turtle.get_heading())
""", [90, 45, 135, 180, 0, 270, 0])

do_test("Get vheading", """
result = []
result.append(turtle.get_v_heading())
turtle.down(45)
result.append(turtle.get_v_heading())
turtle.fd(10)
turtle.down(90)
result.append(turtle.get_v_heading())
turtle.fd(10)
turtle.down(45)
result.append(turtle.get_v_heading())
turtle.up(180)
result.append(turtle.get_v_heading())
turtle.up(90)
result.append(turtle.get_v_heading())
turtle.down(90)
result.append(turtle.get_v_heading())
""", [0, 0, 180, 180, 0, 0, 0])

do_test("Head towards coord", """
result = []
side1 = 100
side2 = 200
turtle.rt(45)
turtle.fd(side1)
turtle.up(90)
turtle.fd(side2)
turtle.set_heading_towards((0,0,0))
dist_from_home = math.sqrt(side1*side1 + side2*side2)
turtle.fd(dist_from_home)
result.append(turtle.get_pos())

start_pos = (1, 2, 3)
turtle.set_pos(start_pos)
turtle.set_heading_towards((10, 20, 30))
turtle.fd(100)
turtle.rt(30)
turtle.up(40)
turtle.rt(30)
turtle.set_heading_towards(start_pos)
turtle.fd(100)
result.append(turtle.get_pos())
""", [(0, 0, 0), (1, 2, 3)])

show_results()