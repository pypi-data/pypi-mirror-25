"""
Prerequisites:
uhubctl is on the path
"""

import subprocess

class UsbPowerSkill:

    def __init__(self,tts_service=None):
        """ Initialisation.
        :param db: the json database.
        :param tts_service: A TTS service, i.e. an object which has a
                            `speak(text)` method for speaking the result.
                                                       
Current status for hub 1-1, vendor 0424:9514, 5 ports
   Port 1: 0503 highspeed power enable connect [0424:ec00]
   Port 2: 0100 power
   Port 3: 0100 power
   Port 4: 0503 highspeed power enable connect [1415:2000 OmniVision Technologies, Inc. USB Camera-B4.09.24.1]
   Port 5: 0103 power enable connect [046d:c52b Logitech USB Receiver]
                            
        """
        self.tts_service = tts_service
        
    def usb_get_devices(self):
        output = subprocess.check_output('uhubctl',shell = True)
        return output
        
    def usb_load_devices(self,output):
        results=[]
        for result in output.splitlines():
            portId = result[8:9]
            partsA = result.split(":")
            if len(partsA) >= 2:
                text = result[16:]
                parts = result.split("[")
                port = {'id':portId}
                if parts[0].find("power") != -1 :
                    port['power'] = True
                else:
                    port['power'] = False
                    
                if parts[0].find("connect") != -1 :
                    port['connect'] = True
                else:
                    port['connect'] = False
                
                if len(parts) == 2:
                    port['deviceId'] = parts[1][0:9]
                    device = parts[1][10:]
                    port['device'] = device[:-1]
                    
                results.append(port)
        return results
    
    def convert_numbers(self,number):
        return number.replace("one",'1').replace("to",'2').replace("too",'2').replace("two",'2').replace("three",'3').replace("four",'4').replace("five",'5').replace("six",'6').replace("seven",'7').replace("eight",'8').replace("nine",'9').replace("ten",'10')
        
    def usb_find_device(self,description,results):
        device = None
        for result in results:
            if ('id' in result.keys() and result['id']==self.convert_numbers(description)):
                device = result
                break
            elif ('device' in result.keys() and result['device'].lower().find(description.lower())!=-1):
                device = result
                break
            elif ('deviceId' in result.keys() and description == result['deviceId']):
                device = result
                break
        print("find device {}".format(device))
        return device
    
    def usb_list_devices(self,results):
        outputs=[]
        portsOff=[]
        for result in results:
            if result['power']:
                if 'device' in result.keys() and len(result['device']) > 0:
                    outputs.append("In U s b port {} is {}".format(result['id'],result['device']))
                elif 'deviceId' in result.keys() and len(result['deviceId']) > 0:
                    outputs.append("In U s b port {} is an unknown device, ".format(result['device'],result['id']))
                else:
                    outputs.append("U s b port {} is unplugged, ".format(result['id']))
            else:
                outputs.append("U s b port {} is switched off".format(result['id']))
        return "\n".join(outputs)
        
    def usb_list_devices_say(self,results):    
        response=self.usb_list_devices(results);
        if self.tts_service:
           self.tts_service.speak(response)

        
    def usb_power_on(self,usbPortIdentifier,results):
        device=self.usb_find_device(usbPortIdentifier,results)
        response=''
        action=None
        if device is not None:
            if not device['power']:
                if 'device' in device.keys() or 'deviceId' in device.keys():
                    response="Turning on power to {}".format(usbPortIdentifier)
                    action = "uhubctl -p {} -a 1".format(device['id'])
                else:
                    response="Turning on power to empty u s b port {}".format(usbPortIdentifier)
                    action = "uhubctl -p {} -a 1".format(device['id'])
            else:
                response="{} is already turned on".format(usbPortIdentifier)
        else:
            response="Could not find a u s b port matching {}".format(usbPortIdentifier)
        return response,action;
        
    def usb_power_on_say(self,usbPortIdentifier,results):
        response,action = self.usb_power_on(usbPortIdentifier,results)
        if action is not None:
            subprocess.check_output(action,shell = True)
        if self.tts_service:
            self.tts_service.speak(response)

    def usb_power_off(self,usbPortIdentifier,results):
        device=self.usb_find_device(usbPortIdentifier,results)
        response=''
        action = None
        if device is not None:
            if device['power']:
                if 'device' in device.keys() or 'deviceId' in device.keys():
                    response="Turning off power to {}".format(usbPortIdentifier)
                    action = "uhubctl -p {} -a 0".format(device['id'])
                else:
                    response="Turning off power to empty u s b port {}".format(usbPortIdentifier)
                    action = "uhubctl -p {} -a 0".format(device['id'])
            else:
                response="{} is already turned off".format(usbPortIdentifier)
        else:
            response="Could not find a u s b port matching {}".format(usbPortIdentifier)
        return response,action;

    def usb_power_off_say(self,usbPortIdentifier,results):
        response,action = self.usb_power_off(usbPortIdentifier,results)
        if action is not None:
            print(action)
            subprocess.check_output(action,shell = True)
        if self.tts_service:
            self.tts_service.speak(response)
