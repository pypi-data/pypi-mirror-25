# Filename: 1208fs.pyx
# Author: Weiyang Wang <wew168@ucsd.edu>
# Date: Sept 5, 2017
# Description: Cython module code, python wrapper of the 
#              MCC USB-1208FS DAQ's C driver. See original C Code for 
#              documentation.
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

from __future__ import print_function
from libc.stdlib cimport malloc, free
from libc.stdint cimport uint8_t, uint16_t, uint32_t, int16_t
cimport c1208fs
from c1208fs cimport *
cimport numpy as np
import numpy as np
import sys
cimport cython

np.import_array()

# initialize libusb on load. Register the exit function for exit. 
if libusb_init(NULL) != 0:
    raise ImportError("Could not load libusb.")

# constants
USB1208FS_PID = _USB1208FS_PID

DIO_PORTA = _DIO_PORTA
DIO_PORTB = _DIO_PORTB

DIO_DIR_IN = _DIO_DIR_IN
DIO_DIR_OUT = _DIO_DIR_OUT

SYNC = _SYNC
EXT_TRIG_EDGE = _EXT_TRIG_EDGE
UPDATE_MODE = _UPDATE_MODE

SE_10_00V = _SE_10_00V
BP_20_00V = _BP_20_00V
BP_10_00V = _BP_10_00V
BP_5_00V = _BP_5_00V
BP_4_00V = _BP_4_00V
BP_2_50V = _BP_2_50V
BP_2_00V = _BP_2_00V
BP_1_25V = _BP_1_25V
BP_1_00V = _BP_1_00V
  
AIN_EXECUTION = _AIN_EXECUTION
AIN_TRANSFER_MODE = _AIN_TRANSFER_MODE
AIN_TRIGGER = _AIN_TRIGGER
AIN_DEBUG = _AIN_DEBUG     
AIN_GAIN_QUEUE = _AIN_GAIN_QUEUE

# module-scale functions
def toVoltsFS(int gain, int num):
    """Wraps volts_FS():
    converts signed short value to volts for Differential Mode
    """
    return <float>volts_FS(gain, num)


def toVoltsSE(int num):
    """ Same as volts_SE, rewritten in cython

    Parameters: 
    num {short} - 16-bit number read by DAQ

    Returns: {np.float32_t} read value in volts
    """
    cdef np.float32_t volt = 0.0
    volt = num * 10.0 / 0x7fff
    return <float>volt

