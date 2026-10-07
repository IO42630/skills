package example.service;

import example.model.Customer;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
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
        List<String> names = new ArrayList<>();
        for (Customer customer : customers.values()) {
            names.add(String.format("%s (%s)", customer.getName(), customer.getId()));
        }
        return names.stream().sorted().toList();
    }

    public void load(Path path) throws IOException {
        List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);
        for (int index = 0; index < lines.size(); index++) {
            Customer customer = parseCustomer(lines.get(index), index + 1);
            customers.put(customer.getId(), customer);
        }
    }

    private static Customer parseCustomer(String line, int lineNumber) throws IOException {
        String[] parts = line.split(",", 2);
        if (parts.length != 2) {
            throw new IOException("Invalid customer CSV at line " + lineNumber + ": expected id,name");
        }
        try {
            return new Customer(parts[0], parts[1]);
        } catch (IllegalArgumentException exception) {
            throw new IOException("Invalid customer CSV at line " + lineNumber + ": "
                    + exception.getMessage(), exception);
        }
    }
}