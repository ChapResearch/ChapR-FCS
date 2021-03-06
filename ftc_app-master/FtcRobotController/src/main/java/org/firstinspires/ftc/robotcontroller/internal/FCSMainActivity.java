package org.firstinspires.ftc.robotcontroller.internal;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.os.Bundle;
import android.app.Activity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.qualcomm.ftcrobotcontroller.R;
import com.qualcomm.robotcore.eventloop.opmode.OpModeMeta;

import java.util.List;



public class FCSMainActivity extends Activity {

    public RelativeLayout screenLayout;
    public Button confirmButton;
    public Button backButton;
    public Spinner autoSelector;
    public Spinner teleopSelector;
    public static Spinner fieldOptions;
    public TextView fieldText;
    public TextView autoText;
    public TextView teleopText;
    public TextView messageText;
    public TextView matchText;
    public TextView matchNum;
    private FCSBLE fcsble = new FCSBLE();

    public ArrayAdapter<String> fieldOptionsAdapter;
    public ArrayAdapter<String> autoOptionsAdapter;
    public ArrayAdapter<String> teleOptionsAdapter;

    private List<OpModeMeta> opModes;

    public int confirmCounter;
    private int counter;

    private int tempTestCount = 0;

    IntentFilter ifilter;
    Intent batteryStatus;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fcsmain);

        screenLayout = (RelativeLayout) findViewById(R.id.screenLayoutFCS);
        confirmButton = (Button) findViewById(R.id.confirmButton);
        backButton = (Button) findViewById(R.id.backButton);
        autoSelector = (Spinner) findViewById(R.id.autoPicker);
        teleopSelector = (Spinner) findViewById(R.id.teleOpPicker);
        fieldOptions = (Spinner) findViewById(R.id.fieldOptions);
        fieldText = (TextView) findViewById(R.id.fieldText);
        autoText = (TextView) findViewById(R.id.autoText);
        teleopText = (TextView) findViewById(R.id.teleopText);
        messageText = (TextView) findViewById(R.id.errorMessage);
        matchText = (TextView) findViewById(R.id.matchText);
        matchNum = (TextView) findViewById(R.id.matchNumber);

        fcsble.init((BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE), getApplicationContext());

        fcsble.setMyRobotName(fcsble.getBluetoothName());

        fieldOptionsAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, android.R.id.text1);
        autoOptionsAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, android.R.id.text1);
        teleOptionsAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, android.R.id.text1);
        fieldOptions.setAdapter(fieldOptionsAdapter);
        autoSelector.setAdapter(autoOptionsAdapter);
        teleopSelector.setAdapter(teleOptionsAdapter);

        confirmCounter = 0;
        opModes = FtcRobotControllerActivity.eventLoop.getOpModeManager().getOpModes();

        if (fieldOptionsAdapter.isEmpty()){
            fieldOptionsAdapter.add("-None-");
        }
        if (autoOptionsAdapter.isEmpty()){
            autoOptionsAdapter.add("-None-");
        }
        if (teleOptionsAdapter.isEmpty()){
            teleOptionsAdapter.add("-None-");
        }

        for (int i = 0; i < opModes.size(); i++){
            switch (opModes.get(i).flavor){
                case AUTONOMOUS:
                    autoOptionsAdapter.add(opModes.get(i).name);
                    break;
                case TELEOP:
                    teleOptionsAdapter.add(opModes.get(i).name);
                    break;
            }

        }

        //mBluetoothService.initialize();

        ifilter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
        batteryStatus = this.registerReceiver(null, ifilter);

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

        fcsble.startFCSConsoleScan(fcsBLECallBack);
        confirmButton.setEnabled(false);
        confirmButton.setAlpha(.5f);

        fieldOptions.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                fcsble.updateMatch(fieldOptionsAdapter.getItem(position));
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                return;
            }
        });

        confirmButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                confirmButton.setVisibility(View.INVISIBLE);
                autoSelector.setVisibility(View.INVISIBLE);
                teleopSelector.setVisibility(View.INVISIBLE);
                fieldText.setVisibility(View.INVISIBLE);
                autoText.setVisibility(View.INVISIBLE);
                teleopText.setVisibility(View.INVISIBLE);
                fieldOptions.setVisibility(View.INVISIBLE);
                matchText.setVisibility(View.INVISIBLE);
                matchNum.setVisibility(View.INVISIBLE);
                messageText.setVisibility(View.VISIBLE);
                backButton.setVisibility(View.VISIBLE);
                fcsble.connectToFCS(fieldOptionsAdapter.getItem(fieldOptions.getSelectedItemPosition()), fcsBLECallBack);
                confirmCounter = 1;
            }
        });
        backButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                fcsBLECallBack.resetToZero();
                confirmCounter = 0;
            }
        });
    }

    public FCSBLE.FCSBLECallback fcsBLECallBack =
            new FCSBLE.FCSBLECallback() {

                @Override
                public void updateMatchNum(final String match) {
                    Thread t = new Thread(new Runnable() {
                        @Override
                        public void run() {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    matchNum.setText(match);
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

                @Override
                public void processConsole(final String name) {
                    Thread t = new Thread(new Runnable() {
                        @Override
                        public void run() {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    for (int i = 1; i <= fieldOptionsAdapter.getCount(); i++){
                                        if (fieldOptionsAdapter.getItem(i-1).equals(name)){
                                            counter++;
                                        }
                                    }
                                    if (counter == 0){
                                        fieldOptionsAdapter.add(name);
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

                @Override
                public void consoleSelected() {
                    Thread t = new Thread(new Runnable() {
                        @Override
                        public void run() {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    messageText.setText("Attempting Connection...");
                                    confirmCounter = 0;
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

                @Override
                public void noConsoleSelected() {
                    Thread t = new Thread(new Runnable() {
                        @Override
                        public void run() {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    messageText.setText("Please go back and select a field to join");
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

                @Override
                public void consoleScanComplete() {
                    Thread t = new Thread(new Runnable() {
                        @Override
                        public void run() {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    confirmButton.setAlpha(1f);
                                    confirmButton.setEnabled(true);
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

                @Override
                public void successfulQueue() {
                    Thread t = new Thread(new Runnable() {
                        @Override
                        public void run() {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    messageText.setText("Waiting...");
                                    backButton.setVisibility(View.INVISIBLE);
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

                @Override
                public void queueComplete(boolean accepted, String position) {
                    if (accepted){
                        if (position.equals("R1")){
                            Thread t = new Thread(new Runnable() {
                                @Override
                                public void run() {
                                    runOnUiThread(new Runnable() {

                                        @Override
                                        public void run() {
                                            screenLayout.setBackgroundColor(Color.RED);
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
                                            screenLayout.setBackgroundColor(Color.RED);
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
                                            screenLayout.setBackgroundColor(Color.BLUE);
                                            messageText.setText("B1");
                                            if (confirmCounter == 1) {
                                                messageText.setVisibility(View.VISIBLE);
                                            }
                                            if (tempTestCount == 0){
                                                fcsBLECallBack.startAutoInit();
                                                tempTestCount = 1;
                                            }
                                            fcsBLECallBack.startAuto();
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
                                            screenLayout.setBackgroundColor(Color.BLUE);
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
                public int getRobotBatteryStatus() {
                    return 0;
                }

                @Override
                public int getPhoneBatteryStatus() {
                    return 0;
                }

                @Override
                public void resetToZero() {
                    Thread t = new Thread(new Runnable() {
                        @Override
                        public void run() {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    confirmButton.setVisibility(View.VISIBLE);
                                    autoSelector.setVisibility(View.VISIBLE);
                                    teleopSelector.setVisibility(View.VISIBLE);
                                    fieldText.setVisibility(View.VISIBLE);
                                    autoText.setVisibility(View.VISIBLE);
                                    teleopText.setVisibility(View.VISIBLE);
                                    fieldOptions.setVisibility(View.VISIBLE);
                                    matchText.setVisibility(View.VISIBLE);
                                    matchNum.setVisibility(View.VISIBLE);
                                    messageText.setVisibility(View.INVISIBLE);
                                    backButton.setVisibility(View.INVISIBLE);
                                    screenLayout.setBackgroundColor(Color.BLACK);
                                    confirmButton.setEnabled(false);
                                    confirmButton.setAlpha(.5f);
                                    confirmCounter = 0;
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

                @Override
                public void startAutoInit() {
                    if (!String.valueOf(autoSelector.getSelectedItem()).equals("-None-"))
                        FtcRobotControllerActivity.eventLoop.getOpModeManager().initActiveOpMode(String.valueOf(autoSelector.getSelectedItem()));
                }

                @Override
                public void startAuto() {
                    FtcRobotControllerActivity.eventLoop.getOpModeManager().startActiveOpMode();
                }

                @Override
                public void stopAuto() {
                    FtcRobotControllerActivity.eventLoop.getOpModeManager().stopActiveOpMode();
                }

                @Override
                public void startTeleInit() {
                    if (!String.valueOf(autoSelector.getSelectedItem()).equals("-None-"))
                        FtcRobotControllerActivity.eventLoop.getOpModeManager().initActiveOpMode(String.valueOf(teleopSelector.getSelectedItem()));
                }

                @Override
                public void startTele() {
                    FtcRobotControllerActivity.eventLoop.getOpModeManager().startActiveOpMode();
                }

                @Override
                public void startEndGame() {
                    Thread t = new Thread(new Runnable() {
                        @Override
                        public void run() {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    screenLayout.setBackgroundColor(Color.YELLOW);
                                }
                            }) ;
                            try {
                                Thread.sleep(1000);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                        }
                    });
                    t.start();
                }

                @Override
                public void stopTele() {
                    FtcRobotControllerActivity.eventLoop.getOpModeManager().stopActiveOpMode();
                }

                @Override
                public void matchPause() {
                    FtcRobotControllerActivity.eventLoop.getOpModeManager().stopActiveOpMode();
                }

                @Override
                public void matchResume() {
                    FtcRobotControllerActivity.eventLoop.getOpModeManager().startActiveOpMode();
                }

                @Override
                public void matchStop() {
                    FtcRobotControllerActivity.eventLoop.getOpModeManager().stopActiveOpMode();
                }
            };
}