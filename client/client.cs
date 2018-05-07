/** Based on the code from https://docs.microsoft.com/ru-ru/dotnet/framework/network-programming/synchronous-client-socket-example */

using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class SynchronousSocketClient {

    public static void StartClient() {
        // Data buffer for incoming data
        byte[] bytes = new byte[1024];

        // Connect to a remote device
        try {
            // Establish the remote endpoint for the socket

            String host = "ec2-54-89-217-31.compute-1.amazonaws.com";
            int    port = 8080;

            IPHostEntry ipHostInfo = Dns.GetHostEntry(host); //Dns.GetHostEntry(Dns.GetHostName());
            IPAddress   ipAddress  = ipHostInfo.AddressList[0]; //IPAddress.Parse("");
            IPEndPoint  remoteEP   = new IPEndPoint(ipAddress, port);

            // Create a TCP/IP socket
            Socket sender = new Socket(
                AddressFamily.InterNetwork, //ipAddress.AddressFamily,
                SocketType.Stream,
                ProtocolType.Tcp
            );

            // Connect the socket to the remote endpoint. Catch any errors
            try {
                sender.Connect(remoteEP); //sender.Connect(host, port);

                Console.WriteLine("Dare to talk!\n"); //sender.RemoteEndPoint.ToString());

                String message = "";

                while (message.ToLower() != "ciao!") {
                    Console.Write("> ");
                    message = Console.ReadLine();

                    // Encode the data string into a byte array
                    byte[] msg = Encoding.ASCII.GetBytes(message + "\n");

                    // Send the data through the socket
                    int bytesSent = sender.Send(msg);

                    // Receive the response from the remote device
                    int bytesRec = sender.Receive(bytes);
                    Console.WriteLine(
                        "> {0}", Encoding.ASCII.GetString(bytes, 0, bytesRec));
                }

                Console.Write("You finished the chat. Press any button to close the application...");
                Console.ReadKey();

                // Release the socket
                sender.Shutdown(SocketShutdown.Both);
                sender.Close();

            }
            catch (ArgumentNullException ane) {
                Console.WriteLine("ArgumentNullException : {0}", ane.ToString());
            }
            catch (SocketException se) {
                Console.WriteLine("SocketException : {0}", se.ToString());
            }
            catch (Exception e) {
                Console.WriteLine("Unexpected exception : {0}", e.ToString());
            }

        }
        catch (Exception e) {
            Console.WriteLine(e.ToString());
        }
    }

    public static int Main(String[] args) {
        StartClient();
        return 0;
    }
}
