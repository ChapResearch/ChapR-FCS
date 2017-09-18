package org.firstinspires.ftc.robotcontroller.internal;

import android.bluetooth.BluetoothDevice;
import android.util.Log;

/**
 * Created by IyengarArnhav on 4/20/2016.
 */
public class FCSBLEScanner {

    public enum AllianceColor {
        RED, BLUE, NONE
    }

    public enum RunMode {
        SCAN_MODE, ON_DECK, READY, MATCH, NONE
    }

    public enum MatchCommand {
        NONE,          // blank command
        AUTO_INIT,
        AUTO_START,
        TELEOP_INIT,
        TELEOP_START,
        ENDGAME_START,
        MATCH_PAUSE,
        MATCH_RESUME,
        ABORT
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
        this.position = 0;
        this.color = AllianceColor.NONE;
        this.command = MatchCommand.NONE;
        this.mode = RunMode.NONE;

        // determine if this is a connectable broadcast or not

        this.is_connectable = (int)scanRecord[2] != 4;

        // set the initial index for scanning the record

        int index = 5;

        // check for the magic value in the scan record to ensure it is a ChapFCS packet

        this.is_ChapFCS = (scanRecord[index] == (byte)0xC4) && (scanRecord[index+1] == (byte)0xA9);
        //Log.d("1", String.format("0x%02x\n", scanRecord[index]));
        //Log.d("2", String.format("0x%02x\n", scanRecord[index+1]));
        //Log.d("Is it", Boolean.toString(is_ChapFCS));

        // get the mode from the broadcast

        getMode(scanRecord);

        // get the name from the broadcast

        this.name = getName(scanRecord);

        // get the match number for the broadcast

        this.matchNumber = getMatch(scanRecord);

        // gets the alliance color, position on the field, and whether or not it is in the next match

        this.is_inNextMatch = readyMode(scanRecord);

        // is it invited to connect in the ready mode

        this.is_invited = is_Invited(scanRecord);

        // gets the command

        getCommand(scanRecord);
    }

    public void getMode (byte[] bytes){
        int mod = (int)bytes[7];
        switch (mod){
            case 0:
                this.mode = RunMode.SCAN_MODE;
                break;
            case 1:
                this.mode = RunMode.ON_DECK;
                break;
            case 2:
                this.mode = RunMode.READY;
                break;
            case 3:
                this.mode = RunMode.MATCH;
                break;
        }
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
        int match = ((int)bytes[17] & 0xFF);
        return match;
    }

    public boolean readyMode(byte[] bytes){
        int R1 = 0, R2 = 0, B1 = 0, B2 = 0;
        String r1, r2, b1, b2;
        for (int i = 18; i < 19; i++){
            int first = (int)bytes[i] & 0x7F;
            int second = (int)bytes[i+1] & 0xFF;
            R1 = first * 256 + second;
        }
        for (int i = 20; i < 21; i++){
            int first = (int)bytes[i] & 0x7F;
            int second = (int)bytes[i+1] & 0xFF;
            R2 = first * 256 + second;
        }
        for (int i = 22; i < 23; i++){
            int first = (int)bytes[i] & 0x7F;
            int second = (int)bytes[i+1] & 0xFF;
            B1 = first * 256 + second;
        }
        for (int i = 24; i < 25; i++){
            int first = (int)bytes[i] & 0x7F;
            int second = (int)bytes[i+1] & 0xFF;
            B2 = first * 256 + second;
        }

        r1 = R1 + "";
        r2 = R2 + "";
        b1 = B1 + "";
        b2 = B2 + "";

        //Log.d("R1", r1);
        //Log.d("R2", r2);
        //Log.d("B1", b1);
        //Log.d("B2", b2);

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

        if (myName.equals(r1)|| myName.equals(r2) || myName.equals(b1)|| myName.equals(b2))
            return true;
        return false;
    }

