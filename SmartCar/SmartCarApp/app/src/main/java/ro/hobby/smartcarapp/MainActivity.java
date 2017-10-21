package ro.hobby.smartcarapp;

import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.SeekBar;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends AppCompatActivity {
    private Timer timer;
    private Handler handler = new Handler();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

    }

    public void connect(View v)
    {
        timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                String ip = ((EditText)findViewById(R.id.editTextIP)).getText().toString();

                float speed = ((SeekBar)findViewById(R.id.seekBarSpeed)).getProgress() / 50.0f - 1.0f;
                float balance = ((SeekBar)findViewById(R.id.seekBarBalance)).getProgress() / 50.0f - 1.0f;
                if(Math.abs(speed) < 0.2)
                    speed = 0;

                try {
                    URL url = new URL("http://" + ip + "/control?speed=" + speed + "&balance=" + balance);
                    HttpURLConnection urlConnection = (HttpURLConnection)url.openConnection();
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
        }, 0, 1000);

        ((Button)findViewById(R.id.buttonConnect)).setEnabled(false);
        ((Button)findViewById(R.id.buttonDisconnect)).setEnabled(true);

    }

    public void disconnect(View v)
    {
        timer.cancel();
        ((Button)findViewById(R.id.buttonConnect)).setEnabled(true);
        ((Button)findViewById(R.id.buttonDisconnect)).setEnabled(false);
    }

}
