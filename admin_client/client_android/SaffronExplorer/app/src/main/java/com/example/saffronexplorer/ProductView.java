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
import android.widget.ImageView;
import android.widget.TextView;

import entities.Product;

public class ProductView extends AppCompatActivity {

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
        departments.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getBaseContext(),D_View.class);
                String user=getIntent().getStringExtra("user");
                String host=getIntent().getStringExtra("host");
                String departments=new Gson().toJson(product_data.getDepartments().get(0));

                intent.putExtra("user",user);
                intent.putExtra("host",host);
                intent.putExtra("item",departments);
                intent.putExtra("type","department");
                startActivity(intent);
            }
        });

        Button vendor = findViewById(R.id.vendors);
        vendor.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getBaseContext(),VBM_View.class);
                String user=getIntent().getStringExtra("user");
                String host=getIntent().getStringExtra("host");
                String vendors=new Gson().toJson(product_data.getVendors().get(0));
                //getIntent().getStringExtra()
                intent.putExtra("user",user);
                intent.putExtra("host",host);
                intent.putExtra("item",vendors);
                intent.putExtra("type","vendor");
                startActivity(intent);
            }
        });
        Button brand = findViewById(R.id.brands);
        brand.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getBaseContext(),VBM_View.class);
                String user=getIntent().getStringExtra("user");
                String host=getIntent().getStringExtra("host");
                String brands=new Gson().toJson(product_data.getBrands().get(0));
                //getIntent().getStringExtra()
                intent.putExtra("user",user);
                intent.putExtra("host",host);
                intent.putExtra("item",brands);
                intent.putExtra("type","brand");
                startActivity(intent);
            }
        });

        Button Manufacturer = findViewById(R.id.manufacturers);
        Manufacturer.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getBaseContext(),VBM_View.class);
                String user=getIntent().getStringExtra("user");
                String host=getIntent().getStringExtra("host");
                String manufacturers=new Gson().toJson(product_data.getManufacturers().get(0));
                //getIntent().getStringExtra()
                intent.putExtra("user",user);
                intent.putExtra("host",host);
                intent.putExtra("item",manufacturers);
                intent.putExtra("type","manufacturer");
                startActivity(intent);
            }
        });

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
