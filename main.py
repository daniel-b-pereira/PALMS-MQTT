import numpy as np
from PalmsGui import PalmsGui
from palms.async_serial_comu import start
import asyncio
import serial_asyncio

#pyinstaller --specpath palms.spec -F main.py


def main():
    
    palms = PalmsGui()

if __name__ == "__main__":
    main()