package example.service;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

import example.model.Customer;

public class CustomerDirectory {
    private final Map<String, Customer> customers;

    public CustomerDirectory(Map<String, Customer> customers) {
        this.customers = Objects.requireNonNull(
            customers,
            "customers must not be null"
        );
    }

    public Optional<Customer> findById(String id) {
        return Optional.ofNullable(customers.get(id));
    }

    public List<String> displayNames() {
        return customers.values()
            .stream()
            .map(customer -> String.format(
                "%s (%s)",
                customer.getName(),
                customer.getId()
            ))
            .sorted()
            .toList();
    }

    public void load(Path path) throws IOException {
        var lines = Files.readAllLines(
            path,
            StandardCharsets.UTF_8
        );
        for (var line : lines) {
            var parts = line.split(
                ",",
                2
            );
            if (parts.length != 2) {
                throw new IOException("Invalid customer row: expected id,name");
            }
            customers.put(
                parts[0],
                new Customer(
                    parts[0],
                    parts[1]
                )
            );
        }
    }
}