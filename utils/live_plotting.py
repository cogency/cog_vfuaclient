# todo: make a nice function

# if 0:
#     # import matplotlib.pyplot as plt
#     # from matplotlib.animation import FuncAnimation
#     # from collections import deque

#     client = Client("opc.tcp://localhost:4840")
#     client.connect()

#     node = client.get_node("ns=2;s=VoluflowMetric")

#     # data = [(x.get_browse_name().Name, x.get_value()) for x in node.get_children()]

#     keep = ['mean_bed', "flow_tracking", "vflow"]

#     nodes = {x.get_browse_name().Name: x for x in node.get_children() if x.get_browse_name().Name in keep}

#     max_len = 60
#     data = {key: deque(maxlen=max_len) for key in nodes}
#     timestamps = deque(maxlen=max_len)

#     fig, ax = plt.subplots()

#     lines = {
#         key: ax.plot([], [], label=key)[0] for key in nodes
#     }

#     ax.set_xlim(0, max_len)
#     ax.set_ylim(0, 100)  # adjust depending on expected range
#     ax.legend()
#     plt.xlabel("Time (s ago)")
#     plt.ylabel("Value")
#     plt.title("Live OPC-UA Variable Plot")

#     start_time = time.time()

#     def update(frame):
#         now = time.time()
#         timestamps.append(now - start_time)

#         for key, node in nodes.items():
#             try:
#                 value = node.get_value()
#             except:
#                 value = None
#             data[key].append(value)

#         ax.clear()
#         for key in nodes:
#             t_vals = list(timestamps)
#             y_vals = list(data[key])
#             ax.plot(
#                 [t_vals[-1] - t for t in t_vals],  # make x-axis go backward in seconds
#                 y_vals,
#                 label=key
#             )

#         ax.set_xlim(0, max_len)
#         ax.set_ylim(auto_ylim())
#         ax.legend()
#         ax.grid(True, which='both')
#         ax.set_xlabel("Seconds Ago")
#         ax.set_ylabel("Value")
#         ax.set_title("Live OPC-UA Variable Plot")

#     def auto_ylim():
#         all_vals = [v for series in data.values() for v in series if v is not None]
#         if not all_vals:
#             return 0, 1
#         min_val = min(all_vals)
#         max_val = max(all_vals)
#         return min_val - 5, max_val + 5

#     ani = FuncAnimation(fig, update, interval=1000)  # every 1000 ms

#     try:
#         plt.show()
#     finally:
#         client.disconnect()