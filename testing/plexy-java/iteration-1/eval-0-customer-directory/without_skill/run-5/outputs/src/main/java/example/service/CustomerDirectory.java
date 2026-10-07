package example.service;

import example.model.Customer;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

public class CustomerDirectory {
    private final Map<String, Customer> customers;

    public CustomerDirectory(Map<String, Customer> customers) {
        this.customers = Objects.requireNonNull(customers, "customers must not be null");
    }

    public Optional<Customer> findById(String id) {
        return Optional.ofNullable(customers.get(id));
    }

    public List<String> displayNames() {
        return customers.values().stream()
                .map(customer -> String.format("%s (%s)", customer.getName(), customer.getId()))
                .sorted()
                .toList();
    }

    public void load(Path path) throws IOException {
        Objects.requireNonNull(path, "path must not be null");
        List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);
        for (int index = 0; index < lines.size(); index++) {
            String[] parts = lines.get(index).split(",", -1);
            if (parts.length != 2) {
                throw new IOException("Invalid customer CSV row " + (index + 1) + ": expected id,name");
            }
            Customer customer;
            try {
                customer = new Customer(parts[0], parts[1]);
            } catch (IllegalArgumentException exception) {
                throw new IOException("Invalid customer CSV row " + (index + 1) + ": "
                        + exception.getMessage(), exception);
            }
            customers.put(customer.getId(), customer);
        }
    }
}