    public boolean is_Invited (byte[] bytes){
        if (this.color == AllianceColor.RED && this.position == 1){
            return (bytes[18] & (byte)0x80) == (byte)0x80;
        }
        if (this.color == AllianceColor.RED && this.position == 2){
            return (bytes[20] & (byte)0x80) == (byte)0x80;
        }
        if (this.color == AllianceColor.BLUE && this.position == 1){
            return (bytes[22] & (byte)0x80) == (byte)0x80;
        }
        if (this.color == AllianceColor.BLUE && this.position == 2){
            return (bytes[24] & (byte)0x80) == (byte)0x80;
        }
        return false;
    }

    public void getCommand(byte[] bytes){
        switch (this.color){
            case RED:
                switch (this.position){
                    case 1:
                        int R1 = (int)bytes[26] & 0xF0;
                        switch (R1){
                            case 0:
                                this.command = MatchCommand.NONE;
                                break;
                            case 1:
                                this.command = MatchCommand.AUTO_INIT;
                                break;
                            case 2:
                                this.command = MatchCommand.AUTO_START;
                                break;
                            case 3:
                                this.command = MatchCommand.TELEOP_INIT;
                                break;
                            case 4:
                                this.command = MatchCommand.TELEOP_START;
                                break;
                            case 5:
                                this.command = MatchCommand.ENDGAME_START;
                                break;
                            case 6:
                                this.command = MatchCommand.ABORT;
                                break;
                            case 7:
                                this.command = MatchCommand.MATCH_PAUSE;
                                break;
                            case 8:
                                this.command = MatchCommand.MATCH_RESUME;
                        }
                        break;
                    case 2:
                        int R2 = (int)bytes[26] & 0x0F;
                        switch (R2){
                            case 0:
                                this.command = MatchCommand.NONE;
                                break;
                            case 1:
                                this.command = MatchCommand.AUTO_INIT;
                                break;
                            case 2:
                                this.command = MatchCommand.AUTO_START;
                                break;
                            case 3:
                                this.command = MatchCommand.TELEOP_INIT;
                                break;
                            case 4:
                                this.command = MatchCommand.TELEOP_START;
                                break;
                            case 5:
                                this.command = MatchCommand.ENDGAME_START;
                                break;
                            case 6:
                                this.command = MatchCommand.ABORT;
                                break;
                            case 7:
                                this.command = MatchCommand.MATCH_PAUSE;
                                break;
                            case 8:
                                this.command = MatchCommand.MATCH_RESUME;
                        }
                        break;
                }
                break;
            case BLUE:
                switch (this.position){
                    case 1:
                        int B1 = (int)bytes[26] & 0xF0;
                        switch (B1){
                            case 0:
                                this.command = MatchCommand.NONE;
                                break;
                            case 1:
                                this.command = MatchCommand.AUTO_INIT;
                                break;
                            case 2:
                                this.command = MatchCommand.AUTO_START;
                                break;
                            case 3:
                                this.command = MatchCommand.TELEOP_INIT;
                                break;
                            case 4:
                                this.command = MatchCommand.TELEOP_START;
                                break;
                            case 5:
                                this.command = MatchCommand.ENDGAME_START;
                                break;
                            case 6:
                                this.command = MatchCommand.ABORT;
                                break;
                            case 7:
                                this.command = MatchCommand.MATCH_PAUSE;
                                break;
                            case 8:
                                this.command = MatchCommand.MATCH_RESUME;
                        }
                        break;
                    case 2:
                        int B2 = (int)bytes[26] & 0x0F;
                        switch (B2){
                            case 0:
                                this.command = MatchCommand.NONE;
                                break;
                            case 1:
                                this.command = MatchCommand.AUTO_INIT;
                                break;
                            case 2:
                                this.command = MatchCommand.AUTO_START;
                                break;
                            case 3:
                                this.command = MatchCommand.TELEOP_INIT;
                                break;
                            case 4:
                                this.command = MatchCommand.TELEOP_START;
                                break;
                            case 5:
                                this.command = MatchCommand.ENDGAME_START;
                                break;
                            case 6:
                                this.command = MatchCommand.ABORT;
                                break;
                            case 7:
                                this.command = MatchCommand.MATCH_PAUSE;
                                break;
                            case 8:
                                this.command = MatchCommand.MATCH_RESUME;
                        }
                        break;
                }
                break;
        }
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
