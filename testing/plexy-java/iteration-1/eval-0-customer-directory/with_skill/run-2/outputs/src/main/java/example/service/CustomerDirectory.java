package example.service;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

import lombok.NonNull;
import lombok.RequiredArgsConstructor;

import example.model.Customer;

@RequiredArgsConstructor
public class CustomerDirectory {
    @NonNull
    private final Map<String, Customer> customers;

    public Optional<Customer> findById(String id) {
        return Optional.ofNullable(customers.get(id));
    }

    public List<String> displayNames() {
        return customers
            .values()
            .stream()
            .map(customer -> customer.getName() + " (" + customer.getId() + ")")
            .sorted()
            .toList();
    }

    public void load(Path path) throws IOException {
        var lines = Files.readAllLines(
            Objects.requireNonNull(path),
            StandardCharsets.UTF_8
        );
        var lineNumber = 0;
        for (var line : lines) {
            lineNumber++;
            var parts = line.split(
                ",",
                2
            );
            if (parts.length != 2) {
                throw new IOException(
                    "Invalid customer row " + lineNumber + ": expected id,name"
                );
            }
            var customer = new Customer(
                parts[0],
                parts[1]
            );
            customers.put(
                parts[0],
                customer
            );
        }
    }
}