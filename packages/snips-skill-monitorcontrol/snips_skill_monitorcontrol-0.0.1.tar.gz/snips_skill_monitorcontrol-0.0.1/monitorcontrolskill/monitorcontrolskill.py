"""
Prerequisites:
uhubctl is on the path
"""

import subprocess

class MonitorControlSkill:

    def __init__(self,tts_service=None):
        """ Initialisation.
        :param db: the json database.
        :param tts_service: A TTS service, i.e. an object which has a
                            `speak(text)` method for speaking the result.
        """
        self.tts_service = tts_service
        
    def monitor_power_on(self):
        try:
            output = subprocess.check_output('ddcutil setvcp D6 1',shell = True)
        except:
            pass
    def monitor_power_off(self):
        try:
            output = subprocess.check_output('ddcutil setvcp D6 4',shell = True)
        except:
            pass

    def monitor_select_input(self,monitorInputNumber):
        try:
            if monitorInputNumber < 0 or monitorInputNumber > 2:
                if self.tts_service is not None:
                    self.tts_service.speak('Input number must be 0,1 or 2')
            else:
                output = subprocess.check_output('ddcutil setvcp 60 {}'.format(int(monitorInputNumber)),shell = True)
        except:
            pass

    def monitor_select_brightness(self,monitorBrightness):
        try:
            if monitorBrightness < 0 or monitorBrightness > 100:
                if self.tts_service is not None:
                    self.tts_service.speak('Brightness must be between 0 and 100')
            else:
                output = subprocess.check_output('ddcutil setvcp 10 {}'.format(int(monitorBrightness)),shell = True)
                print(output)
                if self.tts_service is not None:
                    self.tts_service.speak('Set brightness to {}'.format(int(monitorBrightness)))
        except:
            pass
      
    def monitor_select_volume(self,monitorVolume):
        try:
            if monitorVolume < 0 or monitorVolume > 100:
                if self.tts_service is not None:
                    self.tts_service.speak('Volume must be between 0 and 100')
            else:
                output = subprocess.check_output('ddcutil setvcp 62 {}'.format(int(monitorVolume)),shell = True)
                if self.tts_service is not None:
                    self.tts_service.speak('Set volume to {}'.format(int(monitorVolume)))
        except:
            pass
