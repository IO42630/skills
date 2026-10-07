package example.model;

import lombok.Data;
import lombok.NonNull;

@Data
public class Customer {
    @NonNull
    private String id;

    @NonNull
    private String name;
}