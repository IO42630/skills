package example.model;

import lombok.Data;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@Data
@RequiredArgsConstructor
public class Customer {
    @NonNull
    private String id;

    @NonNull
    private String name;
}