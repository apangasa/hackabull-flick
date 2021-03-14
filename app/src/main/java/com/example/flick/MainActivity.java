package com.example.flick;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DiffUtil;

import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.LinearInterpolator;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;


import com.yuyakaido.android.cardstackview.CardStackLayoutManager;
import com.yuyakaido.android.cardstackview.CardStackListener;
import com.yuyakaido.android.cardstackview.CardStackView;
import com.yuyakaido.android.cardstackview.Direction;
import com.yuyakaido.android.cardstackview.StackFrom;
import com.yuyakaido.android.cardstackview.SwipeableMethod;


import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import java.util.ArrayList;
import java.util.List;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    private TextView mTextViewResult;
    private static final String TAG = "MainActivity";
    private CardStackLayoutManager manager;
    private CardStackAdapter adapter;

    private static MainActivity Instance = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        requestData();

        Toast liked_toast = new Toast(this);
        ImageView view1 = new ImageView(this);
        view1.setImageResource(R.drawable.like_toast);
        liked_toast.setGravity(Gravity.TOP|Gravity.RIGHT, 5, 5);
        liked_toast.setView(view1);

        Toast disliked_toast = new Toast(this);
        ImageView view2 = new ImageView(this);
        view2.setImageResource(R.drawable.dislike_toast);
        disliked_toast.setGravity(Gravity.TOP|Gravity.LEFT, 5, 5);
        disliked_toast.setView(view2);


        CardStackView cardStackView = findViewById(R.id.card_stack_view);
        manager = new CardStackLayoutManager(this, new CardStackListener() {
            @Override
            public void onCardDragging(Direction direction, float ratio) {
                Log.d(TAG, "onCardDragging: d=" + direction.name() + " ratio=" + ratio);
            }

            @Override
            public void onCardSwiped(Direction direction) {
                Log.d(TAG, "onCardSwiped: p=" + manager.getTopPosition() + " d=" + direction);
                if (direction == Direction.Right){
                    liked_toast.show();
                }
                if (direction == Direction.Left){
                    disliked_toast.show();
                }
                if (direction == Direction.Top){
                    Toast.makeText(MainActivity.this, "Direction Top", Toast.LENGTH_SHORT).show();
                }
                if (direction == Direction.Bottom){
                    Toast.makeText(MainActivity.this, "Direction Bottom", Toast.LENGTH_SHORT).show();
                }

                // Paginating
                if (manager.getTopPosition() == adapter.getItemCount() - 5){
                    paginate();
                }

            }

            @Override
            public void onCardRewound() {
                Log.d(TAG, "onCardRewound: " + manager.getTopPosition());
            }

            @Override
            public void onCardCanceled() {
                Log.d(TAG, "onCardRewound: " + manager.getTopPosition());
            }

            @Override
            public void onCardAppeared(View view, int position) {
                TextView tv = view.findViewById(R.id.item_name);
                Log.d(TAG, "onCardAppeared: " + position + ", Name: " + tv.getText());
            }

            @Override
            public void onCardDisappeared(View view, int position) {
                TextView tv = view.findViewById(R.id.item_name);
                Log.d(TAG, "onCardAppeared: " + position + ", Name: " + tv.getText());
            }
        });
        manager.setStackFrom(StackFrom.None);
        manager.setVisibleCount(3);
        manager.setTranslationInterval(8.0f);
        manager.setScaleInterval(0.95f);
        manager.setSwipeThreshold(0.3f);
        manager.setMaxDegree(20.0f);
        manager.setDirections(Direction.FREEDOM);
        manager.setCanScrollHorizontal(true);
        manager.setSwipeableMethod(SwipeableMethod.Manual);
        manager.setOverlayInterpolator(new LinearInterpolator());
        adapter = new CardStackAdapter(addList());
        cardStackView.setLayoutManager(manager);
        cardStackView.setAdapter(adapter);
        cardStackView.setItemAnimator(new DefaultItemAnimator());

    }

    private void paginate() {
        List<ItemModel> old = adapter.getItems();
        List<ItemModel> new_item = new ArrayList<>(addList());
        CardStackCallback callback = new CardStackCallback(old, new_item);
        DiffUtil.DiffResult hasil = DiffUtil.calculateDiff(callback);
        adapter.setItems(new_item);
        hasil.dispatchUpdatesTo(adapter);
    }

    private List<ItemModel> addList() {
        List<ItemModel> items = new ArrayList<>();
        items.add(new ItemModel(R.drawable.twilight, "Twilight", "5.2/10", "When Bella Swan moves to a small town in the Pacific Northwest, she falls in love with Edward Cullen, a mysterious classmate who reveals himself to be a 108-year-old vampire."));
        items.add(new ItemModel(R.drawable.pacific_rim, "Pacific Rim", "6.9/10", "As a war between humankind and monstrous sea creatures wages on, a former pilot and a trainee are paired up to drive a seemingly obsolete special weapon in a desperate effort to save the world from the apocalypse."));
        items.add(new ItemModel(R.drawable.shrek, "Shrek", "7.8/10", "A mean lord exiles fairytale creatures to the swamp of a grumpy ogre, who must go on a quest and rescue a princess for the lord in order to get his land back."));;

        return items;
    }

    private void requestData() {

        mTextViewResult = findViewById(R.id.text_view_result);
        OkHttpClient client = new OkHttpClient();
        String url = "https://reqres.in/api/users?page=2";

        okhttp3.Request request = new okhttp3.Request.Builder().url(url).build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if(response.isSuccessful()) {
                    String myResponse = response.body().string();
                    //try {
                        //JSONObject jObject = new JSONObject(response.body().string());
                        //Toast.makeText(MainActivity.this, jObject.getString("page"), Toast.LENGTH_SHORT).show();
                    //} catch (JSONException e) {
                        //e.printStackTrace();
                    //}
                    //String myResponse = response.body().string();
                    MainActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mTextViewResult.setText(myResponse);
                        }
                    });
                }
            }
        });

    }

}