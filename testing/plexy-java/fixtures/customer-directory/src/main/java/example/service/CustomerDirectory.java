package example.service;

import example.model.Customer;
import java.util.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.io.IOException;

public class CustomerDirectory {
    private final Map customers;

    public CustomerDirectory(Map customers) {
        this.customers = customers;
    }

    public Customer findById(String id) {
        return (Customer) customers.get(id);
    }

    public List displayNames() {
        List<String> names = new ArrayList<>();
        for (Object value : customers.values()) {
            Customer customer = (Customer) value;
            names.add(String.format("%s (%s)", customer.getName(), customer.getId()));
        }
        return names.stream().sorted().toList();
    }

    public void load(Path path) throws IOException {
        try {
            List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);
            for (String line : lines) {
                String[] parts = line.split(",", 2);
                customers.put(parts[0], new Customer(parts[0], parts[1]));
            }
        } catch (IOException ignored) {
        }
    }
}