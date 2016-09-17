package com.chapresearch.ftcchaprfcs;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.content.Context;
import android.os.Handler;
import android.util.Log;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Created by IyengarArnhav on 7/9/2016.
 */

public class FCSBLE {

    public BluetoothAdapter mBluetoothAdapter;
    public BluetoothManager mBluetoothManager;
    public BluetoothGatt mBluetoothGatt;

    private String myRobotName;
    private String mBluetoothDeviceAddress;

    private Context mContext;

    private Handler bHandler;
    private static final long SCAN_PERIOD = 10000;

    private Map<String, String> consoles = new HashMap<>();
    private Map<String, FCSBLEScanner> fcsConsoleRecords = new HashMap<>();

    private FCSBLECallback UIConsoleScanCallback;

    private FCSBLEScanner record;

    private static final String FCSConsoleServiceID = "1840e436-bf53-45f1-a1dd-a56336e20377";   // The basic the UUID for the Service
    private static final String RobotNumJoin = "0d48b2e8-3312-11e6-ac61-9e71128cae77";          // 2 bytes
    private static final String R1 = "0d48b6da-3312-11e6-ac61-9e71128cae77";                    // 10 byte report
    private static final String R2 = "0d48b900-3312-11e6-ac61-9e71128cae77";                    // 10 byte report
    private static final String B1 = "0d48ba22-3312-11e6-ac61-9e71128cae77";                    // 10 byte report
    private static final String B2 = "0d48bb08-3312-11e6-ac61-9e71128cae77";                    // 10 byte report

    private int modeCounter = 0;
    private int connectDone = 0;
    private boolean inMatch = false;

    public interface FCSBLECallback {
        //
        // processConsole() - this routine is called once for every FCS console discovered during
        //                    the scan for consoles. This callback happens after the call to
        //                    startFCSConsoleScan().
        //
        public void processConsole(String name);

        public void consoleSelected();

        public void noConsoleSelected();

        //
        // consoleScanComplete() - this routine is called once a scan for FCS consoles has been
        //                         completed / timed out. This callback happens after the call to
        //                         startFCSConsoleScan().
        //
        public void consoleScanComplete();

        //
        // successfulQueue() - this is called once the robot has been successfully queued to join
        //                     a match. However, this does not indicate that you have been accepted
        //                     into the match. This callback happens after connectToFCS().
        //
        public void successfulQueue();

        //
        // queueComplete() - this is called once the current queuing session has terminated. The
        //                   argument "accepted" will be set to true if the robot has been accepted
        //                   into the match. False means the robot was not accepted into the match
        //                   which may occur for many reasons: wrong match number, console reboot,
        //                   etc. The argument "position" will be "R1", "R2", "B1", or "B2". The
        //                   position will only matter if "accepted" is true. If "accepted" is false
        //                   "position" will be a blank string. This callback happens after
        //                   connectToFCS().
        //
        public void queueComplete(boolean accepted, String position);

        //
        // getBatteryStatus() - this is the FCSBLE asking the FCSMainActivity() for battery status.
        //                      The "battery" argument is either 1 or 2 where 1 is the Robot Battery
        //                      and 2 is the Robot Controller Battery. It returns a number from 0 to
        //                      100.
        //
        public int getBatteryStatus(int battery);

        //
        // startAutoInit() - this is called once the autonomous needs to be initialized.
        //
        public void startAutoInit();

        //
        // startAuto() - this is called once the autonomous needs to be started.
        //
        public void startAuto();

        //
        // stopAuto() - this is called once the autonomous needs to be stopped.
        //
        public void stopAuto();

        //
        // startTeleInit() - this is called once the Tele-Op needs to be initialized.
        //
        public void startTeleInit();

        //
        // startTele() - this is called when the Tele-Op needs to start.
        //
        public void startTele();

        //
        // startEndGame() - this is called once the endgame starts.
        //
        public void startEndGame();

        //
        // stopTele() - this is called when the Tele-Op needs to be stopped.
        //
        public void stopTele();

        //
        // matchPause() - this is called when the match is paused.
        //
        public void matchPause();

        //
        // matchResume() - this is called when the match is resumed.
        //
        public void matchResume();

