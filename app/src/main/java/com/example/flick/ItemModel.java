package com.example.flick;

public class ItemModel {
    private int image;
    private String name, rating, description;

    public ItemModel () {
    }

    public ItemModel(int image, String name, String rating, String description) {
        this.image = image;
        this.name = name;
        this.rating = rating;
        this.description = description;
    }

    public int getImage() {
        return image;
    }

    public String getName() {
        return name;
    }

    public String getRating() {
        return rating;
    }

    public String getDescription() {
        return description;
    }
}
