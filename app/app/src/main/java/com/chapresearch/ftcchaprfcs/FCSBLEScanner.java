package com.chapresearch.ftcchaprfcs;

import android.bluetooth.BluetoothDevice;

/**
 * Created by IyengarArnhav on 4/20/2016.
 */
public class FCSBLEScanner {

    public enum AllianceColor {
        RED, BLUE, NONE
    }

    public enum RunMode {
        ON_DECK, READY, MATCH, NONE
    }

    public enum MatchCommand {
        NONE,          // blank command
        AUTO_INIT,
        AUTO_START,
        TELEOP_INIT,
        TELEOP_START,
        ENDGAME_START,
        STOP
    }

    public av1String       getName;         // The object to decode the 6 bit ascii
    public String          myName;          // name of robot controller (team number)
    public boolean         is_ChapFCS;      // true if it is a good ChapFCS packet
    public BluetoothDevice device;
    public int             rssi;            // power measurement relieved from broadcast
    public boolean         is_connectable;  // true if the incoming broadcast is connectable
    public RunMode         mode;            // the current protocol mode that the broadcast sets
    public String          name;            // the name of the field that the broadcast sets
    public int             matchNumber;     // the current match number that the console sent
    public AllianceColor   color;           // the alliance color
    public int             position;        // position in the alliance ( 1 or 2 )
    public boolean         is_inNextMatch;  // true if broadcast contains robot number for next match
    public boolean         is_invited;      // true if I have a ready mode connection invite
    public MatchCommand    command;         // the command for me in match mode

    public FCSBLEScanner (final BluetoothDevice device, int rssi, byte[] scanRecord, String myTeamNumber){

        this.device = device;
        this.rssi = rssi;
        this.myName = myTeamNumber;
        this.matchNumber = 0;
        this.position = 0;
        this.is_inNextMatch = false;
        this.is_invited = false;
        this.mode = getMode(scanRecord);
        this.color = AllianceColor.NONE;
        this.command = MatchCommand.NONE;

        // determine if this is a connectable broadcast or not

        this.is_connectable = (int)scanRecord[2] != 4;

        // set the inital index for scanning the record

        int index = 5;

        // check for the magic value in the scan record to ensure it is a ChapFCS packet

        this.is_ChapFCS = (char)scanRecord[index] == 0xC4 && (char)scanRecord[index+1] == 0xA9;

        // get the name from the broadcast

        this.name = getName(scanRecord);

        // get the match number fro the broadcast

        this.matchNumber = getMatch(scanRecord);
    }

    public RunMode getMode (byte[] bytes){
        if (bytes[7] == 0)
            return RunMode.ON_DECK;
        else if (bytes[7] == 1)
            return RunMode.READY;
        else if (bytes[7] == 2)
            return RunMode.MATCH;
        return RunMode.NONE;
    }

    public String getName(byte[] bytes){
        byte[] temp = new byte[9];
        for (int i = 8, k = 0; i < 17; i++, k++){
            temp[k] = bytes[i];
        }
        this.getName = new av1String(temp, 12);

        return getName.toString();
    }

    public int getMatch(byte[] bytes){
        int match = 0;
        for (int i = 17; i < 18; i++){
            match = (int) bytes[i];
        }
        return match;
    }

    public boolean readyMode(byte[] bytes){
        int R1 = 0, R2 = 0, B1 = 0, B2 = 0;
        String r1, r2, b1, b2;
        for (int i = 18; i < 20; i++){
            R1 += (int)bytes[i];
        }
        for (int i = 20; i < 22; i++){
            R2 += (int)bytes[i];
        }
        for (int i = 22; i < 24; i++){
            B1 += (int)bytes[i];
        }
        for (int i = 24; i < 26; i++){
            B2 += (int)bytes[i];
        }

        r1 = R1 + "";
        r2 = R2 + "";
        b1 = B1 + "";
        b2 = B2 + "";

        if (myName.equals(r1) || myName.equals(r2)){
            color = AllianceColor.RED;
        }
        else if (myName.equals(b1)|| myName.equals(b2)){
            color = AllianceColor.BLUE;
        }
        else {
            color = AllianceColor.NONE;
        }

        if (myName.equals(r1)|| myName.equals(b1)){
            position = 1;
        }
        else if (myName.equals(r2) || myName.equals(b2)){
            position = 2;
        }
        else {
            position = 0;
        }

        if (myName.equals(r1)|| myName.equals(r2) || myName.equals(r1)|| myName.equals(r2))
            return true;
        return false;
    }

    final protected static char[] hexArray = "0123456789ABCDEF".toCharArray();
    public static String bytesToHex(byte[] bytes) {
        char[] hexChars = new char[bytes.length * 2];
        for ( int j = 0; j < bytes.length; j++ ) {
            int v = bytes[j] & 0xFF;
            hexChars[j * 2] = hexArray[v >>> 4];
            hexChars[j * 2 + 1] = hexArray[v & 0x0F];
        }
        return new String(hexChars);
    }
}
