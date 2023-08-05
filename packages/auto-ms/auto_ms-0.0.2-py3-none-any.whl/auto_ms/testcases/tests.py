from automation_ms.modules import parse, process
import os


class Test1:
    def setUp(self):
        self.test_input = 'testdata/ErCOTTHFBPh4-ac-vartemp-1750Oe.ac.dat'

    def test_input_exists(self):
        assert(os.path.exists(self.test_input))

    def test_parse_file(self):
        filepath = os.path.join(os.getcwd(), self.test_input)

        parsed = parse.parse_file(self.test_input)
        # test if the number of lines is correct. Test random
        assert('header' in parsed)
        assert('data' in parsed)
        assert(len(parsed['header']) == 18)
        print(len(parsed['data']))
        assert(len(parsed['data']) == 287)

    def test_parse_header(self):
        parsed = parse.parse_file(self.test_input)
        header = parse.parse_header(parsed['header'])
        assert(len(header['info']) == 8)
        assert(True)

    def test_parse_data(self):
        parsed = parse.parse_file(self.test_input)
        data = parse.parse_data(parsed['data'])
        assert(len(data) == 286)

    def test_process_data(self):
        parsed = parse.parse_file(self.test_input)
        data = parse.parse_data(parsed['data'])
        splat = process.split_data(data)
        assert(sum(len(item) for key, item in splat.items()) == 286)
