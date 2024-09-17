package com.example.spamdetection;

import android.view.View;

public class Button {
    private View.OnClickListener onClicklistener;

    public void setOnClicklistener(View.OnClickListener onClicklistener) {
        this.onClicklistener = onClicklistener;
    }
}
