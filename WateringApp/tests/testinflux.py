from influxdb import InfluxDBClient


client = InfluxDBClient(host='localhost', port=8086)
# client.switch_database('humidity')

# print(client.get_list_database())
# client.create_database('pyexample')
if 'activation' not in client.get_list_database():
    client.create_database('activation')

client.switch_database('activation')


json_body = [
    {
        "measurement": "activation",
        "fields": {
            "value": 1
        }
    },

]

wasSuccessfull = client.write_points(json_body)

print(wasSuccessfull)

response = client.query('SELECT * FROM "humidity"')

# print('response: {}'.format(response))

# json_body = [
#     {
#
#     }
# ]
