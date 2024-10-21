import java.util.Scanner;

class crrc {

    
    static String Xor(String a, String b) {
        StringBuilder result = new StringBuilder();
        int n = b.length();

        
        for (int i = 1; i < n; i++) {
            if (a.charAt(i) == b.charAt(i))
                result.append("0");
            else
                result.append("1");
        }
        return result.toString();
    }

    
    static String Mod2Div(String dividend, String divisor) {
        int pick = divisor.length(); // Number of bits to be XORed at a time
        String tmp = dividend.substring(0, pick);
        int n = dividend.length();

        while (pick < n) {
            if (tmp.charAt(0) == '1')
                tmp = Xor(divisor, tmp) + dividend.charAt(pick);
            else
                tmp = Xor("0".repeat(pick), tmp) + dividend.charAt(pick);

            pick += 1;
        }

        
        if (tmp.charAt(0) == '1')
            tmp = Xor(divisor, tmp);
        else
            tmp = Xor("0".repeat(pick), tmp);

        return tmp;
    }

   
    static void EncodeData(String data, String key) {
        int l_key = key.length();
        String appended_data = data + "0".repeat(l_key - 1);
        String remainder = Mod2Div(appended_data, key);
        String codeword = data + remainder;

        System.out.println("Appended Data: " + appended_data);
        System.out.println("Remainder: " + remainder);
        System.out.println("Encoded Data (Data + Remainder): " + codeword);
    }

   
    static void Receiver(String data, String key) {
        String currxor = Mod2Div(data.substring(0, key.length()), key);
        int curr = key.length();

        while (curr < data.length()) {
            if (currxor.length() != key.length()) {
                currxor += data.charAt(curr++);
            } else {
                currxor = Mod2Div(currxor, key);
            }
        }

        if (currxor.length() == key.length()) {
            currxor = Mod2Div(currxor, key);
        }

        if (currxor.contains("1")) {
            System.out.println("There is some error in data");
        } else {
            System.out.println("Correct message received");
        }
    }

  
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter data (message):");
        String data = sc.nextLine();
        System.out.println("Enter key (divisor):");
        String key = sc.nextLine();

        System.out.println("\nSender side...");
        EncodeData(data, key);

        String encodedData = data + Mod2Div(data + "0".repeat(key.length() - 1), key);

        System.out.println("Receiver side...");
        Receiver(encodedData, key);

    }
}
