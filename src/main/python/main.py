from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
import subprocess
import sys

appctxt = ApplicationContext()
window = QWidget()
layout = QVBoxLayout()

xrandr_output = subprocess.run(['xrandr'], stdout=subprocess.PIPE).stdout.decode('utf-8')


class MonitorSlider(QSlider):
    def slider_change(self, value):
        percent_value = (value + 1) / 100;

        # make sure brightness is still in visible range
        if percent_value < 0.2:
            percent_value = 0.2

        subprocess.run(['xrandr', '--output', self.OutputName, '--brightness', str(percent_value)])
        # print(self.OutputName)
        print(self.OutputName + ': setting brightness to ' + str(percent_value))

    def set_output_name(self, output_name):
        self.OutputName = output_name

    OutputName = ''


i = 0
active_outputs = []
for line in xrandr_output.split('\n'):
    i += 1
    if i == 1:
        continue

    if line.startswith(' '):
        continue

    outputLine = line.split(' ')

    if len(outputLine) < 2:
        continue

    output = outputLine[0]
    connected = outputLine[1]

    print('detected output: ' + output + ' (' + connected + ')')

    if connected != 'connected':
        continue

    print('Creating slider ...')
    active_outputs.append(output)
    layout.addWidget(QLabel(output))

    slider = MonitorSlider(Qt.Horizontal)
    slider.setValue(100)
    slider.set_output_name(output)
    slider.valueChanged[int].connect(slider.slider_change)

    layout.addWidget(slider)

window.setLayout(layout)
window.show()
exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()

for output in active_outputs:
    subprocess.run(['xrandr', '--output', output, '--brightness', str(1)])

sys.exit(exit_code)