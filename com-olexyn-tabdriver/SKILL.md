---
name: com-olexyn-tabdriver
description: >
  Use when integrating, wiring, or modifying the com.olexyn:tabdriver browser-automation library in a JVM/Java app 
  with any DI framework (Spring, Quarkus, or none) — shared TabDriver, config provider, Purpose tabs, TabDriverHolder, 
  session login handling. Triggers on TabDriver, tabdriver, chromedriver, TabDriverHolder, TabDriverConfigProvider, 
  Purpose, browser session.
---

# Integrating TabDriver

TabDriver (`com.olexyn:tabdriver`) is a thin wrapper around Selenium `ChromeDriver`
that adds named tabs (`Purpose`) and convenience finders. This skill describes how
to wire it into a Java application. The code is plain Java and does not depend on a
DI framework; register the classes below as application-scoped singletons in
whatever container you use (Spring `@Service`, Quarkus `@ApplicationScoped`/
`@Singleton`, or a hand-rolled singleton).

## 1. Dependency

Declare the version once in the parent `<dependencyManagement>` and depend on it
without a version in each module that talks to the browser:

```xml
<!-- root pom.xml -->
<dependency>
  <groupId>com.olexyn</groupId>
  <artifactId>tabdriver</artifactId>
  <version>1.5.1</version>
</dependency>

<!-- module pom.xml -->
<dependency>
  <groupId>com.olexyn</groupId>
  <artifactId>tabdriver</artifactId>
</dependency>
```

TabDriver pulls in Selenium; it is the only browser dependency you should need.

## 2. Implement the config provider

TabDriver needs a driver path, a download dir, a headless flag, and `ChromeOptions`.
Read them from your configuration source, never hardcode.

```java
public class AppTabDriverConfig implements TabDriverConfigProvider {

  private final Path driverPath;
  private final Path downloadDir;
  private final boolean headless;

  public AppTabDriverConfig(Path driverPath, Path downloadDir, boolean headless) {
    this.driverPath = driverPath;
    this.downloadDir = downloadDir;
    this.headless = headless;
  }

  @Override public Path getDriverPath() { return driverPath; }
  @Override public String getDownloadDir() { return downloadDir.toString(); }
  @Override public boolean isHeadless() { return headless; }

  @Override
  public ChromeOptions getOptions() {
    ChromeOptions options = new ChromeOptions();
    options.setCapability(CapabilityType.ACCEPT_INSECURE_CERTS, true);
    if (headless) {
      options.addArguments("--window-size=1920,1080");
      options.addArguments("--headless");
    } else {
      options.addArguments("--start-minimized");
      options.addArguments("--disable-blink-features=AutomationControlled");
      // ... focus-stealing / sandbox flags
    }
    HashMap<String, Object> prefs = new HashMap<>();
    prefs.put("download.default_directory", getDownloadDir());
    prefs.put("download.prompt_for_download", false);
    options.setExperimentalOption("prefs", prefs);
    return options;
  }
}
```

Adapt the constructor parameters to your config mechanism (properties file, env
vars, config framework). The three values are the only inputs TabDriver requires.

Notes:
- `TabDriver` builds a `ChromeDriverService` on any free port, so no port config
  is needed. It sets a 2s implicit wait itself.
- `getOptions()` on `TabDriverConfigProvider` is required; `DefaultTabDriverConfig`
  is available as an abstract fallback if you do not need custom flags.

## 3. Hold one shared TabDriver

There must be exactly one `TabDriver` per JVM. A holder creates it lazily on first
use under a private lock, and exposes an `Optional` for callers that must not
trigger creation. Register it as a singleton if your DI container manages
lifecycles.

```java
public class TabDriverHolder {

  private final TabDriverConfigProvider tdConfig;
  private TabDriver td = null;
  private final Object lock = new Object();

  public TabDriverHolder(TabDriverConfigProvider tdConfig) {
    this.tdConfig = tdConfig;
  }

  public TabDriver get() {
    synchronized (lock) {
      if (td == null) { td = new TabDriver(tdConfig); }
      return td;
    }
  }

  public Optional<TabDriver> getOpt() { return Optional.ofNullable(td); }
  public boolean isInit() { return td != null; }
}
```

Do not instantiate raw `WebDriver`/`ChromeDriver` anywhere else. Always obtain the
driver through this holder. In Quarkus an `@ApplicationScoped` bean is lazy through
its client proxy; in Spring declare the bean `@Lazy` or construct it by hand.

## 4. Name every tab with a Purpose

TabDriver tracks tabs in a `Map<windowHandle, Tab>` and switches by `Purpose`.
Wrap the enum once and reuse the `Purpose` instances (equality is by name):

```java
public enum TabPurpose {
  LOGIN, DOWNLOAD, OBSERVE, SUBMIT /* ... */;

  private static final Map<TabPurpose, Purpose> MAP = new HashMap<>();
  static {
    Arrays.stream(values()).forEach(tp -> MAP.put(tp, new Purpose(tp.name())));
  }
  public static Purpose getTabPurpose(TabPurpose tp) { return MAP.get(tp); }
}
```

