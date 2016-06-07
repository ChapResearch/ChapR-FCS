package com.chapresearch.ftcchaprfcs;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;



public class FCSMainActivity extends AppCompatActivity {

    private Button confirmButton;
    private Button scanButton;
    private Button backButton;
    private Spinner autoSelector;
    private Spinner teleopSelector;
    private Spinner fieldOptions;
    private TextView fieldText;
    private TextView autoText;
    private TextView teleopText;
    private TextView messageText;
    private BluetoothAdapter mBluetoothAdapter;

    private boolean bScanning;
    private Handler bHandler;
    private static final long SCAN_PERIOD = 10000;

    private ArrayAdapter<String> spinnerAdapter;

    private int counter;
    private int confirmCounter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fcsmain);

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
        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        bHandler=new Handler();
        bScanning = true;

        final BluetoothManager bluetoothManager =
                (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);

        spinnerAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, android.R.id.text1);
        fieldOptions.setAdapter(spinnerAdapter);

        counter = 0;
        confirmCounter = 0;

        if (spinnerAdapter.isEmpty()){
            spinnerAdapter.add("-None-");
        }

        if (mBluetoothAdapter == null) {
            Toast.makeText(this,"bluetooth hardware not found :(", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        if (mBluetoothAdapter == null || !mBluetoothAdapter.isEnabled()) {
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
                backButton.setVisibility(View.VISIBLE);
                mBluetoothAdapter.startLeScan(bLeScanCallback);
                confirmCounter++;
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
                mBluetoothAdapter.stopLeScan(bLeScanCallback);
                confirmCounter--;
            }
        });

        scanButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mBluetoothAdapter.stopLeScan(bLeScanCallback);
                scanLeDevice(true);
                //mBluetoothAdapter.startLeScan(bLeScanCallback);
            }
        });
    }

    private BluetoothAdapter.LeScanCallback bLeScanCallback =
            new BluetoothAdapter.LeScanCallback() {

                @Override
                public void onLeScan(final BluetoothDevice device, int rssi, byte[] scanRecord) {

                    FCSBLEScanner record = new FCSBLEScanner(device, rssi, scanRecord, mBluetoothAdapter.getName());

                    counter = 0;

                    if (record.is_ChapFCS){
                        switch (record.mode){
                            case ON_DECK:
                                Log.d("Address", device.getAddress());
                                Log.d("RSSI",Integer.toString(rssi));
                                Log.d("Name", record.name);
                                Log.d("Match", Integer.toString(record.matchNumber));
                                Log.d("My Name", mBluetoothAdapter.getName());

                                for (int i = 1; i <= spinnerAdapter.getCount(); i++){
                                    if (spinnerAdapter.getItem(i-1).equals(record.name + "\n" + device.getAddress())){
                                        counter++;
                                    }
                                }
                                if (counter == 0){
                                    spinnerAdapter.add(record.name + "\n" + device.getAddress());
                                }
                                break;
                            case READY:
                                Log.d("Name", record.name);
                                Log.d("Match", Integer.toString(record.matchNumber));
                                Log.d("Is in", Boolean.toString(record.is_inNextMatch));
                                if (record.is_inNextMatch){
                                    messageText.setTextColor(Color.GREEN);
                                    messageText.setText("Access: Granted");
                                    if (confirmCounter == 1){
                                        messageText.setVisibility(View.VISIBLE);
                                    }
                                    switch (record.color){
                                        case RED:
                                            break;
                                        case BLUE:
                                            break;
                                        case NONE:
                                            break;
                                    }
                                }
                                else {
                                    messageText.setTextColor(Color.RED);
                                    messageText.setText("Access: Denied");
                                    if (confirmCounter == 1){
                                        messageText.setVisibility(View.VISIBLE);
                                    }
                                }
                                break;
                            case MATCH:
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
                                    case STOP:
                                        break;
                                    case NONE:
                                        break;
                                }
                                break;
                        }
                    }
                }

            };


    private void scanLeDevice(final boolean enable) {
        if (enable) {
            // Stops scanning after a pre-defined scan period.
            bHandler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    bScanning = false;
                    mBluetoothAdapter.stopLeScan(bLeScanCallback);
                    invalidateOptionsMenu();
                }
            }, SCAN_PERIOD);
            bScanning = true;
            mBluetoothAdapter.startLeScan(bLeScanCallback);
        } else {
            bScanning = false;
            mBluetoothAdapter.stopLeScan(bLeScanCallback);
        }
        invalidateOptionsMenu();
    }
}