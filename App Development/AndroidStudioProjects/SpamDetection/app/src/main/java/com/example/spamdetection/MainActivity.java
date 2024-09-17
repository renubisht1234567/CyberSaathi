package com.example.spamdetection;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okhttp3.MediaType;
import org.json.JSONObject;

import java.io.IOException;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private Button predict;
    private EditText mail;
    private TextView result;
     String url = "http://127.0.2.2:5000/predict"; // Replace with your Flask API endpoint

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mail = findViewById(R.id.mail);
        predict = findViewById(R.id.predict);
        result = findViewById(R.id.result);

        predict.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String emailText = mail.getText().toString();
                // Call the API
                callApi(emailText);
            }
        });
    }

    private void callApi(String emailText) {
        OkHttpClient client = new OkHttpClient();

        // Create JSON payload
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("email_content", emailText); // Match the field name
        } catch (Exception e) {
            e.printStackTrace();
        }

        RequestBody body = RequestBody.create(
                jsonObject.toString(),
                MediaType.get("application/json; charset=utf-8")
        );

        Request request = new Request.Builder()
                .url("http://10.0.2.2:5000/predict") // Use the emulator address
                .post(body) // Ensure this is a POST request
                .addHeader("Content-Type", "application/json") // Add Content-Type header
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                runOnUiThread(() -> result.setText("Request failed: " + e.getMessage()));
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    final String responseData = response.body().string();

                    // Parse JSON and create a friendly message
                    try {
                        JSONObject jsonObject = new JSONObject(responseData);
                        boolean isSpam = jsonObject.getBoolean("is_spam");
                        double spamProbability = jsonObject.getDouble("spam_probability") * 100; // Convert to percentage

                        String message;
                        if (isSpam) {
                            message = "The email is SPAM with a probability of " + String.format("%.2f", spamProbability) + "%.";
                        } else {
                            message = "The email is NOT spam with a probability of " + String.format("%.2f", 100 - spamProbability) + "%.";
                        }

                        runOnUiThread(() -> result.setText(message));
                    } catch (Exception e) {
                        // Handle JSON parsing or any other exceptions
                        runOnUiThread(() -> result.setText("Error parsing response: " + e.getMessage()));
                    }
                } else {
                    runOnUiThread(() -> result.setText("Request failed with code: " + response.code()));
                }
            }
        });
    }
}
