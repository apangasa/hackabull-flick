package com.example.flick;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class PreferencesActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_preferences);


        // Capture our button from layout
        Button next = (Button)findViewById(R.id.next);

        // Register the onClick listener with the implementation above
        next.setOnClickListener(nextListener);

    }

    // Create an anonymous implementation of OnClickListener
    private View.OnClickListener nextListener = new View.OnClickListener() {
        public void onClick(View v) {
                Intent intent = new Intent(PreferencesActivity.this, MainActivity.class);
                startActivity(intent);
                finish();
        }
    };

}