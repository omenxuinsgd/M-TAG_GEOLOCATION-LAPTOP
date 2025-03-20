import asyncio
import winsdk.windows.devices.geolocation as wdg


async def getCoords():
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()

    return [pos.coordinate.latitude, pos.coordinate.longitude]

    # -6.317718, 106.687184


def getLoc():
    try:
        return asyncio.run(getCoords())
    except PermissionError:
        print("ERROR: You need to allow applications to access you location in Windows settings")


print(getLoc())