# Filename: c1208fs.pxd
# Author: Weiyang Wang <wew168@ucsd.edu>
# Date: Sept 5, 2017
# Description: Cython extension definition for python wrapper of the 
#              MCC USB-1208FS DAQ.
#              C-arrays treated as numpy arrays
#              
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import numpy as np
cimport numpy as np

# OS headers 
cdef extern from "<stdlib.h>":
    pass
cdef extern from "<stdio.h>":
    pass
cdef extern from "<string.h>":
    pass
cdef extern from "<sys/ioctl.h>":
    pass
cdef extern from "<sys/types.h>":
    pass
cdef extern from "<sys/stat.h>":
    pass
cdef extern from "<asm/types.h>":
    pass
cdef extern from "<fcntl.h>":
    pass
cdef extern from "<unistd.h>":
    pass
cdef extern from "<errno.h>":
    pass
cdef extern from "<math.h>":
    pass
cdef extern from "<string.h>":
    pass

# <libusb-1.0/libusb.h> which is included by pmd.h
cdef extern from "<libusb-1.0/libusb.h>":
    struct libusb_device_handle:
        pass
    struct libusb_context:
        pass
    int LIBUSB_ENDPOINT_OUT
    int LIBUSB_ENDPOINT_IN
    int  libusb_init(libusb_context ** context)
    void libusb_exit(libusb_context * ctx) 
    int  libusb_clear_halt(libusb_device_handle * dev, unsigned char endpoint)
    int  libusb_release_interface (libusb_device_handle * dev, \
        int interface_number)
    void libusb_close(libusb_device_handle * dev_handle)

# pmd.h
cdef extern from "pmd.h":
    libusb_device_handle * usb_device_find_USB_MCC(int productId,
        char * serialID)
    int usb_get_max_packet_size(libusb_device_handle * udev, int endpointNum)


# usb-1208FS.h
cdef extern from "usb-1208FS.h":
    # #define entries
    int _USB1208FS_PID "USB1208FS_PID"  

    int _DIO_PORTA "DIO_PORTA"
    int _DIO_PORTB "DIO_PORTB"

    int _DIO_DIR_IN  "DIO_DIR_IN"
    int _DIO_DIR_OUT "DIO_DIR_OUT"

    int _SYNC "SYNC"
    int _EXT_TRIG_EDGE "EXT_TRIG_EDGE"
    int _UPDATE_MODE  "UPDATE_MODE"

    int _SE_10_00V "SE_10_00V"
    int _BP_20_00V "BP_20_00V"
    int _BP_10_00V "BP_10_00V"
    int _BP_5_00V "BP_5_00V"
    int _BP_4_00V "BP_4_00V"
    int _BP_2_50V "BP_2_50V"
    int _BP_2_00V "BP_2_00V"
    int _BP_1_25V "BP_1_25V"
    int _BP_1_00V "BP_1_00V"

    int _AIN_EXECUTION "AIN_EXECUTION"
    int _AIN_TRANSFER_MODE "AIN_TRANSFER_MODE"
    int _AIN_TRIGGER "AIN_TRIGGER"
    int _AIN_DEBUG "AIN_DEBUG"
    int _AIN_GAIN_QUEUE  "AIN_GAIN_QUEUE"

    # functions
    # numerical are converted to np equivs, arrays are converted to numpy arrays
    int usbDConfigPort_USB1208FS(libusb_device_handle *udev, 
        np.uint8_t port, np.uint8_t direction);
    int usbDIn_USB1208FS(libusb_device_handle *udev, 
        np.uint8_t port, np.uint8_t* din_value);
    void usbDOut_USB1208FS(libusb_device_handle *udev, 
        np.uint8_t port, np.uint8_t value);

    signed short usbAIn_USB1208FS(libusb_device_handle *udev, 
        np.uint8_t channel, np.uint8_t range);
    void usbAOut_USB1208FS(libusb_device_handle *udev, 
        np.uint8_t channel, np.uint16_t value);
    int usbAOutScan_USB1208FS(libusb_device_handle *udev, 
        np.uint8_t lowchannel, np.uint8_t highchannel, np.uint32_t count,
        np.float32_t * frequency, np.uint16_t data[], np.uint8_t options);
    void usbAOutStop_USB1208FS(libusb_device_handle *udev);
    void usbAInStop_USB1208FS(libusb_device_handle *udev);
    int usbAInScan_USB1208FS(libusb_device_handle *udev, 
        np.uint8_t lowchannel, np.uint8_t highchannel, np.uint32_t count,
        np.float32_t *frequency, np.uint8_t options, np.int16_t data[]);
    int usbAInScan_USB1208FS_SE(libusb_device_handle *udev, 
        np.uint8_t lowchannel, np.uint8_t highchannel, np.uint32_t count,
        np.float32_t *frequency, np.uint8_t options, np.int16_t data[]);
    void usbALoadQueue_USB1208FS(libusb_device_handle *udev, 
        np.uint8_t num, np.uint8_t chan[], np.uint8_t gains[]);

    void usbInitCounter_USB1208FS(libusb_device_handle *udev);
    np.uint32_t usbReadCounter_USB1208FS(libusb_device_handle *udev);

    void usbReadMemory_USB1208FS(libusb_device_handle *udev, 
        np.uint16_t address, np.uint8_t count, np.uint8_t memory[]);
    int usbWriteMemory_USB1208FS(libusb_device_handle *udev, 
        np.uint16_t address, np.uint8_t count, np.uint8_t data[]);
    void usbBlink_USB1208FS(libusb_device_handle *udev);
    int usbReset_USB1208FS(libusb_device_handle *udev);
    np.uint16_t usbGetStatus_USB1208FS(libusb_device_handle *udev);
    void usbSetTrigger_USB1208FS(libusb_device_handle *udev, np.uint8_t type);
    void usbSetSync_USB1208FS(libusb_device_handle *udev, np.uint8_t type);
    void usbGetAll_USB1208FS(libusb_device_handle *udev, np.uint8_t data[]);
    np.float32_t volts_FS(int gain, int num);
    np.float32_t volts_SE(int num);
    int init_USB1208FS(libusb_device_handle *udev);
