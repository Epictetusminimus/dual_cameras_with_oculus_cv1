using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPOculusRotationSend : MonoBehaviour
{
    private static int localPort;

    int rotInverted = 0;

    // Port 5007 for Oculus
    public string IP;  // define in init
    public int port;  // define in init

    // "connection" things
    IPEndPoint remoteEndPoint;
    UdpClient client;

    // gui
    string rotValues = "";

    // start from unity3d
    void Start()
    {
        init();
    }

    void Update()
    {
        float rotX, rotY, rotZ;

        // Inverts the rotation values before sending them.
        // Sometimes the Oculus Rift inverts its rotation values from nowhere.
        // This code tries to address this problem.
        if (Input.GetButton("space"))
        {
            if (rotInverted == 0)
            {
                rotInverted = 1;
            }
            else
            {
                rotInverted = 0;
            }
        }

        if (rotInverted == 0)
        {
            rotX = Camera.main.transform.rotation.x;
            rotY = Camera.main.transform.rotation.y;
            rotZ = Camera.main.transform.rotation.z;
        }
        else
        {
            rotX = -Camera.main.transform.rotation.x;
            rotY = -Camera.main.transform.rotation.y;
            rotZ = -Camera.main.transform.rotation.z;
        }


        rotValues = rotX.ToString() + " " + rotY.ToString() + " " + rotZ.ToString();

        print(rotValues);

        sendString(rotValues);
    }

    // init
    public void init()
    {
        remoteEndPoint = new IPEndPoint(IPAddress.Parse(IP), port);
        client = new UdpClient();
    }

    // sendData
    private void sendString(string message)
    {
        try
        {
            byte[] data = Encoding.UTF8.GetBytes(message);

            client.Send(data, data.Length, remoteEndPoint);
        }
        catch (Exception err)
        {
            print(err.ToString());
        }
    }
}