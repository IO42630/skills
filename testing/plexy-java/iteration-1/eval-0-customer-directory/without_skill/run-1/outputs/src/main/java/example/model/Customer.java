package example.model;

import java.util.Objects;

public class Customer {
    private String id;
    private String name;

    public Customer(String id, String name) {
        this.id = requireText(id, "id");
        this.name = requireText(name, "name");
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = requireText(id, "id");
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = requireText(name, "name");
    }

    private static String requireText(String value, String field) {
        Objects.requireNonNull(value, field + " must not be null");
        if (value.isBlank()) {
            throw new IllegalArgumentException(field + " must not be blank");
        }
        return value;
    }
}