        //
        // matchStop() - this is called once a "fatal stop" has occurred or after stopTele().
        //
        public void matchStop();
    }

    public void init(BluetoothManager blm, Context context) {
        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        mBluetoothManager = blm;
        bHandler = new Handler();
        mContext = context;
    }

    public void setMyRobotName(String name) {
        myRobotName = name;
    }

    public String getBluetoothName() {
        return mBluetoothAdapter.getName();
    }

    public String getPosition(){
        if (record.color == FCSBLEScanner.AllianceColor.BLUE) {
            if (record.position == 1) {
                return "B1";
            } else {
                return "B2";
            }
        }
        else {
            if (record.position == 1){
                return "R1";
            }
            else {
                return "R2";
            }
        }
    }

    public void startFCSConsoleScan(FCSBLECallback consoleCallback) {
        // Stops scanning after a pre-defined scan period.
        bHandler.postDelayed(new Runnable() {
            @Override
            public void run() {
                mBluetoothAdapter.stopLeScan(bleFCSConsoleScanCallback);
                UIConsoleScanCallback.consoleScanComplete();
            }
        }, SCAN_PERIOD);
        mBluetoothAdapter.startLeScan(bleFCSConsoleScanCallback);
        consoles.clear();

        UIConsoleScanCallback = consoleCallback;
    }

    public void connectToFCS(String consoleName, FCSBLECallback consoleCallback) {
        UIConsoleScanCallback = consoleCallback;
        if (modeCounter == 0){
            if (!consoles.isEmpty()){
                //Log.d("modeCounter", Integer.toString(modeCounter));
                UIConsoleScanCallback.consoleSelected();
                mBluetoothDeviceAddress = consoles.get(consoleName);
                final BluetoothDevice device = mBluetoothAdapter.getRemoteDevice(mBluetoothDeviceAddress);
                mBluetoothGatt = device.connectGatt(mContext, false, mGattCallback);
            }
            else {
                UIConsoleScanCallback.noConsoleSelected();
            }
        }
    }

    public void afterConnectInteract(){
        while (modeCounter == 1 && connectDone == 1){
            modeCounter = 2;
            Log.d("modeCounter", Integer.toString(modeCounter));
            UIConsoleScanCallback.successfulQueue();
        }
        if (modeCounter == 2){
            modeCounter = 3;
            mBluetoothAdapter.startLeScan(bleFCSConsoleScanCallback);
        }
        if (modeCounter == 3){
            if (record.is_inNextMatch){
                UIConsoleScanCallback.queueComplete(record.is_inNextMatch, getPosition());
            }
            if (record.is_invited){
                mBluetoothAdapter.stopLeScan(bleFCSConsoleScanCallback);
                final BluetoothDevice device = mBluetoothAdapter.getRemoteDevice(mBluetoothDeviceAddress);
                mBluetoothGatt = device.connectGatt(mContext, false, mGattCallback);
            }
        }
    }

    public BluetoothAdapter.LeScanCallback bleFCSConsoleScanCallback =
            new BluetoothAdapter.LeScanCallback() {

                @Override
                public void onLeScan(final BluetoothDevice device, int rssi, byte[] scanRecord) {

                    record = new FCSBLEScanner(device, rssi, scanRecord, getBluetoothName());

                    if (record.is_ChapFCS) {
                        if (record.mode == FCSBLEScanner.RunMode.ON_DECK) {
                            //Log.d("Address", device.getAddress());
                            //Log.d("RSSI", Integer.toString(rssi));
                            //Log.d("Name", record.name);
                            //Log.d("Match", Integer.toString(record.matchNumber));
                            //Log.d("My Name", mBluetoothAdapter.getName());

                            consoles.put(record.name, device.getAddress());
                            fcsConsoleRecords.put(record.name, record);
                            afterConnectInteract();
                            UIConsoleScanCallback.processConsole(record.name);
                        }
                        if (record.mode == FCSBLEScanner.RunMode.READY){
                            afterConnectInteract();
                        }
                    }
                }

            };

