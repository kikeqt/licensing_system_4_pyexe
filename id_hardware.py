
from subprocess import Popen, PIPE
from platform import node

def get_command_output(cmd: str):
    cmd = cmd.split(' ')
    proc = Popen(cmd, stdout=PIPE)
    output = proc.communicate()[0]
    return output.strip()

class Id_Hardware(object):
    __bios_serial_number = b''
    __windows_license = b''
    __hostname = b''
    
    def __init__(self):
        """
        Get equipment identifiers
        """
        cmd = "Get-WmiObject win32_bios | Format-List SerialNumber"
        cmd = f'powershell {cmd}'
        self.__bios_serial_number = get_command_output(cmd)

        cmd = "(Get-WmiObject -query 'select * from SoftwareLicensingService').OA3xOriginalProductKey"
        cmd = f'powershell {cmd}'
        self.__windows_license = get_command_output(cmd)

        # We encode it because we need it in binary.
        self.__hostname = node().encode()
        
    def __str__(self):
        # we concatenate identifiers
        id = self.__bios_serial_number + b"\\"
        id += self.__windows_license + b"\\" + self.__hostname
        
        # We transform bytes into strings, because __str__ only understands strings
        id = id.decode()
        id = id.replace('SerialNumber : ', '')
        return id

    @property
    def get_bios_serial_number(self):
        return self.__bios_serial_number

    @property
    def get_windows_license(self):
        return self.__windows_license

    @property
    def get_hostname(self):
        return self.__hostname


if __name__ == '__main__':
    id_hardware = Id_Hardware()
    print(id_hardware.get_bios_serial_number)
    print(id_hardware.get_windows_license)
    print(id_hardware.get_hostname)
    print()
    print(id_hardware)
