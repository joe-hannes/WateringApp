from influxdb import InfluxDBClient


client = InfluxDBClient(host='localhost', port=8086)
# client.switch_database('humidity')


# client.create_database('pyexample')
client.switch_database('humidity')


json_body = [
    {
        "measurement": "humidity",
        "fields": {
            "value": 27
        }
    },

]

wasSuccessfull = client.write_points(json_body)

print(wasSuccessfull)

response = client.query('SELECT * FROM "humidity"')

print('response: {}'.format(response))

# json_body = [
#     {
#
#     }
# ]
