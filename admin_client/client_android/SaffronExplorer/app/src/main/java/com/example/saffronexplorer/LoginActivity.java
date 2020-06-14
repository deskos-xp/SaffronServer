package com.example.saffronexplorer;

import android.content.Intent;
import android.os.Build;
import android.os.Bundle;

import android.os.Parcel;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import com.google.gson.Gson;

import java.util.HashMap;

import clients.Callable;
import clients.Client;
import entities.Status;
import entities.User;
import pages.UserPages;
import retrofit2.Call;

public class LoginActivity extends AppCompatActivity {
    private HashMap makeDefaultAuth(){
        HashMap auth = new HashMap();
        auth.put("server_address","http://saffronexpressapi.ngrok.io");
        auth.put("uname","");
        auth.put("password","");
        return auth;
    }
    private HashMap auth;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        //Client client = new Client();
        this.auth=this.makeDefaultAuth();
        final EditText username = findViewById(R.id.username);
        final EditText password = findViewById(R.id.password);
        Button Login = findViewById(R.id.login);
        Login.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.M)
            @Override
            public void onClick(View v) {
                EditText uname=findViewById(R.id.username);
                EditText password=findViewById(R.id.password);
                auth.put("uname",uname.getText().toString());
                Client client = new Client();
                System.out.println(new Gson().toJson(auth));
                try {
                    HashMap u=new HashMap();
                    u.put("uname",username.getText().toString());
                    UserPages userPages = (UserPages) client.client((String)auth.get("server_address"),(String)auth.get("uname"),password.getText().toString(),UserPages.class);
                    client.get((Call) userPages.get_all(new Gson().toJson(u)), userPages, new Callable() {
                        @Override
                        public void call(Object o) {

                        }

                        @Override
                        public void call() {

                        }

                        @Override
                        public void call(Object o, Integer integer) {
                            if (integer == 200) {
                                System.out.println(new Gson().toJson(o));
                                auth.put("password",password.getText().toString());

                                Status stat = (Status) new Gson().fromJson(new Gson().toJson(o), Status.class);
                                User u= new Gson().fromJson(new Gson().toJson(stat.getObjects().get(0)),User.class);
                                u.setPassword(password.getText().toString());

                                Intent intent = new Intent(getBaseContext(),loggedIn.class);
                                intent.putExtra("user",new Gson().toJson(u));
                                intent.putExtra("host",(String)auth.get("server_address"));

                                startActivity(intent);
                            }
                        }
                    });
                } catch (Exception e) {

                }
            }
        });


    }
}
