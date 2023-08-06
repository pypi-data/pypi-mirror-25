from drivelink import List
import pytest
import os
#from Process import freeze_support


def test_list():
    lst = List("testList")
    for i in range(10):
        lst.append(i)
    for i in range(10):
        assert lst[i] == i


def test_change_settings():
    with List("testListChangeSettings", 1, 1) as l:
        l.append(1)
        l.append("c")
        l.append(3.4)
    with List("testListChangeSettings", 2, 2) as l:
        assert l[0] == 1
        assert l[1] == "c"
        assert l[2] == 3.4
    with List("testListChangeSettings", 1, 1) as l:
        assert l[0] == 1
        assert l[1] == "c"
        assert l[2] == 3.4


def test_init():
    with pytest.raises(ValueError) as excinfo:
        List("testListInit", 0)
    excinfo.match(".* per page.*")
    with pytest.raises(ValueError) as excinfo:
        List("testListInit", 1, 0)
    excinfo.match(".* in RAM.*")
    with List("testListInit", 1, 1):
        pass
    List("testListInit", 1, 1)


def test_guarantee_page():
    with List("testListGuaranteePage", 1, 1) as l:
        l.append(1)
        l.append("c")
        l.append(3.4)
        assert l[0] == 1
        assert l[1] == "c"
        assert l[2] == 3.4


def test_save():
    l = List("testListSave", 1, 1)
    l.append(1)
    l.append("c")
    l.append(3.4)
    l.close()
    with List("testListSave", 1, 1) as l:
        assert l[0] == 1
        assert l[1] == "c"
        assert l[2] == 3.4


def test_string_funcs():
    l = List("testListStringFuncs")
    assert str(l).startswith("List ")
    assert str(l).endswith("testListStringFuncs")
    assert repr(l).startswith("List(")
    assert repr(l).endswith(".DriveLink')")


def test_insert():
    l = List("testInsert", 1, 1)
    l.append(0)
    l.extend([1, 3])
    l.insert(2, 2)
    for i in range(4):
        assert l[i] == i
    l = List("testInsert", 2, 2)
    l.insert(1,-1)
    assert l[1] == -1
    assert l[2] == 1


def test_delete():
    l = List("testDelete", 1, 1)
    l.append(0)
    l.extend([0, 1, 2, 5, 3])
    del l[1]
    del l[3]
    for i in range(4):
        assert l[i] == i


def test_reverse():
    l = List("testReverse", 2, 2)
    l.extend([i for i in reversed(range(10))])
    for i, v in enumerate(reversed(l)):
        assert i == v
    for i in range(1,11):
        assert l[-i] == i-1

def test_contains():
    with List("testListContains", 1, 1) as l:
        l.append(1)
        l.append("c")
        l.append(3.4)
        assert 1 in l
        assert "c" in l
        assert 3.4 in l
        assert 2 not in l
        assert "d" not in l
        assert 3.3 not in l


if __name__ == '__main__':
    freeze_support()
    ut.main()
