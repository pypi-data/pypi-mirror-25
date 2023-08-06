from contextional import GCM
import os
import psutil


def thing():
    with GCM("Stuff") as S:

        @GCM.add_test("test description")
        def test(case):
            pass

        with GCM.add_group("More Stuff"):

            @GCM.add_test("test description")
            def test(case):
                pass

            with GCM.add_group("More Stuff"):

                @GCM.add_test("test description")
                def test(case):
                    pass

    return S



with GCM("Main Group") as MG:


    GCM.includes(thing())

    with GCM.add_group("Mor ethings"):

        @GCM.add_test("othe rtest")
        def test(case):
            pass




MG.create_tests()
