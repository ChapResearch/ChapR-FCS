package com.chapresearch.ftcchaprfcs;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;


public class FCSMainActivity extends AppCompatActivity {

    public RelativeLayout screenLayout;
    public Button confirmButton;
    public Button scanButton;
    public Button backButton;
    public Spinner autoSelector;
    public Spinner teleopSelector;
    public Spinner fieldOptions;
    public TextView fieldText;
    public TextView autoText;
    public TextView teleopText;
    public TextView messageText;
    private FCSBLE fcsble = new FCSBLE();

    public ArrayAdapter<String> spinnerAdapter;

    public int confirmCounter;
    private int counter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fcsmain);

        screenLayout = (RelativeLayout) findViewById(R.id.screenLayout);
        confirmButton = (Button) findViewById(R.id.confirmButton);
        scanButton = (Button) findViewById(R.id.scanButton);
        backButton = (Button) findViewById(R.id.backButton);
        autoSelector = (Spinner) findViewById(R.id.autoPicker);
        teleopSelector = (Spinner) findViewById(R.id.teleOpPicker);
        fieldOptions = (Spinner) findViewById(R.id.fieldOptions);
        fieldText = (TextView) findViewById(R.id.fieldText);
        autoText = (TextView) findViewById(R.id.autoText);
        teleopText = (TextView) findViewById(R.id.teleopText);
        messageText = (TextView) findViewById(R.id.errorMessage);

        fcsble.init((BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE), getApplicationContext());

        fcsble.setMyRobotName(fcsble.getBluetoothName());

        spinnerAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, android.R.id.text1);
        fieldOptions.setAdapter(spinnerAdapter);

        confirmCounter = 0;

        if (spinnerAdapter.isEmpty()){
            spinnerAdapter.add("-None-");
        }

        //mBluetoothService.initialize();

        if (fcsble.mBluetoothAdapter == null) {
            Toast.makeText(this,"bluetooth hardware not found :(", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        if (fcsble.mBluetoothAdapter == null || !fcsble.mBluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, 1);
            return;
        }

        confirmButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                scanButton.setVisibility(View.INVISIBLE);
                confirmButton.setVisibility(View.INVISIBLE);
                autoSelector.setVisibility(View.INVISIBLE);
                teleopSelector.setVisibility(View.INVISIBLE);
                fieldText.setVisibility(View.INVISIBLE);
                autoText.setVisibility(View.INVISIBLE);
                teleopText.setVisibility(View.INVISIBLE);
                fieldOptions.setVisibility(View.INVISIBLE);
                messageText.setVisibility(View.VISIBLE);
                backButton.setVisibility(View.VISIBLE);
                //fcsble.scanLEDevice(true);
                //fcsble.mBluetoothAdapter.startLeScan(bLeScanCallback);
                fcsble.connectToFCS(spinnerAdapter.getItem(fieldOptions.getSelectedItemPosition()), fcsBLECallBack);
                confirmCounter = 1;
            }
        });
        backButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                scanButton.setVisibility(View.VISIBLE);
                confirmButton.setVisibility(View.VISIBLE);
                autoSelector.setVisibility(View.VISIBLE);
                teleopSelector.setVisibility(View.VISIBLE);
                fieldText.setVisibility(View.VISIBLE);
                autoText.setVisibility(View.VISIBLE);
                teleopText.setVisibility(View.VISIBLE);
                fieldOptions.setVisibility(View.VISIBLE);
                messageText.setVisibility(View.INVISIBLE);
                backButton.setVisibility(View.INVISIBLE);
                confirmCounter = 0;
            }
        });

        scanButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //fcsble.mBluetoothAdapter.stopLeScan(bLeScanCallback);
                //mBluetoothAdapter.startLeScan(bLeScanCallback);
                fcsble.startFCSConsoleScan(fcsBLECallBack);
                scanButton.setText("Wait...");
                scanButton.setClickable(false);
                confirmButton.setAlpha(.5f);
                confirmButton.setClickable(false);
            }
        });
    }

    public FCSBLE.FCSBLECallback fcsBLECallBack =
            new FCSBLE.FCSBLECallback() {
                @Override
                public void processConsole(String name) {
                    for (int i = 1; i <= spinnerAdapter.getCount(); i++){
                        if (spinnerAdapter.getItem(i-1).equals(name)){
                            counter++;
                        }
                    }
                    if (counter == 0){
                        spinnerAdapter.add(name);
                    }
                }

                @Override
                public void consoleScanComplete() {
                    scanButton.setText("Scan");
                    scanButton.setClickable(true);
                    confirmButton.setAlpha(1f);
                    confirmButton.setClickable(true);
                }

                @Override
                public void successfulQueue() {

                }

                @Override
                public void queueComplete(boolean accepted, String position) {
                    if (accepted){
                        if (confirmCounter == 1) {
                            backButton.setVisibility(View.INVISIBLE);
                        }
                        if (position.equals("R1")){
                            Thread t = new Thread(new Runnable() {
                                @Override
                                public void run() {
                                    runOnUiThread(new Runnable() {

                                        @Override
                                        public void run() {
                                            messageText.setText("R1");
                                            if (confirmCounter == 1) {
                                                messageText.setVisibility(View.VISIBLE);
                                            }
                                        }
                                    }) ;
                                    try {
                                        Thread.sleep(500);
                                    } catch (InterruptedException e) {
                                        e.printStackTrace();
                                    }
                                }
                            });
                            t.start();
                        }
                        if (position.equals("R2")){
                            Thread t = new Thread(new Runnable() {
                                @Override
                                public void run() {
                                    runOnUiThread(new Runnable() {

                                        @Override
                                        public void run() {
                                            messageText.setText("R2");
                                            if (confirmCounter == 1) {
                                                messageText.setVisibility(View.VISIBLE);
                                            }
                                        }
                                    }) ;
                                    try {
                                        Thread.sleep(500);
                                    } catch (InterruptedException e) {
                                        e.printStackTrace();
                                    }
                                }
                            });
                            t.start();
                        }
                        if (position.equals("B1")){
                            Thread t = new Thread(new Runnable() {
                                @Override
                                public void run() {
                                    runOnUiThread(new Runnable() {

                                        @Override
                                        public void run() {
                                            messageText.setText("B1");
                                            if (confirmCounter == 1) {
                                                messageText.setVisibility(View.VISIBLE);
                                            }
                                        }
                                    }) ;
                                    try {
                                        Thread.sleep(500);
                                    } catch (InterruptedException e) {
                                        e.printStackTrace();
                                    }
                                }
                            });
                            t.start();
                        }
                        if (position.equals("B2")){
                            Thread t = new Thread(new Runnable() {
                                @Override
                                public void run() {
                                    runOnUiThread(new Runnable() {

                                        @Override
                                        public void run() {
                                            messageText.setText("B2");
                                            if (confirmCounter == 1) {
                                                messageText.setVisibility(View.VISIBLE);
                                            }
                                        }
                                    }) ;
                                    try {
                                        Thread.sleep(500);
                                    } catch (InterruptedException e) {
                                        e.printStackTrace();
                                    }
                                }
                            });
                            t.start();
                        }
                    }
                    else {
                        Thread t = new Thread(new Runnable() {
                            @Override
                            public void run() {
                                runOnUiThread(new Runnable() {

                                    @Override
                                    public void run() {
                                        messageText.setTextColor(Color.RED);
                                        messageText.setText("Connection Rejected");
                                        if (confirmCounter == 1)
                                            messageText.setVisibility(View.VISIBLE);
                                    }
                                }) ;
                                try {
                                    Thread.sleep(500);
                                } catch (InterruptedException e) {
                                    e.printStackTrace();
                                }
                            }
                        });
                        t.start();
                    }
                }

                @Override
                public int getBatteryStatus(int battery) {
                    return 0;
                }

                @Override
                public void startAutoInit() {

                }

                @Override
                public void startAuto() {

                }

                @Override
                public void stopAuto() {

                }

                @Override
                public void startTeleInit() {

                }

                @Override
                public void startTele() {

                }

                @Override
                public void startEndGame() {

                }

                @Override
                public void stopTele() {

                }

                @Override
                public void matchPause() {

                }

                @Override
                public void matchResume() {

                }

                @Override
                public void matchStop() {

                }
            };

    public BluetoothAdapter.LeScanCallback bLeScanCallback =
            new BluetoothAdapter.LeScanCallback() {

                @Override
                public void onLeScan(final BluetoothDevice device, int rssi, byte[] scanRecord) {

                    FCSBLEScanner record = new FCSBLEScanner(device, rssi, scanRecord, fcsble.getBluetoothName());

                    counter = 0;

                    if (record.is_ChapFCS){
                        switch (record.mode){
                            case ON_DECK:
                                //Log.d("Address", device.getAddress());
                                //Log.d("RSSI",Integer.toString(rssi));
                                //Log.d("Name", record.name);
                                //Log.d("Match", Integer.toString(record.matchNumber));
                                //Log.d("My Name", mBluetoothAdapter.getName());

                                for (int i = 1; i <= spinnerAdapter.getCount(); i++){
                                    if (spinnerAdapter.getItem(i-1).equals(record.name + " " + device.getAddress())){
                                        counter++;
                                    }
                                }
                                if (counter == 0){
                                    spinnerAdapter.add(record.name + " " + device.getAddress());
                                }
                                break;
                            case READY:
                                //Log.d("Name", record.name);
                                //Log.d("Match", Integer.toString(record.matchNumber));
                                //Log.d("Is in", Boolean.toString(record.is_invited));
                                if (record.is_inNextMatch){
                                    Thread t = new Thread(new Runnable() {
                                        @Override
                                        public void run() {
                                            runOnUiThread(new Runnable() {

                                                @Override
                                                public void run() {
                                                    messageText.setTextColor(Color.GREEN);
                                                    messageText.setText("Connection Successful");
                                                    if (confirmCounter == 1) {
                                                        messageText.setVisibility(View.VISIBLE);
                                                    }
                                                }
                                            }) ;
                                            try {
                                                Thread.sleep(500);
                                            } catch (InterruptedException e) {
                                                e.printStackTrace();
                                            }
                                        }
                                    });
                                    t.start();
                                    if (record.is_invited){

                                    }
                                }
                                else {
                                    Thread t = new Thread(new Runnable() {
                                        @Override
                                        public void run() {
                                            runOnUiThread(new Runnable() {

                                                @Override
                                                public void run() {
                                                    messageText.setTextColor(Color.RED);
                                                    messageText.setText("Connection Rejected");
                                                    if (confirmCounter == 1)
                                                        messageText.setVisibility(View.VISIBLE);
                                                }
                                            }) ;
                                            try {
                                                Thread.sleep(500);
                                            } catch (InterruptedException e) {
                                                e.printStackTrace();
                                            }
                                        }
                                    });
                                    t.start();
                                }
                                break;
                            case MATCH:
                                if (record.is_inNextMatch){
                                    switch (record.command){
                                        case AUTO_INIT:
                                            break;
                                        case AUTO_START:
                                            break;
                                        case TELEOP_INIT:
                                            break;
                                        case TELEOP_START:
                                            break;
                                        case ENDGAME_START:
                                            break;
                                        case ABORT:
                                            break;
                                        case NONE:
                                            break;
                                    }
                                }
                                break;
                        }
                    }
                }

            };

    /*private BluetoothAdapter.LeScanCallback FCSOnDeckJoin =
            new BluetoothAdapter.LeScanCallback() {

                @Override
                public void onLeScan(final BluetoothDevice device, int rssi, byte[] scanRecord) {

                    FCSBLEScanner record = new FCSBLEScanner(device, rssi, scanRecord, fcsble.getName());

                    if (record.is_connectable){
                        if (confirmCounter == 1) {
                            mBluetoothService.connect(device.getAddress());
                        }
                    }
                }

            };*/
}