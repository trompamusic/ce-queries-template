# Tests for mutations pertaining to person objects.
import os
import unittest

from trompace.queries import person as person_query
from trompace.mutations.person import mutation_create_person, mutation_update_person, mutation_delete_person
from tests import util


class TestPerson(unittest.TestCase):

    def setUp(self) -> None:
        super()
        self.data_dir = os.path.join(os.path.dirname(__file__), "data", "person")

    def test_query(self):
        expected = util.read_file(self.data_dir, "EXPECTED_PERSON_QUERY.txt")

        created_person = person_query.query_person("ff59650b-1d47-4ea5-b356-31fddeb48315")
        self.assertEqual(created_person, expected)

    def test_query_all(self):
        expected = util.read_file(self.data_dir, "EXPECTED_PERSON_QUERY_ALL.txt")

        created_person = person_query.query_person()
        self.assertEqual(created_person, expected)

    def test_create(self):
        expected = util.read_file(self.data_dir, "EXPECTED_PERSON.txt")

        created_person = mutation_create_person("A. J. Fynn", "https://www.cpdl.org","https://www.upf.edu", "https://www.cpdl.org/wiki/index.php/A._J._Fynn",
         "en", description="Born circa 1860Died circa 1920A. J. Fynn was an early 20th Century scholar in literature and anthropology")
        self.assertEqual(created_person, expected)

    def test_update(self):
        expected = util.read_file(self.data_dir, "EXPECTED_PERSON_UPDATE.txt")

        created_update = mutation_update_person('2eeca6dd-c62c-490e-beb0-2e3899fca74f',
                                                title="A. J. Fynn")
        self.assertEqual(created_update, expected)

    def test_delete(self):
        expected = util.read_file(self.data_dir, "EXPECTED_PERSON_DELETE.txt")

        created_delete = mutation_delete_person('2eeca6dd-c62c-490e-beb0-2e3899fca74f')
        self.assertEqual(created_delete, expected)