cdef class USB1208FS:
    """Python wrapper of the C-based USB_1208FS DAQ driver written by 
    Warren J. Jasper. Wraps the driver in an object-ordinated way.

    Attributes:
        udev {libusb_device_handle *} - 1208FS usb device  
        maxPacketSize {int} - max packet size, should be 64
        data {np.ndarray *} - output array for data. Need to be allocated 
                              on the heap

    Constants are from usb-1208FS.h"""
    
    cdef libusb_device_handle * udev
    cdef int maxPacketSize


    @cython.boundscheck(False)
    @cython.wraparound(False)
    def __cinit__(self):
        """Constructor of the DAQ.
        Calls relevant C functions to acquire the handler of USB_1208FS"""

        self.udev = usb_device_find_USB_MCC(USB1208FS_PID, NULL)
        if (self.udev == NULL) or (<int>self.udev == -1):
            raise ValueError("Could not initialize USB1208FS, no device found.")
        else:
            init_USB1208FS(self.udev)
        self.maxPacketSize = usb_get_max_packet_size(self.udev, 0)

    def __del__(self):
        """Fully close the device."""
        print("Closing...")
        cdef int i = 0
        libusb_clear_halt(self.udev, LIBUSB_ENDPOINT_IN | 1)
        libusb_clear_halt(self.udev, LIBUSB_ENDPOINT_OUT| 2)
        libusb_clear_halt(self.udev, LIBUSB_ENDPOINT_IN | 3)
        libusb_clear_halt(self.udev, LIBUSB_ENDPOINT_IN | 4)
        libusb_clear_halt(self.udev, LIBUSB_ENDPOINT_IN | 5)
        for i in range(4):
            libusb_release_interface(self.udev, i)
        libusb_close(self.udev);

    def dConfigPort(self, np.uint8_t port, np.uint8_t direction):
        """Configure director of digital port. Wraps usbDConfigPort_USB1208FS():
        This command sets the direction of the DIO port to input or output. 
            Port:      0 = Port A,  1 = Port B
            Direction: 0 = output,  1 = input
        """
        if usbDConfigPort_USB1208FS(self.udev, port, direction) != 0:
            raise ValueError("Could not configure port.")
        return self     # allows chaining

    def din(self, np.uint8_t port):
        """Wraps usbDIn_USB1208FS():
        This command reads the current state of the DIO ports. The return
        value will be the value seen at the port pins.

        Returns: {np.uint8_t} Read at port @port.
        """
        cdef np.uint8_t din_value
        if usbDIn_USB1208FS(self.udev, port, &din_value) != 0:
            raise ValueError("Could not configure port.")
        return din_value

    def dout(self, np.uint8_t port, np.uint8_t value):
        """Wraps usbDOut_USB1208FS():
        This command writes data to the DIO port bits 
        that are configured as outputs.
            Port: 0 = Port A, 1 = Port B
            value: value to write to the port
        """
        usbDOut_USB1208FS(self.udev, port, value)

    def ain(self, np.uint8_t channel, np.uint8_t _range):
        """Wraps usbAIn_USB1208FS():
        This command reads the value from an analog input channel,
        setting the desired gain range first. The returned value is a
        2’s-complement signed 16-bit number.
            channel: the channel to read (0-7)
            range:   the gain range (0-7)
        """
        return usbAIn_USB1208FS(self.udev, channel, _range)

    def aout(self, np.uint8_t channel, np.uint16_t value):
        """Wraps usbAOut_USB1208FS():
        This command writes the value to an analog output channel. The value
        is a 16-bit unsigned value, but the DAC is a 12-bit DAC. The lower 4
        bits of the value are ignored by the DAC. The equation for the
        output voltage is:

            V_out = ( k / 2^16 ) * V_ref 

        where k is the value written to the device and V_ref = 4.096V.

        channel: the channel to write (0 or 1)
        value:   the value to write
        """
        usbAOut_USB1208FS(self.udev, channel, value)

    def aoutScan(self, np.uint8_t lowchannel, np.uint8_t highchannel, 
                 np.uint32_t count, np.float32_t freq, np.uint8_t options):
        """Wraps usbAOutScan_USB1208FS(), change the return value to the array:
        This command writes values to the analog output channels at a fixed rate

          lowchannel:   the first channel of the scan (0 – 1)
          highchannel:  the last channel of the scan (0 – 1)
          count:        the total number of scans to perform

          options:    bit field that controls various options
                      bit 0: 1 = single execution, 0 = continuous execution
                      bit 1: 1 = use external trigger
                      bits 2-7: not used

        The values lowchannel and hichannel specify the channel range for
        the scan. If lowchannel is higher than hichannel, the parameters
        will be reversed in the device (lowchannel must be less than
        hichannel.)  The rate of data output is set by the internal 16-bit
        incrementing timer running at a base rate of 10MHz. The timer is
        controlled by timer_prescale and timer_preload.
        
        The data will be sent in packets utilizing the interrupt out
        endpoint on interface 1. The endpoint allows 64 bytes of data to
        be sent every millisecond, so the theoretical limit is:

             64 bytes/ms = 64,000byte/s = 32,000S/s

        The data will be in the format:
        lowchannel sample 0 : [hichannel sample 0]
        lowchannel sample 1 : [hichannel sample 1]
        lowchannel sample n : [hichannel sample n]

        The external trigger may be used to start data output
        synchronously. If the bit is set, the device will wait until the
        appropriate trigger edge is detected, then begin outputting data
        at the specified rate.  The data transfer is controlled by the PMD
        using data requests. The USB-1208FS will send an input report on
        interface 0 with the report ID = CMD_AOUTSCAN to request a new
        packet of data.  It will maintain its internal FIFO by requesting
        new data when it is ready.  The count parameter is only used in
        single execution mode. In continuous execution mode data will be
        sent by the host indefinitely, with the host sending an AOutStop
        command to end the scan.

        Modified: 
        Parameter:
        freq: {np.float32_t} - frequency of the scanning, will be taken address
                               when passed to the C function

        Returns: {list} - result of the scan. 

        For safety issue, I'll copy the result of scan to a python list
        """

        cdef np.uint16_t * data = \
                <np.uint16_t*>malloc(count * sizeof(np.uint16_t))
        if not data:
            raise MemoryError()

        cdef int i = 0
        try:
            if usbAOutScan_USB1208FS(self.udev, lowchannel, highchannel, count, \
                    &freq, data, options) < 0:
                raise ValueError("Analog out scan failed, see C error message.")
            dataList = []
            for i in range(count):
                dataList.append(<int>data[i])
            return dataList             #XXX

        finally:
            free(data)

    def aoutStop(self):
        """Wraps usbAOutStop_USB1208FS():
        This command stops the analog output scan (if running.)
        Unlikely to be used.
        """
        usbAOutStop_USB1208FS(self.udev)

    def ainStop(self):
        """Wraps usbAInStop_USB1208FS():
        This command stops the analog input scan (if running.)
        Unlikely to be used.
        """
        usbAInStop_USB1208FS(self.udev)

    def ainScan(self, np.uint8_t lowchannel, np.uint8_t highchannel, 
            np.uint32_t count, np.float32_t freq, np.uint8_t options):
        """Wraps usbAInScan_USB1208FS() with modifications:
        This command scans a range of analog input channels and sends the
        readings in interrupt transfers. The gain ranges that are
        currently set on the desired channels will be used (these may be
        changed with AIn or ALoadQueue.

        lowchannel:  the first channel of the scan (0 – 7)
        highchannel: the last channel of the scan (0 – 7)
        count:       the total number of samples to perform, 
                     used only in single execution mode
        options:     bit 0: 1 = single execution, 0 = continuous execution
                     bit 1: 1 = immediate transfer mode, 0 = block transfer mode
                     bit 2: 1 = use external trigger
                     bit 3: 1 = debug mode (scan returns consecutive 
                                integers instead of sampled data, used for 
                                checking for missed data, etc.)
                     bit 4: 1 = use channel gain queue, 0 = use channel 
                                parameters specified
                     bits 5-7: not used
        
        The sample rate is set by the internal 16-bit incrementing timer
        running at a base rate of 10MHz. The timer is controlled by
        timer_prescale and timer_preload. These values are only used if the
        device has been set to master the SYNC pin with the SetSync command.

        The data will be returned in packets utilizing interrupt in endpoints. 
        Two endpoints will be used; each endpoint allows 64 bytes of data to be 
        sent every millisecond, so the theoretical limit is:
            2 endpoints * 64 bytes/ms = 128 bytes/ms = 
            128,000 bytes/s = 64,000 samples/s

        The data will be in the format:
        lowchannel sample 0 : lowchannel + 1 sample 0 :… : hichannel sample 0
        lowchannel sample 1 : lowchannel + 1 sample 1 :… : hichannel sample 1
        .
        .
        .
        lowchannel sample n : lowchannel + 1 sample n : … : hichannel sample n

        The data will use successive endpoints, beginning with the first
        endpoint at the start of a scan and cycling through the second
        endpoint until reaching the specified count or an AScanStop is sent.
        Immediate transfer mode is used for low sampling rates to avoid
        delays in receiving the sampled data. The data will be sent at the
        end of every timer period, rather than waiting for the buffer to
        fill. Both endpoints will still be used in a sequential manner. This
        mode should not be used if the aggregate sampling rate is greater
        than 2,000 samples per second in order to avoid data loss.

        The external trigger may be used to start data collection
        synchronously. If the bit is set, the device will wait until the
        appropriate trigger edge is detected, then begin sampling data at
        the specified rate. No messages will be sent until the trigger is
        detected.

        Modified: 
        Parameter:
        freq: {np.float32_t} - frequency of the scanning, will be taken address
                               when passed to the C function

        Returns: {list} - result of the scan. 

        For safety issue, I'll copy the result of scan to a python list
        """
        cdef np.int16_t * data = <np.int16_t*>malloc(count * sizeof(np.int16_t))
        if not data:
            raise MemoryError()

        cdef int i = 0
        try:
            if usbAInScan_USB1208FS(self.udev, lowchannel, highchannel, count, \
                    &freq, options, data) < 0:
                raise ValueError("Analog in scan failed, see C error message.")
            dataList = []
            for i in range(count):
                dataList.append(<int>data[i])
            return dataList             #XXX

        finally:
            free(data)

    def ainScanSE(self, np.uint8_t lowchannel, np.uint8_t highchannel, 
            np.uint32_t count, np.float32_t freq, np.uint8_t options):
        """Wraps usbAInScan_USB1208FS_SE() with modifications:
        scan for Single Ended
        Modified: 
        Parameter:
        freq: {np.float32_t} - frequency of the scanning, will be taken address
                               when passed to the C function

        Returns: {list} - result of the scan. 

        For safety issue, I'll copy the result of scan to a python list
        """
        cdef np.int16_t * data = <np.int16_t*>malloc(count * sizeof(np.int16_t))
        if not data:
            raise MemoryError()
            
        cdef int i = 0
        try:
            if usbAInScan_USB1208FS_SE(self.udev, lowchannel, highchannel, \
                    count, &freq, options, data) < 0:
                raise ValueError("Analog in SE scan failed, see C error message.")

            dataList = []
            for i in range(count):
                dataList.append(<int>data[i])
            return dataList         #XXX

        finally:
            free(data)

    def aLoadQueue(self, np.uint8_t num, chan, gains):
        """Wraps usbALoadQueue_USB1208FS(), with modifications:
        The device can scan analog input channels with different gain
        settings. This function provides the mechanism for configuring each
        channel with a unique range. 

        num:  the number of channel / gain pairs to follow (max 8)
        chan[]: array of the channel numbers (0 – 7)
        gain[]: array of the  gain ranges (0 – 7)

        Modified:
        Parameters: 
        chan {list} - list of channels to be scanned
        gains {list} - list of gains
        """
        if len(chan) != len(gains):
            raise ValueError("length of chans and gains are not the same.")

        cdef np.uint8_t * chanArr = \
            <np.uint8_t*>malloc(len(chan) * sizeof(np.uint8_t))
        if not chanArr:
            raise MemoryError()
        cdef np.uint8_t * gainArr = \
            <np.uint8_t*>malloc(len(gains) * sizeof(np.uint8_t))
        if not gainArr:
            raise MemoryError()

        cdef int i
        try:
            for i in range(len(chan)):
                chanArr[i] = <np.uint8_t>chan[i]
                gainArr[i] = <np.uint8_t>gains[i]

            usbALoadQueue_USB1208FS(self.udev, num, chanArr, gainArr)

        finally:
            free(chanArr)
            free(gainArr)

    def initCounter(self):
        """Wraps usbInitCounter_USB1208FS():
        This command initializes the event counter and resets the count to zero.
        """
        usbInitCounter_USB1208FS(self.udev)

    def readCounter(self):
        """Wraps usbReadCounter_USB1208FS():
        This function reads the 32-bit event counter on the device. This
        counter tallies the transitions of an external input attached to
        the CTR pin on the screw terminal of the device.
        """
        return <int>usbReadCounter_USB1208FS(self.udev)

    def readMemory(self, np.uint16_t address, np.uint8_t count):
        """Wraps usbReadMemory_USB1208FS():
        This command reads data from the configuration memory (EEPROM.) 
        All of the memory may be read

        Addresses 0x000 - 0x07F are reserved for firmware data
        Addresses 0x080 - 0x3FF are available for use as calibraion or user data

        address: the start address for the read.
        count:  the number of bytes to read (62 max)

        Returns: {list} data in the memory
        """
        cdef np.uint8_t * memory = \
                <np.uint8_t*>malloc(count * sizeof(np.uint8_t))
        if not memory:
            raise MemoryError()

        cdef int i = 0

        try:
            usbReadMemory_USB1208FS(self.udev, address, count, memory)
            dataList = []
            for i in range(count):
                dataList.append(<int>memory[i])
            return dataList         #XXX

        finally:
            free(memory)

    def writeMemory(self, np.uint16_t address, np.uint8_t count, data):
        """Wraps usbWriteMemory_USB1208FS():
        This command writes to the non-volatile EEPROM memory on the
        device. The non-volatile memory is used to store calibration
        coefficients, system information, and user data. 

        Locations 0x00-0x7F are reserved for firmware and my not be written.

        Arguments:
        data {list} - data to be written into the memory
        """
        cdef np.uint8_t * dataArr = \
            <np.uint8_t*>malloc(count * sizeof(np.uint8_t))
        if not dataArr:
            raise MemoryError()

        cdef int i
        try:
            for i in range(count):
                dataArr[i] = data[i]

            if usbWriteMemory_USB1208FS(self.udev, address, count, dataArr) < 0:
                raise ValueError("Could not write to memory.")

        finally:
            free(dataArr)

    def blink(self):
        """Wraps usbBlink_USB1208FS():
        blinks the LED of USB device
        """
        usbBlink_USB1208FS(self.udev)

    def reset(self):
        """Wraps usbReset_USB1208FS():
        This function causes the device to perform a reset. 
        The device disconnects from the USB bus and resets its microcontroller.
        """
        usbReset_USB1208FS(self.udev)

    def getStatus(self):
        """Wraps usbGetStatus_USB1208FS():
        This command retrieves the status of the device.
        """
        return <int>usbGetStatus_USB1208FS(self.udev)

    def setTrigger(self, np.uint8_t _type):
        """Wraps usbSetTrigger_USB1208FS():
        This function configures the external trigger for analog
        input. The trigger may be configured to activate with either a
        logic rising edge or falling edge input. Once the trigger is
        received, the analog input will proceed as configured. The
        EXTTRIG option must be used in the AInScan command to utilize
        this feature.

        type: the type of trigger 
            0 = external trigger falling edge, 1 = external trigger rising edge
        """
        usbSetTrigger_USB1208FS(self.udev, _type)

    def setSync(self, np.uint8_t _type):
        """Wraps usbSetSync_USB1208FS():
        This command configures the sync signal. The sync signal may be
        used to synchronize the analog input scan of multiple
        devices. When multiple devices are to be used, one device is
        selected as the master and the rest as slaves. The sync signal of
        all devices must be wired together. The master will output a pulse
        every sample, and all of the devices will acquire their samples
        simultaneously.

        This may also be used to pace one or more devices from an external
        TTL/CMOS clock signal (max rate = 50kHz.)  This may also be used
        with an external trigger; the external trigger signal should be
        brought to the master device, and all devices will begin sampling
        when the master is triggered.

        If a device is configured as a slave, it will not acquire data
        when given an AInScan command until it detects a pulse on the sync
        input.  The device will switch the SYNC pin to the appropriate
        input / output state when this command is received.

        type: 0 = master, 1 = slave
        """
        usbSetSync_USB1208FS(self.udev, _type)

    def _getAll(self):
        """Wraps usbGetAll_USB1208FS():
        This command reads the value from all analog input channels 
        and digital I/Os.

        The original function seems to be not working. 

        XXX: Returns: {list} - all data from all ports
        """
        raise NotImplementedError("Currently not supported")

    def init(self):
        """Wraps init_USB1208FS():
        claim interfaces 1-3 for the USB-1208FS
        
        Should not be used in user code.
        """
        if init_USB1208FS(self.udev) < 0:
            raise ValueError("Failed to initialize USB1208FS.")