    private final BluetoothGattCallback mGattCallback = new BluetoothGattCallback() {

        @Override
        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                Log.d("GattCallBack", "Connected to GATT server.");
                // Attempts to discover services after successful connection.
                Log.d("GattCallBack", "Attempting to start service discovery:" + mBluetoothGatt.discoverServices());
                //writeCustomCharacteristic();
            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                afterConnectInteract();
                Log.d("GattCallBack", "Disconnected from GATT server.");
            }
        }

        @Override
        public void onServicesDiscovered(BluetoothGatt gatt, int status) {
            if (status == BluetoothGatt.GATT_SUCCESS) {
                BluetoothGattService mBluetoothGattService = mBluetoothGatt.getService(UUID.fromString(FCSConsoleServiceID));
                if (mBluetoothGattService != null) {
                    Log.i("GattCallBack", "Service characteristic UUID found: " + mBluetoothGattService.getUuid().toString());
                    if (record.mode == FCSBLEScanner.RunMode.ON_DECK){
                        writeRobotNumJoin();
                        modeCounter = 1;
                    }
                    if (record.mode == FCSBLEScanner.RunMode.READY){
                        writeRobotBattery(record.color, record.position, UIConsoleScanCallback.getBatteryStatus(1));
                    }
                } else {
                    Log.i("GattCallBack", "Service characteristic not found for UUID: " + FCSConsoleServiceID);
                }
            }
        }

        @Override
        public void onCharacteristicWrite(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status) {
            mBluetoothGatt.disconnect();
        }
    };


        public void writeRobotNumJoin() {
            if (mBluetoothAdapter == null || mBluetoothGatt == null) {
                Log.w("GattCallBack", "BluetoothAdapter not initialized");
                return;
            }
            /*check if the service is available on the device*/
            BluetoothGattService mCustomService = mBluetoothGatt.getService(UUID.fromString(FCSConsoleServiceID));
            if (mCustomService == null) {
                Log.w("GattCallBack", "Custom BLE Service not found");
                return;
            }
            /*get the write characteristic from the service*/
            BluetoothGattCharacteristic mWriteCharacteristic = mCustomService.getCharacteristic(UUID.fromString(RobotNumJoin));
            mWriteCharacteristic.setValue(myRobotName);
            connectDone = 1;
            if (mBluetoothGatt.writeCharacteristic(mWriteCharacteristic) == false) {
                Log.w("GattCallBack", "Failed to write characteristic");
            }
        }

        public void writeRobotBattery(FCSBLEScanner.AllianceColor color, int position, int percentage) {
            if (mBluetoothAdapter == null || mBluetoothGatt == null) {
                Log.w("GattCallBack", "BluetoothAdapter not initialized");
                return;
            }
                /*check if the service is available on the device*/
            BluetoothGattService mCustomService = mBluetoothGatt.getService(UUID.fromString(FCSConsoleServiceID));
            if (mCustomService == null) {
                Log.w("GattCallBack", "Custom BLE Service not found");
                return;
            }
            BluetoothGattCharacteristic mWriteCharacteristic = null;
            if (color == FCSBLEScanner.AllianceColor.RED){
                if (position == 1){
                        /*get the write characteristic from the service*/
                    mWriteCharacteristic = mCustomService.getCharacteristic(UUID.fromString(R1));
                    mWriteCharacteristic.setValue(Integer.toString(percentage));
                }
                else {
                        /*get the write characteristic from the service*/
                    mWriteCharacteristic = mCustomService.getCharacteristic(UUID.fromString(R2));
                    mWriteCharacteristic.setValue(Integer.toString(percentage));
                }
            }
            else {
                if (position == 1){
                        /*get the write characteristic from the service*/
                    mWriteCharacteristic = mCustomService.getCharacteristic(UUID.fromString(B1));
                    mWriteCharacteristic.setValue(Integer.toString(percentage));
                }
                else {
                        /*get the write characteristic from the service*/
                    mWriteCharacteristic = mCustomService.getCharacteristic(UUID.fromString(B2));
                    mWriteCharacteristic.setValue(Integer.toString(percentage));
                }
            }
            connectDone = 2;
            if (mBluetoothGatt.writeCharacteristic(mWriteCharacteristic) == false) {
                Log.w("GattCallBack", "Failed to write characteristic");
            }
        }
}
