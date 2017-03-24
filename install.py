import subprocess
import sys
import os,Tkinter, time, re
import timeit
from tkFileDialog import askdirectory

'''
Requirements to run this script:
- Python 2.7.13
- Connected Android devices
'''

def split_lines(s):
    """Splits lines in a way that works even on Windows and old devices.
    Windows will see \r\n instead of \n, old devices do the same, old devices
    on Windows will see \r\r\n.
    """
    # rstrip is used here to workaround a difference between splineslines and
    # re.split:
    # >>> 'foo\n'.splitlines()
    # ['foo']
    # >>> re.split(r'\n', 'foo\n')
    # ['foo', '']
    return re.split(r'[\r\n]+', s.rstrip())

# after starting the script prompt some information
global apkDirectory
apkDirectory = 0
def overview():
    subprocess.call(['cls'], shell=True)
    print("\n##################################################################\n\n#  Welcome to Octodroid: multiple android device installer     #\n\n##################################################################\n")
    global apkDirectory
    if apkDirectory != 0:
        print'APK directory is: ', apkDirectory
    elif apkDirectory == 0:
        print 'No APK directory selected'
    else:
        print 'Get them APKs, krakakaka!'

    # Simple command
    # subprocess.call(['adb','devices','-l'], shell=True)
    # p = split_lines(subprocess.check_output('adb get-serialno', stderr=subprocess.STDOUT))
    def get_devices(adb_path='adb'):
        with open(os.devnull, 'wb') as devnull:
            subprocess.check_call([adb_path, 'start-server'], stdout=devnull,
                                  stderr=devnull)
        out = split_lines(subprocess.check_output([adb_path, 'devices']))
        # The first line of `adb devices` just says "List of attached devices", so
        # skip that.
        devices = []
        for line in out[1:]:
            if not line.strip():
                continue
            if 'offline' in line:
                continue
            serial, _ = re.split(r'\s+', line, maxsplit=1)
            devices.append(serial)
        return devices
    # print '\ncheck_output result: ', p
    current_devices = get_devices()
    print 'connected device(s):',len(current_devices)
    print 'serial of device(s):', current_devices


    def select_apk_folder():
        print("please select the folder with APK's you want to install:")
        root = Tkinter.Tk()
        root.withdraw() # hide the main GUI window for our example
        # global selectedDirectory
        global apkDirectory
        apkDirectory = str(askdirectory())
        print 'You selected:', apkDirectory
        time.sleep(3)
        return apkDirectory
        # overview()
        # return selection
        # return selectedDirectory
        # apkDirectory = select_apk_folder()

    global feedback
    feedback =[]
    def install_to_all_devices(adb_path='adb'):
        # with open(os.devnull, 'wb') as devnull:
            global apkDirectory
            get_apk()
            for device in current_devices:
                # print device
                if apkDirectory != 0 and len(apkDirectory) > 2:
                    # print apkDirectory
                    print '\nInstallation started on device: ', device,'\n__________________________________________________________________'
                    # print 'Length of apk retrieval', len(apk)
                    # for each in get_apk():
                    #     print apkDirectory
                    file = open("log.txt","w")
                    e = 0
                    global apk
                    print 'amount of APK\'s being installed: ', len(apk)
                    for each in apk:
                        print(apk[e])
                        # process= subprocess.call([adb_path, '-s', device,'install-multiple', '[-r]',  apk[e]])
                        process= subprocess.call([adb_path, '-s', device,'install',  apk[e]])
                        # print process
                        report = ''
                        if process == 1:
                            report = 'Error occured.'
                        elif process == 0:
                            report = 'Installation succesfull.'

                        line = '\n'+device+': '+str(report)
                        global feedback
                        feedback.append(line)
                        # print feedback
                        e +=1
                    # subprocess.check_output(['adb', 'wait-for', '[-usb]'])

                elif apkDirectory == 0 or len(apkDirectory) < 2:
                    print 'You have not yet selected a APK folder, you are being redirected...'
                    time.sleep(2)
                    apkDirectory = select_apk_folder()
                    install_to_all_devices()

                # Timer("install_to_all_devices()","from __main__ import install")

            # report_of_installation()


            print '\n\nInstallation completed, redirecting you to home screen in 2 seconds'
            # print feedback
            file.writelines(feedback)
            file.close()
            log = 1
            time.sleep(2)
            install_options(log)

    def get_apk():
        # for each file run this
        global apkDirectory
        global apk
        apk = []
        if apkDirectory != 0 and len(apkDirectory) > 2:
            for file in os.listdir(str(apkDirectory)):
                if file.endswith(".apk"):
                    #print APKs for test
                    apk.append(os.path.join(apkDirectory,file).replace('\\','/'))
            return apk
        elif apkDirectory == 0 or len(apkDirectory) < 2:
            print 'Get yo APK folder setup, fool!'

    def install_options(log):
        # log = False
        subprocess.call(['cls'], shell=True)
        # print log
        if log == 1 :
            file = open('log.txt', 'r')
            cont = file.read()
            print 'Log file from completed installation: \n', cont[1:]

        installOption = input('\nYour input is required:\n1 = Install to all connected devices\n2 = Select devices\n3 = Return\n')
        if installOption == 1:
            # install on all devices
            install_to_all_devices()
        elif installOption == 2:
            print 2
        elif installOption == 3:
            overview()
        elif installOption != 1 | 2 | 3 or int():
           install_options()


    menuOption = input('\nYour input is required:\n1 = Select the APK folder\n2 = Install to devices\n3 = Run through all the steps\n4 = To exit the script\n')
    if menuOption == 1:
        # start file selection function
        # when option 1 is selected, start this function
        apkDirectory = select_apk_folder()
        overview()
    if menuOption == 2:
        log = False
        install_options(log)
    if menuOption == 3:
        print("Step 3 is selected")
    if menuOption == 4:
        exit()

overview()
