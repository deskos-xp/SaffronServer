package com.example.saffronexplorer;

import android.content.Intent;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.gson.Gson;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import java.util.HashMap;

import clients.Callable;
import clients.Client;
import entities.User;
import pages.ProductPages;

public class productSearch extends AppCompatActivity {
    private String fieldsToJson(View view){
        EditText name=findViewById(R.id.name);
        EditText homecode=findViewById(R.id.homecode);
        EditText upc=findViewById(R.id.upc);
        EditText ID=findViewById(R.id.id_row);
        HashMap toBe = new HashMap<>();
        if (!name.getText().toString().equals("")) {
            toBe.put("name", name.getText().toString());
        }
        if (!homecode.getText().toString().equals("")) {
            toBe.put("home_code", homecode.getText().toString());
        }
        if (!upc.getText().toString().equals("")) {
            toBe.put("upc", upc.getText().toString());
        }
        if (!ID.getText().toString().equals("")) {
            toBe.put("id", Integer.parseInt(ID.getText().toString()));
        }
        toBe.put("page",0);
        toBe.put("limit",55);
        return new Gson().toJson(toBe);
    }

    private void search(String json) throws Exception {
        Intent intent = getIntent();
        User u = new Gson().fromJson(intent.getStringExtra("user"),User.class);
        Client client = new Client();
        ProductPages productPages = (ProductPages) client.client(intent.getStringExtra("host"),u.getUname(),u.getPassword(),ProductPages.class);
        client.get(productPages.get_all(json), productPages, new Callable() {
            @Override
            public void call(Object o) {

            }

            @Override
            public void call() {

            }

            @Override
            public void call(Object o, Integer integer) {
                if (integer == 200){
                    String d=new Gson().toJson(o);
                    Intent i=new Intent(getBaseContext(),ProductSearchResults.class);
                    i.putExtra("user",getIntent().getStringExtra("user"));
                    i.putExtra("host",getIntent().getStringExtra("host"));
                    i.putExtra("results",d);
                    i.putExtra("page",0);
                    i.putExtra("limit",55);
                    startActivity(i);
                }
                Toast.makeText(getBaseContext(),String.valueOf(integer),Toast.LENGTH_SHORT).show();
            }
        });

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_product_search);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab_next);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //getIntent().getStringExtra("user")
                try {
                    search(fieldsToJson(view));
                } catch (Exception e) {
                    e.printStackTrace();
                }
                Snackbar.make(view,fieldsToJson(view) , Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
    }
}
