package ro.hobby.smartcarapp;

import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.HttpURLConnection;
import java.net.SocketException;
import java.net.URL;
import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends AppCompatActivity {
    private Timer timer;
    private Handler handler = new Handler();
    private String ip;
    private static final String MAGIC = "smartcar";
    private DatagramSocket serverSocket;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        disconnect(null);
    }

    @Override
    protected void onPause() {
        super.onPause();
        disconnect(null);
    }

    public void connect(View v)
    {
        timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                if(ip == null)
                {
                    try {
                        if(serverSocket == null)
                        {
                            try {
                                serverSocket = new DatagramSocket(5000);
                                serverSocket.setBroadcast(true);
                                serverSocket.setSoTimeout(800);
                            } catch (Exception e) {
                                e.printStackTrace();
                                return;
                            }

                        }
                        byte[] receiveData = new byte[256];
                        DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                        serverSocket.receive(receivePacket);

                        String sentence = new String( receivePacket.getData());
                        if(sentence.startsWith(MAGIC))
                        {
                            ip = sentence.split(" ")[1] + ":8082";
                            handler.post(new Runnable() {
                                @Override
                                public void run() {
                                    TextView tv = (TextView)findViewById(R.id.textView2);
                                    tv.setText("Connected to: " + ip);
                                }
                            });
                        }

                    } catch (SocketException e) {
                        e.printStackTrace();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                }
                else {
                    float speed = ((SeekBar) findViewById(R.id.seekBarSpeed)).getProgress() / 50.0f - 1.0f;
                    float balance = ((SeekBar) findViewById(R.id.seekBarBalance)).getProgress() / 50.0f - 1.0f;
                    if (Math.abs(speed) < 0.2)
                        speed = 0;

                    try {
                        URL url = new URL("http://" + ip + "/control?speed=" + speed + "&balance=" + balance);
                        HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                        InputStream in = new BufferedInputStream(urlConnection.getInputStream());
                        in.read();
                        urlConnection.disconnect();
                    } catch (Exception e) {
                        e.printStackTrace();
                        handler.post(new Runnable() {
                            @Override
                            public void run() {
                                disconnect(null);
                            }
                        });
                    }
                }
            }
        }, 0, 1000);

        ((Button)findViewById(R.id.buttonConnect)).setEnabled(false);
        ((Button)findViewById(R.id.buttonDisconnect)).setEnabled(true);

    }

    public void disconnect(View v)
    {
        if(timer != null)
            timer.cancel();
        if(serverSocket != null)
        {
            serverSocket.disconnect();
            serverSocket.close();
            serverSocket = null;
        }

        ((Button)findViewById(R.id.buttonConnect)).setEnabled(true);
        ((Button)findViewById(R.id.buttonDisconnect)).setEnabled(false);

        TextView tv = (TextView)findViewById(R.id.textView2);
        tv.setText("Disconnected");
    }

}
