using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPLeftImageReceive : MonoBehaviour
{

    // receiving Thread
    Thread receiveThread;

    // udpclient object
    UdpClient client;

    // public
    // Port 5005 is for the RIGHT Camera!
    // Port 5006 is for the LEFT Camera!
    public string IP; //default local
    public int port; // define > init

    string img_str;
    byte[] img = new Byte[65536];
    Texture2D texture;

    // start from unity3d
    public void Start()
    {
        texture = new Texture2D(2, 2);
        init();
        GetComponent<Renderer>().material.mainTexture = texture;
        
    }

    void Update()
    {
        texture.LoadImage(img);
    }

    // init
    private void init()
    {    
        receiveThread = new Thread(
            new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();

    }

    // receive thread
    private void ReceiveData()
    {
        client = new UdpClient(port);
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);

                img = Convert.FromBase64String(Encoding.UTF8.GetString(data));
            }
            catch (Exception err)
            {
                print(err.ToString());
            }
        }
    }
}