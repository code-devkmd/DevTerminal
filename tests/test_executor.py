from devcli.core.executor import execute_command

def test_empty():
    assert execute_command("") == True