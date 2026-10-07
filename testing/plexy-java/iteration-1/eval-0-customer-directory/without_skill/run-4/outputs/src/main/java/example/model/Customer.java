package example.model;

import java.util.Objects;

public class Customer {
    private String id;
    private String name;

    public Customer(String id, String name) {
        this.id = requireNonBlank(id, "id");
        this.name = requireNonBlank(name, "name");
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = requireNonBlank(id, "id");
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = requireNonBlank(name, "name");
    }

    private static String requireNonBlank(String value, String field) {
        Objects.requireNonNull(value, field + " must not be null");
        if (value.isBlank()) {
            throw new IllegalArgumentException(field + " must not be blank");
        }
        return value;
    }
}