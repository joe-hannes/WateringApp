from WateringApp.Fachwerte.URI import URI
import unittest


class TestURI(unittest.TestCase):


    def test_get_uri_string(self):
        uri = URI(
            db_type = "sqlite",
            db_name = "testdb",
        )

        self.assertTrue(uri.get_uri_string() == "sqlite:///testdb.db")

        uri2 = URI(
            db_type = "influx",
            db_port = 8086
        )
        self.assertTrue(uri2.get_uri_string() == "localhost")

        uri3 = URI(
            db_type = "mysql+pymysql",
            db_username = "username",
            db_password = "password",
            base_uri = "192.168.178.27",
            db_port = "3306",
            db_name = "watering_system"
        )

        self.assertTrue(uri3.get_uri_string() == "mysql+pymysql://username:password@192.168.178.27:3306/watering_system")


if __name__ == '__main__':
    unittest.main()
