import unittest
import index


class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        print("testing response.")
        result = index.handler(None, None)
        print(result)


if __name__ == '__main__':
    unittest.main()
