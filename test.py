import board
import busio
import digitalio
import adafruit_ina219
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

# GPIO setup for TPS63020 EN pin (GPIO 18)
en_pin = digitalio.DigitalInOut(board.D18)  # GPIO 18
en_pin.direction = digitalio.Direction.OUTPUT

# Start with power OFF
en_pin.value = False
print("TPS63020 power is OFF")

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# INA219 setup
ina219 = adafruit_ina219.INA219(i2c)

# First ADS1115 setup (address 0x48)
ads1 = ADS.ADS1115(i2c, address=0x48)
channels_ads1 = [
    AnalogIn(ads1, ADS.P0),  # Channel 0 (A0)
    AnalogIn(ads1, ADS.P1),  # Channel 1 (A1)
    AnalogIn(ads1, ADS.P2),  # Channel 2 (A2)
    AnalogIn(ads1, ADS.P3)   # Channel 3 (A3)
]

# Second ADS1115 setup (address 0x4a)
ads2 = ADS.ADS1115(i2c, address=0x4a)
channels_ads2 = [
    AnalogIn(ads2, ADS.P0),  # Channel 4 (A0)
    AnalogIn(ads2, ADS.P1),  # Channel 5 (A1)
    AnalogIn(ads2, ADS.P2),  # Channel 6 (A2)
    AnalogIn(ads2, ADS.P3)   # Channel 7 (A3)
]

try:
    while True:
        command = input("> ")
        if command == "power on":
            en_pin.value = True
            print("TPS63020 power is ON")
        elif command == "power off":
            en_pin.value = False
            print("TPS63020 power is OFF")
        elif command == "read":
            voltage = ina219.bus_voltage  # Voltage at VIN+
            current = ina219.current / 1000  # Current in mA
            print(f"INA219 Voltage: {voltage:.2f} V")
            print(f"INA219 Current: {current:.2f} mA")
        elif command.startswith("volt"):
            try:
                channel = int(command.split()[1])
                if 0 <= channel <= 3:
                    volt = channels_ads1[channel].voltage
                    print(f"ADS1115 #1 Channel {channel} (A{channel}): {volt:.3f} V")
                elif 4 <= channel <= 7:
                    volt = channels_ads2[channel - 4].voltage
                    print(f"ADS1115 #2 Channel {channel} (A{channel-4}): {volt:.3f} V")
                else:
                    print("Channel must be 0-7")
            except (IndexError, ValueError):
                print("Usage: volt <channel> (0-7)")
        elif command == "exit":
            break
except KeyboardInterrupt:
    pass
finally:
    en_pin.deinit()  # Clean up GPIO
    print("GPIO cleaned up")