from adapters import InputAdapter, OutputAdapter


def test_input_adapter():
    def mock_input():
        return "mock"

    adapter = InputAdapter(mock_input)
    assert adapter.get_input() == "mock"


def test_output_adapter():
    def mock_output(output):
        assert output == "mock"

    adapter = OutputAdapter(mock_output)
    adapter.send_output("mock")
