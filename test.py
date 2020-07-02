def returns_true():
    return True

def returns_false():
    return False

def stored_value():
    foo = True
    return foo

def if_true_test():
    foo = returns_true()
    if foo:
        return foo
    else:
        return False

def never_used():
    return True

def main():
    print(returns_true())
    print(returns_false())

if __name__ == "__main__":
    main()

def test_always_passes():
    assert returns_true()

def test_always_fails():
    assert returns_false()

def test_stored_value():
    assert stored_value()

def test_if_true():
    assert if_true_test()