Usage: `td.newTab(Purpose)` is idempotent per purpose (it no-ops if a tab with that
purpose exists), and `td.goToTab(Purpose)` switches to it. Always `newTab` then
`goToTab` if you need it active.

## 5. Synchronize all browser access on `td`

`TabDriver` methods are `synchronized` internally, but compound find-click sequences
are not atomic. Guard each sequence with `synchronized (td)`:

```java
synchronized (td) {
  td.goToTab(getTabPurpose(OBSERVE));
  WebElement row = td.findByCss("[data-id*='%s']".formatted(id)).orElseThrow();
  row.click();
}
```

Keep sections short — never hold `td` across a `sleep`, a network wait, or while
acquiring another lock. Do not acquire a second monitor while holding `td`.

## 6. Model sessions, not just tabs

For sites that require login, add a `Session` that knows how to detect liveness and
how to wait for a human to log in. It owns the `td` reference. The cancellation hook
below is any `BooleanSupplier` your app already has (job state, shutdown flag,
`AtomicBoolean`, etc.).

```java
public abstract class Session {
  public final TabDriver td;
  private volatile boolean loggedIn = false;

  protected Session(TabDriver td) { this.td = td; }

  public abstract void doLogin(BooleanSupplier cancelled) throws InterruptedException;
  public boolean isSessionAlive() { return loggedIn; }
  public boolean isLoggedIn() { return loggedIn; }
  protected void setLoggedIn(boolean value) { this.loggedIn = value; }

  public void ensureLoggedIn(BooleanSupplier cancelled) throws InterruptedException {
    synchronized (td) { if (isSessionAlive()) return; }
    setLoggedIn(false);
    while (!cancelled.getAsBoolean()) {
      synchronized (td) { if (isSessionAlive()) break; }
      Thread.sleep(2000);
    }
    if (!cancelled.getAsBoolean()) { setLoggedIn(true); }
  }
}
```

Subclasses override `isSessionAlive()` with a DOM probe and open the login URL in
`doLogin`, then call `ensureLoggedIn`:

```java
@Override
public boolean isSessionAlive() {
  synchronized (td) { return td.findByCss("button[class*=Account]").isPresent(); }
}

@Override
public void doLogin(BooleanSupplier cancelled) throws InterruptedException {
  synchronized (td) {
    if (isSessionAlive()) return;
    td.newTab(getTabPurpose(LOGIN));
    td.get("https://example.com/login");
  }
  ensureLoggedIn(cancelled);
}
```

Load credentials from an external file or secret store referenced by config — never
inline secrets in code.

## 7. Navigator construction

Navigators extend the platform `Session` and take the holder in their constructor;
pass `tdh.get()` to the super constructor. Register them as singletons if the
container manages them.

```java
public class ExampleNavigator extends ExampleSession {
  public ExampleNavigator(TabDriverHolder tdh) {
    super(tdh.get());
  }
}
```

Useful `TabDriver` API:
- `findByCss(String)` / `findByCss(WebElement ctx, String)` → `Optional<WebElement>`
- `findAllByCss(...)` → `List<WebElement>` (empty on missing)
- `findByCssAndText(css, text)` → `Optional<WebElement>`
- `getByText(String)` → XPath contains-text lookup
- `sendDeleteKeys(WebElement, n)`, `click(WebElement)` (JS click),
  `setRadio(WebElement, boolean)`, `setComboByDataValue(WebElement, String)`,
  `followContainedLink(WebElement)`
- `refresh()`, `get(url)`, `navigate()`, `switchTo()`, `executeScript(script)`,
  `getPageSource()`, `getCurrentUrl()`
- `newTab(Purpose)`, `goToTab(Purpose)`, `close()`, `quit()`

## 8. Lifecycle

Close the browser on shutdown. Use `getOpt()` so you never create a browser just to
close it. A JVM shutdown hook is the framework-agnostic default; a control/API
endpoint can call the same method on demand.

```java
Runtime.getRuntime().addShutdownHook(new Thread(
  () -> holder.getOpt().ifPresent(TabDriver::quit)
));
```

In containers that expose lifecycle callbacks (Spring `@PreDestroy`, Quarkus
`@PreDestroy` / `@Observes Shutdown`), prefer those over the shutdown hook.

## 9. Gotchas

- `Purpose` is a record whose `equals` compares `name`; prefer a singleton map (one
  `Purpose` per enum constant) over constructing new instances.
- `newTab` is idempotent, but a tab's purpose is decided at creation. Reusing a
  window for a different purpose silently keeps the old purpose.
- `executeScript(String, Object...)` and `executeAsyncScript(...)` are stubs that
  return `null`; use `executeScript(String)` if you need a JS call.
- Missing driver path / download dir config fails at first browser use, not at
  startup.
- Elements parsed from the page are unreliable; validate text/values before
  publishing them to the rest of the app, and keep CSS selectors easy to update.
