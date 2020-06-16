package com.example.saffronexplorer;

import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.gson.Gson;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import entities.Product;

public class ResultView extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result_view);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        Product product_data=new Gson().fromJson(getIntent().getStringExtra("product"),Product.class);

        TextView name = findViewById(R.id.name);
        name.setText(product_data.getName());

        TextView id = findViewById(R.id.id);
        id.setText(String.valueOf(product_data.getId()));

        TextView price = findViewById(R.id.price);
        String priceString = String.format("%s %.2f",product_data.getPriceUnit(),product_data.getPrice());
        price.setText(priceString);

        TextView weight = findViewById(R.id.weight);
        String weightString=String.format("%.2f %s",product_data.getWeight(),product_data.getWeightUnit());
        weight.setText(weightString);

        TextView homecode = findViewById(R.id.homecode);
        homecode.setText(product_data.getHome_code());


        //more work will be done here, each needs a new activity
        Button upc = findViewById(R.id.upc);
        Button departments = findViewById(R.id.departments);
        Button vendor = findViewById(R.id.vendors);
        Button brand = findViewById(R.id.brands);
        Button Manufacturer = findViewById(R.id.manufacturers);

        ImageView product_img = findViewById(R.id.product_image);
        ImageView upc_img = findViewById(R.id.upc_image);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view,getIntent().getStringExtra("product"), Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
    }
}
