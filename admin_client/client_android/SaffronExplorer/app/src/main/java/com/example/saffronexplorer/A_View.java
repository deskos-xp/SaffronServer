package com.example.saffronexplorer;

import android.os.Bundle;

import com.google.android.material.appbar.CollapsingToolbarLayout;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.gson.Gson;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.widget.TextView;

import java.util.ArrayList;

import entities.Address;
//to display addresses

public class A_View extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_a__view);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        CollapsingToolbarLayout toolBarLayout = (CollapsingToolbarLayout) findViewById(R.id.toolbar_layout);
        toolBarLayout.setTitle(getTitle());

        Address address =null;
        ArrayList<Address> addressArrayList = new Gson().fromJson(getIntent().getStringExtra("item"),ArrayList.class);
        if (addressArrayList != null){
            address = new Gson().fromJson(new Gson().toJson(addressArrayList.get(0)),Address.class);
        }

        TextView city = findViewById(R.id.city);
        TextView state=findViewById(R.id.state);
        TextView zip=findViewById(R.id.zip);
        TextView id=findViewById(R.id.id);
        TextView street_number=findViewById(R.id.street_number);
        TextView street_name=findViewById(R.id.street_name);
        TextView apartment_suite=findViewById(R.id.apartment_suite);

        if (address != null){
            city.setText(address.getCity());
            state.setText(address.getState());
            zip.setText(address.getZIP());
            id.setText(String.valueOf(address.getId()));
            street_number.setText(address.getStreet_number());
            street_name.setText(address.getStreet_name());
            apartment_suite.setText(address.getApartment_suite());
        }


        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
    }
}