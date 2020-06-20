package com.example.saffronexplorer.Interceptor;

import android.os.Build;

import androidx.annotation.RequiresApi;

import java.io.IOException;

import okhttp3.Interceptor;
import okhttp3.Request;
import okhttp3.Response;
//import android.util.Base64;
import java.util.Base64;
import static android.util.Base64.NO_WRAP;

public class BasicAuthInterceptor implements Interceptor {
    String username;
    String password;

    public BasicAuthInterceptor(String username, String password) {
        this.username = username;
        this.password = password;
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    public Response intercept(Chain chain) throws IOException {

        String auth=java.util.Base64.getEncoder().encodeToString((username + ":" + password).getBytes());
        Request compressedRequest = chain.request().newBuilder()
                .header("Authorization", "Basic " + auth)
                .build();

        return chain.proceed(compressedRequest);
    }
}