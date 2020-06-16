package com.example.saffronexplorer;

import android.os.Bundle;

import com.example.saffronexplorer.ProductResults.ResultClass;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.gson.Gson;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

import entities.Product;
import entities.Status;

public class ProductSearchResults extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_product_search_results);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        EditText page = findViewById(R.id.page);
        page.setText(String.valueOf(getIntent().getIntExtra("page", 0)));
        EditText limit = findViewById(R.id.limit);
        limit.setText(String.valueOf(getIntent().getIntExtra("limit", 10)));

        Button home = findViewById(R.id.Home);
        home.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        this.resultsBuilder();
    }
    public void resultsBuilder(){
        Status x=new Gson().fromJson(getIntent().getStringExtra("results"), Status.class);
        System.out.println(new Gson().toJson(x));
        TableLayout table=findViewById(R.id.resultTable);
        //table.

        //table.addView(res);

        ArrayList<ResultClass> results = new ArrayList<ResultClass>();
        for (Object xx : x.getObjects()){
            if (x.getStatus().equals("invalid_id")) {
                //Product p=new Gson().fromJson(new Gson().toJson(xx), Product.class);
                break;
            }
            System.out.println(new Gson().toJson(xx));
            Map m=new Gson().fromJson(new Gson().toJson(xx),Map.class);
            Log.v("result",new Gson().toJson(xx));
            Log.v("result_name",String.valueOf(m.get("name")));
            Product product = new Gson().fromJson(new Gson().toJson(xx),Product.class);
            View res=LayoutInflater.from(this).inflate(R.layout.content_product_search_result,table,false);
            ResultClass resultClass=new ResultClass(product,table,res,getApplicationContext(),getIntent());
            results.add(resultClass);

            //ArrayList<ResultClass> contains reference to table,contains table row,contains table data for the item
        }

    }
}
