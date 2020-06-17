package com.example.saffronexplorer.ProductResults;

import android.content.Context;
import android.content.Intent;
import android.view.View;
import android.widget.Button;
import android.widget.TableLayout;

import com.example.saffronexplorer.R;
import com.example.saffronexplorer.ProductView;
import com.google.gson.Gson;

import entities.Product;

public class ResultClass {
    //data
    private Product product;
    private TableLayout tableLayout;
    private View tableRow;

    public TableLayout getTableLayout() {
        return tableLayout;
    }

    public void setTableLayout(TableLayout tableLayout) {
        this.tableLayout = tableLayout;
    }

    public Product getProduct() {
        return product;
    }

    private Context context;
    private Intent intent;

    public void setProduct(Product product) {
        this.product = product;
    }
    public ResultClass(Product product, TableLayout tableLayout, View tableRow, Context context, Intent intent){
        setIntent(intent);
        setContext(context);
        setProduct(product);
        setTableLayout(tableLayout);
        setTableRow(tableRow);
        Button selection=getTableRow().findViewById(R.id.selection);
        selection.setText(getProduct().getName());
        selection.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent1 = new Intent(getContext(), ProductView.class);
                intent1.putExtra("user",intent.getStringExtra("user"));
                intent1.putExtra("host",intent.getStringExtra("host"));
                intent1.putExtra("product",new Gson().toJson(getProduct()));
                intent1.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                getContext().startActivity(intent1);
            }
        });
        getTableLayout().addView(getTableRow());
    }

    public Context getContext() {
        return context;
    }

    public void setContext(Context context) {
        this.context = context;
    }

    public View getTableRow() {
        return tableRow;
    }

    public void setTableRow(View tableRow) {
        this.tableRow = tableRow;
    }

    public Intent getIntent() {
        return intent;
    }

    public void setIntent(Intent intent) {
        this.intent = intent;
    }
}
