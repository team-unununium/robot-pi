import aioice
import asyncio
import logging

import src.robot_settings as settings

logger = logging.getLogger("Video Stream")

class VideoProgram:
    def __init__(self):
        logger.info("Video program initiated")
        if len(settings.STUN_URL.split(":")) == 2:
            stun_port = int(settings.STUN_URL.split(":")[1])
        else:
            stun_port = 19302
        if settings.TURN_URL is not None and len(settings.TURN_URL.split(":")) == 2:
            turn_port = int(settings.TURN_URL.split(":")[1])
        else:
            turn_port = 3478
        self.testEventLoop()
        if settings.TURN_URL is None:
            self.connection = self.connection = aioice.Connection(ice_controlling=True, stun_server=(settings.STUN_URL.split(":")[0], stun_port))
        else:
            self.connection = aioice.Connection(ice_controlling=True, stun_server=(settings.STUN_URL.split(":")[0], stun_port), turn_server=(settings.TURN_URL.split(":")[0], turn_port), turn_username=settings.TURN_USERNAME, turn_password=settings.TURN_PASSWORD, turn_transport=settings.TURN_TRANSPORT, turn_ssl=settings.TURN_TLS)
        self.working = True # Whether the module is up and running
        self.clients = [] # The list of recognised remote candidates

    def testEventLoop(self):
        try:
            asyncio.get_event_loop()
        except Exception as e:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

    def start(self):
        if self.working:
            try:
                logger.info("Video program started")
                loop = asyncio.new_event_loop()
                loop.run_until_complete(self.asyncStart())
                self.working = True
            except Exception as e:
                logger.error(f"ICE handshake failed with the following error: {str(e)}")
                print("An error occured while attempting to start the video program. Please check the logs for more information.")
                self.working = False
        else:
            logger.warning(f"Video program is not working, cannot start program")
            print("An error occured while attempting to start the video program. Please check the logs for more information.")

    async def asyncStart(self):
        await self.connection.gather_candidates()
        logger.info(f"Local candidates: {self.connection.local_candidates}")
        print("Waiting for peers on video module")

    def stop(self):
        if self.working:
            logger.info("Video program stopped")
            self.working = False
        else:
            logger.warning(f"Video program is not working (already stopped)")
