import cv2
import asyncio
import keyboard

from djitellopy import Tello, TelloException


class TelloDrone:

    def __init__(self):
        self.tello = Tello()

    async def connection(self):
        try:

            await self.tello.connect()
            await self.tello.streamon()

            print("[+] Successfully connected to the drone!")

            while True:
                frame = self.tello.get_frame_read().frame
                cv2.imshow("Fly-By-Tello", frame)
                if cv2.waitKey(1):
                    break

        except TelloException as exception:
            print(f"\n[!] Error occurred while connection to the drone -> \n{exception}\n")

        finally:
            await self.tello.streamoff()

    async def control(self):
        try:

            while True:
                if keyboard.is_pressed('w'):
                    await self.tello.send_rc_control(0, 30, 0, 0)

                elif keyboard.is_pressed('s'):
                    await self.tello.send_rc_control(0, -30, 0, 0)

                elif keyboard.is_pressed('a'):
                    await self.tello.send_rc_control(-30, 0, 0, 0)

                elif keyboard.is_pressed('d'):
                    await self.tello.send_rc_control(30, 0, 0, 0)

                elif keyboard.is_pressed('up'):
                    await self.tello.send_rc_control(0, 0, -30, 0)

                elif keyboard.is_pressed('down'):
                    await self.tello.send_rc_control(0, 0, 30, 0)

                elif keyboard.is_pressed('left'):
                    await self.tello.send_rc_control(0, 0, 0, 30)

                elif keyboard.is_pressed('right'):
                    await self.tello.send_rc_control(0, 0, 0, -30)

                elif keyboard.is_pressed("+"):
                    await self.tello.takeoff()

                elif keyboard.is_pressed("1"):
                    await self.tello.flip_forward()

                elif keyboard.is_pressed("2"):
                    await self.tello.flip_back()

                elif keyboard.is_pressed('-'):
                    await self.tello.land()

        except TelloException as exception:
            print(f"\n[!] Error occurred while controlling the drone. -> \n{exception}\n")


if __name__ == '__main__':
    banner = """
           ____ ___  _____
          / __// o.)/_  _/    Fly-By-Tello v.0.1
         / _/ / o \  / /    [ Created By Arl3q1n ]
        /_/  /___,' /_/   
    
    {01} - Connect and fly
    {02} - Byee 

    """

    print(banner)

    try:
        cmd = int(input("@tello_> "))

        if cmd == 1:
            drone = TelloDrone()

            run_async = [drone.connection(), drone.control()]
            asyncio.gather(*run_async)
        elif cmd == 2:
            exit("[~] Exit...")
    except KeyboardInterrupt:
        exit("[~] Exit...")
