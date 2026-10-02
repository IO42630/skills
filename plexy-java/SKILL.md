---
name: plexy-java
description: >
  When working on Java. 
  Keywords: java, maven, quarkus, spring
---

# Java Conventions

## Imports
- NEVER use wildcard imports (`import java.util.*` → `import java.util.List`)
- Sort imports: java/javax first, then third-party, then project-internal

## Code Style
- Use Lombok annotations: `@Data`, `@Builder`, `@Slf4j`, `@RequiredArgsConstructor` — not manual
  getters/setters/constructors
- Use `var` for local variables when the right-hand side makes the type obvious
- NEVER use raw types — always specify generic parameters
- NEVER catch and swallow exceptions silently

## Null Handling
- Use `Optional` for return types that may be absent, never return null from public methods
- Use `Objects.requireNonNull` for constructor parameters that must not be null

## Build
- NEVER add dependencies without checking if they already exist in pom.xml.

## Line Breaks
- Keep lines short.
- Method chaining: insert a newline before each chained method call. Put the dot on the new line.
- Function calls with multiple arguments: insert a newline after the opening parenthesis and before each argument
  and before the closing parenthesis.
