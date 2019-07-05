import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import psutil as p


POINTS = 300
fig, ax = plt.subplots(2,1)
axes=ax.flatten()

axes[0].set_ylim([0, 100])
axes[0].set_xlim([0, POINTS])
axes[0].set_autoscale_on(False)
axes[0].set_xticks([])
axes[0].set_yticks(range(0, 101, 20))
axes[0].set_ylabel("Percent")
axes[0].set_xlabel("T")
axes[0].set_title("CPU/Memory")
axes[0].grid(True)

axes[1].set_ylim([0, 200])
axes[1].set_xlim([0, POINTS])
axes[1].set_autoscale_on(False)
axes[1].set_xticks([])
axes[1].set_ylabel("Packets")
axes[1].set_xlabel("T")
axes[1].set_title("Network Packets")
axes[1].set_yticks(range(0, 201, 40))
axes[1].grid(True)

cpu = [None] * POINTS
memory = [None] * POINTS

l_cpu, = axes[0].plot(range(POINTS), cpu, label='CPU %')
l_memory, = axes[0].plot(range(POINTS), memory, label='Memory %')
axes[0].legend(loc='upper center', ncol=6, prop=font_manager.FontProperties(size=10))
bg = fig.canvas.copy_from_bbox(axes[0].bbox)


packet_send = [None] * POINTS
packet_recv = [None] * POINTS
l_packet_send, = axes[1].plot(range(POINTS), packet_send, label='packet_send')
l_packet_recv, = axes[1].plot(range(POINTS), packet_recv, label='packet_recv')
axes[1].legend(loc='upper center', ncol=3, prop=font_manager.FontProperties(size=10))
#bg_net = fig.canvas.copy_from_bbox(axes[1].bbox)

def network_packet():
	t = p.net_io_counters()
	return [t.packets_sent, t.packets_recv]


before_net = network_packet()



def get_network_packet():
	global before_net
	now_net = network_packet()
	delta = [now_net[i] - before_net[i] for i in range(len(now_net))]
	before_net = now_net
	return [dt for dt in delta]

def OnTimer(ax):
	global bg, memory, packet_send, packet_recv, cpu
	tmp_net = get_network_packet()
	packet_send = packet_send[1:] + [tmp_net[0]]
	packet_recv = packet_recv[1:] + [tmp_net[1]]
	cpu = cpu[1:] + [p.cpu_percent()]
	memory = memory[1:] + [p.virtual_memory().percent]
	"""
	l_user.set_ydata(user)
	l_sys.set_ydata(sys)
	l_idle.set_ydata(idle)
	"""
	l_cpu.set_ydata(cpu)
	l_memory.set_ydata(memory)
	l_packet_send.set_ydata(packet_send)
	l_packet_recv.set_ydata(packet_recv)
	while True:
		try:
			"""
			axes[0].draw_artist(l_user)
			axes[0].draw_artist(l_sys)
			axes[0].draw_artist(l_idle)
			"""
			axes[0].draw_artist(l_cpu)
			axes[0].draw_artist(l_memory)
			axes[1].draw_artist(l_packet_send)
			axes[1].draw_artist(l_packet_recv)
			break
		except:
			pass
	axes[0].figure.canvas.draw()


def start_monitor():
	timer = fig.canvas.new_timer(interval=100)
	timer.add_callback(OnTimer, axes[0])
	timer.start()
	plt.show()
	


if __name__ == '__main__':
	start_monitor()