from contextional import GCM


with GCM("Main Group") as MG:

    @GCM.add_setup("do a thing")
    def setUp():
        GCM.value = 1

    @GCM.add_teardown("undo all the things")
    def tearDown():
        GCM.value += 1

    with GCM.add_group("Child Group"):

        @GCM.add_setup("do another thing")
        def setUp():
            GCM.value += 1

        @GCM.add_teardown("undo that last thing")
        def setUp():
            GCM.value -= 1

        @GCM.add_test("value is 2")
        def test(case):
            case.assertEqual(GCM.value, 2)

    with GCM.add_group("Child Group"):

        @GCM.add_setup("do another thing")
        def setUp():
            GCM.value += 1

        @GCM.add_teardown("undo that last thing")
        def setUp():
            GCM.value -= 1

        @GCM.add_test("value is 2")
        def test(case):
            case.assertEqual(GCM.value, 2)


MG.create_tests()
