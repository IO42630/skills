package example.service;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
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
        var names = new ArrayList<String>();
        for (var customer : customers.values()) {
            names.add(customer.getName() + " (" + customer.getId() + ")");
        }
        return names.stream()
                .sorted()
                .toList();
    }

    public void load(Path path) throws IOException {
        var lines = Files.readAllLines(
                Objects.requireNonNull(path),
                StandardCharsets.UTF_8
        );
        for (var index = 0; index < lines.size(); index++) {
            var parts = lines.get(index)
                    .split(
                            ",",
                            2
                    );
            if (parts.length != 2) {
                throw new IOException("Expected id,name at line " + (index + 1));
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