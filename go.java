import java.util.Scanner;

public class go {

    public static void gobackn(int fs, int ws) {
        int i, m = 0, j = 0, ack = 0;
        int[] window = new int[ws];
        int[] frame = new int[fs];

        // frames
        for (i = 0; i < fs; i++) {
            frame[i] = i + 1;
        }

        Scanner sc = new Scanner(System.in);

        while (j < fs) {
            // window
            for (i = 0; i < ws && (j + i) < fs; i++) {
                System.out.println("Sent frame: " + frame[j + i]);
                ack++;
                window[i] = frame[j + i];
            }

            System.out.print("Enter frame number with error (or 99 to exit): ");
            m = sc.nextInt();

            if (m == 99) {
                if (j >= fs) {
                    System.out.println("All frames are transmitted");
                    System.out.println("Total number of transmissions: " + ack);
                    break;
                } else {
                    System.out.println("Not all frames are transmitted, Continuing: ");
                    m = 0;  
                }
            }

            boolean errorOccurred = false;

            // Retransmit
            for (i = 0; i < ws && (j + i) < fs; i++) {
                if (window[i] == m) {
                    System.out.println("Frame " + m + " not received, retransmitting window");
                    errorOccurred = true;
                    break;
                } else {
                    System.out.println("Acknowledgement received for frame: " + window[i]);
                }
            }

            // Set j to error index
            if (errorOccurred) {
                j += i; // Retransmit from error frame
            } else {
                j += ws; // next window
            }

            System.out.println();
        }

        // Ensure that if the loop exits, the transmission is complete
        if (j >= fs) {
            System.out.println("All frames transmitted successfully.");
            System.out.println("Total number of transmissions: " + ack);
        }
        
        sc.close();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter the frame size: ");
        int fs = sc.nextInt();
        System.out.print("Enter the window size: ");
        int ws = sc.nextInt();
        gobackn(fs, ws);
        sc.close();
    }
}
