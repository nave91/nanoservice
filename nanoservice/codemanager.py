class CodeManager:


    def train(self):
        raise NotImplemented

    def test_code(self, trained_algorithm, input):
        raise NotImplemented

    def validate_input(self, input):
        raise NotImplemented
