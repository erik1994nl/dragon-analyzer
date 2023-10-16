from route_animation import animate_route

from speedcoach.reader import read_data, read_data_data_frame

speed_data_data_frame = read_data_data_frame()
speed_data = read_data()

animate_route(speed_data)
