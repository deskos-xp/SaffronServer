package com.example.saffronexplorer;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.gson.Gson;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import entities.Status;

public class loggedIn extends AppCompatActivity {
    public Context context;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_logged_in);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        context=this;

        final Intent intent_old= getIntent();

        Button search = findViewById(R.id.lookup);
        search.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent_new=new Intent(context,productSearch.class);
                intent_new.putExtra("user",intent_old.getStringExtra("user"));
                intent_new.putExtra("host",intent_old.getStringExtra("host"));
                startActivity(intent_new);
            }
        });
        //view.setText(intent.getStringExtra("user"));
        //Toast.makeText(this,intent_old.getStringExtra("user"),Toast.LENGTH_LONG).show();
    }
}
