package com.example.saffronexplorer.Picasso;

import android.content.Context;

import com.example.saffronexplorer.Interceptor.BasicAuthInterceptor;

import com.jakewharton.picasso.OkHttp3Downloader;
import com.squareup.picasso.Picasso;

import okhttp3.OkHttpClient;


public abstract class PicassoGet {
    public static Picasso getPicasso(Context context,String username,String password) {
        Picasso.Builder builder = new Picasso.Builder(context);

        OkHttpClient client = new OkHttpClient();
        client.networkInterceptors().add(new BasicAuthInterceptor(username,password));

        OkHttp3Downloader downloader = new OkHttp3Downloader(client);

        return builder.downloader(downloader).build();
    }
}
