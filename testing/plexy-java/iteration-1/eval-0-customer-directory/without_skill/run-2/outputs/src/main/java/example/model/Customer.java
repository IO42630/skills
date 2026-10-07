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

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (other == null || getClass() != other.getClass()) {
            return false;
        }
        Customer customer = (Customer) other;
        return id.equals(customer.id) && name.equals(customer.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name);
    }

    @Override
    public String toString() {
        return "Customer{id='" + id + "', name='" + name + "'}";
    }

    private static String requireNonBlank(String value, String field) {
        Objects.requireNonNull(value, field + " must not be null");
        if (value.isBlank()) {
            throw new IllegalArgumentException(field + " must not be blank");
        }
        return value;
    }
}