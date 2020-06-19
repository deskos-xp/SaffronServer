package com.example.saffronexplorer;

import android.content.Intent;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.gson.Gson;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.util.ArrayList;

import entities.Address;
import entities.Brand;
import entities.Manufacturer;
import entities.Vendor;

public class VBM_View extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_v_b_m__view);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        //Object item;
        String type=getIntent().getStringExtra("type");
        String cap=String.valueOf(type.toCharArray()[0]).toUpperCase();
        int count=0;
        for ( char x : type.toCharArray()){
            if (count > 0){
                cap+=String.valueOf(x);
            }
            count+=1;
        }
        getSupportActionBar().setTitle(cap);
        String name_str="";
        String id_str="";
        String phone_str="";
        String email_str="";
        String comment_str="";
        ArrayList<Address> addr = null;
        switch (type){
            case "vendor":
                Vendor item_vendor =(Vendor) new Gson().fromJson( getIntent().getStringExtra("item"), Vendor.class);
                if (item_vendor != null) {
                    name_str = item_vendor.getName();
                    id_str = String.valueOf(item_vendor.getId());
                    phone_str = item_vendor.getPhone();
                    email_str = item_vendor.getEmail();
                    comment_str = item_vendor.getComment();
                    addr=item_vendor.getAddress();
                }
                break;
            case "brand":
                Brand item_brand=(Brand) new Gson().fromJson(getIntent().getStringExtra("item"), Brand.class);
                if (item_brand != null) {
                    name_str = item_brand.getName();
                    id_str = String.valueOf(item_brand.getId());
                    phone_str = item_brand.getPhone();
                    email_str = item_brand.getEmail();
                    comment_str = item_brand.getComment();
                    addr=item_brand.getAddress();
                }
                break;
            case "manufacturer":
                Manufacturer item_manufacturer=(Manufacturer) new Gson().fromJson(getIntent().getStringExtra("item"), Manufacturer.class);
                if (item_manufacturer != null) {
                    name_str = item_manufacturer.getName();
                    id_str = String.valueOf(item_manufacturer.getId());
                    phone_str = item_manufacturer.getPhone();
                    email_str = item_manufacturer.getEmail();
                    comment_str = item_manufacturer.getComment();
                    addr=item_manufacturer.getAddress();
                }
                break;
            default:
                break;
        }
        final ArrayList<Address> addrF=addr;
        Button address = findViewById(R.id.address);
        address.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (addrF != null) {
                    String addr_Str = new Gson().toJson(addrF);
                    Intent intent = new Intent(getBaseContext(),A_View.class);
                    intent.putExtra("user",getIntent().getStringExtra("user"));
                    intent.putExtra("host",getIntent().getStringExtra("host"));
                    intent.putExtra("item",addr_Str);
                    intent.putExtra("type","address");
                    startActivity(intent);
                }
            }
        });
        TextView name = findViewById(R.id.name);
        name.setText(name_str);
        TextView id = findViewById(R.id.id);
        id.setText(id_str);
        TextView phone = findViewById(R.id.phone);
        phone.setText(phone_str);
        TextView email = findViewById(R.id.email);
        email.setText(email_str);
        TextView comment = findViewById(R.id.comment);
        comment.setText(comment_str);

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
