import asyncio
import struct
from bleak import BleakScanner, BleakClient

# Standard Environmental Sensing Service and Characteristics
ENV_SENSE_SERVICE_UUID = "0000181a-0000-1000-8000-00805f9b34fb"
TEMP_CHAR_UUID = "00002a6e-0000-1000-8000-00805f9b34fb"
HUMIDITY_CHAR_UUID = "00002a6f-0000-1000-8000-00805f9b34fb"

async def scan_and_read_sensors():
    print("Scanning for BLE Environmental Sensors...")
    
    # Discover devices - filtering by the ENV SENSE Service UUID
    devices = await BleakScanner.discover()
    
    target_device = None
    for device in devices:
        if ENV_SENSE_SERVICE_UUID in device.metadata.get("uuids", []):
            print(f"Found Sensor Device: {device.name} [{device.address}]")
            target_device = device
            break
            
    if not target_device:
        print("No environmental sensors found in range.")
        print("Devices found:")
        for d in devices:
             print(f" - {d.name} [{d.address}]")
        return

    print(f"Connecting to {target_device.name}...")
    
    # Establish GATT Connection
    async with BleakClient(target_device.address) as client:
        print(f"Connected: {client.is_connected}")
        
        # Read Temperature
        try:
            temp_bytes = await client.read_gatt_char(TEMP_CHAR_UUID)
            # Temperature is natively stored as sint16 with 0.01 resolution
            temp_raw = struct.unpack('<h', temp_bytes)[0]
            temperature_celcius = temp_raw / 100.0
            print(f"Ambient Temperature: {temperature_celcius} °C")
        except Exception as e:
            print(f"Could not read temperature: {e}")

        # Read Humidity
        try:
            hum_bytes = await client.read_gatt_char(HUMIDITY_CHAR_UUID)
            # Humidity is stored as uint16 with 0.01% resolution
            hum_raw = struct.unpack('<H', hum_bytes)[0]
            humidity_percent = hum_raw / 100.0
            print(f"Ambient Humidity: {humidity_percent} %")
        except Exception as e:
            print(f"Could not read humidity: {e}")


if __name__ == "__main__":
    asyncio.run(scan_and_read_sensors())
