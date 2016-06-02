package com.chapresearch.ftcchaprfcs;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.chapresearch.ftcchaprfcs.av1String;

import java.util.Arrays;

public class FCSMainActivity extends ActionBarActivity {

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

        if (mBluetoothAdapter == null) {
            Toast.makeText(this,"bluetooth hardware not found :(", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        if (mBluetoothAdapter == null || !mBluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, 1);
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
                backButton.setVisibility(View.VISIBLE);
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
                messageText.setVisibility(View.INVISIBLE);
                backButton.setVisibility(View.INVISIBLE);
            }
        });

        scanButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
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
                    if (record.is_ChapFCS){
                        Log.d("Address", device.getAddress());
                        Log.d("RSSI",Integer.toString(rssi));
                        Log.d("SR",record.bytesToHex(scanRecord));
                        switch (record.mode){
                            case ON_DECK:
                                if (record.is_connectable){

                                }
                                break;
                            case READY:
                                if (record.is_inNextMatch){
                                    messageText.setTextColor(Color.GREEN);
                                    messageText.setText("Access: Granted");
                                    messageText.setVisibility(View.VISIBLE);
                                    try {
                                        Thread.sleep(500);
                                    } catch (InterruptedException e) {
                                        e.printStackTrace();
                                    }
                                    messageText.setVisibility(View.INVISIBLE);
                                }
                                else {
                                    messageText.setTextColor(Color.RED);
                                    messageText.setText("Access: Denied");
                                    messageText.setVisibility(View.VISIBLE);
                                }
                                break;
                            case MATCH:
                                break;
                        }
                    }
                    if (record.mode == FCSBLEScanner.RunMode.READY || record.mode == FCSBLEScanner.RunMode.MATCH){
                        mBluetoothAdapter.startLeScan(bLeScanCallback);
                    }
                    else {
                        scanLeDevice(false);
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