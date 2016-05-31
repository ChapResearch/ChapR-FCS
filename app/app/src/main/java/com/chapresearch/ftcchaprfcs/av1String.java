package com.chapresearch.ftcchaprfcs;

/**
 * Created by IyengarArnhav on 5/2/2016.
 */
public class av1String {

    static byte[] av1encoding = {
            0,  'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
            'P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e',
            'f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u',
            'v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','-'
    };
    
    // this is an ascii translation table to av1 that starts at 0x20
    static byte[] av1ReverseEncoding = {
    		(byte)0x00,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,
    		(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,
    		(byte)0x3E,(byte)0x35,(byte)0x36,(byte)0x37,(byte)0x38,(byte)0x39,(byte)0x3A,(byte)0x3B,
    		(byte)0x3C,(byte)0x3D,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,
    		(byte)0x3F,(byte)0x01,(byte)0x02,(byte)0x03,(byte)0x04,(byte)0x05,(byte)0x06,(byte)0x07,
    		(byte)0x08,(byte)0x09,(byte)0x0A,(byte)0x0B,(byte)0x0C,(byte)0x0D,(byte)0x0E,(byte)0x0F,
    		(byte)0x10,(byte)0x11,(byte)0x12,(byte)0x13,(byte)0x14,(byte)0x15,(byte)0x16,(byte)0x17,
    		(byte)0x18,(byte)0x19,(byte)0x1A,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,
    		(byte)0x3F,(byte)0x1B,(byte)0x1C,(byte)0x1D,(byte)0x1E,(byte)0x1F,(byte)0x20,(byte)0x21,
    		(byte)0x22,(byte)0x23,(byte)0x24,(byte)0x25,(byte)0x26,(byte)0x27,(byte)0x28,(byte)0x29,
    		(byte)0x2A,(byte)0x2B,(byte)0x2C,(byte)0x2D,(byte)0x2E,(byte)0x2F,(byte)0x30,(byte)0x31,
    		(byte)0x32,(byte)0x33,(byte)0x34,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,(byte)0x3F,
    };

    private byte[] storage;
    private int count;

    public av1String (){
    }

    public av1String (byte[] bytes, int achars){        //the input is packed av1

        storage = new byte[achars];
        count = achars;
        int slots = bytes.length;

        for (int i = 0, b = 0; i < achars; i+=4, b+=3){
            //int selector = (i % 4 == 0) ? 4: i % 4;
            storage[i] = (byte)((bytes[b] >> 2) & 0x3f);
            //System.out.printf("0x%02x\n", storage[i]);
            if (i+1 < achars && b + 1 < slots) {
                storage[i + 1] = (byte) (((bytes[b] << 4) & 0x30) | ((bytes[b + 1] >> 4) & 0x0f));
                //System.out.printf("0x%02x\n", storage[i+1]);
                if (i+2 < achars && b + 2 < slots) {
                    storage[i + 2] = (byte) (((bytes[b + 1] << 2) & 0x3c) | ((bytes[b + 2] >> 6) & 0x03));
                    //System.out.printf("0x%02x\n", storage[i+2]);
                    if (i+3 < achars) {
                        storage[i + 3] = (byte) (bytes[b + 2] & 0x3f);
                        //System.out.printf("0x%02x\n", storage[i+3]);
                    }
                }
            }
        }
        //System.out.println(storage);
    }
    
    public av1String(String theMessage){
    	count = theMessage.length();
        while (count % 4 != 0){
            count++;
        }
    	while(theMessage.length() != count){
    		theMessage += " ";
    	}
    	storage = new byte[count];
    	for (int i = 0; i < count; i++){
    		storage[i] = av1ReverseEncoding[((int)theMessage.charAt(i))-0x20];
    	}
    }

    public byte[] packed(){
    	int pos = (count * 3) / 4;
    	if (pos % 4 != 0){
    		pos++;
    	}
    	System.out.println(pos);
    	byte[] arr = new byte[pos];
    	
    	for (int i = 0, k = 0; k < pos - 3; i+=4, k+=3){
    		arr[k] = (byte)(((storage[i] << 2) & 0xfc) | ((storage[i + 1] >> 4 & 0x03)));
    		//System.out.printf("0x%02x\n", arr[k]);
    		if (i+2 < count) {
    			arr[k + 1] = (byte)(((storage[i + 1] << 4) & 0xf0) | ((storage[i + 2] >> 2 & 0x0f)));
    			//System.out.printf("0x%02x\n", arr[k+1]);
                if (i+3 < count) {
                	arr[k + 2] = (byte)(((storage[i + 2] << 6) & 0xc0) | ((storage[i + 3] & 0x3f)));
                	//System.out.printf("0x%02x\n", arr[k+2]);
                }
            }
    	}
    	return arr;
    }

    public String toString(){

        StringBuilder s = new StringBuilder();
        for (int i = 0; i < count; i++){
            s.append((char)(av1encoding[storage[i]]));
        }
        return s.toString();

    }
}
