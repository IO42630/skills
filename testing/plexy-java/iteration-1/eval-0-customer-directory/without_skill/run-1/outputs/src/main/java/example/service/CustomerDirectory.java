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
        Objects.requireNonNull(path, "path must not be null");
        List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);
        for (int index = 0; index < lines.size(); index++) {
            String line = lines.get(index);
            String[] parts = line.split(",", 2);
            if (parts.length != 2 || parts[0].isBlank() || parts[1].isBlank()) {
                throw new IOException("Invalid customer row at line " + (index + 1)
                        + " in " + path + ": expected non-blank id,name");
            }
            customers.put(parts[0], new Customer(parts[0], parts[1]));
        }
    }
}