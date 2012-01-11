from bossy.commands import Command, command, argument


def test_calling_a_Command_calls_its_function():
    def func():
        return 123

    assert Command(func)() == 123


def test_command_decorator_uses_function_name_if_none_provided():
    @command
    def func():
        return 123
    assert func.name == 'func'


def test_command_decorator_uses_explicit_name_if_one_provided():
    @command(name='explicit')
    def func():
        return 123
    assert func.name == 'explicit'


def test_argument_decorator_adds_an_argument_to_the_argument_list():
    @command
    @argument('-r', '--repetitions', type=int)
    def hello_n(repetitions):
        for i in xrange(repetitions):
            print 'Hello'
    assert len(hello_n.arguments) == 1
    assert hello_n.arguments[0] == (('-r', '--repetitions'), {'type': int})
