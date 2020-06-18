package com.example.saffronexplorer;

import android.os.Bundle;

import com.google.android.material.appbar.CollapsingToolbarLayout;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.gson.Gson;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.widget.TextView;

import entities.Department;

public class D_View extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_d__view);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        CollapsingToolbarLayout toolBarLayout = (CollapsingToolbarLayout) findViewById(R.id.toolbar_layout);
        toolBarLayout.setTitle("Department");

        String departmentStr = getIntent().getStringExtra("item");
        Department department = new Gson().fromJson(departmentStr,Department.class);

        TextView id=findViewById(R.id.id);
        TextView name=findViewById(R.id.name);
        TextView store_department_number=findViewById(R.id.store_department_number);
        TextView comment=findViewById(R.id.comment);

        if (department != null){
            id.setText(String.valueOf(department.getId()));
            name.setText(department.getName());
            store_department_number.setText(String.valueOf(department.getStore_department_number()));
            comment.setText(department.getComment());
        }

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, String.valueOf(departmentStr), Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
    }
}