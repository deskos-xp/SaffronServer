package com.example.saffronexplorer;

import android.os.Bundle;

import com.google.android.material.appbar.CollapsingToolbarLayout;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.gson.Gson;
import com.squareup.picasso.Picasso;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import com.example.saffronexplorer.Picasso.PicassoGet;

import entities.User;

public class UPC_View extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_u_p_c__view);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        CollapsingToolbarLayout toolBarLayout = (CollapsingToolbarLayout) findViewById(R.id.toolbar_layout);
        toolBarLayout.setTitle(getTitle());

        String upc_code = getIntent().getStringExtra("item");
        Integer product_id=getIntent().getIntExtra("product_id",-1);
        String host = getIntent().getStringExtra("host");

        String userStr=getIntent().getStringExtra("user");
        User user = new Gson().fromJson(userStr,User.class);
        String uname=user.getUname();
        String password=user.getPassword();

        TextView upc = findViewById(R.id.upc);
        upc.setText(upc_code);
        ImageView upc_image = findViewById(R.id.upc_image);

        String upcUri = String.format("%s/product/barcode/%d/ean13",host,product_id);
        //Picasso.with(getBaseContext()).load(upcUri)
        PicassoGet.getPicasso(this,uname,password).load(upcUri).into(upc_image);
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