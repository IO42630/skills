import example.model.Customer;
import example.service.CustomerDirectory;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.List;
import java.util.Optional;

public class BehaviorCheck {
    private static Customer customer(String id, String name) throws Exception {
        try {
            var constructor = Customer.class.getDeclaredConstructor(String.class, String.class);
            constructor.setAccessible(true);
            return constructor.newInstance(id, name);
        } catch (NoSuchMethodException missing) {
            var constructor = Customer.class.getDeclaredConstructor();
            constructor.setAccessible(true);
            var result = constructor.newInstance();
            result.setId(id);
            result.setName(name);
            return result;
        }
    }

    private static Object unwrap(Object value) {
        return value instanceof Optional<?> optional ? optional.orElse(null) : value;
    }

    private static void check(boolean condition, String description) {
        if (!condition) {
            throw new AssertionError(description);
        }
    }

    public static void main(String[] args) throws Exception {
        var customers = new HashMap<String, Customer>();
        var directory = new CustomerDirectory(customers);
        switch (args[0]) {
            case "core" -> {
                check(directory.displayNames().isEmpty(), "empty display list");
                check(unwrap(directory.findById("absent")) == null, "absent lookup");
                var alice = customer("a", "Alice");
                alice.setName("Alicia");
                check(alice.getName().equals("Alicia"), "mutable name");
                alice.setName("Alice");
                alice.setId("changed");
                check(alice.getId().equals("changed"), "mutable id");
                alice.setId("a");
                customers.put("b", customer("b", "Bob"));
                customers.put("a", alice);
                check(unwrap(directory.findById("a")) == alice, "supplied map remains live");
                check(directory.displayNames().equals(List.of("Alice (a)", "Bob (b)")), "sorted displays");
                var csv = Files.createTempFile("customers-", ".csv");
                try {
                    Files.writeString(csv, "c,Zoë\nb,Bobby\n", StandardCharsets.UTF_8);
                    directory.load(csv);
                    check(customers.size() == 3, "load inserts and replaces in supplied map");
                    check(customers.get("c").getName().equals("Zoë"), "UTF-8 name");
                    check(customers.get("b").getName().equals("Bobby"), "replacement name");
                    check(directory.displayNames().equals(List.of("Alice (a)", "Bobby (b)", "Zoë (c)")), "loaded displays");
                } finally {
                    Files.deleteIfExists(csv);
                }
            }
            case "null" -> {
                try {
                    new CustomerDirectory(null);
                    throw new AssertionError("null map accepted by constructor");
                } catch (NullPointerException expected) {
                    // Required map must fail at construction, not later use.
                }
            }
            case "io" -> {
                var missing = Files.createTempFile("missing-customers-", ".csv");
                Files.delete(missing);
                try {
                    directory.load(missing);
                    throw new AssertionError("missing-file IOException swallowed");
                } catch (IOException expected) {
                    // Preserve the declared file-read error contract.
                }
            }
            case "optional" -> {
                var method = CustomerDirectory.class.getMethod("findById", String.class);
                check(method.getGenericReturnType().getTypeName().equals("java.util.Optional<example.model.Customer>"), "typed Optional return");
                Object absent = directory.findById("missing");
                check(absent instanceof Optional<?> optional && optional.isEmpty(), "Optional.empty for absence");
                var alice = customer("a", "Alice");
                customers.put("a", alice);
                Object present = directory.findById("a");
                check(present instanceof Optional<?> optional && optional.orElse(null) == alice, "Optional customer for presence");
            }
            default -> throw new IllegalArgumentException(args[0]);
        }
        System.out.println("PASS " + args[0]);
    }
}