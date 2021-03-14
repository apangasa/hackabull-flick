package com.example.flick;

import java.util.List;

import androidx.recyclerview.widget.DiffUtil;

public class CardStackCallback extends DiffUtil.Callback {

    private List<ItemModel> old_item, new_item;

    public CardStackCallback(List<ItemModel> old_item, List<ItemModel> new_item) {
        this.old_item = old_item;
        this.new_item = new_item;
    }

    @Override
    public int getOldListSize() {
        return old_item.size();
    }

    @Override
    public int getNewListSize() {
        return new_item.size();
    }

    @Override
    public boolean areItemsTheSame(int oldItemPosition, int newItemPosition) {
        return old_item.get(oldItemPosition).getImage() == new_item.get(newItemPosition).getImage();
    }

    @Override
    public boolean areContentsTheSame(int oldItemPosition, int newItemPosition) {
        return old_item.get(oldItemPosition) == new_item.get(newItemPosition);
    }
}
