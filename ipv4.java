import java.util.Scanner;

public class ipv4subnetcalc {
   public static void main(String[] args) {
       Scanner sc = new Scanner(System.in);

       System.out.println("Enter an IP Address (in the format x.x.x.x): ");
       String IP = sc.next();

       // Validate the IP address format
       if (!IP.matches("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}")) {
           System.out.println("IP address " + IP + " is invalid");
           sc.close();
           return;
       }

       String[] octets = IP.split("\\.");
       int firstOctet = Integer.parseInt(octets[0]);

       String ipClass;
       String netMask;
       int totalAddresses;

       // Determine the IP class and default subnet mask
       if (firstOctet >= 1 && firstOctet <= 126) {
           ipClass = "A";
           netMask = "255.0.0.0";
           totalAddresses = 256 * 256 * 256;
       } else if (firstOctet >= 128 && firstOctet <= 191) {
           ipClass = "B";
           netMask = "255.255.0.0";
           totalAddresses = 256 * 256;
       } else if (firstOctet >= 192 && firstOctet <= 223) {
           ipClass = "C";
           netMask = "255.255.255.0";
           totalAddresses = 256;
       } else if (firstOctet >= 224 && firstOctet <= 239) {
           ipClass = "D (Multicast)";
           System.out.println("IP address " + IP + " is a multicast address (Class D)");
           sc.close();
           return;
       } else if (firstOctet >= 240 && firstOctet <= 255) {
           ipClass = "E (Reserved)";
           System.out.println("IP address " + IP + " is reserved (Class E)");
           sc.close();
           return;
       } else {
           System.out.println("IP address " + IP + " is invalid");
           sc.close();
           return;
       }

       System.out.println("The IP address " + IP + " belongs to class " + ipClass);
       System.out.println("Default Netmask: " + netMask);
       System.out.println("Total no. of IP addresses possible: " + totalAddresses);

       System.out.println("Enter the number of subnets (power of 2): ");
       int subnets = sc.nextInt();

       // Check if the number of subnets is a power of 2
       if (subnets == 0 || (subnets & (subnets - 1)) != 0) {
           System.out.println("Number of subnets is not a power of 2");
           sc.close();
           return;
       }

       // Subnet calculation
       int subnetBits = (int) (Math.log(subnets) / Math.log(2));
       int newMaskBits = subnetBits + (ipClass.equals("A") ? 8 : ipClass.equals("B") ? 16 : 24);
       String newMask = calculateSubnetMask(newMaskBits);

       int hostsPerSubnet = (int) Math.pow(2, 32 - newMaskBits) - 2;

       System.out.println("New subnet mask: " + newMask);
       System.out.println("Number of subnets: " + subnets);
       System.out.println("Hosts per subnet: " + hostsPerSubnet);

       // Display each subnet range (simplified, assumes classful addressing)
       displaySubnets(IP, subnets, hostsPerSubnet);

       sc.close();
   }

   // Function to calculate subnet mask from CIDR bits
   private static String calculateSubnetMask(int maskBits) {
       int mask = 0xffffffff << (32 - maskBits);
       return String.format("%d.%d.%d.%d",
               (mask >>> 24) & 0xff,
               (mask >>> 16) & 0xff,
               (mask >>> 8) & 0xff,
               mask & 0xff);
   }

   // Function to display each subnet address range
   private static void displaySubnets(String IP, int subnets, int hostsPerSubnet) {
       String[] octets = IP.split("\\.");
       int baseAddress = (Integer.parseInt(octets[0]) << 24) |
               (Integer.parseInt(octets[1]) << 16) |
               (Integer.parseInt(octets[2]) << 8) |
               Integer.parseInt(octets[3]);

       for (int i = 0; i < subnets; i++) {
           int subnetAddress = baseAddress + (i * (hostsPerSubnet + 2));
           int broadcastAddress = subnetAddress + hostsPerSubnet + 1;

           System.out.println("\nSubnet " + i + ":");
           System.out.println("Subnet Address: " + intToIp(subnetAddress));
           System.out.println("Broadcast Address: " + intToIp(broadcastAddress));
           System.out.println("Valid host range: " + intToIp(subnetAddress + 1) + " - " + intToIp(broadcastAddress - 1));
       }
   }

   // Helper function to convert integer to IP address string
   private static String intToIp(int ip) {
       return String.format("%d.%d.%d.%d",
               (ip >>> 24) & 0xff,
               (ip >>> 16) & 0xff,
               (ip >>> 8) & 0xff,
               ip & 0xff);
   }
}
