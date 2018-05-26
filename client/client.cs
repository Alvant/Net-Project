/** Based on the code from https://docs.microsoft.com/ru-ru/dotnet/framework/network-programming/synchronous-client-socket-example */

using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.IO;

using Newtonsoft.Json;

public class SynchronousSocketClient {

    public class Config {
        public string host;
        public string port;
    }

    public static bool IsSocketConnected(Socket s) { // https://stackoverflow.com/questions/2661764/how-to-check-if-a-socket-is-connected-disconnected-in-c // https://gist.github.com/Boushhh/6a579ea81326679bcafdce4291d0eb21
        return !((s.Poll(1000, SelectMode.SelectRead) && (s.Available == 0)) || !s.Connected);
    }

    public static void ByeClient() {
        Console.WriteLine("Press any button to close the application...");
        Console.ReadKey();
    }

    public static void StartClient() {
        if (!System.Net.NetworkInformation.NetworkInterface.GetIsNetworkAvailable()) {
            Console.WriteLine("No Internet connection");
            ByeClient();
        }

        // Data buffer for incoming data
        byte[] bytes = new byte[1024];

        // Connect to a remote device
        try {
            // Establish the remote endpoint for the socket

            string configJson = File.ReadAllText(@".\config.data");
            Config config = JsonConvert.DeserializeObject<Config>(configJson);

            String host = config.host;
            int port;

            if (!Int32.TryParse(config.port, out port)) {
                Console.WriteLine("Invalid port.");
                ByeClient();
                return;
            }

            IPHostEntry ipHostInfo = Dns.GetHostEntry(host); //Dns.GetHostEntry(Dns.GetHostName());
            IPAddress ipAddress = ipHostInfo.AddressList[0]; //IPAddress.Parse("");
            IPEndPoint remoteEP = new IPEndPoint(ipAddress, port);

            // Create a TCP/IP socket
            Socket sender = new Socket(
                AddressFamily.InterNetwork, //ipAddress.AddressFamily,
                SocketType.Stream,
                ProtocolType.Tcp
            );

            // Connect the socket to the remote endpoint. Catch any errors

            try {
                sender.Connect(remoteEP); //sender.Connect(host, port);
            }
            catch (Exception) {
                Console.WriteLine("Wrong host or port.");
                Console.WriteLine("See docs more closely on https://github.com/Alvant/Net-Project.");
                ByeClient();
                return;
            }

            try {
                Console.WriteLine("Dare to talk!\n"); //sender.RemoteEndPoint.ToString());

                String message = "";

                while (message.ToLower() != "ciao!") {
                    if (!IsSocketConnected(sender)) {
                        throw new SocketException();
                    }

                    Console.Write("> ");
                    message = Console.ReadLine();

                    // Encode the data string into a byte array
                    byte[] msg = Encoding.ASCII.GetBytes(message + "\n");

                    // Send the data through the socket
                    int bytesSent = sender.Send(msg);

                    // Receive the response from the remote device
                    int bytesRec = sender.Receive(bytes);
                    string answer = Encoding.ASCII.GetString(bytes, 0, bytesRec);

                    Console.WriteLine("> {0}", answer);
                }

                Console.Write("You finished the chat. Press any button to close the application...");
                Console.ReadKey();

                // Release the socket
                sender.Shutdown(SocketShutdown.Both);
                sender.Close();
            }
            catch (ArgumentNullException ane) {
                Console.WriteLine("ArgumentNullException : {0}", ane.ToString());
                ByeClient();
            }
            catch (SocketException se) {
                // Console.WriteLine("SocketException : {0}", se.ToString());
                Console.WriteLine("Socket closed.");
                ByeClient();
            }
            catch (Exception e) {
                Console.WriteLine("Unexpected exception : {0}", e.ToString());
                ByeClient();
            }

        }
        catch (Exception e) {
            Console.WriteLine(e.ToString());
            ByeClient();
        }
    }

    public static int Main(String[] args) {
        StartClient();
        return 0;
    }
}
